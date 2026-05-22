# Model-Facing Benchmark Sensitivity Check

This completed diagnostic uses one real model ranking, CHGNet, on a deterministic 5,000-structure subset of the 43,139 strict MP-Alex denominator. Scores are negative CHGNet formation-energy proxies constructed from CHGNet structure energies and MP elemental reference structures. The result is not a leaderboard and does not compare multiple models; it checks whether the label-source effect observed in the oracle/source-label analysis also appears under a real ranking.

## Scoring Manifest

| model   |   n_scored |   n_target |   sample_seed |   batch_size | device   | mp_structure_cache                                                                                                                                     | mp_structure_cache_sha256                                        | claim_scope                                    |
|:--------|-----------:|-----------:|--------------:|-------------:|:---------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------|:-----------------------------------------------|
| CHGNet  |       5000 |       5000 |      20260523 |           64 | cuda     | /home/waas/paper_experiments/github/discordance-/outputs/milestones/materials_label_discordance_full_mp_alex_43984/mp_records_summary_structures.jsonl | fe9763ec3d931cdb6e3095fe36dcd2d47be4f2e50935a015d63c70855e6565ef | model_facing_sensitivity_check_not_leaderboard |

## Threshold-Free Metrics

| model   | denominator           | label_source   |    n |   positive_rate |    auroc |    auprc |   median_threshold_precision |   median_threshold_f1 | claim_scope                                    |   delta_vs_alex_auroc |   delta_vs_alex_auprc |
|:--------|:----------------------|:---------------|-----:|----------------:|---------:|---------:|-----------------------------:|----------------------:|:-----------------------------------------------|----------------------:|----------------------:|
| CHGNet  | full_sample_5000      | mp_stable      | 5000 |        0.3928   | 0.454422 | 0.353325 |                     0.3336   |              0.373656 | model_facing_sensitivity_check_not_leaderboard |            -0.0118587 |             0.0369094 |
| CHGNet  | full_sample_5000      | alex_stable    | 5000 |        0.3462   | 0.466281 | 0.316415 |                     0.3      |              0.354526 | model_facing_sensitivity_check_not_leaderboard |           nan         |           nan         |
| CHGNet  | source_agreement_only | mp_stable      | 4441 |        0.353074 | 0.456434 | 0.316525 |                     0.293111 |              0.343626 | model_facing_sensitivity_check_not_leaderboard |           nan         |           nan         |

## Precision at K

| model   | denominator           | label_source     |    K |   precision_at_K |   stable_n_at_K |   discordant_fraction_at_K | claim_scope                                    |
|:--------|:----------------------|:-----------------|-----:|-----------------:|----------------:|---------------------------:|:-----------------------------------------------|
| CHGNet  | full_sample_5000      | mp_stable        |  100 |         0.37     |              37 |                      0.15  | model_facing_sensitivity_check_not_leaderboard |
| CHGNet  | full_sample_5000      | mp_stable        |  300 |         0.333333 |             100 |                      0.11  | model_facing_sensitivity_check_not_leaderboard |
| CHGNet  | full_sample_5000      | mp_stable        |  500 |         0.304    |             152 |                      0.084 | model_facing_sensitivity_check_not_leaderboard |
| CHGNet  | full_sample_5000      | mp_stable        | 1000 |         0.261    |             261 |                      0.08  | model_facing_sensitivity_check_not_leaderboard |
| CHGNet  | full_sample_5000      | mp_stable        | 2000 |         0.292    |             584 |                      0.09  | model_facing_sensitivity_check_not_leaderboard |
| CHGNet  | full_sample_5000      | alex_stable      |  100 |         0.34     |              34 |                      0.15  | model_facing_sensitivity_check_not_leaderboard |
| CHGNet  | full_sample_5000      | alex_stable      |  300 |         0.29     |              87 |                      0.11  | model_facing_sensitivity_check_not_leaderboard |
| CHGNet  | full_sample_5000      | alex_stable      |  500 |         0.268    |             134 |                      0.084 | model_facing_sensitivity_check_not_leaderboard |
| CHGNet  | full_sample_5000      | alex_stable      | 1000 |         0.237    |             237 |                      0.08  | model_facing_sensitivity_check_not_leaderboard |
| CHGNet  | full_sample_5000      | alex_stable      | 2000 |         0.262    |             524 |                      0.09  | model_facing_sensitivity_check_not_leaderboard |
| CHGNet  | source_agreement_only | agreement_stable |  100 |         0.37     |              37 |                      0     | model_facing_sensitivity_check_not_leaderboard |
| CHGNet  | source_agreement_only | agreement_stable |  300 |         0.276667 |              83 |                      0     | model_facing_sensitivity_check_not_leaderboard |
| CHGNet  | source_agreement_only | agreement_stable |  500 |         0.268    |             134 |                      0     | model_facing_sensitivity_check_not_leaderboard |
| CHGNet  | source_agreement_only | agreement_stable | 1000 |         0.222    |             222 |                      0     | model_facing_sensitivity_check_not_leaderboard |
| CHGNet  | source_agreement_only | agreement_stable | 2000 |         0.271    |             542 |                      0     | model_facing_sensitivity_check_not_leaderboard |

## MP-minus-Alex Precision Shift

|    K |   mp_precision_at_K |   alex_precision_at_K |   metric_shift_mp_minus_alex | model   | claim_scope                                    |
|-----:|--------------------:|----------------------:|-----------------------------:|:--------|:-----------------------------------------------|
|  100 |            0.37     |                 0.34  |                    0.03      | CHGNet  | model_facing_sensitivity_check_not_leaderboard |
|  300 |            0.333333 |                 0.29  |                    0.0433333 | CHGNet  | model_facing_sensitivity_check_not_leaderboard |
|  500 |            0.304    |                 0.268 |                    0.036     | CHGNet  | model_facing_sensitivity_check_not_leaderboard |
| 1000 |            0.261    |                 0.237 |                    0.024     | CHGNet  | model_facing_sensitivity_check_not_leaderboard |
| 2000 |            0.292    |                 0.262 |                    0.03      | CHGNet  | model_facing_sensitivity_check_not_leaderboard |
