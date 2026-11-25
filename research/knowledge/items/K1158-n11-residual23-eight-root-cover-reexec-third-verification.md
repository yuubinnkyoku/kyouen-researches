---
id: K1158
title: "残余23行 8根被覆判定（K1147外部第二検証）のpristine再実行第三検証: 入力散在stageのGitHub byteのみからの完全再生・4再実行+検証機3実行byte-identical・tamper 2件fail-closed捕捉・出版監査のbasename依存性の確定"
kind: computation
status: computed
topics: [search-methods, certificates, verification]
aliases:
  - "third verification (post-publication independent re-execution) of K1147 residual23 eight-root cover decision external second verification: five published input records scattered across five different experiment dirs were re-fetched from GitHub raw by SHA-256 pin only, the published decision machine was pristine-re-executed 4 times (2 same-cwd, isolated tree/cwd/HOME with re-copied inputs, isolated + PYTHONHASHSEED=random), every output byte-identical to the published decision record c5aaf83e (UNSAT, 18 gates, cover3 calls 451 / memo 211 / shapeB tries 100)"
  - "the published external verification machine was re-run 3 times on the four fresh re-execution outputs (2 same-cwd + isolated tree/cwd/HOME with published-stage basenames): every output byte-identical to the published audit 17dbd6ab with 71/71 checks, and both 1-byte tamper variants (decision record offset 7701; k1097 record offset 77) were caught fail-closed with no output written"
  - "reproducibility finding first observed here: the published verifier records input base names inside its pin-* check details, so byte-reproduction of the published audit requires the original stage file names (published-decision.json / k1097-refsolve.json / k1102-second-verification.json / lower-bound-audit.json); SHA-256 pins themselves are name-independent. no row closed; cover numbers remain candidate-root plan bookkeeping, not certificates"
relations:
  - type: verifies
    target: K1147
    note: 残余23行8根被覆判定の外部第二検証（出版 commit e8d6025745・外部検証機 7bee45ec・出版監査 17dbd6ab）の、出版後の別実行者によるpristine再実行第三検証。判定機 da51063c の4回pristine再実行が全て出版正本 c5aaf83e とbyte一致し、検証機3実行が出版監査 17dbd6ab とbyte一致（71/71）。入力5正本が5別実験dirに散在するwide stageの「出版byteのみからの独立再検証可能性」を第三者が確定した
  - type: depends_on
    target: K1147
    note: 本検証はK1147の出版byte（判定機・判定正本・K1097/K1102/下界監査5正本・外部検証機・出版監査）にSHA-256 fail-closed pinで依存し、それ以外の入力を使わない
artifacts:
- path: research/experiments/n11-residual23-eight-root-cover-decision-reexec-third-verification-20261120/README.md
  role: document
  note: 実験README（7 pin表・2段機械（判定機→外部検証機）の4+3実行手順・tamper 2件・ベース名依存性の記録・解釈規約・収穫物SHA）
- path: research/experiments/n11-residual23-eight-root-cover-decision-reexec-third-verification-20261120/scripts/verify_k1147_reexec_third_20261120.py
  role: verifier
  note: 第三検証harness（stdlibのみ・fail-closed・乱数・時刻・絶対path出力なし・7入力snapshot stage・判定機4回pristine再実行+検証機3回+tamper gate 2件・SHA-256 a9dcc35616ad5d649646bcb41c3853ac420c63923028e566fa31b2a8e9598f13・19,045 bytes）
- path: research/experiments/n11-residual23-eight-root-cover-decision-reexec-third-verification-20261120/output/third-verification-audit-20261120.json
  role: data
  note: 監査正本（SHA-256 2bb40f705f00b8bc24b24f9c133729a8f156f4f2285980d624568f610d64420d・5,349 bytes・pin 7/7・reexec pass 4/4・verifier run 3/3（71/71 checks）・tamper 2/2捕捉・rows_closed 0・interpretation_guard 5文言同梱・harness 4実行（同一cwd2+隔離+隔離+PYTHONHASHSEED=random）byte-identical）
