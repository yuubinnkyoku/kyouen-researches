# Kit: multi-c web F2 スプレッド法則表（K1287・2026-11-24）

宣言ノート: [single-owner note](../../log/2026-11-24-multic-web-f2-single-owner-note.md)・
K item: [K1287](../../knowledge/items/K1287-multic-web-f2-spread-laws.md)・
run log: [run log](../../log/2026-11-24-multic-web-f2.md)

## 内容

- `verify_k1287.py`: 監査機体。engine block 内蔵（pin
  `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`・
  起動時 sha256 ゲート）。sha256 = `52e7eea70090ef41095d19b33de177793a80d7b3a5619ff7708d12ae851fe434`。
  使用法: `python3 verify_k1287.py`（公式走・rc 0 で
  overall_bad 0）、《干し》`--tamper-engine`（rc 2）・
  `--tamper=wlaw|dlaw|elaw|aplaw|alaw|amlaw|identity|mex`（rc 1・
  宣言ノート §4 の bad 個数期待値）。
- `engine_block.py`: 単体 engine（K1282–K1286 kit と同一 bytes・
  sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`）。
- `explore_k1287.py`: 広域 census explorer（stage: `z0|z1|z2|frontier`・
  stdout 決定的）。`output/explore_z*.out`・`output/explore_frontier.out`
  がその出版走。箱は README §1 の explore 箱を参照。
- `predry/`: 宣言前ローカル dryrun（決定論 3 走 + 変異電池 9 走・
  sha256 は宣言ノート §3/§4 と同じ）。
- `output/`: explore 出版走・公式 4 走（audit_run1-4）・公式変異電池
  （tamper_*）・detcheck.json・MANIFEST-sha256。

## 注意

- 値法則は有限箱内 census（machine コア箱 + explore 広域箱）で
  bad=0 の**予想／観測**であり、全称定理ではない。恒等式 I1–I11
  のみが代数定理。詳細は宣言ノート §1/§2 の区分。
- K1286 対抗レーン（border-slices・`f6db3f33` 系列・kit は
  [multic 対抗](../border-slices-20261124/README.md) の `research/experiments/border-slices-20261124/`)
  とは、F2 web の d ≤ 3 OBS 入力（K1286 §5 O3）→ d ≤ 8 5 族 3 面
  拡張として接続。重複全称主張はなし。
