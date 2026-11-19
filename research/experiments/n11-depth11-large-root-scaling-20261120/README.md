# n11 depth-11 大型root倍率標本測定（K1082台帳上位4根、2026-11-20）

## 目的

depth-11倍率系列（K1081）が「倍率はD10 node数の大きいrootで高め」という残余リスクを明示
していた。K1082台帳のroot別コスト出版により対象を選べるようになったので、**大型root帯
（D10合計8.7M〜13.0M nodes）でのdepth-11倍率を追加標本で検証**した。
コスト測定のみであり、判定変更・行の閉鎖・掃引は行わない。単一オーナー宣言ノート
（`research/log/2026-11-20-n11-depth11-large-root-scaling-single-owner-note.md`・commit 0e9da3cb）の下で実施。

## 対象とプロトコル

- 対象: K1082台帳 `by_root` の sum_nodes 降順で、既測定の最大probe根
  `00000000010000809002000040000080`（pilot測定済み・倍率1.0220/1.0132）を除く上位4根
  （assemble gate `ledger-selection-pin` で再導出検証）:
  - rank1 `00000000000040809002000800100000`（bit 20・ac0 12,796,034 + ac1 218,055）
  - rank2 `00000000000000801202040000101000`（bit 12・ac0 5,785,671 + ac1 6,215,710）
  - rank3 `00000000000000003800000009080004`（bit 2・ac0 3,422,095 + ac1 5,385,035）
  - rank4 `00000000000000003800000009840000`（bit 18・ac0 6,009,248 + ac1 2,710,668）
- runner v17固定コピー（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）・
  cap 30M・timeout 280s・両AND順序・pilot_d6制御必須・逐次・D10再測定+D11（計16 probe）。

## 結果（16/16完走・capped 0・error 0・gate 7/7 PASS）

| label | ordering | D10 nodes | D11 nodes | 倍率 |
| --- | --- | --- | --- | --- |
| rank1 | andclose1 | 218,055 | 218,575 | 1.0024 |
| rank1 | andclose0 | 12,796,034 | 13,289,457 | **1.0386** |
| rank2 | andclose1 | 6,215,710 | 6,393,337 | 1.0286 |
| rank2 | andclose0 | 5,785,671 | 5,963,443 | 1.0307 |
| rank3 | andclose1 | 5,385,035 | 5,522,167 | 1.0255 |
| rank3 | andclose0 | 3,422,095 | 3,496,655 | 1.0218 |
| rank4 | andclose1 | 2,710,668 | 2,803,695 | 1.0343 |
| rank4 | andclose0 | 6,009,248 | 6,409,440 | **1.0666** |

- **D10再測定8/8がK1082台帳のper-probe node値と厳密一致**（`ledger-determinism-crosscheck`
  PASS・三度目の独立再測定による決定論合意）。
- **大型root帯の倍率は1.0024〜1.0666**。系列全体（10根・20 probe・D10 0.12M〜14.2M nodes）では
  **倍率バンドは1.0004〜1.0666**に拡張された。「大きいrootほど倍率高め」の傾向は弱く成立するが、
  上限でも+6.7%に留まり、逐次深化の経験則「+1手ごとおおむね+7%以内」は大型rootでも維持される。

## 再現性

- 正本 `output/depth11-large-root-scaling-20261120.json`（SHA-256
  `c9927a2345edff7e6fe2e90ad1f3f255622aca7b35bb61d7876757d1fdbcecd0`）は生probe記録
  `output/probe-records-largeroot.jsonl` から assemble のみで生成され、別cwd・別プロセスで
  byte-identical（2回確認）。
- 再現: repoからK1069正本と台帳正本をraw取得し、
  `python3 scripts/depth11_large_root_scaling_20261120.py assemble <k1069.json> <ledger.json>`。

## 解釈規約

node数はcap内で決定的（機種非依存の費用単位）。capped/timeoutはいかなる方向の証拠にもならない
（本実験でcapped 0）。depth-11のloss=falseはREFUTED-D11分類でも行の閉鎖でもない。
REFUTED-D10はLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4 はすべて UNKNOWN のまま。**
