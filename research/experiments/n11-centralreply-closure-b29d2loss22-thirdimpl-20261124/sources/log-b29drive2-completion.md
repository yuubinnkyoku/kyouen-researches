# Part CI takeover drive-2 完了 log (2026-11-24): batch-29 (closure class 2251) 残38キー完走 — batch-29 全54キー probe-complete

単一オーナー: n11中央応答レーン (長期レーン本セッション)。宣言:
`research/log/2026-11-24-part-ci-takeover-batch29-drive2-declaration.md` (commit
`ec9c7191`・push戻りgit blob sha1 `a4350fe5dae8ae45f2edbff72355834827764a0f` =
ローカル事前計算と一致・fetch-back sha256 `8819c366…` byte一致)。
takeover正当化・継承pin・protocol D1-D5は宣言ノートどおり (CI takeover session 3.5h無音
21:52:36Z→01:2xZ・Part U/Z/CG/CI基準)。

## 1. 結果 (honest probe labels・verdict不消費)

- **batch-29 全54キー (ab001..ab054) probe-complete**: 2-pass fresh-cold budget 15M・
  **54/54 p1/p2 node-exact (54 PASS + 1 WIN-HALT行・status.log 55行・append-only)**・
  MISMATCH 0・truncated 0・EXHAUSTED 0・P-FAIL 0。
- **verdict内訳** (honest label): **LOSS 53 / WIN 1 / EXHAUSTED 0**。
  WINは **ab028** のみ (key (1297036830121656320, 131074)・s5 93815・legal 80・
  membership 3・nodes **3,167,121**・WIN-CONTINUE設計どおり継続・status.log に
  `WIN-HALT ab028` 行として記録)。
- drive-2 (ab017..ab032 checkpoint分 + ab033..ab054 final分): 38キーすべて PASS系
  (loss 37 / win 1)・drive-2 nodes合計 (p1単計) **162,492,687**。drive-1分 16キー
  **57,463,971** (Part CVのpinned-replica値 `57,463,971/pass` と一致)・batch-29全体
  **219,956,658**。
- **val-gate fresh 4/4 node-exact** (本host初回solver実行・D2): at2m×2 (result 0,
  nodes 2,000,000)・15m×2 (result 2, nodes 3,651,923 / 5,040,200)。published
  baselinesと一致 (wall_s比較外)・`*.d2-host.out` として出版。
- 予備的機械一致確認 (宣言D4のとおり公式row-auditは別セッション): 全54キー
  p1/p2がreplay行 field 6/7/8 (budget,result,nodes) で一致・`# replay_done` 54/54・
  status.logのPASSキー集合 == 54キー全体・EXHAUSTED/MISMATCH/TRUNCATED行なし。

## 2. 出版 (全fetch-back byte一致)

- 宣言 `ec9c7191` (宣言ノート) → **checkpoint 2/3 `dc93e5d6`** (38 files:
  ab017..ab032 raw 32 + val-gate d2-host 4 + drive2_step.sh 1 + status.log) fetch-back
  38/38 → **B final `c608660e`** (45 files: ab033..ab054 raw 44 + status.log 55行) fetch-back
  45/45。実験dir `research/experiments/n11-centralreply-closure-class2251-batch29-20261123/`。
- status.logは published drive-1 prefix (16行) のまま純append (21:43:13Z開始行は不変)。
  kit (scripts/input)は不変・実験dir READMEは本Partでは更新せず (checkpoint・finalとも
  drive-1先例と同じ最小構成・row-audit担当セッションが更新する)。

## 3. 誠実記録

- runbatch.shは byte-clone のまま実行 (rc=45 WIN-HALTをorchestration層で捕捉し
  WIN-CONTINUE・runner自体は一切変更せず)。drive2_step.sh (session-local) は
  checkpointで出版済み (残キー動的列挙・`timeout 260` wrap・2 worker・`if rem`ガード)。
- truncated pass 0・環境リセット 0・solver異常終了 0。push 1件で戻り値parse TypeError
  (push自体は成功・HEAD確認で重複pushなし・commit `dc93e5d6` はfetch-back 38/38で無傷)。
- 並走観察 (すべて非接触): push前にHEADが前進したことが3回 (K1276完結 `dc…`系
  高速レーン出版・Part CY batch-31宣言 `afc1bcc5` + scaffold・Part CP takeover
  `87e19b5a`)。いずれもbatch-29領域に非接触のためfast-forwardで出版継続。

## 4. UNKNOWN担保 (宣言・原CI宣言と同一)

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343・class 2251 (54キーすべて・ab028 WIN行を
含む)・class 343k (34269)・class 5804 (batch-31・Part CY所有) は本Partの実行・出版の
どの時点でもUNKNOWNのまま。** nodes数・wall秒数を勝敗として読まない。
ab028のWIN行は honest labelのまま (verdict不消費)。閉鎖・被覆・secured・
root勝敗の主張はしない。WIN/LOSS採用は scrutiny owner C++第二実装 gate
`9193f5b6…` 通過後の別adoption Part (pinned merger `90711961…` 経由) のみ。

## 5. レジューム (着手前に必ず最新main再取得・hourly並走注意)

次回最有力:
- (a) **batch-29 row-audit** (54行全行の公式監査・Part CV先例の
  `row_audit … v2` 形式でdrive-2 38行のp1/p2照合・status.log整合・キー/入力照合) —
  別セッション実施を原CI宣言が予定していた窓口。
- (b) **drive-2 LOSS 37行のloss-only adoption Part** (CU先例: merger `90711961…`・
  BASE `30ddad9d…` 6,317行に増分merge・reaudit込みフルセッション) — ただしclass 2251の
  serving 38キー (rank 4) に対する本adoptionが closure表をどう動かすかは出版物の
  機械値として確定するまで主張しない。**ab028 WIN行は採用対象外 (scrutiny専権)**。
- (c) ab028第三実装交叉検証 (CW/CX kitのb29適応・nodes 3,167,121でreplica 2-passは
  inner window内) はCX系レーン候補に追加可能 (CXオーナーの進行確認後に)。
- (d) Part CY (batch-31 class 5804)・Part CP takeover (batch-30) は並走所有・非接触。
