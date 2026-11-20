# K1167（fold22外部第二検証）のpristine再実行第三検証: 監査byte再現・W入力再構成・pin再照合・tamper防衛の独立確認（2026-11-20）

## 位置づけ

K1167（commit `4eb6cbf05` 出版・fold22 receipt fold の外部第二検証）は、fold22正本
（K1132・root `00000000000000801202000000840500`）の全主張を第三実装検証機
`verify_fold22_external_20261120.py`（gate 1,463）で値単位再確認し、監査正本
`output/external-audit.json`（141,752 bytes・SHA-256 `b4b082f8..`）を出版した。
本実験はその**第三検証**（K1165 が fold24/K1164 に対して行った手続きの fold22/K1167 適用）である:
同じrepoの出版byteのみを素材に、(a) K1167実験dir 5ファイルのpinned commit再取得とSHA-256照合、
(b) K1167同梱の再構成機 `reconstruct_inputs.py` を固定Git参照で2回独立実行したW入力treeのbyte一致確認、
(c) 出版K1167検証機を**改変なしに（pristine）** 4回実行して全監査出力が出版正本とbyte一致すること、
(d) 本レーン独自offsetのtamper 3件が出版社・K1167双方のfail-closed防衛と本harness自身のpin gateで
捕捉されること、(e) 本harness監査の決定性、を独立に確かめる。

単一オーナー宣言: [宣言ノート](../../log/2026-11-20-n11-k1167-fold22-ext2-pristine-reexec-third-single-owner-note.md)
（commit `53501d73`・受入条件6項目・宣言時点でfold22 ext2 pristine-reexec laneは不在）。

## 固定pin

K1167出版5ファイル（part1 commit `4eb6cbf05` から再取得・fail-closed照合）:

- `README.md` SHA-256 `6b32ce997aa160cbb82bed10e89c11e9eba31d77dccf2c94cbe46e2694206d88`（10,287 bytes）
- `scripts/reconstruct_inputs.py` `dfa50996463fe31000e2bc3b03e37dabe33981bf00708a29ae7634d4a6594a27`（10,102 bytes）
- `scripts/verify_fold22_external_20261120.py` `ca11cbbc4b9d5ce3b1569d0af67060d20ec2873efdf3bd22720b3ba50b683792`（48,949 bytes）
- `output/external-audit.json` `b4b082f8cb0aa943aad7458ae0c6eb179a27704c5ea781eb18907d869c97522c`（141,752 bytes）
- `output/reproduction.log` `5059c458ec08e046a74356bfb7fb6a796865b0c0fb97f12ca983093991c53a90`（2,559 bytes）

再構成機の固定Git参照 `34c29854c64286bbb1792ff28dc1973aef341e20`（K1167検証機が監査JSONに
記録したrefそのもの・trees APIは12 legacy blob pinのSHA→path写像のみに使用）。
上流fold22出版byte 4点（receipt `f6e011f4..`・機 `d5721408..`・builder `a73995be..`・README `0e6861bf..`）は
2回の再構成で出力された両pub copyでSHA-256照合・相互byte一致を確認した。
固定byte写しの同梱は省略する（本実験dirはK1167本体と同様にraw pinned URL＋
同梱再構成機＋SHA-256 pinsで独立再現可能・byte重複を避ける）。

## 実施内容と結果

本レーンharness `scripts/verify_k1167_fold22ext2_third_20261120.py`
（stdlibのみ・fail-closed・stage分割設計: pin | reconstruct-w1 | reconstruct-w2 | wcmp |
rerun-r1..r4 | tampers | finalize・各stageは1コマンド枠内で完了）。

- **pin（6 gate）**: 上誅ファイルをpinned commitから再取得しbyte照合。5/5一致。
- **reconstruct ×2**: K1167同梱の再構成機を同一固定refで2回独立実行。
  W1/W2ともpub 4・blob 12・sha256 48行（43 PIN256 pin + 5 chain機）のwrite_checkedで
  returncode 0。**实験事実**: 試行1回目はapi.github.comの共有IP無認証枠でHTTP 403
  rate limit（quota 0・21:45:19Zリセット）に到達し、fail-closedで中断・記録保存のうえ
  リセット後に同一手順で再試行し成功（workaround不使用・失敗も实験事実として
  stage recordに保存）。
- **wcmp（10 gate）**: 2本のW treeは60ファイル・14,673,721 bytesで全ファイルbyte-identical
  （manifestのpath欄のみ相違・対象外）。両manifestは同一ref・pin数（12 blob + 43 SHA-256）・
  機械リスト一致。fold22 pub 4ファイルも両再構成間でbyte一致。
