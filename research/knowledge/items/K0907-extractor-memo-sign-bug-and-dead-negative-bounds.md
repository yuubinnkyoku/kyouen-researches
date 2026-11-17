---
id: K0907
title: 証明書extractorの符号付きmemoキーと死んだ負境界の検証（K0906 v16 repairの予告したextractor監査）— 重複挿入機構の定量（high-bitキーのみ・最大64コピー・私有窓）とcost-73k帯修正battery（fixB −73.9%・全22証明書byte同一・健全性無影響）と残り全エンジンコピーの構造監査完了（バグ持ち6コピー・修正済み3コピー・v17掃引エンジンは両fix済み）
kind: verification
status: verified
topics: [certificates, verification, search-methods]
aliases: [certificate extractor memo sign bug, extractor dead negative bounds, duplicate memo insertion mechanism, fixed-memo battery cost73k, KYOENSLT memo dump, extractor copies memo defect audit, v17 sweep engine memo fixed]
relations: []
artifacts:
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_extractor_memo_sign_bug_73k_20261117.py
  role: verifier
  note: 自己完結検証器（stdlib+Node 22・決定的・約1分・2回実行で出力JSON byte同一）。24チェック全合格、pin検証3件（extractor blob 52bcaf50…・legal_candidates 8e97082c…・manifest 0892aed0…）・verbatimソースのbugパターン計数（Uint32Arrayキー宣言行・死んだsentinel負境界更新行×2・符号比較行×2が各正確な回数で存在）・Node.js符号実証（Uint32Arrayへのint32格納は符号反転して読み戻り===比較が不成立・Int32Arrayは正確）・verbatim engineへのdump出口注入（検索挙動変更なし・bug修正なし）でbit0先頭12手を再抽出（834,262 nodes・MS=1<<23）しKYOENSLT dump（16B header+24Bレコード・slot index付き）を2回生成してbyte同一・dump分析（records 216,719 / distinct 112,731 / 重複キー 16,417 が全てbit31 high-bitで非high-bitキーの重複0 / 最大64コピー / 64コピーキー7個がspan 63の私有窓 / 全重複キーが64スロット探査窓内に収まるwindow fit・ただし連続runは主張しない / high-bitレコード125,293=57.81% / nowin=nolose全レコード255）・修正battery JSONのgate読み込み
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_fresh_battery_fixed_memo_73k_20261117.py
  role: verifier
  note: fixA/fixB battery orchestrator。repo-verbatim extractorへの行レベル手術（MS=1<<23化・clearRows()/memoStats()測定出口注入・fixAはmK0..mK3のInt32Array化の正確1行・fixBはさらにsentinel対応負境界更新の正確2行）をassertしてから、出版cost-73k帯の22 bitをfresh processで再抽出し、各bitの証明書snapshotを出版証明書（19件の分割ファイルは連結）とbyte比較。埋め込み回帰gate全10件合格（fixA総和75,108,849・fixB総和28,290,025・fixB bit0 1,277,392・bit95 1,415,400・fixA bit0 occupied 372,070・fixA==fixB per-bit occupancy・fixB bit0決定性・byte同一22/22×2）。
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/extractor-memo-sign-bug-verify-73k-20261117.json
  role: data
  note: 検証器監査JSON（24チェック・dump分析統計・2回実行byte同一）
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-fixed-memo-battery-73k-20261117.json
  role: data
  note: 修正battery出版JSON（per-bit nodes/ratio/occupied/byte同一/md5・verbatim fresh ms23対比（総和108,499,241）・出版ms18 baseline対比（155,946,109）・10 gate・interpretation guard）
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_extractor_copies_memo_defects_20261117.py
  role: verifier
  note: 残り全コピー監査スクリプト（stdlib+Node・決定的・2回実行で出力JSON byte同一）。9ファイルのgit blob pin検証・memoFind/memoEntryブロックの空白正規化token比較（extractor族3本同一・sweep-side族3本同一・両バグ持ち族は完全空白除去後に同一=textualに同一機構）・bugパターン計数（符号比較2箇所・死んだ負境界更新行nowin/nolose各1行・修正版sentinel対応形の存在）・ms23==exactの1行差assert・node -e符号demo（Uint32Array格納は+2^32で読み戻り===不成立・Int32Array成立）。
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-extractor-copies-memo-defect-audit-20261117.json
  role: data
  note: 全コピー監査JSON（9エントリ・家族token同一性・bug A/B分類・consumer履歴・解釈境界）。
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_fresh_battery_fixed_memo_73l_20261117.py
  role: verifier
  note: 73lバンドfixB battery（K0907の73k batteryの第2バンド拡張・測定のみ）。repo-verbatim extractorへの行レベル手術（MS=1<<23・mK0..mK3のInt32Array化・sentinel対応負境界更新の各正確行をassert）でfixB変種を生成し、出版cost-73l帯32 bitをfresh processで再抽出して出版証明書（分割ファイルは連結）とbyte比較。pin 4件（extractor 52bcaf50…・driver 73l f997a7cf…・legal 8e97082c…・manifest 6e0a94ab…）・bit1二重実行のnodes・bytes決定性gate・全bitのfbt_drops 0・rows一致gate・2回のフル実行で出力JSON byte同一。
