# Project Truth

## Active Manuscript Source

No active manuscript file exists yet. The intended manuscript source of truth is:

```text
paper_bootstrap/output/doc/main.tex
```

Do not draft paper prose directly from memory. Draft from the evidence blocks and claim boundaries listed in `paper_bootstrap/notes/result_summary.md` and `paper_bootstrap/notes/paper_handoff.md`.

## Dominant Contribution Type

Benchmark reliability / source-label uncertainty study for computational-materials stability benchmarks.

This is not currently a PARC methods paper, a prospective materials-discovery paper, a new materials generator paper, or a full model leaderboard paper.

## Working Venue Style

Use journal-oriented Nature-style structure by default unless the user redirects to another venue.

The likely venue target is computational-materials / AI-for-science reliability rather than a machine-learning methods conference.

## Central Claim

Public DFT stability labels are not source-invariant even on strict MP-Alexandria structure matches. This source dependence creates a measurable benchmark uncertainty band, visible in full-denominator label-source transfer analysis and in a real CHGNet model-facing sensitivity check.

## Stable Claim Boundaries

Allowed:

- MP-Alex strict-match denominator contains 43,139 structures.
- MP-Alex exact-stability discordance is 5,060 / 43,139 = 0.1173.
- MP-exact-stable subset has higher cross-source discordance than the full denominator.
- Source-native label transfer creates measurable benchmark metric shifts.
- A deterministic 5,000-structure CHGNet diagnostic shows label-source sensitivity in a real ranking.
- A source-aware benchmark card is a practical reporting recommendation.

Forbidden:

- Prospective materials discovery.
- Full common-hull mechanism decomposition.
- Third-source triangulation success.
- Full-denominator ML leaderboard.
- Model ranking flip on the full denominator.
- Claiming external DFT databases are interchangeable ground truth.
- Treating protocol-only artifacts as completed evidence.