- path: research/experiments/n11-residual23-eight-root-cover-decision-reexec-third-verification-20261120/inputs/published-decision.json
  role: data
  note: 入力snapshot（判定正本 c5aaf83e…・16,324 bytes）。inputs/配下の7 snapshot（計168,846 bytes・ベース名はK1147原本stageと同一）で実験dirは自己完結し、第三者がこのdirのみから再実行可能
- path: research/log/2026-11-20-n11-residual23-eight-root-cover-third-verification.md
  role: log
  note: 実行記録（取得→宣言→harness（転写ミス捕捉・ベース名依存の発見）→4実行→part1出版・fetch-back 10/10）
- path: research/log/2026-11-20-n11-residual23-eight-root-cover-third-verification-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit 887e594de70e41290d5db27590d4d971d91b4515・宣言2026-11-20T15:21:00Z・先行出版）
scope: >-
  K1147（残余23行 8根被覆判定の外部第二検証・出版 commit e8d6025745）のpristine再実行第三検証。
  GitHub上の出版byteのみから、(1) 5別実験dirに散在する入力5正本と外部検証機・出版監査を再取得して
  SHA-256 pin 照合、(2) 判定機 eight_root_cover_decision_20261120.py（da51063c…）のpristine再実行4回
  （同一cwd 2回・隔離tree/cwd/HOME入力複写・隔離+PYTHONHASHSEED=random）の出力が出版正本 c5aaf83e…
  （16,324 bytes・UNSAT・18 gate・cover3 451/memo 211/shapeB 100）と4回ともbyte一致、(3) 外部検証機
  verify_external_cover8_decision_20261120.py（7bee45ec…）の3回実行（同一cwd 2回・隔離tree/cwd/HOME
  ベース名保存複写1回）の出力が出版監査 17dbd6ab…（71/71 checks）と3回ともbyte一致、(4) 1 byte
  tamper（判定正本・K1097正本）の2件がfail-closed捕捉（returncode非零・出力未書込）、(5) 第三検証
  harness自身の監査が4環境実行（同一cwd2・隔離・隔離+PYTHONHASHSEED=random）でbyte-identical
  （2bb40f70…）、(6) part1出版のfetch-back検証 10/10 までを含む。行の閉鎖・証明書抽出・receipt fold・
  触れる宇宙/safe8述語の第三実装再導入・他レーン成果（fold26・round-5 refsolve・WIN8証明書抽出・
  zero-triple第4幾何）への着手は含まない。
evidence: >-
  （1）出版byte完全性: GitHub raw（main）から7ファイルを取得しSHA-256を機械照合（判定機 da51063c…・
  判定正本 c5aaf83e…・K1097 2896deb0…・K1102 d0b5d845…・下界監査 1310ef74…・外部検証機 7bee45ec…・
  出版監査 17dbd6ab…）全一致。輸送打ち切りなし。
  （2）判定機pristine再実行4回: 1 byteも改変せず、同一cwd 2回・隔離tree/cwd/HOME（入力は別path複写）
  1回・隔離+PYTHONHASHSEED=random 1回。全4回 returncode 0・出力SHA-256 c5aaf83e… が出版正本と
  byte-identical・UNSAT・18 gate all ok・cover3 451・memo 211・Shape B 100（K1147出版記録と全同一）。
  1実行あたり約43秒。
  （3）外部検証機3回実行: 4再実行出力を入力として同一cwd 2回・隔離1回（複写は出版stageのベース名を
  保持）で実行し、3回とも出力SHA-256 17dbd6ab… が出版監査とbyte-identical・71/71 check PASS
  （provider hist {1:40,065, 2:4,857, 3:297}・triple availability 891==3×297・greedy 9根
  gains {3:6, 2:2, 1:1}・exactly-once 23行分割・数え上げ証明書 k_min=2/k_max=1 の全記録事実が確認）。
  （4）tamper gate 2件: 判定正本 offset 7701 の1 byte XOR 0x01 →外部検証機のpin-decision gateが捕捉
  （returncode 2・出力未書込）。K1097正本 offset 77 の1 byte XOR →判定機自身のfail-closed pinが捕捉
  （returncode 1・K1097 sha256 pin FAIL・出力未書込）。
  （5）ベース名依存性（新規実験事実）: 外部検証機の監査JSONはpin-*チェックdetailに入力の
  os.path.basename()を記録する。ベース名が異なると（内容が同一でも）監査のbyte再現が崩れる
  （差分は4箇所のdetailのみ・全71 checkの判定はPASSのまま）。実験dirのsnapshot命名と隔離複写は
  この規約に沿って設計。SHA-256 pin自体はベース名非依存。
  （6）harness決定性と透明性: harness初版のK1102 pin定数に転写ミス（…f268…）があり、harness自身の
  fail-closed pinが初回実行で即捕捉（K1149出版時・K1155と同種の捕捉実例）。修正は正本実byteから機械
  抽出し7 pinを全機械照合後に実行。harness監査は同一cwd 2回＋隔離tree/cwd/HOME 1回＋隔離+
  PYTHONHASHSEED=random 1回の4実行でbyte-identical（2bb40f70…・sorted keys・時刻実行時間なし）。
  （7）出版とfetch-back: part1を commit 43512c4ba1f4a33d3a2a657ad030dc9327b86ae6（2026-11-20T15:57:56Z・
  10ファイル）で出版し、同commitのraw CDNから全10ファイルを再取得してcmp照合 10/10 byte-identical。
  本検証は残余23行のどの行も閉じない。監査下界8は任意の宇宙で有効・9はpool P‴に特有。被覆数は候補root
  計画の簿記であり証明書ではない。REFUTED-D10はLOSS証明ではなく、nodes/solved数を勝敗として読まない。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。