- path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-fixed-memo-battery-73l-20261117.json
  role: data
  note: 73l fixB battery出版JSON（per-bit nodes/ratio/md5・総計52,079,030=出版比0.1226・byte同一32/32・決定性bit1・gate全合格・interpretation guard）。
evidence: 'verify_extractor_memo_sign_bug_73k_20261117.py: 24/24チェック合格・2回実行で監査JSON byte同一。bug A（符号キー）: mK0..mK3がUint32Arrayで比較相手M0..M3はint32 JS数値。cell 31/63/95を含む位置はword 0/1/2のbit 31が立ちM0..M2が負になるため格納された符号なし値との===比較が永久不成立・memoFindが該当位置を見つけられずmemoEntryが訪問のたびに次の空きslotへ重複挿入する（上限64コピー=キー自身の64スロット探査窓の全占有）。bit0先頭12手dump（834,262 nodes・MS=1<<23）で216,719レコード/112,731 distinctキー/16,417重複キーを観測し、重複キーは全てbit31 high-bit（非high-bitキーの重複は0）・最大64コピー・64コピーキーは7個でspan 63の私有窓・全コピーが64スロット探査窓内（window fit・連続runは主張せず初版の過大主張はFAIL gateが補正）・125,293レコード（57.81%）がhigh-bit。この重複挿入は出版ms18帯測定のbit-0停滞（clumped-hash insertion failures・占有76.6%）と整合する具体的機構。bug B（死んだ負境界）: `if(h>=0&&d>mNoWin[h]) mNoWin[h]=d;`（mNoLose版も）はsentinel 255との比較方向が逆でdepth<=64では一度も発火せず、全216,719レコードでnowin=nolose=255・memoFindの両負境界ショートカットが死んでいる。両bugともmemoは最適化のみでサウンド性無影響（見逃しのみを生じ、誤ったhitはない）。battery: fixA（bug Aのみ・正確1行修正）は22 bit fresh process MS=1<<23で75,108,849 nodes=verbatim fresh ms23総和108,499,241の0.6923（−30.8%）・22/22証明書byte同一・wall 198.6s。fixB（両bug修正）は28,290,025 nodes=0.2607（−73.9%・3.83倍）かつ出版ms18 baseline 155,946,109の0.1814（−81.9%・5.51倍）・22/22 byte同一・wall 128.5s・bit0 1,277,392 nodesは2回実行で一致（決定性gate）・bit95は11,857,737の0.119に相当する1,415,400。fixA==fixBのper-bit occupiedが全22 bitで一致（重複挿入除去がエントリ集合を確定させ、負境界修正は既存エントリに境界値を与えるのみでノード再探索を潰すという解釈と整合）。byte同一は出版証明書の再出版ではなくgateであり、repo-verbatim extractorは出版決定性連鎖のため意図的に未修正のまま（修正採用は別レーン判断）。全出版verdict・ノード数はverbatim値として有効. 2026-11-17追記: 残り全エンジンコピーの構造監査を完了 （audit_extractor_copies_memo_defects_20261117.py・2回実行byte同一）。bug A+Bは extractor族3本 （cert_extractor 6716075d…・exact 52bcaf50…・exact_ms23 c267f260…（exactとちょうど1行差=MS行））と sweep-side族3本（v15 sweep_engine bd6a650a…・chunk_prover fc74d215…・FBT runner 8744fc65…・いずれも 2026-11-13 batch1世代）の計6コピーに存在し、両族のmemoブロックは空白除去後に完全同一のため K0907のdump定量機構がそのまま全コピーに妥当。修正済みは runner_v16 0a4a86f6…・runner_v17 c132cc64… （両fix・memoブロック同一）と extractor_exact_v16 5518d375… の3コピー。出版73i/73j/73k/73l raw掃引で 使用したv17エンジンは両fix済みのため掃引側のMS容量測定の利得は純容量効果。全コピーで性能のみで サウンド性無影響は不変. 2026-11-17追記2: fixB byte同一gateを第2出版バンドcost-73l（32 root・manifest 6e0a94ab…・出版verbatim ms23 424,657,112 nodes）に拡張した（measure_fresh_battery_fixed_memo_73l_20261117.py・fresh process per bit・MS=1<<23・kill table空）。fixB総計52,079,030 nodes=出版比0.1226（−87.7%・8.2倍・73k帯の0.2607より更に低く削減率はバンド依存）・per-bit比はbit25の0.0981（最小）からbit119の0.1587（最大）・32/32証明書byte同一・bit1二重実行でnodes 1,456,164とbytes md5 114b255f（=出版bit1）が同一・全bit fbt_drops 0・2回のフル実行で出力JSON byte同一（md5 c4b085eb）。byte同一累計は2バンド54証明書。'
scope: 'class4_child1_cert_extractor_exact.ts（git blob 52bacf509ea12fad4c936501d30d26b5b66c0085）のmemo実装に関する実装検証と性能測定。2026-11-14のv15→v16 runner repair（log 2026-11-14-n11-class4-lane-v16-memo-key-repair.md・milestone-5実験README）が「certificate extractor copiesは再利用前に別途監査せよ」と予告したうちの証明書extractor 1コピーに対する監査の完了。2026-11-17追記でclass4_child1系エンジンコピー9本（extractor 3・sweep-side 3・修正済み3）の監査が完了し、「他コピーは未監査」の限界は閉じた（bug A+Bはbatch1世代の6コピーに存在・v16/v17 runnerとv16 extractorは修正済み）。測定はcost-73k WIN7-D10帯（S6 child 00000000000000801206000000000400・22 bit・fresh process MS=1<<23・kill table空）とcost-73l WIN7-D10帯（S6 child 00000000000000c09002000000400000・32 bit・同一fresh process処方）に限定した有限測定であり、無界の性能主張ではない。勝敗への影響はゼロ（memoは最適化のみ）'
---

