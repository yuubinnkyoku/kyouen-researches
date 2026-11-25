# Part DU 宣言 (2026-11-24): batch-34 — closure表 rank 1/2 small-pocket classes 23101・1849 の最終未確定cost子 2キー probe (publish-then-execute・単一オーナー)

単一オーナー: n11中央応答 長期レーン (本セッション・Part DT直接の後継)。
対抗宣言なし: push直前に最新mainを再取得し、最近コミットを機械grepして
batch-34 / Part DU / class 23101 / class 1849 / small-pocket を主張する
commit・宣言がないことを確認してから着手する (後述の観測HEAD参照)。

## 1. レジューム経緯と選定根拠

Part DT完了 (commit `305d1590`) のレジューム候補 (a)「closure表 rank上位
small-pocket batch選定」を採る。Part DT kit reaudit 3出力
(refresh-summary `38fc4e19…`・closure-classes `6cc33dd7…`・per-root-coverage
`c5a2721d…`) によれば、closure表 (807行) の上位は:

- rank 1: **class 23101** (`[1152921504892059648, 16]`) — unknown_now **1**
- rank 2: **class 1849** (`[1152922672972169216, 0]`) — unknown_now **1**
- rank 3: class 2251 (unknown 1 = 未採用WIN ab028・Part CZ thirdimpl corroboration済み)
- rank 4: class 5804 (unknown 4 = 未採用WIN 3 + EXHAUSTED 1 ad043)
- rank 5: class 34908 (unknown 9 = 未採用WIN 4 + EXHAUSTED 5)

rank 3以下の残余は採用待ち (scrutiny owner C++ gate) または高budget再probe
(別宣言必須) であり、**本バッチでprobe可能な未知子はrank 1とrank 2の各1キー
のみ**。この2キーをbatch-34とする。2キーの対象データはrefresh-summaryの
`worklist_first` probe_order 1, 2 ( публикации由来・手転写ゼロ):

- **ag001**: serving class 23101・lo=1152921505747697664・hi=1032・
  legal=85・s5_index=745184・membership_class_count=4
- **ag002**: serving class 1849・lo=1153485622925590528・hi=0・
  legal=88・s5_index=81011・membership_class_count=3

両キーとも canonical chain cache (`973bcd19…`・6,547行) に exact-pair不在
(機械確認・G4 gate)・quarantine登録なし (G5 gate)・legal は Board再計算値を
inputに固定 (jsreplayは実行時にもlegalを再導出して不一致なら例外停止)。

## 2. スコープ・手法

実験dir: `research/experiments/n11-centralreply-closure-smallpockets-batch34-20261124/`。

- 手法: pinned runner `runbatch.sh` (sha256 `f591f8c2…`・batch-33 kitとbyte-clone)
  + pinned replica `jsreplay.js` (sha256 `84585617…`・byte-clone)。
  2-pass fresh-cold replay・budget 15,000,000・1 solver / 1 row / 1 process。
  実行前にpublished val-gate 4行 (batch-33 kitの2 target × 2M/15M) を本環境で
  fresh再現し node-exact (result・nodes) 一致が必須 (fresh実行は宣言後)。
- maker `make_batch34_keys.py` (本kit新規): fail-closed gates G1–G6
  (source sha pins・worklist_first全field照合・closure表rank anchor・
  canonical cache exact-pair不在・quarantine不在・legal出所固定)。
  宣言前ローカル実行で gates PASS 3回byte-identical・tamper battery
  pin層5/5 + semantic層2/2 (pin再標的化した攻撃モデルでG2 legal driftと
  G4 cache hitを検出)・復旧後pristine greenを確認済み。kit出版後は
  published bytesから同一手順を再実行する。
- **停止規則 (事前登録)**:
  1. determinism mismatch → 即時HARD-STOP (rc=42)、以後のキー着手不可。
  2. budget枯渇 (result 0) → honest UNKNOWN。15M同条件の再探索は禁止。
     次ラダー (budget昇格) は将来の新規宣言が必要。
  3. **WIN-CONTINUE (事前登録・Part CK先例)**: WIN (result 1) はhonest label
     としてstatus.log・rawに記録するが、driveは継続する。batch-34は2キーで
     あるため、両クラスの最終未確定子が WIN/LOSS/EXHAUSTED いずれでも
     honest label を完走させる。WIN採用は本レーンでは行わない
     (verdict不消費・scrutiny owner C++第二実装 gate `9193f5b6…` 待ち)。
- 消費規則: 本Partはprobeの完走とhonest labelの出版のみ。canonical cache
  への書込なし (adoptionは別adoption Part・pinned merger `90711961…` 専権)。
  クラス閉鎖・root被覆・securedの主張はしない (判定は後続の
  refresh再実行+独立監査が行う)。

## 3. 期待機械簿記 (事前登録)

- probed total: 0 → 2 (ag001, ag002)。**結果非予告** — WIN/LOSS/EXHAUSTEDの
  分布は実行後のhonest label。
- closure表・free_now・excluded_now・unknown・update8・greedy等の変化は
  本Partでは derive しない (adoption後のreauditが機械導出する)。
- nodes数・wall秒数はbookkeepingであり勝敗ではない。

## 4. scrutiny owner C++ gate (Part DT レジューム(d)) の現状

Part DT レジューム⑤(d)「WIN 4行 scrutiny-owner C++ gate `9193f5b6…` 実施」を
本セッション冒頭に検討した。採用ゲートはC++第二実装
`cpp/solvers/kyouen_dfpn_root.cpp` (pin `9193f5b6…`) だが、本実行環境には
C++コンパイラが存在せず、パッケージ導入も禁止されている
(2026-11-22 Part G当初の障害と同一)。よって本レーンはC++ gateを引き続き
実行できず、WIN行採用の專権はscrutiny ownerのまま不変。この情報を実験事実
として完了logに記録する。

## 5. 出版形態 (宣言後に順次)

A) 宣言 (本note) → B) kit (scripts 3 + input 3 + val-gate 8) →
C) outputs (status.log・raw 4・val-gate fresh .b34-host.out 4) →
D) README + MANIFEST-sha256 + 完了log。全files commit-pinned
fetch-back byte照合・branch path URL (CDN stale) は使わない。

## 6. 並走との不接触

- fast lane (K1302出版済み・K1303 general-w induction宣言/kitは別レーン所有)・
  cap-games lane (PG(2,9) orbit系)・moment/s-parameter系レーン: 対象キー・
  class・文件が全く別で非接触。
- batch-33 (Part DQ/DR/DS)・adoption Part DT のpublished dirs (不変)。
- unconsumed WIN候補 (class 5343 46行・2251 ab028・5804 3行・34269 11行・
  34908 4行) の採用状態・scrutiny owner gate。EXHAUSTED 5行 (34908) の
  高budget再probe (別宣言必須)。

## 7. UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 23101・class 1849 (本batchの2キーを含む全メンバー) は
本Partの実行・出版のどの時点でもUNKNOWNのまま。** nodes数を勝敗や距離として
読まない。WIN/LOSS採用はscrutiny owner C++ gate 通過後の別adoption Part
(pinned merger `90711961…`) のみ。closure表・worklistはscheduling bookkeeping
でありclass statusを運ばない。
