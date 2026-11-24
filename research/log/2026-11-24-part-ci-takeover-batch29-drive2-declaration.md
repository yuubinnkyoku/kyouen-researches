# Part CI takeover drive-2 宣言 (2026-11-24): batch-29 (closure class 2251) 残38キー ab017..ab054 — 停滞CIオーナーからのtakeover (publish-then-execute)

単一オーナー: n11中央応答レーン (長期レーン本セッション・drive-2 takeover)。takeover対象:
Part CI takeover宣言 `f35ef5ae` (2026-11-23T20:57:47Z・drive-1) の後続 drive-2。

## 0. takeover正当化 (宣告session消失判定・Part U / Z / Part CG re-takeover / Part CI takeover と同一基準 3.5h無音)

- Part CI takeover session (drive-1) は checkpoint 1/3 `a5a159d7` (2026-11-23T21:52:36Z出版・
  32 pass files ab001..ab016 + status.log 16 PASS行・全LOSS) を最後に、drive-2宣言note・
  outputs・status更新・完了logを一切出版していない。本宣言push直前 (2026-11-24T01:2xZ時点) で
  **3時間30分以上の無音** (21:52:36Z + 3.5h = 01:22:36Z超過を機械確認)。
- 時系列 (最新main commit一覧で機械確認): CI drive-1 checkpoint 21:52:36Z → CS (23:18Z-) →
  CT (00:03Z-) → CU (00:14Z宣言・16-LOSS adoption出版 00:22-00:25Z) → CV (00:17Z宣言・
  ckpt-1/3 16キー row-audit+replica+第三実装出版 00:17-01:07Z) → CW (00:24Z宣言・完了) →
  CX (00:49Z宣言・scaffold A `3185a672`) → K1276 (01:02Z)。**batch-29 drive-2宣言・
  continuation・所有権の再主張は存在しない** (最新main 3b6ad066 の直近コミット点検・
  commit message一覧の機械grep済み)。CV完了log (3b6ad066) はdrive-2を「Part CIオーナー専権・
  停滞takeoverは別宣言条件」と記録しており、本宣言がその別宣言条件に対応する。
- よって Part U / Part Z / Part CG re-takeover (4h30m) / Part CI takeover自体 (3.5h) と同一基準で
  **CI takeover session消失**と判定し、本セッションがbatch-29 drive-2 をtakeoverする。
  原CI所有sessionが後に復帰して本takeoverより先にdrive-2結果を出版した場合はその出版物を
  正本として扱う (先着出版が正本・重複実行はliteratureとして残す)。
  本takeoverは原CI宣言・CI takeover宣言のgoal・stop rules・検証gateの意味論を一切変更しない。

## 1. 継承 (全pinを本hostでfetch・sha256機械検証済み・solver実行は宣言後のみ)

- **kit byte-pin再検験 (宣言前read-only fair開示)**: commit-pinned raw fetch (HEAD 3b6ad066) で
  scripts/input/val-gate/drive-1 outputs を取得し検証:
  - kernel 4件 = jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df` /
    runbatch.sh `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84` /
    make_batch29_keys.py `44575cb244ad02535a6878a4dd5d105971dc791354d3b8bc536004fd6970d873` /
    batch-keys.json `330c0b9f3166e9f6e21b739a851a881d800ab9f58a14dccaa0c772118dee716c`
    — 4/4 宣言pinと sha256 完全一致。
  - input 54 csv (ab001..ab054)・val-gate 16 publishedファイル・status.log 16行・
    drive-1 raw 32 files (ab001..ab016 p1/p2) fetch完了・構造確認 (replay行 field=
    order,stones,legal,is_or,budget,result,nodes,wall_s,key_lo,key_hi)。
  - **solver実行 (val-gate fresh・probe) は本宣言の出版後にのみ実行する**
    (宣言前はfetch・sha検証・runner source review・JSON構造確認のみ・aboveのとおり開示)。
- **継承するstop rules (runbatch.sh byte-clone内蔵・不変)**: budget 15M・2-pass fresh-cold・
  MISMATCH rc=42 hard-stop・p1/p2 fail rc=43/44・`# replay_done`のないpassファイルは
  TRUNCATED-RETRY (evidenceでない)・EXHAUSTED (result 0) は honest UNKNOWN (same-condition
  再probeなし・継続)・WIN rc=45 (runbatch.sh内蔵の事前登録halt)。
  **drive-2はWIN-CONTINUE** (Part CE/CK/CN先例・CI takeover宣言§2.4どおり):
  orchestration層のみ rc=45 を捕捉して次キーへ継続 (runner byte は一切変更しない・
  status.logのWIN-HALT行はrunbatch.sh自身がappend)。
