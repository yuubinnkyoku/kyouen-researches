# 単一オーナー宣言ノート: fold22外部第二検証（K1167）のpristine再実行第三検証（2026-11-20）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold22 receipt fold（K1132）の**外部第二検証**として出版されたK1167実験一式に対する
**pristine再実行第三検証**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-20T21:15:01Z
- 宣言時点の main HEAD: `d323e780f950d6adea15b8bd7a3309e11d136d55`
  （K1167第三検証の先行宣言なし。fold21外部第二検証は並走レーンが宣言済み
  `98c90cb510`/`d323e780f9`・fold23外部第二検証は `90ac8eed`・fold25外部第二検証は
  `aad3b71ca` が宣言済みで、いずれも本宣言の対象外）
- 対象出版物: `research/experiments/n11-fold22-external-second-verification-root840500-20261120/`
  （part1 `4eb6cbf05..`・part2 item/log `19bcb1e04..`・part3 README bullet `5e1273f57..`）
- 対象正本（SHA-256）:
  - K1167 検証機 `scripts/verify_fold22_external_20261120.py`
    `ca11cbbc4b9d5ce3b1569d0af67060d20ec2873efdf3bd22720b3ba50b683792`（48,949 bytes）
  - K1167 監査正本 `output/external-audit.json`
    `b4b082f8cb0aa943aad7458ae0c6eb179a27704c5ea781eb18907d869c97522c`（141,752 bytes・gate 1463）
  - K1167 実行記録 `output/reproduction.log`
    `5059c458ec08e046a74356bfb7fb6a796865b0c0fb97f12ca983093991c53a90`（2,559 bytes）
  - K1167 実験README `README.md`
    `6b32ce997aa160cbb82bed10e89c11e9eba31d77dccf2c94cbe46e2694206d88`（10,287 bytes）
  - K1167 再構成機 `scripts/reconstruct_inputs.py`
    `dfa50996463fe31000e2bc3b03e37dabe33981bf00708a29ae7634d4a6594a27`（10,102 bytes）
  - 上流fold22出版byte 4点（receipt `f6e011f4…`・出版機 `d5721408…`・生成機 `a73995be…`・
    README `0e6861bf…`）はK1167検証機自身のP-gate pinが検証対象とする入力である。

## 位置づけ

K1167（fold22外部第二検証）は出版社（外部第二検証レーン）が外部実行と第三実装検証機の
全再導出（1463 gate）を出版済みだが、出版後の第三者が出版byteだけから検証機の監査正本を
byte再生できること（pristine再実行第三検証）はまだない。本検証で確定するのは、
K1167の実験dir 5ファイル・W再構成・検証機・監査正本が輸送・転写・ローカル記憶に依存せず
再現可能であることである。

## 作業範囲（受入条件）

1. K1167出版byte 5点をGitHub（pinned commit `4eb6cbf05..`）から再取得し、SHA-256 pin照合を
   fail-closedで行う（W入力はK1167検証機自身のpin gateが再照合する）。
2. 出版済み再構成機 `reconstruct_inputs.py`（`dfa50996…`・固定Git参照 `34c29854c64286bbb1792ff28dc1973aef341e20`）
   でW入力tree（12 Git blob + 43 SHA-256 = 55 pinとchain機4点を含む）を**2回**独立に再構成し、
   2回のW全ファイル（copied machines・manifestを除く収録55 pin対象＋chain機4点）が
   byte一致することを確認する。
3. K1167検証機（`ca11cbbc…`）をpristine再実行する（計4回: 同一cwd 2回＋隔離HOME/cwd＋
   `PYTHONHASHSEED=random` 1回を含む）。全実行の監査JSONが出版監査正本 `b4b082f8…` と
   byte-identicalであること（各実行はfold22機pristine 4回・fold21機推移rerun・
   別実装再導出1463 gate・出版社T-gate tamper 2件〔worklist@1099・K1125証明書@21212〕の内訳を含む）。
4. tamper検査: 出版社検証機・本レーンharnessが検査済みのoffsetと**異なる**位置で
   1 byte XOR 0x01を入力に施した実行が、fail-closed（returncode≠0・監査未書込）で
   捕捉されることを3件確認する（本レーンのoffset: W入力 `inputs/worklist.csv` offset 1234・
   W入力K1125証明書 offset 17522 → 出版検証機自身のpin gateで捕捉。
   出版監査正本 `output/external-audit.json` offset 4096 → 本レーンharnessのpin gateで捕捉）。
5. 本レーンharnessの監査正本JSON（時刻・実行時間フィールドを含まない決定論的出力）は、
   同一cwd 2回＋隔離＋`PYTHONHASHSEED=random` の3実行でbyte-identicalであること。
   300秒cap下の段階実行のため、harnessはstage分割（pin|reconstruct|rerun r1..r4|tampers|finalize）
   し、finalizeは既存stage記録のfail-closed検査の下で監査を組立ること。
6. 監査正本に解釈ガード文言（行を1行も閉じない・UNKNOWNのまま）を同梱すること。

上記1〜6の受入条件は本宣言の受入条件を構成する。

## やらないこと・非主張

- fold21外部第二検証（`98c90cb510`/`d323e780f9`所有）・fold23外部第二検証（`90ac8eed`所有）・
  fold25外部第二検証（`aad3b71ca`所有）・fold26 receipt fold（`23bffdd4e4`所有）・
  round-5 refsolve（`ace38772d9`所有）・WIN8-D10候補 `00000000010000809002000040002001`
  の証明書抽出（`63877ffd2e`所有）・WIN8証明書行共有監査（`c403614f`所有）は
  他レーン宣言済みで着手しない。新規depth-10 probe・新規証明書抽出・行の閉鎖claimは
  一切行わない。K1167出版社自身によるpost-publication記録は本宣言の対象外とする。
- K番号はpush時に3点確認で空きを取得する（現時点では仮番号も確定しない）。
- 本検証は検証の検証（簿記・決定性・入力pin・fail-closed防衛の再検査）であり、
  関係する行は1行も閉じない。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
  REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**

失敗・timeout・入力取得失敗・api.github.com rate limitも実験事実として記録し、
部分的な数値のみで成果としない。重要証拠は再現可能なrepo成果物として出版する。