# 証明書extractorの符号付きmemoキーと死んだ負境界の検証

## 命題（verified）

v16 runner repair（2026-11-14）と同じ2欠陥が証明書extractor
`class4_child1_cert_extractor_exact.ts`（blob 52bcaf50…）にも存在し、
ともに**性能のみ**に影響する（サウンド性への影響なし・全出版証明書・
verdictはそのまま有効）:

- **bug A（符号付きmemoキー）**: `mK0..mK3`は`Uint32Array`だが比較相手
  `M0..M3`はint32 JS数値。cell 31/63/95を含む位置（word 0/1/2の
  bit 31）では格納値（符号なし）と比較値（負）が等しくならず、
  memoFindが永久に失敗し、memoEntryが訪問のたびに同じキーを次の空き
  slotへ重複挿入する（上限は探査窓64スロット＝キーによる窓の私有）。
- **bug B（死んだ負境界）**: `mNoWin`/`mNoLose`の更新条件がsentinel 255
  と逆方向の比較で、depth<=64では一度も発火しない。両負境界
  ショートカットは死んでいる。

## 重複挿入機構の定量（bug A）

verbatim engineに検索挙動を変えないdump出口を注入し、bit0先頭12手を
再抽出（834,262 nodes・MS=1<<23）してmemo表全体を解析:

