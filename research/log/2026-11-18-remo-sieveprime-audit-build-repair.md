# 2026-11-18 K0939実験dirのaudit_build.py混入の診断と修復

K0941ログの次課題「K0939実験dirのaudit_build.py混入」を実施。高速レーン。

## 診断

- `remo-sieveprime-endgame-20261118/audit_build.py`（1,033 bytes）は
  `output/sieveprime_audit.json` とbyte同一（sha256 76ed144d…）の
  **監査JSON本文そのもの**で、builderスクリプトがrepoから欠落していた
  （出版時のファイル混入。dirへのコミットは K0939 出版の単一コミット
  b0bac427 のみ）。
- **監査JSON自体は正しかった**: 本文から末尾改行を除いた sha256 が
  出版値 `07d844c62df54014d8b720a98dbcd51e44dd6e50b52d74c8b05a3e2d03f6a0b3`
  （K0937型builderは sha256(out) を印刷してから out+"\n" を書く）。
- committed監査JSONの構造（小文字check名・region・first_fails・
  runs_identicalラッパ）はK0937のaudit_build.pyと同一パターンで、
  committed sieveprime_verify.py の run_checks()（大文字check名）からの
  明示的フィールド写像で再構成可能と判明。

## 修復

- K0937のaudit_build.pyパターンで失われたbuilderを再構成:
  run_checks() を2回in-process実行して一致確認し、
  `output/sieveprime_audit.json` を書く（フィールド写像:
  engine.games=ENGINE.count・entry.prime_games=ENTRY.count・
  family.family_states=FAMILY.count・pinrepro.games=PINREPRO.count・
  pin.{p,uv}_sha256_8=PIN.{p,uv}_sha256・pinsieveはcountを落とす・
  regionはモジュール定数 MBIG/M_REPRO/M_ENG/FAM_W から）。
- 検証（本環境・pin表は ../remo-pc-twin-laws-20261117/data/ から取得）:
  - run_checks() 3回実行すべて all_ok・決定的。
  - 再生成 output/sieveprime_audit.json が committed監査JSONとbyte同一
    （cmp 0差分・sha256 76ed144d…）。
  - builder印刷sha256 == 出版値 07d844c6…。
  - 2回のbuilder実行で出力byte同一（各回 run_checks 2回込み・約66秒/回）。
- これにより fresh checkout から K0939 の機械アンカーが
  byte-exactに再現可能になった（出版report/itemの監査記述がそのまま
  真になる。report/item/output/verify.py/core は無編集）。

## 備考

- 同種の混入が他の実験dirにないかは本項では走査していない
  （K0937/K0941/K0943のaudit_build.pyは本体確認済み）。
  残る実験dirのaudit_build.py一斉sha256点検は次回の候補。
