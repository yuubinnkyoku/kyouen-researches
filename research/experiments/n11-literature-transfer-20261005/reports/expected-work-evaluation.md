# Chronological Expected-Work evaluation for n=11 s5 scheduling

Date: 2026-10-05

**11×11 empty-board outcome remains UNKNOWN.**

## Question

The reply=27 coordinator needs two different estimates:

1. how likely an unresolved canonical s5 root is to be a class-disqualifying WIN;
2. how much exact work that root will cost.

Expected Work Search suggests combining those quantities rather than ordering
only by estimated proof size or only by win probability.

The experiment here tests that transfer chronologically on the original
reply=27 exact frontier. Predictions are used only for scheduling; exact replay
remains the sole verdict source.

## Data and split

The independently replayed original reply=27 frontier supplied 2,229 exact s5
roots. The global frontier sequence was split at 80%:

- train: **1,782** exact roots, **34 WIN**;
- chronological holdout: **447** exact roots, **8 WIN / 439 LOSS**.

The 33 roots unresolved at the original 15M-node cap are right-censored and are
not used as exact-cost labels.

## Models

WIN ranking uses the same residual/geometric structural features as the
chronological WIN-model experiment.

Exact cost uses ridge regression for `log(exact nodes)`. On the 447-root
holdout:

- legal-only cost model: corr(actual log nodes, prediction) = **0.2554**;
- structural cost model: **0.3540**;
- median multiplicative error improves from **1.4258×** to **1.4144×**.

The structural cost model is therefore somewhat better, but still noisy.

WIN ranking on this particular chronological split is stronger:

- low-legal baseline AUC = **0.8108**;
- structural WIN score AUC = **0.8690**.

## Proof-search efficiency

Four deterministic policies were evaluated using the *actual* exact nodes paid
in the holdout:

| policy | first WIN rank | nodes to first WIN | top-20 WIN | top-20 nodes | top-40 WIN | top-40 nodes |
|---|---:|---:|---:|---:|---:|---:|
| low legal first | **11** | **46,284,716** | **1** | 88,020,429 | 2 | 162,646,869 |
| predicted cost first | 43 | 137,791,747 | 0 | **54,719,305** | 0 | **119,663,888** |
| structural WIN score first | 23 | 99,735,457 | 0 | 80,688,565 | 2 | 163,250,337 |
| WIN logit − predicted log nodes | 23 | 99,819,187 | 0 | 80,688,565 | 2 | **150,922,923** |

The Expected-Work-style score is the log of estimated WIN odds per predicted
solve cost up to an additive prior constant.

It does **not** beat the existing low-legal ordering on the metric that matters
for class falsification: actual nodes paid before obtaining WIN witnesses.

The probability model has better AUC, and the structural cost model has better
cost correlation, yet their naive combination is worse at the early part of the
search. Rare WINs and imperfect cost estimates make ranking quality alone an
insufficient acceptance criterion.

## Consequence

Do **not** replace the current cheap-probe scheduler by the present
Expected-Work score.

The useful lesson from Expected Work Search remains conceptual:

- estimate outcome likelihood and solve cost separately;
- validate the combination on actual proof work, not only AUC/RMSE;
- a scheduler is accepted only if it reduces exact nodes or wall time to useful
  witnesses on chronological holdout.

For the current reply=27 proof, exact shared-boundary probes and selective full
class completion have stronger empirical support than this first
Expected-Work implementation.

## Reproduction

- WIN model:
  `research/experiments/n11-literature-transfer-20261005/scripts/evaluate_s5_win_model.py`
- cost model:
  `research/experiments/n11-literature-transfer-20261005/scripts/evaluate_s5_cost_model.py`
- combined evaluation:
  `research/experiments/n11-literature-transfer-20261005/scripts/evaluate_s5_expected_work.py`
- workflow:
  `.github/workflows/n11-s5-expected-work.yml`
- successful Actions run: `37320387179`
- artifact digest:
  `sha256:8c4b69b82e237c9f6dac86c4bd90445a209d505400e1f1d6950e43d5e13ee5f8`
