# z1-delta45-ladder-20261124 — K1284 専用機体（宣言 66f06ad2(+訂正 c5709b87) の protocol 実行用・公式実行の前に凍結）

宣言ノート: `research/log/2026-11-24-z1-delta45-ladder-single-owner-note.md`
（commit 66f06ad2・訂正 c5709b87〔§3 E1 探査 hist 記載の修正と push
競合の honest 記録・宣言期待値は不変〕・publish-then-execute）。
本キットは §4 の機械監査 protocol D1–D10 の実行体であり、
公式実行は fetch-back 機体から行う。

## 構成

- `verify_k1284.py`（17,685B・sha256
  `377acf932143d40f5cd39fbed220f0965b8a6e70934a35aeaee3ae3eb822af82`）:
  電池 D1–D10。engine block を byte 埋め込み・sha ゲート内蔵
  （pin
  `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`）。
  埋め込み block は出版 chain（K1138→K1257→K1281→K1282→K1283）の
  ものを byte 流用・手転写ゼロ。TAMPER 環境変数相当の CLI で 7 種の
  変異電池（`--tamper-engine`〔rc=2〕・`--tamper=l4|z5f|ls2|ii12|alpha|fl`
  〔rc=1〕）。
- `engine_block.py`（2,540B・sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`）:
  単体 engine block（K1283 出版 kit の同梱 file と同一 bytes。
  import 行の配置が埋め込み block と異なるため sha は block pin と
  一致しない・埋め込み block 自体の sha を機体が起動時に検証する
  設計は K1282/K1283 と同一）。宣言前に独立参照実装と
  R<=8・arity<=3・token<=8・z<=2 の 3,936 点で突合 bad 0 済み
  （宣言ノート §3）。
- `exploration/explore_k1284.py` + `explore_k1284.out`: 宣言前探査
  （E1–E9・§3 honest 記録: E1 の tall-giant 48 点は hist 集計
  対象外〔860 点全て 0〕・E7/E8 は open 登録用 census）。
- `output/dryrun1.json`–`dryrun4.json`（+ `.info` ×4）: 4 走とも
  全 green・counts 総計 13,120・bad 0・byte-identical
  （PYTHONHASHSEED 1/random/99/7・~3.7s/走）。

## 宣言期待値（公式実行の判定基準・宣言ノート §4 と同一）

- 正常走行: rc=0・counts
  `[860, 480, 43, 858, 2506, 683, 420, 463, 4800, 2007]`・
  total_comparisons **13,120**・overall_bad 0・
  l4_hist `{"0":860}`・z5f_hist `{"1":480}`・
  alpha_hist `{"1":2499,"2":7}`・ls2_val j=1..11 全 2・
  stdout sha256
  `703199490ea26659ab458d8498d94a9c3de45912d647451fadd6b93f2de0e64c`
  （volatile 情報は stderr のみ・canonical stdout は走行間で
  byte-identical）。
- 変異電池（7 種・すべて fail-closed 期待値）:
  `--tamper-engine` rc=2（engine sha ゲート発火・変異後 sha
  `0ea47a80…` ≠ pin）/ `--tamper=l4` rc=1 bad=860 /
  `--tamper=z5f` rc=1 bad=480 / `--tamper=ls2` rc=1 bad=11 /
  `--tamper=ii12` rc=1 bad=810 / `--tamper=alpha` rc=1 bad=2506 /
  `--tamper=fl` rc=1 bad=322。

## 実行方法

```
python3 verify_k1284.py                     # 正常走行 (stdout=audit JSON)
python3 verify_k1284.py --tamper=l4       # 変異電池
```

公式 4 走: 同一 cwd ×2（PYTHONHASHSEED=random / 1）+ 隔離
tree/env -i ×2（PYTHONHASHSEED=99 / 7・`/usr/local/bin/python3`・
HOME=/tmp）。stdout 4 本の sha256 が宣言値と byte 一致することを
要件とする。

## PROVENANCE

- engine pin: K1281/K1282/K1283 と同一の engine block
  （H_canonical/H_ordered 双実装・byte互換）。pin は machine 内
  `ENGINE_BLOCK_SHA256` 定数と埋め込み block の両方と機械照合
  （ゲート内蔵）。
- 依存定理（監査アンカー D7/D8）: K0832 / K1265 / K1267 / K1269 /
  K1270 / K1278 / K1281 / K1282 の出版値（T-H1・T-L3・T-C4・
  T-Q・T-LC・T-II・T-E・J1/J2 など）と K1282/K1283 の床・行1基底
  （F2–F5・G3z2・B2z3・T-H2・T-E1・T-N0z1）を再照合。
- MANIFEST-sha256: 全構成ファイルの sha256（公式実行後の成果物
  出版時に同梱・fetch-back 照合用）。
