# Part CI takeover 宣言 (2026-11-23): batch-29 (closure class 2251) drive-1 — 中断Part CIのtakeover (publish-then-execute)

単一オーナー: n11中央応答レーン (長期レーン本セッション・takeover)。takeover対象:
Part CI 宣言 commit `efd2d488` (2026-11-23T17:27Z出版・note `research/log/2026-11-23-part-ci-batch29-declaration.md`)。

## 0. takeover正当化 (宣告session消失判定・Part U / Part Z / Part CG takeoverと同一基準)

- Part CI宣言 (17:27Z) 以降 **3時間30分以上** (本宣言push直前 20:5xZ時点)、scaffold以降の
  batch-29系commit (outputs・status update・完了log) はmainに存在しない。scaffold commit
  `c6ae987a` (scripts 3 + input 55 + val-gate 12 + README + MANIFEST) で停止しており、
  実験dir `research/experiments/n11-centralreply-closure-class2251-batch29-20261123/` に
  output/ は存在しない (最新main b215813a で確認済み・dir listingで再確認)。
- 同一時間帯に Part CJ (17:32-17:39Z)・Part CK (17:40Z-)・Part CL (17:41-17:51Z)・
  Part CM・Part CN (18:38-19:28Z)・Part CO (20:10-20:32Z) が他セッションで出版されて
  おり、Part CI宣言sessionのみが長時間無音。batch-29 continuation宣言・takeover宣言・
  所有権の再主張は存在しない (push直前 最新main直近12コミット + code searchの機械grep済み)。
- よって Part U (batch-8) / Part Z (batch-11) / Part CG takeover (b28drive2win) と同一基準で
  **宣告session消失**と判定し、本セッションがPart CI (batch-29 drive) をtakeoverする。
  原CI所有sessionが後に復帰して本takeoverより先にdrive結果を出版した場合はその出版物を
  正本として扱う (先着出版が正本・重複実行はliteratureとして残す)。
  本takeoverは原宣言のgoal・stop rules・検証gateの意味論を変更しない。

## 1. 継承 (原Part CI宣言・scaffoldの全pinを本hostで再検証済み)

- **kit byte-pin再検験 (宣言前read-only fair開示)**: 本hostで published scaffold 71エントリ
  中70エントリ (README 56fa34e3… 別途一致・MANIFEST自身を除く) をcommit-pinned raw fetchし
  `sha256sum -c` で全件一致。特に kernel 4件 = jsreplay.js `84585617…` / runbatch.sh
  `f591f8c2…` / make_batch29_keys.py `44575cb2…` / batch-keys.json `330c0b9f…` はREADME記載pin
  と完全一致。なお **solver実行 (val-gate fresh・probe) は宣言後にのみ実行する**
  (事前実施はfetch・sha検証・JSON構造確認・runner source reviewのみ・上記のとおり開示)。
- **継承するstop rules (runbatch.sh byte-clone内蔵・不変)**: budget 15M・2-pass fresh-cold・
  WIN rc=45 (事前登録: drive-1でWIN 2行観測でwave halt・batch-28 drive-1/2と同じ設計)・
  MISMATCH rc=42 hard-stop・p1/p2 fail rc=43/44・`# replay_done`のないpassファイルは
  TRUNCATED-RETRY (evidenceでない)・EXHAUSTED (result 0) は honest UNKNOWN (same-condition
  再probeなし・継続)。54キー ab001..ab054 (s5昇順 3964..93841・legal 79..101)。
- **orchestration層 (Part CN運用知見の継承・stop rulesとは独立)**: 各worker起動は
  `timeout 260` でwrapし外側shell上限290sに対してinnerを先発火させる (truncated passは
  guardが次invocationで回収)。2 worker (2-key parallel) 上限・2核host。status.logはappend-only。
  残キー列挙が空の場合のsession script空キーバグ (runbatch.sh "") 防止の `if rem` ガードを
  事前登録する (Part CNの教訓)。

## 2. 本takeoverの追加事前登録 (原CI protocolへの追加・意味論不変)

1. **takeover-host val-gate fresh 4**: 原CI scaffoldのval-gate (sanctioned 4キー: at2m×2 budget
   2M・15m×2 budget 15M・published baselines byte-verified) を本hostで再実行し
   `*.takeover-host.out` として出版。判定: published baselines 4件との node-exact一致
   (result・nodes・replay_done・wall_sは比較対象外)。不一致ならhard-stop。
2. **drive-1実行**: 未完キーをab001からs5昇順に2キーずつ並列でprobe。WIN-HALT設計どおり
   WIN 2行観測でwave haltしdrive-1終了。EXHAUSTEDは継続 (honest UNKNOWN)。
3. **出版**: outputsは原CI宣言どおり本dirのoutput/ (raw p1/p2 outs + status.log) に蓄積し、
   drive-1完了時 (またはセッション時間切れによる誠実打ち切り時) に出版。
   row-auditは別セッションで実施予定 (原CI宣言どおり)。
4. **drive-2+**: drive-1終了後に実行時間が残る場合、WIN-CONTINUE (Part CE/CK/CN先例・
   orchestration層のみの継続・runner内蔵stop rules不変) を**別の短いdrive-2宣言noteの
   出版後に**実行する。drive-2の宣言は残キー集合・継続設計を機械確定した上で出版する。

## 3. 事前機械確認 (read-only・正直開示)

- takeover判定に使った観測はすべて本宣言の出版前に取得した機械データ (コミット一覧・
  dir listing・sha256検験)。probe key選択のcherry-pick不可能性は原CI宣言のfail-closed
  maker `44575cb2…` (batch-keys.json pin `330c0b9f…`・54キー固定) がすでに担保しており、
  本takeoverは鍵集合・順序を一切改変しない (ab001..ab054のpublished順・runbatch.shへは
  未完キーを昇順で渡すのみ)。
- 原CI宣言の UNKNOWN担保・不接触条項を全部継承する。

## 4. UNKNOWN担保 (原CI宣言と同一)

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて)・class 2251
(54キーすべて・本batch-29の全キーを含む)・class 34269 は本Partの実行・出版のどの時点でも
UNKNOWNのまま。** nodes数・wall秒数を勝敗として読まない。WIN/LOSS probe行は honest label
のまま (verdict不消費)。採用は scrutiny owner C++第二実装 gate `9193f5b6…` 通過後の
別adoption Part (pinned merger `90711961…` 経由) のみ (本レーンは代行しない)。
閉鎖・被覆・secured・root勝敗の主張はしない。

## 5. 不接触

Part CG takeover (宣言 d5e9acc2 18:01Z・outputs停滞中) のdir・outputs・進行 (本宣言時点では
takeover判定の記録のみ行い、本セッションでは着手しない)、batch 1..28各published dir (不変)、
BASE caches (`3124461b…` 6,294行 Part CH merged・`854800f3…` 6,301行 Part CO merged) は
read-only不変、fast lane・finite-field lane・inversive lane・19root計画、EXHAUSTED行の
高budget再probe (別宣言条件)・WIN行のscrutiny (C++ `9193f5b6…` 専権)。
