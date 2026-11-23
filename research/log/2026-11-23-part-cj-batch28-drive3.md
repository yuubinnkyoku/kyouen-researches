# Part CJ (2026-11-23): batch-28 (class 5343) drive-3 continuation — fileless 47キー aa008..aa054, wave 1でaa008/aa009両WIN-HALTによる事前登録stop val完了

単一オーナー: n11中央応答レーン (本セッション)。宣言:
`research/log/2026-11-23-part-cj-batch28-drive3-declaration.md` (commit `42cecf36…`・
publish-then-execute・fetch-back byte照合済み SHA-256 `c525a7a4…`)。

## 0. 要約

- **drive-3 wave 1 (1 invocation・2 worker・timeout 285) の結果: aa008 WIN-HALT
  (result 1・nodes 5,270,340・s5 index 140489・legal 85・key (1171516445255794704,0)・
  2-pass fresh-cold node-exact @budget 15M)・aa009 WIN-HALT (result 1・nodes 7,319,605・
  s5 index 142299・legal 91・key (1747977197559218176,0)・2-pass node-exact)**。
  事前登録stop rule「本driveで2 WIN行観測でwave halt」(batch-28 drive-1/2と同じ設計)が
  発動し drive-3はwave 1で完了。残り45キー (aa010..aa054) はfileless UNPROBEDのまま。
- **verdict不消費**。aa008/aa009はhonest WIN label = unconsumed closure WIN候補
  34/35番目 (route statementのみ: 採用されればclass 5343の全LOSS閉包ルートに対する
  反駁証拠。採用判断はscrutiny owner C++第二実装 gate `9193f5b6…` のみ・本レーンは
  代行しない)。
- val-gate fresh 4/4本host node-exact (at2m 2,000,000 x2・15m行 result 2 nodes
  3,651,923/5,040,200・禁止四角 95,670・`# replay_done` x4・wall_s比較外)。
- row-audit(winhalt) PASS (pinned `96867282…`): **probed 9 (aa001..aa009) = WIN 6
  (aa001, aa002, aa006, aa007, aa008, aa009)・LOSS 1 (aa003)・EXHAUSTED 2 (aa004,
  aa005)・fragment 0・fileless 45・mismatch 0**・3回実行byte同一 (json SHA-256
  `eb1d1e98…`)。
- 実験dir 105ファイル (README + MANIFEST-sha256込み) main出版済み・**最終commit
  `eed9f348` pinned HEADでfetch-back 104/104 sha OK + MANIFEST byte同一 (105/105)**。
- tamper battery 4/4検出 + post-battery pristine全104ファイルsha不変。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa008/aa009を含む) は
  本Partの実行・出版のどの時点でもUNKNOWNのまま。** nodes数はbookkeepingであり勝敗
  ではない。canonical cache (Part CH merged 6,294行 `3124461b…`) への書込は一切ない。

## 1. 出版commit一覧 (fetch-back検証)

| Part | commit | 内容 |
| --- | --- | --- |
| 宣言 | `42cecf36` | `research/log/2026-11-23-part-cj-batch28-drive3-declaration.md` (対抗宣言なしgrep・未着手47キー確認・stop rules事前登録) |
| A | `a0d2b488` | scaffold 79: scripts 8 (7 pinned byte-clone + session-local `drive3_local_step.sh` `5d478283…`) + input 55 (published pinsそのまま) + val-gate 16 (published 12 + 本host fresh `.cj-host.out` 4) |
| B | `55fe0a81` | outputs 24: raw 22 (seed 18 + aa008/aa009 p1/p2) + status.log (17行seed + 4行追記 = 21行) + row-audit-winhalt.json (`eb1d1e98…`) |
| C | `eed9f348` | README + MANIFEST-sha256 (104行・45の`…/drive3…` pathをpin) |

実験dir: `research/experiments/n11-centralreply-closure-class5343-batch28-drive3-20261123/`。
fetch-back: commit `eed9f348` で全104内容ファイルsha256 OK + MANIFEST byte同一。

## 2. 実行記録 (宣言protocolどおり)

1. val-gate fresh 4/4 (宣言後・本host): at2m×2 budget 2M EXHAUSTED nodes 2,000,000・
   15m×2 budget 15M result 2 nodes 3,651,923/5,040,200・全node-exact・禁止四角
   95,670・`# replay_done` x4。
2. wave 1: `drive3_local_step.sh` 1回 (17:35-17:36Z・2 worker・`timeout 285`)。
   REM=47からaa008/aa009を選定 (status.log昇順・機械導出)。両worker rc=45。
   - 比較器初回誤検出の正直記録: val-gate集計スクリプトの自前比較器がwall_s除去
     indexを誤りat2m 2件を一度MISMATCHとした (solver出力側は最初からnode-exact)。
     index修正 (field 8除去) とquad検査のall/any誤り修正で4/4 MATCH確定。実行結果に
     影響なし。
3. finish: 残45キーを再計算せず終了 (pre-registered halt)。row-audit x3 byte同一。
   tamper battery 4/4検出 (T1初回harness no-op → T1'でDETECTED。詳細は実験dir README
   の正直開示)。

## 3. 誠実記録・運用知見 (今回new)

- (a) **val-gate比較器の wall_s field indexは `'replay,'` prefix込みで数える**
  (split配列で index 8・「f6,7,8=budget,result,nodes」のcut慣習と混同しない)。
  初回実装でnodesを除去してwall_sを比較し、wall差1秒 (9 vs 8) をMISMATCHと誤読した。
  比較器バグは実験の正本に触れないが「PASS/FAIL」の記録そのものを崩すので修正と
  開示が必要。quad検査 (禁止四角95670) は行単体ではなく「その行を含む」で判定する
  (`all()`を掛けない)。
- (b) **tamper batteryのT1初回no-op**: sedパターンにval-gate行のlegal (98)を流用し
  aa008行 (legal 85) に不動作・実効性検証が`grep -c`の「0」出力を非emptyと誤判定
  (Part CD T1・Part BT T1と同型の事故。**実効性assertはcount閾値比較で書く**)。
- (c) drive3_local_step.shはPart CD `drive2_local_step.sh`のpath/workerlog差のみ
  (二重sed差分で同一性を機械確認)。pinned runner/solver/stop rulesは不変。

## 4. 次回候補 (Part CJ以降)

1. **drive-4 (aa010..aa054・45キー・WIN-CONTINUE設計)**: batch-28の2-WIN halt設計は
   drive毎に最初のWIN対で停止してしまうため、Part CE (batch-23) 先例のWIN-CONTINUE
   (WIN行をhonest labelとして記録しつつ継続) を事前登録した継続driveが列挙効率上
   有力。ただし本レーンは宣言前に最新mainの対抗宣言・batch-24 fileless等の並走状況を
   再確認すること。
2. batch-23 (Part CE)・batch-24 fileless・batch-29 (Part CI) の並走成果回収。
3. aa004/aa005 (EXHAUSTED @15M) の高budget再probeは別宣言のみ。
4. unconsumed closure WIN候補35キー (aa008/aa009を含む) の採用は引き続きscrutiny
   owner gate待ち (本レーンは非代行)。

## 5. UNKNOWN担保 (最終)

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa001..aa009を含む) は
2026-11-23 Part CJ完了時点でUNKNOWNのまま。** class 5343はWIN 6行 unconsumed +
EXHAUSTED 2行 + fileless 45キーが残るため閉じない (closure tableの同class行はadoption
Partを通らない限り不変)。閉鎖・被覆・secured・root勝敗の主張は一切しない。
