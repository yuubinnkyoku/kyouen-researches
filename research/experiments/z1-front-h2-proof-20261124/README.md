# z1-front-h2-proof-20261124 — K1283 専用機体（宣言 c075b512 の protocol 実行用・公式実行の前に凍結）

宣言ノート: `research/log/2026-11-24-z1-front-h2-proof-single-owner-note.md`
（commit c075b512・publish-then-execute）。本キットは §4 の機械監査
protocol D1–D10 の実行体であり、公式実行は fetch-back 機体から行う。

## 構成

- `verify_k1283.py`（16,317B・sha256
  `ca515df5887948bd880928fde4576877e23b4addb613566d6b252a20d5deaeb3`）:
  電池 D1–D10。engine block を byte 埋め込み・sha ゲート内蔵
  （pin
  `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`）。
  header（ENGINE_BLOCK+PIN 行）は K1282 機体 verify_k1282.py
  （sha 7b70993a…・出版済み）から byte 流用・手転写ゼロ。
  TAMPER 環境変数で 10 種の変異電池（engine モードは engine_block.py
  の 1 byte 反転を模擬し rc=2 でゲート発火）。
- `engine_block.py`（2,540B）: 単体 engine block（pin と byte 一致）。
- `exploration/explore1.py` + `explore1.out`: 宣言前探査
  （E1–E10・E9 の G3z2 (1,1)→2 例外捕捉〔bad=1・FAIL 行〕を含む
  honest 記録）。
- `output/dryrun1.json`（+ `.info`）: D7 比較演算子の初版誤実装を
  fail-closed 検出した dry run（bad[6]=650・宣言ノート §3 honest 記録1）。
- `output/dryrun2.json` / `dryrun3.json` / `dryrun4.json`（+ .info:
  dryrun3 の info は当時 stderr 取得漏れで不在・記録上の時刻は
  宣言ノート §3 のとおり）: 全 green・counts 総計 33,691・bad 0・
  宣言ノート §4 の期待値と合致（3 本とも stdout sha cf182f24…）。

## 宣言期待値（公式実行の判定基準・宣言ノート §4 と同一）

- 正常走行: rc=0・counts
  `[6947, 64, 2976, 3388, 4278, 21, 650, 790, 8757, 5820]`・
  total_comparisons 33,691・overall_bad 0・h2_ones 7・
  n0_hist `{"1":454,"2":196}`・ii_hist `{"2":790}`・
  stdout sha256
  `cf182f24df6af7dc622f181011024e0447c5493291d63c8fa1b3f8666240df69`
  （volatile 情報は stderr のみ・canonical stdout は走行間で
  byte-identical）。
- 変異電池（10 種・すべて fail-closed 期待値）:
  `engine` rc=2 / `h2` rc=1 bad=6947 / `e1` rc=1 bad=56 /
  `q1` rc=1 bad=2940 / `band` rc=1 bad=3388 / `lzf` rc=1 bad=4278 /
  `ls` rc=1 bad=14 / `n0` rc=1 bad=650 / `ii` rc=1 bad=790 /
  `g3` rc=1 bad=4355。

## 実行方法

```
python3 verify_k1283.py                    # 正常走行 (stdout=audit JSON)
python3 verify_k1283.py --tamper=h2      # 変異電池
```

公式 4 走: 同一 cwd ×2（PYTHONHASHSEED=random / 1）+ 隔離 tree/env -i ×2
（PYTHONHASHSEED=99 / 7・`/usr/local/bin/python3`・HOME=/tmp）。
stdout 4 本の sha256 が宣言値と byte 一致することを要件とする。

## PROVENANCE

- engine pin: K1281/K1282 と同一の engine block（H_canonical/H_ordered
  双実装・byte互換）。pin は machine 内 `ENGINE_BLOCK_SHA256` 定数と
  埋め込み block の両方と機械照合（ゲート内蔵）。
- 依存定理（監査アンカー D10）: K0832 / K1265 / K1267 / K1269 / K1270 /
  K1278 / K1281 / K1282 の出版値を再照合。
- MANIFEST-sha256: 全構成ファイルの sha256（fetch-back 照合用）。