| 量 | 値 |
|---|---|
| 格納レコード | 216,719 |
| distinctキー | 112,731 |
| 重複キー（2〜64コピー） | 16,417（全てbit31 high-bit・非high-bitの重複は0） |
| 最大コピー数 | 64（64コピーキーは7個・span 63の私有窓） |
| high-bitレコード | 125,293（57.81%） |
| nowin=nolose | 全レコードで255（bug B） |

全コピーは各キーの64スロット探査窓内に収まる（window fit）。ただし
コピーの連続性（contiguous run）は主張しない: 検証器の初版がこの
過大主張を含み、独自のFAIL gateが出版前に補正した。重複挿入は
出版ms18帯測定のbit-0停滞（clumped-hash insertion failures・占有
76.6%）と整合する具体的機構である。

## 修正の定量（cost-73k帯・fresh per-bit・byte同一gate）

| 変種 | 総ノード | vs verbatim fresh ms23 (108,499,241) | vs 出版ms18 baseline (155,946,109) | 証明書byte同一 |
|---|---|---|---|---|
| fixA（bug Aのみ） | 75,108,849 | 0.6923（−30.8%） | 0.4816 | 22/22 |
| fixB（両bug） | 28,290,025 | 0.2607（−73.9%・3.83倍） | 0.1814（−81.9%・5.51倍） | 22/22 |

- fixB bit0 = 1,277,392 nodes（2回実行で一致・決定性gate）。
- fixA==fixBのper-bit occupiedが全22 bitで一致する（重複挿入の除去が
  エントリ集合を確定させ、負境界修正は既存エントリに境界値を足す
  のみで再探索を潰す、という機構と整合）。
- byte同一は再出版ではなくgate: 出版証明書のbytesは変わらない。
- 73l帯拡張（2026-11-17追記）: fixBはcost-73l 32 bit fresh process（同一処方）
  で52,079,030 nodes = 出版verbatim ms23 424,657,112の0.1226（−87.7%・
  8.2倍）。32/32 byte同一・bit1二重実行でnodes・bytes同一（md5
  114b255f=出版bit1）・2回のフル実行で出力JSON byte同一。削減率は
  バンド依存（73k 0.2607 vs 73l 0.1226）。

## 根拠

- 検証器: 上記evidenceの24チェック全合格・2回実行で監査JSON byte同一。
  pin検証・ソースパターン計数・Node.js符号実証・dump 2回生成のbyte
  同一・battery JSON gate読み込みを含む。
- battery: 埋め込み回帰gate全10件合格（上記の総和・bit0/bit95・
  occupied・occupancy一致・決定性・byte同一）。
- 機構の帰属: 2026-11-14のv16 runner repair logが同一2欠陥を
  v15 runnerで先行発見し、extractor copiesの個別監査を予告していた。
  本項はその予告された証明書extractor監査の完了である。

## 限界

- memoは最適化のみ。bugは見逃し（hitしない・境界が書かれない）だけを
  生じ、誤ったhitは生まない。全出版証明書・ノード数・verdictは有効
  （ノード数はbug込みのverbatim値）。
- repo-verbatim extractorは出版決定性連鎖のため意図的に未修正。
  修正の採用（新規抽出のfixB化）は別レーン判断で、本項は測定のみ。
- 他コピー監査は2026-11-17に完了: sweep engine・chunk prover・
  FBT-saturation runnerとextractor族残り2本の計6コピーに同一2欠陥、
  v16/v17 runnerとv16 extractorの3コピーは両fix済み（構造監査・token
  同一性・blob pin。コピー個別のdump定量や修正battery測定は実施せず、
  K0907の機構定量がtoken同一性を通じて妥当するという根拠）。
- 測定はcost-73k帯（22 bit）とcost-73l帯（32 bit・いずれもdepth 10・kill table空）の有限測定。
- WIN7-D10は個別7石rootの深さ10以内の先手勝ちのみ、REFUTED-D10は
  LOSS証明ではない。**11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 はいずれも UNKNOWN のまま**。本項は勝敗を1mmも動かさない。
