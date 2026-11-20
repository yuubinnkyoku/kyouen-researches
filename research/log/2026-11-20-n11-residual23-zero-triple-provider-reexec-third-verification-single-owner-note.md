# 単一オーナー宣言: 残余23行 zero triple provider（K1148）pristine再実行による第三検証

- 宣言時刻: 2026-11-20T14:53:03Z
- オーナー: 本レーン（n11 残余23行 zero-triple-provider 再実行第三検証）。同一成果物の並走レーンが存在する場合は先着出版を優先し、後着は撤退して記録する（AGENTS.md 規則）。

## 対象

K1148（残余23行 残余23行宇宙の zero triple provider 幾何・第三独立再構成、commit `6564fded75038c887c095873c5d3e5633c4fcd35`・2026-11-20T14:28:01Z 出版）の実験一式の pristine 再実行による第三検証。

出版 pin（上記 commit の raw CDN から取得し、SHA-256 3点とも一致を本宣言前に確認済み）:

- 実験dir: `research/experiments/n11-residual23-zero-triple-provider-third-geometry-20261120/`
- 検証機 `scripts/audit_zero_triple_providers.py`: SHA-256 `cb8c95c8799e6c12bbc7fdb2cc9b6236f664724f29827e56d2e75de62a084892`（14,225 bytes）
- 入力 `input/residual23-provider-input.json`: SHA-256 `51e7a465e18646097073e4f8231f89cbff327d05f9bfeac102e57c754b4ff822`（3,105 bytes）
- 出版監査 `output/third-geometry-audit.json`: SHA-256 `526eada2c94457f06a7cf27a86011586e394c342687e539a6b545b42577b9573`（4,418 bytes）

## 範囲

byte 同一の上記 3 ファイルに対して:

1. 同一 cwd で 2 回の pristine 再実行
2. 機械一式と入力を複写した隔離 cwd・隔離 HOME の別 tree で 1 回
3. 隔離環境に加え `PYTHONHASHSEED=random` で 1 回（計 4 回）
4. 各出力の出版監査との SHA-256・byte 一致確認
5. tamper test（fixture の 1 byte を変更した偽入力で fail-closed pin が捕捉されることの確認）

を、stdlib のみ・fail-closed・乱数・時刻・環境依存出力なしの独立検証機（harness）で実施する。harness 自身の決定性（同一 cwd 2 回＋隔離 cwd 1 回の監査 byte 一致）も確認する。

幾何の新規計算、残余行の閉鎖、他レーン成果の検証、K1146/K1147/K1149/K1151 レーン成果の改変は行わない。

なお本宣言前に実施した事前 probe として 1 回の pristine 再実行（実行約 4.2 秒・出力 SHA-256 出版監査と一致・byte 一致、12 checks PASS `third-independent-geometric-reconstruction-passed`）を兵站的事実として記録する。

## item 採番

本検証の item は K1153 を取得する（現 main の次の空き番号。K1150=general-multiset merge レーン〔14:39:25Z 先着〕、K1151=replace9 whole-record 第二検証〔自レーン〕、K1152=y12 two-token fit レーン〔14:50:56Z 再採番 commit `855d7d98cd`〕を確認済み）。K1149 二重採番（replace9 reexec 先着 14:30:20Z vs six-row 後着 14:31:45Z）は本レーンの管轄外のため触れない。

## 解釈規約

本検証は残余23行のどの行も閉じない。zero rows の列挙は残余行の勝敗決着ではない。nodes/solved 等の計数を勝敗として読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
