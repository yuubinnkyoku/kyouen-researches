# class2-lane cost-69c WIN7 certificates

WIN7-D10 certificate for candidate bit 103 of S6 child `00000000000000809082040000000000` (edge cost 69, demand c1=2 c2=1 c4=0).

## Certificate

- Root: `00000080000000809082040000000000` (7 stones, second to move loses; loser mobility 53, matches independent legal_candidates.py enumeration)
- 52,338 rows, 20,357,850 extracted nodes, fbt_drops=0, no fatal drops
- Fully verified: 53/53 sub-roots PASS, union intersections 0, union missing 0, terminal stone range [13,17]

## Reconstruction

The certificate (1.89 MB) is stored as xz+base64 split into 3 parts:

```
cat cert-bit103-root-00000080000000809082040000000000.txt.xz.b64.part1of3 \
    cert-bit103-root-00000080000000809082040000000000.txt.xz.b64.part2of3 \
    cert-bit103-root-00000080000000809082040000000000.txt.xz.b64.part3of3 > cert.b64
base64 -d cert.b64 | xz -d > cert.txt
```

Expected checksums:
- cert.b64: 230,885 bytes, md5 `fdf83e5a3434ee5cc1ee198dcf871db2`
- cert.txt: md5 `4bb1299324fb69634a848cebc109961c`, 52,340 lines (2-line header + 52,338 rows)

Verified at commit fb71dbff013e13e8e5040ca9cfbbb22f4c70e00f: all 3 parts fetched raw, concatenated, decoded - md5 and full content identical to the locally verified certificate.

## Provenance

- Sweep: `../../n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69c-sweep-20261114.json` and raw batches A-I + determinism rerun
- Record: `class2-lane-cost69c-win7-certificates-20261114.json`
- Log: `research/log/2026-11-14-class2-lane-cost69c-win7.md`