---

## 詳細

単一オーナー宣言ノート（commit `887e594de70e41290d5db27590d4d971d91b4515`・2026-11-20T15:21:00Z・先行出版）の下で、
[K1147 外部第二検証実験](../../experiments/n11-residual23-eight-root-cover-decision-external-second-verification-20261120/README.md)（出版 commit `e8d6025745`・2026-11-20T13:29:51Z宣言）に対して第三検証層を追加した:
出版byte 7 pin（判定機・判定正本・K1097・K1102・下界監査・外部検証機・出版監査）確認・判定機のpristine再実行4回の全byte一致・外部検証機の3回実行の全byte一致（71/71 checks）・1 byte tamper 2件のfail-closed捕捉・第三検証harness自身の4実行監査byte一致、である。

本検証の個性は、K1147の入力5正本が5個所の異なる実験dirに**散在するwide stage**である点にある。
実験dir自己完結型のK1151（K1155第三検証）と異なり、第三者はまず「どの正本がどこにあるか」を
出版文書のpinから再用意する必要がある。本検証はその再構成（散在5正本の特定とSHA-256照合）を
出版byteのみで完結させ、その上で判定機（約43秒/回）の4回再実行出力が出版正本 c5aaf83e とbyte一致し、
外部検証機が出版監査 17dbd6ab（71 checks）をbyte一致で再生することを確定した。

新規の実験事実が2点ある。(a) 出版外部検証機の監査JSONは入力のベース名をpin-* detailに記録するため、
出版監査のbyte再現には原本stageのファイル名（`published-decision.json` 等4名）が必要である
（内容pinはベース名非依存）。(b) harness作成過程のSHA-256転写ミス1件がharness自体のfail-closed pinで
捕捉された（K1149出版時・K1155と同種。正本実byteからの機械抽出で修正後に全実行）。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

詳細は[検証実験](../../experiments/n11-residual23-eight-root-cover-decision-reexec-third-verification-20261120/README.md)・
[検証機](../../experiments/n11-residual23-eight-root-cover-decision-reexec-third-verification-20261120/scripts/verify_k1147_reexec_third_20261120.py)・
[監査正本](../../experiments/n11-residual23-eight-root-cover-decision-reexec-third-verification-20261120/output/third-verification-audit-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual23-eight-root-cover-third-verification.md)・
[単一オーナー宣言](../../log/2026-11-20-n11-residual23-eight-root-cover-third-verification-single-owner-note.md)。
