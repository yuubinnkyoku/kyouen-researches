---
id: K1147
title: 残余23行 8根被覆判定（K1097最小被覆9・interval [9,9]）の外部第二検証: 出版機4実行byte-identical・記録交差71チェック全PASS・数え上げ証明書の外部再計算・triple availability総和恒等式891==3×297
kind: computation
status: computed
topics: [search-methods, certificates, verification]
aliases:
  - external second verification of the eight-root cover decision over pool P-triple-prime (published UNSAT, minimum cover 9, K1097 interval [8,9] collapsed to [9,9]): published machine re-executed pristine 4 times (2 same-tree, isolated cwd/HOME, isolated + PYTHONHASHSEED=random), all byte-identical to the published master c5aaf83e
  - 71 record-level cross-document checks pass (rows/demand/hist/greedy/matching/gates/pin-chain across K1097, K1102, lower-bound audit, decision master); counting certificate recomputed externally (k_min=2 > k_max=3*8-23=1, both published derivations have no k in 0..8)
  - new cross-identity: per-row triple availability table sums to 891 == 3 * 297 (each triple provider covers 3 rows); availability range 0..140, mean 38.74, top-6 rows (all `...82108...` family) share 86.5%, 3 zero rows plus 2 rows below 5
relations:
  - type: verifies
    target: K1097
    note: 8根被覆判定（UNSAT・最小被覆9・数え上げ証明書・interval [8,9]→[9,9]）の出版機・出版正本・入力pin鎖の外部第二検証。判定が確定したgreedy9根計画の候補根数最小性の独立確認
  - type: depends_on
    target: K1102
    note: K1097 refsolve第二検証正本（d0b5d845…・23行・demand・greedy選定・matching witness）を交差検証の入力として使用し、行集合・demand・greedy9根・matching 23の文書間一致を確認
artifacts:
- path: research/experiments/n11-residual23-eight-root-cover-decision-external-second-verification-20261120/README.md
  role: document
  note: 実験README（4実行byte-identical・71チェック・数え上げ証明書の外部再計算・availability二極化観察・trust境界）
- path: research/experiments/n11-residual23-eight-root-cover-decision-external-second-verification-20261120/scripts/verify_external_cover8_decision_20261120.py
  role: verifier
  note: 外部検証機（出版機と別実装・stdlibのみ・fail-closed・5出版pin＋4再実行出力を入力に71チェック・環境非依存出力）
- path: research/experiments/n11-residual23-eight-root-cover-decision-external-second-verification-20261120/output/external-verification-audit.json
  role: data
  note: 監査正本（SHA-256 17dbd6ab…・71 checks all ok・3実行byte-identical・interpretation_guard 5文言同梱）
- path: research/log/2026-11-20-n11-residual23-eight-root-cover-decision-external-second-verification.md
  role: log
  note: 実行記録（宣言参照・発見順・環境依存性の出版前捕捉と修正・次回への引継ぎ）
- path: research/log/2026-11-20-n11-residual23-eight-root-cover-decision-external-second-verification-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit e8d6025745・2026-11-20T13:29:51Z）
scope: >-
  K1097残余23行8根被覆判定（commit b4d8b3ac52出版）の外部第二検証。出版byte 5ファイルの
  SHA-256 pin確認、判定機のpristine再実行4回（同一tree 2回・隔離cwd/HOME・別path入力1回・
  隔離+PYTHONHASHSEED=random 1回）による出版正本とのbyte一致、4正本＋4再実行出力だけを
  入力とする記録レベル交差検証71チェック（行集合・demand・hist・greedy・matching・gate・
  pin鎖・数え上げ証明書の算術）、triple availability総和恒等式891==3×297の確認、
  availability分布の測定記録。触れる宇宙・safe8述語・provider幾何の第三実装による再導入、
  新規probe・掃引・証明書抽出・receipt fold・行の閉鎖は含まない。
