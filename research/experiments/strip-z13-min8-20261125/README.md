# kit: strip-z13-min8-20261125 — z=13 min>=8 (floor-8) セル梯子 + T-Z13

単一オーナー宣言: `research/log/2026-11-25-strip-z13-min8-single-owner-note.md`
(仮採番 K1317)。事前探査 log:
`research/log/2026-11-25-z13-predecl-exploration.md`。

## ファイル

| ファイル | sha256 | 役割 |
|---|---|---|
| `engine_block.py` | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0` | K1138 再帰 engine + K0832 単一トークン閉形式 (K1282..K1315 chain と同一 bytes) |
| `explore_k1317.py` | `182ec937122d3a1f0a6fd379cce38279d80f6386ab7c9fdd2443ceb2303bfaf8` | 凍結探索機体 (pin `bd5f22e4…` startup ゲート内蔵) |
| `explore_k1317.out` | `3fbdd1e8e1340c9cb097b5d5acdedc1854901c216845d22d4688e64a2f39c712` | 凍結 census stdout |
| `verify_k1317.py` | `b2394c87abb0a0e07c43c433409f4a0c9098e75443245948d439b961b647d728` | 宣言 battery 監査機体 (8,631 点 fail-closed・変異 7 モード) |
| `published/official_runs/run{1..4}.out` | 宣言ノート §4 参照 | 公式 4 走 stdout (byte-identical) |
| `published/detcheck.json` | 宣言ノート §4 参照 | OFFICIAL-PASS 判定 |

## 使い方

```sh
python3 explore_k1317.py            # 凍結 census 再現 (~16s)
python3 verify_k1317.py             # battery: PASS rc 0 / FAIL rc 1
python3 verify_k1317.py --tamper-engine   # rc 2 (engine sha 破り)
python3 verify_k1317.py --tamper=cell     # rc 1 (D1 fail-closed)
python3 verify_k1317.py --tamper=strip    # rc 1 (D2)
python3 verify_k1317.py --tamper=anchor12 # rc 1 (D3)
python3 verify_k1317.py --tamper=stair   # rc 1 (D4)
python3 verify_k1317.py --tamper=deviant # rc 1 (D6)
python3 verify_k1317.py --tamper=ext     # rc 1 (D7)
```

メモリ: engine cache (maxsize 6,000,000) は gate/セル毎に clear する設計
(値・決定性への影響なし・数百 MB 以内)。
