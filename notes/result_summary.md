# Result Summary

## Main Result 1: Full MP-Alex Denominator

Artifact path: `outputs/milestones/materials_label_discordance_full_mp_alex_43984/`

Lead numbers:

- Alexandria rows with MP identifiers: 43,984.
- MP records successfully queried: 43,169.
- Strict StructureMatcher matches: 43,139.
- Exact-stability discordances: 5,060.
- Discordance rate: 0.1173.

Paper role: denominator foundation and primary label-source uncertainty result.

## Main Result 2: Selection-Conditioned Discordance and Reporting Burden

Artifact path: `outputs/milestones/benchmark_reliability_enhancement/`

Lead numbers:

- Full denominator discordance: 5,060 / 43,139 = 0.1173.
- MP-exact-stable subset discordance: 0.2150.
- Alex-exact-stable subset discordance: 0.0976.
- 5 meV either-source near-hull flag captures 5,060 / 5,060 discordant pairs and flags 21,354 / 43,139 structures.

Paper role: shows discordance is denominator/selection dependent and motivates source-aware reporting.

## Main Result 3: Label-Source Benchmark Impact

Artifact path: `outputs/milestones/benchmark_impact_label_source_choice/`

Lead numbers:

- MP-stable but Alexandria-unstable: 3,628 / 16,872 = 21.5%.
- Alexandria-stable but MP-unstable: 1,432 / 14,676 = 9.8%.
- Perfect MP-source labeler evaluated by Alexandria: F1 = 0.8396, accuracy = 0.8827.
- Source-agreement-only denominator retained: 38,079 / 43,139 = 88.27%.

Paper role: converts label discordance into benchmark metric consequence.

## Main Result 4: CHGNet Model-Facing Sensitivity Check

Artifact path: `outputs/milestones/model_facing_benchmark_sensitivity_check/`

Lead numbers:

- CHGNet scored denominator: 5,000 strict MP-Alex matched structures.
- Precision@100: MP 0.370, Alexandria 0.340, shift +0.030.
- Precision@300: MP 0.333, Alexandria 0.290, shift +0.043.
- Precision@500: MP 0.304, Alexandria 0.268, shift +0.036.
- K=300 top-K decomposition: both-stable 77, MP-only stable 23, Alex-only stable 10, both-unstable 190.
- K=300 bootstrap CI for MP-minus-Alex precision shift: [0.0067, 0.0800].
- Sample discordance: 0.1118 versus full denominator 0.1173.

Paper role: demonstrates label-source sensitivity under one real model ranking. Not a leaderboard.

## Boundary Result: Common-Composition Hull Proxy

Artifact path: `outputs/milestones/common_hull_mechanism_subset/`

Lead numbers:

- Discordant sample common-composition proxy availability: 10 / 1,000.
- Concordant control availability: 6 / 500.

Paper role: coverage-boundary result showing lightweight public-table joins are insufficient for mechanism attribution.

## Related Work Assets

Artifacts:

- `docs/RELATED_WORK_POSITIONING.md`
- `docs/bibliography_additions.bib`

Paper role: position against Matbench Discovery, JARVIS-Leaderboard, foundation MLIPs, model-side MLIP reliability, MP-ALOE, MatterGen, and stability prediction/generation work.

