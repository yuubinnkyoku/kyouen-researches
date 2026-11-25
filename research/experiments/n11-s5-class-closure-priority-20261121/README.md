# n11 S5 class-closure priority measurement (2026-11-21)

Lane declaration: `research/log/2026-11-21-n11-s5-ccp-exclusive-probe-single-owner.md` (declaration HEAD `1045fb39`, fix commit `99d2c312` after a PLACEHOLDER byte-incident recorded transparently in the declaration itself).

## Purpose

Part A (measurement only, deterministic) of the class-closure priority lane: quantify **which live candidate class cheapest to close first**, and how much concentrated class-targeted probing beats the global cheapest-first supply order, without making any verdict claim.

Under the pinned probe-13 merged exact S5 cache there are 62 live (UNKNOWN) candidate classes within the 4,562-child post-probe-13 supply (claimable pool 2,653). This experiment measures, per class:

- `s5_unknown`: remaining unknown S5 children (closure distance),
- `unknown_exclusive` / `unknown_shared`: split into single-live-parent (exclusive) vs multi-live-parent (shared) unknown children,
- `proxy_exclusive_sum` / `proxy_shared_sum` / `proxy_total`: frozen-profile truncated cost-proxy sums of those unknowns,
- `bin_prior_all_loss_index`: bin-implied remaining-WIN index (biased historical evidence; explicitly NOT a probability; 0 means observed LOSS-only, near 1 means bin-history WIN-heavy),
- `complete_at_queue_rank` / `queue_cum_proxy_to_completion`: under the static all-LOSS scenario, the global cheapest-first queue position and cumulative proxy at which this class would complete.

## Headline static-scheduling result (all-LOSS scenario, no probability used)

Global cheapest-first order (the reply27 supply order) completes its **first** live class at queue probe #3,927 with cumulative proxy **21,911,941,676** nodes, whereas class-targeted completion needs 93 probes / **530,074,022** proxy for the focus class `1188950301626859520:536870912` (queue rank 4,548, last among the 62) and 99 probes / **546,960,111** for the certificate class `1297036692683752448:0`, both roughly **40x** cheaper in proxy terms than waiting for the global queue. The certificate class exclusive/shared split is 38 exclusive children (204,622,151 proxy) vs 61 shared (342,337,960 proxy).

These are **scheduling measurements**, not verdicts: node counts and proxies of unknown children are never evidence of WIN or LOSS.

## Inputs (all fail-closed sha-pinned at main `a423c2f0`)

- geometry `n11-strategy-redesign-20261010/output/geometry.json.gz` - sha256 `146be80b...100b54`
- merged exact S5 cache after reply27 JS probe-13 - `research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/merged-exact-s5-after-js-probe-13.cache` - sha256 `60e0dc34...bc28c6`
- probe-13 post-probe supply table (shared-s5-tasks.csv) - sha256 `31f0d29b...ea954`
- candidate ledger - sha256 `2a4c2382...da80`
- frozen historical cost profile - sha256 `6b2971e5...` (see json `input_pins`)

## Outputs

- `output/class-closure-priority.csv` - one row per live candidate class (62 rows), fields as listed above.
- `output/class-closure-priority.json` - gates, input pins, the static all-LOSS queue simulation (first completion + next five classes), bin-prior ranking (top 5), cost ranking (top 5), the **authoritative machine-regenerated 38-key certificate-class exclusive probe order** (`certificate_class_exclusive_probe_order`; prose in the declaration is secondary, any discrepancy aborts the probe), and the focus class 35-key exclusive reference list.

## Gates (all PASS; script fails closed otherwise)

Geometry/cache/supply/ledger/profile sha pins; 3,384 classes; 119 third moves; 115 candidates; 62 UNKNOWN / 53 WIN / 0 LOSS; secured coverage 117; remaining third moves {100,108}; supply 4,562 (deg-1 2,688 / deg-2 1,874); claimable pool 2,653; candidate ledger cross-check 62/62; focus-lane 35-key equality; certificate-class 38-key non-overlap with both concurrent lane claims.

## Reproduction

```
python3 scripts/class_closure_priority.py \
  --geometry <geometry.json.gz> --cache <merged-exact-s5-after-js-probe-13.cache> \
  --supply <shared-s5-tasks.csv probe-13 post-probe> \
  --candidate-ledger <candidate-classes.csv> \
  --profile <historical-cost-profile.json> \
  --out output/
```

## Status guard

The standard 11x11 empty board, the two-stone root {60,27}, and its remaining third moves 100/108 remain UNKNOWN. This experiment makes no verdict claim of any kind; proxy values, node counts and bin-prior indices are never read as verdicts.
