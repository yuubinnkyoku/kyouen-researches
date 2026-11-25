---
id: K1060
title: "第9〜第12 WIN7-D10証明書の第三方法（交差乗算有理式）独立検証とsweep43/census・fold/resolve5の静的交差監査（全gate合格・出版流量と全件一致）"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases:
  - third-method (cross-multiplied rational circle solve) verification of the ninth to twelfth WIN7-D10 certificates
  - static third-implementation audits of the K1057 census/sweep43 witness structure and the ninth-twelfth fold and resolve5 records
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K0007
  note: ranked AND/OR certificateの構造と検証境界
- type: depends_on
  target: K1057
  note: 検証対象となる第9〜第12証明書・sweep43・fold・resolve5の出版正本
- type: depends_on
  target: K1046
  note: resolve4残余86行と117-rootプール判定の設定
artifacts:
- path: research/experiments/n11-ninth-twelfth-win7-third-method-verification-20261119/README.md
  role: source
  note: 実験の目的・方法・再生手順・結果一覧
- path: research/experiments/n11-ninth-twelfth-win7-third-method-verification-20261119/scripts/verify_third_method.py
  role: verifier
  note: 証明書1枚の第三方法検証器（交差乗算整数式・python3 stdlibのみ・repoコード非読取）
- path: research/experiments/n11-ninth-twelfth-win7-third-method-verification-20261119/scripts/audit_sweep43_census.py
  role: verifier
  note: sweep43/census静的監査（43根の構造と被覆関係・分類とnodes総計の第三再導出）
- path: research/experiments/n11-ninth-twelfth-win7-third-method-verification-20261119/scripts/audit_fold_resolve5.py
  role: verifier
  note: fold/resolve5交差監査（9 S6行閉鎖・frontier・universe・39 witnessの第三再計算）
- path: research/experiments/n11-ninth-twelfth-win7-third-method-verification-20261119/scripts/run_third_method_verification_20261119.sh
  role: verifier
  note: 出版repoファイルのみから6成果物を再生するwrapper（第9証明書はbase64 -d|gunzip復元）
- path: research/experiments/n11-ninth-twelfth-win7-third-method-verification-20261119/output/win7-root-00000000000000801202000001040200-third-method-verification-20261119.json
  role: data
  note: 第9証明書の第三方法検証出力（39 gate全合格・visited 171,066/terminal 27,410）
- path: research/experiments/n11-ninth-twelfth-win7-third-method-verification-20261119/output/win7-root-00000000000000821082040200000000-third-method-verification-20261119.json
  role: data
  note: 第10証明書の第三方法検証出力（39 gate全合格・visited 96,862/terminal 15,936）
- path: research/experiments/n11-ninth-twelfth-win7-third-method-verification-20261119/output/win7-root-00000000000000821092200000000000-third-method-verification-20261119.json
  role: data
  note: 第11証明書の第三方法検証出力（39 gate全合格・visited 56,207/terminal 8,516）
- path: research/experiments/n11-ninth-twelfth-win7-third-method-verification-20261119/output/win7-root-00000000001020003800000048000000-third-method-verification-20261119.json
  role: data
  note: 第12証明書の第三方法検証出力（39 gate全合格・visited 61,065/terminal 9,191）
- path: research/experiments/n11-ninth-twelfth-win7-third-method-verification-20261119/output/sweep43-census-third-method-static-audit-20261119.json
  role: data
  note: sweep43/census静的監査出力（17 gate全合格）
- path: research/experiments/n11-ninth-twelfth-win7-third-method-verification-20261119/output/fold-resolve5-third-method-cross-check-20261119.json
  role: data
  note: fold/resolve5交差監査出力（62 gate全合格）
scope: >-
  K1057が出版した第9〜第12 WIN7-D10証明書4枚の戦略木全体、43-witness掃引と
  86行censusの静的構造、4-receipt foldとresolve5の簿記主張を、第三の実装・
  第三の代数経路（円方程式のCramer解を交差乗算した整数判定式・共線組は
  直線外積式）で独立検証したことの記録。探索の新規実行・行の新規閉鎖・
  勝敗の確定は対象外。
