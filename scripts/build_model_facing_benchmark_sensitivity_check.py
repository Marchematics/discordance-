from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from chgnet.model.model import CHGNet
from pymatgen.core import Composition, Structure
from sklearn.metrics import average_precision_score, f1_score, precision_score, roc_auc_score


ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "outputs" / "milestones" / "materials_label_discordance_full_mp_alex_43984"
OUT = ROOT / "outputs" / "milestones" / "model_facing_benchmark_sensitivity_check"
MP_STRUCTURE_CACHE = Path(
    "/home/waas/paper_experiments/github/discordance-/outputs/milestones/"
    "materials_label_discordance_full_mp_alex_43984/mp_records_summary_structures.jsonl"
)

SAMPLE_SEED = 20260523
N_TARGET = 5000
BATCH_SIZE = int(os.environ.get("CHGNET_BATCH_SIZE", "64"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_manifest() -> None:
    rows = []
    for path in sorted(OUT.rglob("*")):
        if path.is_file() and path.name != "MANIFEST_SHA256.txt":
            rows.append(f"{sha256_file(path)}  {path.relative_to(OUT).as_posix()}")
    (OUT / "MANIFEST_SHA256.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")


def reduced_formula(formula: str) -> str:
    try:
        return Composition(str(formula)).reduced_formula
    except Exception:
        return str(formula)


def load_denominator() -> pd.DataFrame:
    df = pd.read_csv(FULL / "table_full_mp_alex_structure_matches.csv")
    df = df[df["match_status"].eq("strict_structure_match")].copy()
    df["mp_e_above_hull"] = pd.to_numeric(df["mp_e_above_hull"], errors="coerce")
    df["alex_e_above_hull"] = pd.to_numeric(df["alex_e_above_hull"], errors="coerce")
    df["mp_stable"] = df["mp_stable_exact"].astype(str).str.lower().eq("true")
    df["alex_stable"] = df["alex_stable_exact"].astype(str).str.lower().eq("true")
    df["discordant"] = df["mp_stable"] != df["alex_stable"]
    df = df.sort_values("material_id").sample(n=N_TARGET, random_state=SAMPLE_SEED).sort_values("material_id")
    df["target_reduced_formula"] = df["formula"].map(reduced_formula)
    return df.reset_index(drop=True)


def load_structure_cache(material_ids: set[str]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    with MP_STRUCTURE_CACHE.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            mid = str(row.get("material_id"))
            if mid in material_ids and row.get("structure"):
                records[mid] = row
    return records


def element_set(df: pd.DataFrame) -> set[str]:
    elements: set[str] = set()
    for formula in df["target_reduced_formula"]:
        try:
            elements.update(str(el) for el in Composition(str(formula)).elements)
        except Exception:
            continue
    return elements


def fetch_element_reference_structures(elements: set[str]) -> dict[str, Structure]:
    from mp_api.client import MPRester

    api_key = os.environ.get("MP_API_KEY")
    if not api_key:
        raise RuntimeError("MP_API_KEY is required; source /root/.mp_api_env before running.")
    refs: dict[str, Structure] = {}
    with MPRester(api_key) as mpr:
        for idx, el in enumerate(sorted(elements), start=1):
            docs = mpr.materials.summary.search(
                chemsys=el,
                fields=["material_id", "energy_above_hull", "structure"],
            )
            candidates = [d for d in docs if getattr(d, "structure", None) is not None]
            if not candidates:
                continue
            candidates.sort(key=lambda d: float(getattr(d, "energy_above_hull", 1e9) or 1e9))
            refs[el] = candidates[0].structure
            print(f"Element reference {idx}/{len(elements)} {el}: {candidates[0].material_id}", flush=True)
            time.sleep(0.05)
    missing = sorted(elements - set(refs))
    if missing:
        raise RuntimeError(f"Missing MP elemental reference structures: {missing}")
    return refs


def predict_energy_per_atom(model: CHGNet, structures: list[Structure], labels: list[str]) -> dict[str, float]:
    out: dict[str, float] = {}
    for start in range(0, len(structures), BATCH_SIZE):
        batch = structures[start : start + BATCH_SIZE]
        batch_labels = labels[start : start + BATCH_SIZE]
        with torch.no_grad():
            preds = model.predict_structure(batch, task="e", batch_size=BATCH_SIZE)
        if isinstance(preds, dict):
            preds = [preds]
        for label, pred in zip(batch_labels, preds):
            val = pred["e"]
            out[label] = float(np.asarray(val).item())
        print(f"CHGNet scored {min(start + BATCH_SIZE, len(structures))}/{len(structures)}", flush=True)
    return out


def score_subset(df: pd.DataFrame) -> pd.DataFrame:
    ids = set(df["material_id"].astype(str))
    records = load_structure_cache(ids)
    if len(records) != len(df):
        missing = sorted(ids - set(records))[:10]
        raise RuntimeError(f"Missing structures in cache: {len(ids) - len(records)} examples={missing}")

    refs = fetch_element_reference_structures(element_set(df))
    model = CHGNet.load()
    structures: list[Structure] = []
    labels: list[str] = []
    for el, struct in refs.items():
        labels.append(f"element::{el}")
        structures.append(struct)
    for mid in df["material_id"].astype(str):
        labels.append(f"target::{mid}")
        structures.append(Structure.from_dict(records[mid]["structure"]))

    energies = predict_energy_per_atom(model, structures, labels)
    element_energy = {label.split("::", 1)[1]: energy for label, energy in energies.items() if label.startswith("element::")}
    rows = []
    for row in df.itertuples(index=False):
        comp = Composition(str(row.target_reduced_formula))
        element_ref = 0.0
        for el, amt in comp.items():
            element_ref += float(amt) / comp.num_atoms * element_energy[str(el)]
        energy = energies[f"target::{row.material_id}"]
        formation_proxy = energy - element_ref
        rows.append(
            {
                "material_id": row.material_id,
                "formula": row.formula,
                "chemical_system": row.chemical_system,
                "model": "CHGNet",
                "model_version": "CHGNet.load()",
                "energy_per_atom": energy,
                "formation_energy_proxy": formation_proxy,
                "score": -formation_proxy,
                "score_type": "negative_chgnet_formation_energy_proxy_higher_is_more_stable",
                "mp_stable": row.mp_stable,
                "alex_stable": row.alex_stable,
                "source_agreement": not bool(row.discordant),
                "mp_e_above_hull": row.mp_e_above_hull,
                "alex_e_above_hull": row.alex_e_above_hull,
            }
        )
    score_df = pd.DataFrame(rows)
    score_df.to_csv(OUT / "candidate_scores_chgnet_5000.csv", index=False)
    pd.DataFrame(
        [
            {
                "model": "CHGNet",
                "n_scored": len(score_df),
                "n_target": N_TARGET,
                "sample_seed": SAMPLE_SEED,
                "batch_size": BATCH_SIZE,
                "device": "cuda" if torch.cuda.is_available() else "cpu",
                "mp_structure_cache": str(MP_STRUCTURE_CACHE),
                "mp_structure_cache_sha256": sha256_file(MP_STRUCTURE_CACHE),
                "claim_scope": "model_facing_sensitivity_check_not_leaderboard",
            }
        ]
    ).to_csv(OUT / "table_chgnet_scored_subset_manifest.csv", index=False)
    return score_df


def threshold_metrics(score_df: pd.DataFrame, label_col: str, denominator: str) -> dict[str, object]:
    df = score_df.copy()
    y = df[label_col].astype(bool)
    score = df["score"].astype(float)
    if y.nunique() < 2:
        auc = ""
        auprc = ""
    else:
        auc = float(roc_auc_score(y, score))
        auprc = float(average_precision_score(y, score))
    cutoff = score.median()
    pred = score >= cutoff
    return {
        "model": "CHGNet",
        "denominator": denominator,
        "label_source": label_col,
        "n": int(len(df)),
        "positive_rate": float(y.mean()),
        "auroc": auc,
        "auprc": auprc,
        "median_threshold_precision": float(precision_score(y, pred, zero_division=0)),
        "median_threshold_f1": float(f1_score(y, pred, zero_division=0)),
        "claim_scope": "model_facing_sensitivity_check_not_leaderboard",
    }


def precision_at_k(score_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    rankings = score_df.sort_values(["score", "material_id"], ascending=[False, True])
    for label_col in ["mp_stable", "alex_stable"]:
        for k in [100, 300, 500, 1000, 2000]:
            sub = rankings.head(k)
            rows.append(
                {
                    "model": "CHGNet",
                    "denominator": "full_sample_5000",
                    "label_source": label_col,
                    "K": k,
                    "precision_at_K": float(sub[label_col].astype(bool).mean()),
                    "stable_n_at_K": int(sub[label_col].astype(bool).sum()),
                    "discordant_fraction_at_K": float((sub["mp_stable"].astype(bool) != sub["alex_stable"].astype(bool)).mean()),
                    "claim_scope": "model_facing_sensitivity_check_not_leaderboard",
                }
            )
    agreement = rankings[rankings["source_agreement"].astype(bool)].copy()
    for k in [100, 300, 500, 1000, 2000]:
        if len(agreement) < k:
            continue
        sub = agreement.head(k)
        rows.append(
            {
                "model": "CHGNet",
                "denominator": "source_agreement_only",
                "label_source": "agreement_stable",
                "K": k,
                "precision_at_K": float(sub["mp_stable"].astype(bool).mean()),
                "stable_n_at_K": int(sub["mp_stable"].astype(bool).sum()),
                "discordant_fraction_at_K": 0.0,
                "claim_scope": "model_facing_sensitivity_check_not_leaderboard",
            }
        )
    return pd.DataFrame(rows)


def write_metrics(score_df: pd.DataFrame) -> None:
    rows = [
        threshold_metrics(score_df, "mp_stable", "full_sample_5000"),
        threshold_metrics(score_df, "alex_stable", "full_sample_5000"),
    ]
    agreement = score_df[score_df["source_agreement"].astype(bool)].copy()
    rows.append(threshold_metrics(agreement, "mp_stable", "source_agreement_only"))
    metrics = pd.DataFrame(rows)
    mp = metrics[metrics["label_source"].eq("mp_stable") & metrics["denominator"].eq("full_sample_5000")].iloc[0]
    alex = metrics[metrics["label_source"].eq("alex_stable") & metrics["denominator"].eq("full_sample_5000")].iloc[0]
    metrics["delta_vs_alex_auroc"] = ""
    metrics["delta_vs_alex_auprc"] = ""
    full_mp_mask = metrics["label_source"].eq("mp_stable") & metrics["denominator"].eq("full_sample_5000")
    metrics.loc[full_mp_mask, "delta_vs_alex_auroc"] = float(mp["auroc"]) - float(alex["auroc"])
    metrics.loc[full_mp_mask, "delta_vs_alex_auprc"] = float(mp["auprc"]) - float(alex["auprc"])
    metrics.to_csv(OUT / "table_model_metric_source_sensitivity.csv", index=False)

    pk = precision_at_k(score_df)
    mp_pk = pk[pk["denominator"].eq("full_sample_5000") & pk["label_source"].eq("mp_stable")][
        ["K", "precision_at_K"]
    ].rename(columns={"precision_at_K": "mp_precision_at_K"})
    alex_pk = pk[pk["denominator"].eq("full_sample_5000") & pk["label_source"].eq("alex_stable")][
        ["K", "precision_at_K"]
    ].rename(columns={"precision_at_K": "alex_precision_at_K"})
    shift = mp_pk.merge(alex_pk, on="K")
    shift["metric_shift_mp_minus_alex"] = shift["mp_precision_at_K"] - shift["alex_precision_at_K"]
    shift["model"] = "CHGNet"
    shift["claim_scope"] = "model_facing_sensitivity_check_not_leaderboard"
    pk.to_csv(OUT / "table_precision_at_k_source_sensitivity.csv", index=False)
    shift.to_csv(OUT / "table_precision_at_k_metric_shift.csv", index=False)


def write_closeout() -> None:
    manifest = pd.read_csv(OUT / "table_chgnet_scored_subset_manifest.csv")
    metrics = pd.read_csv(OUT / "table_model_metric_source_sensitivity.csv")
    pk = pd.read_csv(OUT / "table_precision_at_k_source_sensitivity.csv")
    shift = pd.read_csv(OUT / "table_precision_at_k_metric_shift.csv")
    (OUT / "MODEL_FACING_BENCHMARK_SENSITIVITY_CHECK.md").write_text(
        "# Model-Facing Benchmark Sensitivity Check\n\n"
        "This completed diagnostic uses one real model ranking, CHGNet, on a deterministic 5,000-structure subset of the 43,139 strict MP-Alex denominator. "
        "Scores are negative CHGNet formation-energy proxies constructed from CHGNet structure energies and MP elemental reference structures. "
        "The result is not a leaderboard and does not compare multiple models; it checks whether the label-source effect observed in the oracle/source-label analysis also appears under a real ranking.\n\n"
        "## Scoring Manifest\n\n"
        f"{manifest.to_markdown(index=False)}\n\n"
        "## Threshold-Free Metrics\n\n"
        f"{metrics.to_markdown(index=False)}\n\n"
        "## Precision at K\n\n"
        f"{pk.to_markdown(index=False)}\n\n"
        "## MP-minus-Alex Precision Shift\n\n"
        f"{shift.to_markdown(index=False)}\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    score_path = OUT / "candidate_scores_chgnet_5000.csv"
    if score_path.exists():
        print(f"Reusing existing score table: {score_path}", flush=True)
        score_df = pd.read_csv(score_path)
    else:
        df = load_denominator()
        score_df = score_subset(df)
    write_metrics(score_df)
    write_closeout()
    write_manifest()


if __name__ == "__main__":
    main()
