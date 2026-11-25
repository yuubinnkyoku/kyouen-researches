# 2026-11-19 two-token y=1 parametric universal proof (P1, all z)

## 選定

前回レーン（2026-11-19	parametric census）は予想P1を z = 1..60 の有限
センサスで支持し、「次の自然成果物は symbolic-band  verifier / z一括証明」
を残した。高速レーンの最優先未解決（かつセッション内で完結可能）な
この項目に着手した。

## 並走出版との差分化（K1022 → K1023再採番）

本レーンの実行中に、並走実行が同じ候補公式を**z>=6限定**でK1022として
出版した（item `K1022-two-token-y1-parametric-z-ge-6.md`・commit fd397b0c、
実験dir `vertical-fiber-two-token-y1-parametric-proof-20261119`・
commit 9179cce6・census verbatim由来のsignature-band構成）。本レーンの
Theorem P1は**全z>=1とz=0基底cand0**を別構成（型機械）で証明しており、
K1022の主張の厳密な拡張として重複しない。よって:

- 実験dirは`vertical-fiber-two-token-y1-parametric-allz-proof-20261119`へ
  改名してpush（並走の同名dirを上書きしない）。
- itemはK1023として採番（K1022への`generalizes`関係を明記）。
- 相互クロスチェック（下記）で両成果の一致性を機械確認した。

## 成果

1. **z=0スライス閉形式 cand0 の初導出**。素エンジンの独立センサス
   （x <= 60, R <= 200）から行パターンを読み取り、閉形式として固定。
   x=1: P0={1}; x>=2: T0={3}; x奇>=3: P0={1}∪E[4,x+1];
   x偶>=2: P0={1}∪E[4,x]∪I[x+2,∞); R=0で0。エンジン照合不一致0。
2. **スライス恒等式の確認**。cand(z,x,R) == mex({A=cand(z,x-1,R-1) [x>=2],
   B=single_token(x,z+1,R-1), C=1^cand(z-1,x,R-1)（z=1では1^cand0）}）を
   公式レベルで z=1..40, x<=40, R<=x+z+41 の131,200点、不一致0。
3. **型機械による全称化**。z>=2: 3パリティ＋6差分族（±8窓・±9番兵）＋
   x=1ビット、z=1/z=0: 絶対/相対クリップ族。実現型 10,750 / 5,458 / 4,994
   を |v|<=60・(x,R)<=（140,320/140,300) のボックスで完全列挙し、
   型ごとに恒等式を検査。証人対confluence 6,275組・不一致0。
   box 45→60 で実現型集合同一（安定性の追加証拠）。
4. **検証器本体**（`verify_p1_universal.py`, 808行, 純Python, 決定論的）：
   23チェック・1,875,269照合点・全ok・不一致0・約5秒・2回実行で
   audit.json byte-identical。押付け項目: 素エンジン二種アンカー（z=0..6・
   z=7..12深部）、K1018/K1020公開公式一致、選択肢分解アンカー、
   seed遠方probe 200k（z,x<=3000・R<=9000）、境界多様体probe
   （z∈{2,3,97,98,997,998,2999,3000}の全族多様体掃引）、z=0/z=1遠方
   probe 120k（x<=5000・R<=15000）、v空間シェル掃引[61,120]
   （箱外新規型0）、2変数リング掃引600k（x<=300・R<=1000・新規型0）。

## 並走K1022検証器との相互クロスチェック

並走実験dirの検証器`verify_y1_parametric_proof.py`を取得し、本環境で
相互検証した:

1. **相手検証器の完全再現**: V0..V7全チェックがpass（約50秒）し、相手の
   `output/audit.json`をbyte-identicalに再生した。
2. **閉形式一致**（census由来の2式が独立導出で一致）:
   - z=6..80・x<=60・R<=x+z+99 の780,750点・不一致0
   - 遠方probe z∈{97,98,997,998,2999,3000}・x<=30 の253,860点・不一致0
3. **拡張領域の素エンジン直接照合**（本項のみが主張するz<=5とz=0を、
   K1022検証器の素再帰エンジン2種H_ordered/H_canonicalが直接検証）:
   - z=1..5・x<=25・R<=x+z+30 の5,875点、cand==両エンジン・不一致0
   - z=0・x<=25・R<=2x+30 の1,425点、cand0==両エンジン・不一致0
   - z=0広域・x=26..40・R<=2x+10 の1,155点・不一致0
   合計1,043,065点・全て不一致0。このプロセスを
   `cross_check_k1022.py`（監査出力`output/cross_check_k1022.json`・
   決定論的）として実験dirに同梱し、CIで再実行・diff検査する。

## 証明構成（report.md抄訳）

cand0（z=0基底・全称）→ z=1スライス（C=1^cand0）→ z>=2一括
（C=1^cand(z-1)、z強帰納）。帰納各段の本体は有限型空間の完全走査。
子の読みは閾値|t|<=6・シフト±2・窓±8・番兵±9（マージン1）で親型から
決まる（シフト閉鎖補題・Appendix B閾値表）。実現型は|v|<=45の連鎖証明
（釘8＋番兵9×鎖長3＋domain調整）でボックス内に証人を持つ
（証人境界補題・Appendix A）。両補題の機械証拠: confluence全組照合・
シェル[61,120]・リング・遠方probeすべて新規型0・不一致0。