- **pristine再実行4回（X相当）**: r1（同一cwd）・r2（同一cwdでのin-place反復・K1167検証機自身の
  x1/x2方式と同じ）・r3（独自再構成W2 + 隔離cwd/HOME）・r4（W2のfresh copytree +
  隔離cwd/HOME + `PYTHONHASHSEED=random`）の全4回がreturncode 0・stderr空・
  stdout `ALL 1463 GATES PASS` + UNKNOWNガード行・出力監査SHA-256 `b4b082f8..` が
  出版正本とbyte-identical。1実行は実測35.0秒（user 28.7秒・fold22機6回起動込み・
  K1167出版時実測約34.4秒と整合）。
- **tamper 3件（T相当・本レーン独自offsetでfold22出版社・K1167レーン双方が未試験）**:
  t1 copytree W上の `inputs/worklist.csv` byte offset 1234 と
  t2 `k1125/certs/win8-root-00000000000000801202000000840500-20261120.n11` byte offset 17522 の
  1 byte XOR 0x01は、K1167検証機自身のW pin gateが`W blob pin`・`W sha256 pin`で
  returncode 1・監査未書込で捕捉。t3 K1167出版監査byte offset 4096の1 byte XOR 0x01
  （实験dir写し上）は本harness自身の实験dir pin gateが`pin mismatch`で捕捉。
  本番W1/W2/W4・両pub copyは無改変（battery後に55 pin全部再照合で確認）。
- **finalize（9 gate）**: 監査正本 `output/harness-audit.json`
  （4,853 bytes・SHA-256 `fdb72c4072e983a109bd1e8713a084a77154a9b7bddf2420548a421714226ca3`）
  は同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random`の3実行でbyte-identical
  （時刻フィールドなし・sort_keys決定論的）。

实行記録は `output/reproduction.log` に置いた。

### 实験事実まとめ

1. K1167監査は第三者環境からでも「出版byte＋同梱再構成機」のみで完全再現可能
   （API rate limit障害を含めて再現手順は公開byteで一意に決まる）。
2. 共有IP上のapi.github.com無認証quotaは併走レーンとの共喰いで枯渇し得る。
   fail-closed設計は取得失敗を「部分W」ではなく「中断＋記録」に落とし、
   固定refからの再取得で冪等に復旧する。
3. K1167検証機のW pin gateは出版社のT-gate（machine内 `input blob/sha mismatch`）とは
   別layer（検証機のI-section `W blob/sha256 pin`）で、本レーンの2探針もこのlayerで捕捉された。
   検証機監査（`b4b082f8..`）への直接tamperは本harnessの实験dir pin gate（第三layer）で捕捉され、
   三層防衛が实測で独立に作動した。
4. part1 push時のREADME転輌1文字の転訮タイポ（実→实相当・1 byte）をfetch-back byte検証が即捕捉し、
   単一ファイル訂正コミットで修正した（証渎連鎖のpush事例と同様の頲止パターン）。

## 再現手順

```
# 1. K1167 5ファイルをpinned commit 4eb6cbf05 から取得して配置（pinned commit 4eb6cbf05 から再取得）
python3 scripts/reconstruct_inputs.py <W_dir> <pub_dir> [<git_ref>]
python3 scripts/verify_fold22_external_20261120.py <W_dir> <pub_dir> <out_json>
# <out_json> のSHA-256が b4b082f8.. なら第二検証の再現成立
python3 scripts/verify_k1167_fold22ext2_third_20261120.py <stage>   # pin/reconstruct-w1/reconstruct-w2/wcmp/rerun-r1..r4/tampers/finalize
```

`<pub_dir>` はfold22出版实験dir（fold22出版实験dirのbyte 4ファイル）、
第三検証harnessのstateは作業dir直下（env `K1167THIRD_ROOT` で変更可）。
finalizeの出力が `fdb72c40..`（4,853 bytes）なら本实験の再現成立。

## 限界（解釈規約）

本検験はK1167監査の決定性・入力pin・fail-closed防衛の再検査であり、
S6行・五親target行を1行も閉じない。fold22 receipt自体の6行閉鎖（残余35→32行）は
Publisherの成果簿記であり、K1167はその外部第二検証、本实験はその第三検証である。
WIN8-D10証明普は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空直・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4は
すべてUNKNOWNのままである。**