evidence: >-
  （1）方法: 3点を通る円 x²+y²+Dx+Ey+F=0 をCramer則で厳密に解き分母Wで交差乗算した
  整数式 W*(s_d-s_1)+DD*(x_d-x_1)+EE*(y_d-y_1)==0 で第4石のbanned判定を行い、
  W==0の共線3点組は直線外積式 dx*(y_d-y_1)-dy*(x_d-x_1)==0 に分岐する。除算・
  浮動小数点なし、python3標準ライブラリのみ、repoコードは読まない。既存の
  BigInt 3×3余因子展開・4×4整数Bareissとは独立の経路で、512サンプル三つ組で
  lifted-cofactor法とのbannedセル完全一致を照合（不一致0）。replay規約は
  出版検証器と同一（rootの各合法loser応手がsubroot、偶数深さは証明書行に厳密
  追随、奇数深さは全合法応手展開、loser詰み>=13石で終端、winner詰みなし）。
  （2）証明書4枚: 第9（72 subroot・84,928行・visited 171,066・winner 110,087/
  loser 33,569・edge 153,450・terminal 27,410）・第10（56・45,450・96,862・
  62,415/18,511・86,443・15,936）・第11（47・24,375・56,207・36,361/11,330・
  51,440・8,516）・第12（51・26,756・61,065・39,578/12,296・55,923・9,191）が
  いずれも出版BigInt流量と全一致、per-subroot統計は出版Bareiss（72/56/47/51）
  と全件一致、証明書SHA-256・行数・root（7石・D4正準・safe・法定手数
  72/56/47/51）はextractionサマリと全一致、strategy/visited union差分0/0、
  終局石数[13,17]、各39 gate全合格。第9の入力は出版 .n11.gz.b64 から
  base64 -d | gunzip で復元しSHA pin一致をgate検証。
  （3）sweep43/census静的監査（17 gate）: 43 pair witnessが86行を各行ちょうど
  1回被覆（被覆集合==resolve4残余86行）、43根すべて7石・D4正準・safe・RAW
  maxbit child・被覆関係（8-D4像−1石の正準形）を第三実装で再導出し完全一致、
  probe 86件のnodes・cap・loss・pilot_d6制御が出版記録と全件一致、分類
  （WIN 4・REFUTED 39・CAPPED 0・矛盾0）とnodes総計173,165,148をraw記録から
  再導出一致、WIN 4根は第9〜第12証明書rootと完全一致。
  （4）fold/resolve5交差監査（62 gate）: foldが閉じた5親target 8行の被覆関係、
  9 S6行閉鎖（8 target行＋第10のextra行 00000000000000801082080400000000
  cost 80）、closed_edge_cost総計667==163+227+133+144、S6保存則（1,626→1,635）、
  frontier 6,222行/492,688→6,213行/492,021・parent incidence 11,848→11,826・
  5親target 26→34/112（残余78行）を第三再計算で全一致。resolve5残余78行==
  86行−fold閉鎖8行、universe 7,969の再列挙一致（in_pool 93・既知REFUTED 46・
  fresh 7,830 = safe 4,728 + unsafe 3,102）、39 witnessの7石・D4正準・safe・
  78行完全1回被覆・43 sweep根および4 receipt根との不交、verdict pool
  379 REFUTED/168 WIN、matched 78/stranded 0/maximum matching 39を再構築一致。
  （5）再現性: 入力はrepo出版正本のみで、wrapper 1本で6成果物が約19秒
  （逐次1プロセス）で再生される。2回実行で wall_s 以外はbyte一致
  （cert_pathは出版ファイル名を記録しスクラッチ位置に依存しない）。
  全6 JSONの全gate（39×4+17+62 = 235）が合格・failed_gates空。
  （6）解釈規約: 本検証はK1057出版事実の検証強化であり勝敗の進展ではない。
  REFUTED-D10はLOSS証明ではなく、foldは行被覆の簿記、resolve5の39 witnessは
  条件付き計画である。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4はすべてUNKNOWNのまま。
