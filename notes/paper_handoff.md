# Paper Handoff

## Current State

The repository is writing-ready for a first manuscript skeleton. The experimental package is complete enough to draft a benchmark-reliability paper under strict claim boundaries.

Latest pushed commit at bootstrap time:

```text
291dec7 Add CHGNet sensitivity reviewer defenses
```

## Recommended Next Skill Sequence

1. `paper-plan`: build the manuscript outline and figure plan.
2. `paper-figure`: generate source-data-driven figures from milestone CSVs.
3. `paper-write`: draft `output/doc/main.tex` section by section.
4. `paper-claim-audit`: verify every numeric sentence before polishing.
5. `citation-audit`: verify bibliography and citation contexts.
6. `paper-compile`: compile once LaTeX exists.

## Suggested Manuscript Structure

1. Introduction: stability benchmarks rely on source-native public DFT labels.
2. Full MP-Alex denominator: 43,139 strict matches and 11.7% exact-stability discordance.
3. Selection-conditioned discordance and near-hull reporting burden.
4. Benchmark consequences of source-label choice before models.
5. CHGNet 5,000-row model-facing sensitivity check.
6. Source-aware benchmark card.
7. Limitations and future work: common-hull mechanism, third-source coverage, full leaderboard, no new DFT.

## Figure Anchors

Recommended main figures:

- Figure 1: Denominator construction and MP-Alex label confusion.
- Figure 2: Selection-conditioned discordance and near-hull/reporting burden.
- Figure 3: Benchmark impact of label-source choice, including source-label transfer and conflict-excluded denominator.
- Figure 4: CHGNet model-facing sensitivity check with precision@K shifts, top-K decomposition, bootstrap uncertainty, and score-direction sanity as supplement/source data.

## Verification Before Any Submission Draft

Run:

```bash
pytest -q tests
sha256sum -c MANIFEST_SHA256.txt
rg -n "(?i)(api[_-]?key|token|secret|credential)" . --glob '!.git/**' || true
```

Last known status before this bootstrap:

- `33 passed`
- manifest passed
- secret scan clean

## Claim Risks

- Do not use the 0.522 WBM-Alex probe as a headline baseline. The full MP-Alex denominator is ~0.117.
- Do not present CHGNet AUROC as strong predictive performance.
- Do not imply common-hull mechanism attribution was completed.
- Do not call source-agreement-only reporting a new benchmark standard without explaining cost and scope.