- 継承する制約: 54キー ab001..ab054 (s5昇順・batch-keys.json pin)・鍵集合・順序は一切改変しない。
  drive-1完了分 (ab001..ab016・全LOSS・CU採用済み) は再実行しない
  (no-15M-re-search規約・runbatch.shのpass-file guardが同一batch条件の再probeを排除)。
  残キーは published順で ab017..ab054 の38キー (drive-2自体が初回probe・fileless UNPROBED)。

## 2. 本takeoverの事前登録 protocol (D1-D5・原CI/CI takeover protocolの意味論不変)

1. **D1 (完了・開示済み)**: kit pin再検証 (§1)。
2. **D2 val-gate fresh 4 (takeover host)**: sanctioned 4キー (at2m×2 budget 2M・15m×2
   budget 15M) を本hostで fresh-cold 実行し `*.d2-host.out` として出版
   (既存published `.takeover-host.out` と衝突しないsuffix)。判定: published baselines 4件との
   node-exact一致 (result・nodes・replay_done有。wall_sは比較対象外)。期待値はpublished
   baselinesから機械読取済み: at2m×2 = (result 0, nodes 2,000,000)・15m = (result 2,
   nodes 3,651,923) / (result 2, nodes 5,040,200)。不一致なら hard-stop して出版しない。
3. **D3 drive-2実行**: 残38キーをab017から昇順に2キー並列 (2 worker上限・2核host) で
   probe。各runbatch.sh起動は `timeout 260` wrap (外側shell上限290sに対しinner先発火・
   truncated passはguardが次invocationで回収)。各invocationは残キーを動的列挙
   (pass-file + `# replay_done` のあるキーを除く) して渡す・列挙が空なら起動しない
   (`if rem` ガード・Part CN空キーバグ教訓)。WIN-HALT (rc=45) は WIN-CONTINUE。
   EXHAUSTEDは継続。MISMATCHは hard-stop。
4. **D4出版**: outputsは原CI宣言どおり本dirの output/ (raw p1/p2 outs + status.log
   append) に蓄積し、 drive-2完了時 (またはセッション時間切れによる誠実打ち切り時) に
   B commitとして出版 (status.log全体・新規raw・truncated sidecars・val-gate d2-host 4件)。
   その後に簡潔な完了log noteを出版する。row-audit (drive-2全行のp1/p2一致・status.log
   照合の公式監査) は原CI宣言どおり別セッションが実施する (本Partでは予備的機械一致
   確認のみ実施・出版はしない)。
5. **D5誠実記録**: 環境リセット・timeout・truncated・rc!=0・例外はそのまま出版・
   隠蔽しない。失敗も実験事実として記録する。

## 3. UNKNOWN担保 (原CI宣言・CI takeover宣言と同一)

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343・class 2251 (54キーすべて・本drive-2の
全キーを含む)・class 343k (34269) は本Partの実行・出版のどの時点でもUNKNOWNのまま。**
nodes数・wall秒数を勝敗として読まない。WIN/LOSS probe行は honest labelのまま
(verdict不消費)。採用は scrutiny owner C++第二実装 gate `9193f5b6…` 通過後の別adoption
Part (pinned merger `90711961…` 経由) のみ (本レーンは代行しない)。閉鎖・被覆・secured・
root勝敗の主張はしない。

## 4. 不接触

Part CX (batch-28残5行第三実装・宣言 1300c10d 00:49Z) のdir・outputs・進行、Part CR
(batch-30 drive-1 thirdimpl)・Part CP (batch-30 drive-2・宣言 7aaa0525 21:56Z outputs停滞
〜3.5h弱・takeover判定は次回実行時に再判定) の観察のみ、batch 1..28各published dir (不変)、
BASE caches (`3124461b…` 6,294行・`854800f3…` 6,301行・`30ddad9d…` 6,317行 CU merged)
read-only不変、fast lane (K1276 z=8)・finite-field lane・inversive lane・19root計画、
batch-28 EXHAUSTED/WIN行の高budget再probe (別宣言条件)・WIN行のscrutiny
(C++ `9193f5b6…` 専権)。CU採用済みの ab001..ab016 16行の再検証レーンも本Partは非接触
(serve継続は次のadoption Partが決定する)。

## 5. 観測時刻

本宣言のpush直前に最新mainを再取得し observed HEAD と対抗宣言の有無を再確認する
(push失敗・競合時は無理に押し進めず記録して中断する)。宣言本文はpush前にローカルsha256
を計算し、push後にfetch-back (raw fetch + sha256 + git blob sha1照合) でbyte一致を確定する。