evidence: >-
  （1）出版byte完全性: main（fcabb2f585時点のbyte）から取得した判定機 da51063c…・判定正本
  c5aaf83e…・K1097 2896deb0…・K1102 d0b5d845…・下界強化監査 1310ef74… の5 SHA-256 pinが
  全て一致（輸送破損なし）。
  （2）pristine再実行4回: 1 byteも改変していない同一byte判定機を、同一tree 2回（各41〜42秒）・
  隔離tree/隔離cwd/隔離HOME/別path入力 1回（42秒）・隔離+PYTHONHASHSEED=random 1回で実行し、
  出力は全4回とも出版正本とbyte-identical（SHA-256 c5aaf83e…）。判定UNSAT・gates 18・
  cover3呼び出し451・メモ211・Shape B試行100も全実行同一。出版社の3実行に加えhash
  randomization明示環境での決定性を追加支持。
  （3）外部検証機71チェック全PASS（fail-closed・stdlibのみ・乱数・時刻・環境依存の出力なし・
  同一cwd2回+隔離cwd/HOME別path1回の3実行で監査正本byte-identical・SHA-256 17dbd6ab…）:
  23行集合の4文書一致・per-row demandの全文書一致と総和50,670==40,065·1+4,857·2+297·3・
  hist総和==45,219==監査providers・eligible 5,154==4,857+297・生成事象150,765==23×C(115,2)・
  宇宙137,959==45,263+92,696・providers 45,219==45,263−44・除外50==44接触+6非接触・
  greedy9根のK1097/K1102選定完全一致と23行exactly-once分割（gains {3:6,2:2,1:1}）・
  matching 23の3文書一致・gate 18全ok・監査interval [8,9]==判定before・[9,9]==after・
  下界8==ceil(23/3)・pin鎖3段（判定→3入力・監査→K1097/K1102・K1102→K1097）の再確認。
  （4）数え上げ証明書の外部再計算: 3行provider零行
  00000000000000003800000008002010・0000000000000000380000000a080000・
  00000000020000801202000000100000 がavailability表で0であることから、これらを被覆する根は
  高々2行被覆であること、k_min=ceil(3/2)=2、k_max=3·8−23=1、判定機記録の両導出
  （2k+3(8−k)≧23 と 21−k≧20）がk=0..8の全kで解を持たないことを外部実装で再計算し一致。
  （5）新規交差恒等式: triple availability表（23行分）の総和891==3×297（各triple providerは
  3行を被覆する。出版README未記録）。availability分布は範囲0..140・平均38.74で、上位6行
  （値140/139/131/126/120/115・全て82108型）が86.5%を占め、零行3行+2未満（値2・3）2行の
  2族に二極化。3行provider零の構造理由特定（判定実験README次の課題3）の材料。
  （6）透明性: 検証機初版は出力detailに入力絶対pathを混入させ隔離実行でbyte差分が発生
  したため、path正規化を行い3実行byte-identicalを確認後に出版（修正後のみ出版・正本の
  環境非依存性規約を検証機にも適用）。
  本検証は行を1つも閉じない。被覆は候補root計画の簿記であり証明書ではない。REFUTED-D10は
  LOSS証明ではなく、nodes数・solved数を勝敗として読まない。監査下界8は任意の宇宙で有効な
  まま（9はP‴特有）。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。

---

## 詳細

単一オーナー宣言ノート（commit `e8d6025745`・2026-11-20T13:29:51Z・先行出版）の下で、
commit `b4d8b3ac52`（K1097更新・commit `cb31752551` 宣言）で出版された
[8根被覆判定実験](../../experiments/n11-residual23-eight-root-cover-decision-20261120/README.md)の
外部第二検証を実施した。出版byte 5 pinの確認、判定機のpristine再実行4回（PYTHONHASHSEED=random
含む）の全byte-identical確認、外部検証機71チェック（K1097・K1102・監査・判定正本の4文書交差と
数え上げ証明書の算術再計算）、triple availability総和恒等式891==3×297の確認、
availability二極化の測定記録からなる。

検証実行中に、判定が最小性を与えたgreedy 9根depth-10掃引が並走レーンのK1146
（commit `e9ea153bc4`・13:35:51Z・WIN8-D10 candidate 1根+REFUTED-D10 8根）として着地した。
本検証はK1146の実施内容には影響しない（着手権・実行済み掃引の妥当性はそれぞれの機械と
宣言が管理する）。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

詳細は[検証実験](../../experiments/n11-residual23-eight-root-cover-decision-external-second-verification-20261120/README.md)・
[監査正本](../../experiments/n11-residual23-eight-root-cover-decision-external-second-verification-20261120/output/external-verification-audit.json)・
[研究ログ](../log/2026-11-20-n11-residual23-eight-root-cover-decision-external-second-verification.md)。
