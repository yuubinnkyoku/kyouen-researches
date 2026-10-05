# Reply=27 geometry cache A/B report

Run date: 2026-10-06 JST. The geometry index was generated at 2026-10-06 02:35:37 JST. Measurements were made on the same local checkout with the commands below; wall times are process elapsed time from PowerShell `Diagnostics.Stopwatch`.

The input was `.local/n11/rebase-held-2822.cache` (117,265 bytes, SHA-256 `D2F758A77896D7A79542970F5D548D423799A69EC9321F6D4FD5610E7E2F498B`). Its preserved tracked copy, `research/experiments/n11-boundary-recovery-20261006/output/post-next2-s5.cache`, is byte-identical (same byte count and SHA-256); that tracked path can be used in the commands below to reproduce the same input. The generated gzip index stayed local at `.local/n11/reply27-geometry-v1.json.gz` (1,798,405 bytes, SHA-256 `F35CE99E8EF0C8729D31970FBC2377F293180ACD6D3CF8435C59FC2C6591FBE0`). Source identity at run time:

- `scripts/reply27_geometry_cache.py`: `84AD12E6ECADBDAB2E5C79EA11CC6123FC1D2C0D03E83EB45983537DEF8D6FC2`
- `research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py`: `6CCA3CFE161FFC9FFC199C56B595E9D0F72B839EE945E8B7E2C4090DAFCF0C0C`

The generator enumerated 119 legal vertices, 6,871 raw edges, and 3,384 canonical s4 classes. For every class it enumerated the s5 children for every raw edge, asserted each edge produced the representative edge's child set, and saved their boundary union. The explicit generation command was:

```powershell
python research/experiments/n11-frontier-selection-20261005/scripts/reply27_geometry_cache.py generate --out .local/n11/reply27-geometry-v1.json.gz
```

Each cold command below omits `--geometry-cache`; each warm command adds `--geometry-cache .local/n11/reply27-geometry-v1.json.gz`. Both use the same exact s5 input cache.

```powershell
uv run --no-project --with numpy --with scipy python research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py --s5-cache .local/n11/rebase-held-2822.cache --out .local/n11/cardinality-cold.json
uv run --no-project --with numpy --with scipy python research/experiments/n11-frontier-selection-20261005/scripts/cache_aware_reply27_cardinality.py --s5-cache .local/n11/rebase-held-2822.cache --geometry-cache .local/n11/reply27-geometry-v1.json.gz --out .local/n11/cardinality-warm.json

uv run --no-project --with numpy --with scipy python research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py --extra-s5-cache .local/n11/rebase-held-2822.cache --out .local/n11/repair-cold.json --targets-out .local/n11/repair-cold.csv
uv run --no-project --with numpy --with scipy python research/experiments/n11-frontier-selection-20261005/scripts/reply27_selected31_repair.py --extra-s5-cache .local/n11/rebase-held-2822.cache --geometry-cache .local/n11/reply27-geometry-v1.json.gz --out .local/n11/repair-warm.json --targets-out .local/n11/repair-warm.csv

uv run --no-project --with numpy --with scipy python research/experiments/n11-frontier-selection-20261005/scripts/rank_reply27_completion_classes.py --repair-json .local/n11/repair-cold.json --extra-s5-cache .local/n11/rebase-held-2822.cache --targets-out .local/n11/rank-cold.csv --out .local/n11/rank-cold.json
uv run --no-project --with numpy --with scipy python research/experiments/n11-frontier-selection-20261005/scripts/rank_reply27_completion_classes.py --repair-json .local/n11/repair-warm.json --extra-s5-cache .local/n11/rebase-held-2822.cache --geometry-cache .local/n11/reply27-geometry-v1.json.gz --targets-out .local/n11/rank-warm.csv --out .local/n11/rank-warm.json
```

| CLI | Cold | Warm | Compared results |
|---|---:|---:|---|
| `cache_aware_reply27_cardinality.py` | 130.47 s | 17.45 s | LOSS 19 / UNKNOWN 3,234 / WIN 131; minimum cover 12; fractional and rational dual 12; certificate tight; selected classes equal |
| `reply27_selected31_repair.py` | 83.28 s | 49.20 s | secured 76 / uncovered 43; minimum repair 12; additive unknown-s5 cost 1,147; exact-15 cost 1,188 (unique 1,184); status summary and target CSV equal |
| `rank_reply27_completion_classes.py` | 76.95 s | 49.08 s | LOSS 19 / WIN-forbidden 131 / repair classes 12; ranking equal; best target `[1153202979717779456,0]` with 91 unknown s5; target CSV equal |

JSON comparisons ignored only output-path fields (`best_target.targets_out`) where the cold and warm filenames differ. Target CSV files had equal SHA-256 within each pair. Cache load and structural validation alone took 12.33 s. Mutations of `n`, `root`, declared class count, data digest, source SHA, and duplicate class were all rejected. For the duplicate-class case, the data digest was recalculated so validation reached and rejected the duplicate key. `py_compile` and `git diff --check` passed.

## Trust scope

The loader checks the board/root and expected counts, the generator and `dfpn_edge_classes.py` source hashes, the canonical data digest, bitboard bounds, stone counts, canonical keys, vertex/edge/class structure, edge safety, duplicates, coverage, and child-key shape. This is an integrity and compatibility boundary for reusing the geometry generated by this version. It does not independently prove the saved child boundaries from first principles: loading deliberately avoids re-enumerating every child boundary, which would repeat the cold work. The generation run performed the all-raw-edge child-set equality assertion before saving. Independent proof or verification workflows must continue to build/check geometry directly rather than treating this optional cache as proof evidence.