## 接続と次のレーン

- センサスのConjecture P1は**定理になった**（z<=60の有限枠は完全に除去）。
- K0877/K0977/K0985/K1003/K1012/K1016/K1017/K1018/K1020のy=1スライスは
  すべて本項の系（generalizes）。
- **次の高速レーン候補**:
  a) P2 height-only縮約の一般証明（R<=z+1帯でcand==single_token(x+1,z,R)、
     本マシンのz帰納を帯上で再利用。センサスの有限観察はz=1..60済み）。
  b) y>=2族への同型機械の拡張（子分解は同じA/B/C、cand_{y>=2}の行構造が
     未抽出。z=16,y=1は本定理で不要になったことの確認も含む）。
  c) 3トークン以上・一般トークン族への帰納の骨格調査。
- 11×11巨大探索は長期レーンのまま。本証明の6差分族+窓の型機械は
  root証明の枝刈りとは独立だが、固定幅・q点版の安定化長問題への
  応用（冨の帯構造の一般則）は記録に値する接続点。

## push前repo整合性監査（2026-11-19・本レーン/session）

main HEAD a4469632時点で、`tools/knowledge/check.py`相当の検査は
**本レーンのpushより前に既に306エラー**で落ちることを、1004 itemの
ローカルレプリカ（raw CDN取得・PyYAML互換サブセットで解析）で確認した。
内訳はすべて他レーン由来で、本レーンpush後もCIのcheck/buildステップは
この既存状態を引き継ぐ:

- **K0926-K0951のREMO系バッチ18件**: `date`/`tags`未知フィールド、
  `artifacts`が文字列リスト（mapping必須）、`relations`が
  `{depends_on: [...], connects: [...]}`辞書形（`connects`は語彙外）、
  `topics`/`aliases`欠落、`status: mixed`（K0931・K0933、語彙外）。
- **`date:`フィールドのみの違反が追加47件**（K0952-K0987付近の
  two-token系item群含む）。
- **重複ID 3組**: `K0936-remo-sieve7-uv-mod210` vs `K0936-two-token-z6-y25`、
  `K0974-p2207-full-drat-audit` vs `K0974-two-token-z6-y-ge4`、
  `K0975-p3251-full-drat-audit` vs `K0975-two-token-z6-uniform`。
  README・log・experiment report双方が自レーン側のK番号を引用しており、
  再採番は両レーンの合意（アービトレーション）が必要で本レーンでは手つかず。

本pushで実施した最小修復は次の2件のみ（意味論に触れないバイト切れの復元）:

1. `K0942-two-token-z6-y28-boundary.md`: ファイル末尾の閉じ`---`直後の
   改行1バイトが欠損しfront matter解析が落ちていた → 改行を補完。
2. `K0955-two-token-z6-y32-boundary.md`: 閉じ`---`行そのものが欠落
   （本文`## 命題`直前に挿入）。

いずれもartifactパス（z6-y28/y28・y32のreport・audit・log）の上流実在を
確認済みで、修復により当該2 itemは検査0エラーとなる。K0980-K0982
（z7,y4-6・`kind: theorem`/`created`/`tags`等の非正規front matter）は
意味を変えうる再構成が必要なため本レーンでは**手つかず**（越権回避）。

`research/knowledge/generated/`の6 viewは、上流`build.py`が上記REMO
バッチでSystemExitするため現状再生成不能であり、本pushには含めない。
これによりK1023（およびK1022）はindex/relations等のview行を持たないが、これは
K0926以降にpushされた全item（K1016-K1021等を含む）と同じ既存状態で
ある。views再同期にはバッチ正規化・重複ID解消が先行必要。

## 本pushの内容（2026-11-19）

単一コミットで次を反映した:

1. `research/experiments/vertical-fiber-two-token-y1-parametric-allz-proof-20261119/`
   （report.md・verify_p1_universal.py・cross_check_k1022.py・output/audit.json・
   output/cross_check_k1022.json の5ファイル）
2. `research/knowledge/items/K1023-two-token-y1-parametric-allz-universal-proof.md`
3. `research/log/2026-11-19-two-token-y1-parametric-allz-universal-proof.md`
4. `research/knowledge/README.md`（K1023弾丸1件の追記のみ）
5. `.github/workflows/knowledge.yml`（K1022監査step直後にK1023検証器・
   クロスチェックの監査step 1件挿入のみ）
6. K0942・K0955のバイト切れ修復2件（上記・意味に触れない1バイト改行と
   閉じ`---`行1行の復元のみ・上流raw bytesとの差分を事前確認済み）

push直前に最新main（HEAD bf8b0530）を再取得し、K1023採番の空き・allz実験
dirの空き・K0942/K0955の未修復状態・ymlのK1022 step登録を確認した上で
反映した。