---

# 第9〜第12 WIN7-D10証明書の第三方法独立検証と静的交差監査

## 命題・範囲

K1057の出版成果（第9〜第12 WIN7-D10証明書、sweep43/census、4-receipt fold、
resolve5）に対して、既存の二検証器（BigInt 3×3余因子展開・4×4整数Bareiss）と
replica再現とは独立の第三実装・第三の代数経路で、証明書の戦略木再生と静的な
被覆・簿記主張の監査を行った。すべてのgateが合格し、出版された状態流量・
行集合・基数と完全に一致した。

## 方法

円の方程式をCramer則で厳密解し、分母を払った交差乗算整数式

```
W*(s_d - s_1) + DD*(x_d - x_1) + EE*(y_d - y_1) == 0    (s = x^2 + y^2)
```

で第4石 d のbanned判定を行う。W==0（3点が共線）のときは直線外積式

```
dx*(y_d - y_1) - dy*(x_d - x_1) == 0
```

に分岐する。除算・浮動小数点を一切使わない整数演算のみの経路であり、512サンプル
三つ組で lifted-cofactor 法とのbannedセル完全一致を照合した（不一致0）。

## 結果

- **証明書4枚（各39 gate）**: 第9 00000000000000801202000001040200（72 subroot・
  84,928行・visited 171,066・terminal 27,410・edge 153,450）、第10
  00000000000000821082040200000000（56・45,450・96,862・15,936・86,443）、第11
  00000000000000821092200000000000（47・24,375・56,207・8,516・51,440）、第12
  00000000001020003800000048000000（51・26,756・61,065・9,191・55,923）。
  出版BigInt流量・Bareiss per-subroot統計・extractionサマリと全件一致、
  union差分0/0、終局石数[13,17]、fbt詰みなし。
- **sweep43/census静的監査（17 gate）**: 43 pair witnessが86行を各行ちょうど
  1回被覆、43根の7石・D4正準形・安全性・RAW maxbit child・被覆関係（8-D4像
  −1石）を全件第三再導出で確認、分類 WIN 4/REFUTED 39/CAPPED 0/矛盾0・nodes
  総計173,165,148をraw probe記録から再導出一致、WIN 4根は証明書rootと一致。
- **fold/resolve5交差監査（62 gate）**: 9 S6行閉鎖（8 target行＋extra行
  00000000000000801082080400000000 cost 80・閉鎖関係も第三再導出）・
  closed_edge_cost 667==163+227+133+144・S6保存則・frontier 6,222/492,688→
  6,213/492,021・5親target 26→34/112・残余78行の再計算一致・universe 7,969
  再列挙一致・39 witnessの78行完全1回被覆と不交性・verdict pool 379/168・
  matched 78/stranded 0/matching 39の全照合合格。
- **再現性**: wrapper 1本でrepo出版入力のみから6成果物を約19秒で再生
  （第9証明書は .n11.gz.b64 からbase64 -d | gunzip復元、SHA pin一致）。
  2回実行で wall_s 以外byte一致。全gate 235個が合格。

## 限界

- 検証はK1057の出版事実の正しさの確認であり、探索の新規実行・行の新規閉鎖は
  行っていない。resolve5の39 witness掃引は本項の出版と同時刻に並走レーンが
  実行・出版した（K1059: WIN 0/REFUTED 39・候補供給枯渇の確定）が、K1059の
  掃引結果の検証は本項の対象外である。
- 第三方法も証明書の規約（depth-10内のWIN7-D10・RAW child・pilot制御）の
  健全性を前提とする。規約自体の検証はK1057のtrust境界と同じ。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべて
  UNKNOWNのまま。**
