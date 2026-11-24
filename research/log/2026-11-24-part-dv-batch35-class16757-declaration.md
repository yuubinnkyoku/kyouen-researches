# Part DV 単一オーナー宣言 (2026-11-24): batch-35 — closure class 16757 (rank 7) clean 28キー probe (publish-then-execute)

単一オーナー: n11中央応答 長期レーン (本セッション・Part DU/DU-b 完了直後の後継)。
対抗宣言なし: push直前に最新mainを再取得し、最近コミットを機械grepして
batch-35 / Part DV / class 16757 probe を主張するcommit・宣言・実験dirが
ないことを確認してから着手する (observed HEADは下記)。

## 1. レジューム経緯と選定根拠

Part DU (batch-34 small-pocket probe・宣言 `5ec15665`・kit `a0d40d47`・
outputs `1039a95d`) と Part DU-b (第三実装交叉検証・宣言
`research/log/2026-11-24-part-du-b-b34win-thirdimpl-declaration.md`・
kit `adc6143a`..3/3d・outputs B1 `662d81bf` / B2 `f1187f4f`・
README/MANIFEST `cf46dbfa`・完了log `d8b849e5`) が本レーン先行実行で
完走した。**batch-34の2キー (ag001 class 23101・ag002 class 1849) は
ともに2-pass node-exact WIN** で、第三実装verdict一致 2/2・tamper
battery 10/10+control PASS まで交叉検証済みだが **verdict不消費**
(scrutiny owner C++第二実装 gate を通過していないため採用不可)。

最新closure表 (Part DT reaudit出版・`6cc33dd7…`・807行) のrank上位は
本宣言時点で以下であり、rank 1..6 のunknownは**全て採用待ち (scrutiny
gate未通過) またはEXHAUSTED (高budget再probeは別宣言必須) の
既ラベル行**である:

- rank 1: class 23101 unknown 1 = ag001 WIN (b34・第三実装一致・不消費)
- rank 2: class 1849 unknown 1 = ag002 WIN (b34・第三実装一致・不消費)
- rank 3: class 2251 unknown 1 = ab028 WIN (batch-29・Part CZ corroboration済み・不消費)
- rank 4: class 5804 unknown 4 = 未採用WIN 4 (ad024/ad028/ad043/ad055・ad043はPart DI 30M再probeでWIN)
- rank 5: class 34908 unknown 9 = 未採用WIN 4 + EXHAUSTED 5 (Part DQ-DS)
- rank 6: class 34269 unknown 11 = 未採用WIN 11 (Part CP drive-1他)
- **rank 7: class 16757 (`[1153204079095185408, 65536]`) unknown 29**
  = b018 WIN (batch-1 2026-11-22・不消費) **+ clean 28キー**

よって**probe可能な (honest labelをまだ持たない) unknown children を
持つ最上位クラスはrank 7 class 16757 であり、そのclean 28キーを
batch-35とする**。28キーはpublished batch-1 packet
(`research/experiments/n11-centralreply-closure-class16757-batch-20261122/`)
の `not_probed_unknown` 集合 {b021..b048} と正確に一致 (手転写ゼロ・
makerが機械照合)。Part DP/DNのamount教訓「reaudit再実行でrank上位の
zero-collision clean候補をmake_batch_keys gateで確認」に従い、
maker fail-closed gates G1-G6 (下記) がその確認を機械実行する。

## 2. 宣言前探査 (read-only・本宣言前に実施・全開示・solver未実行)

1. canonical cache `973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6f9412ca5b`
   (Part DT出版・6,547 unique s5verdict行) をpair-level parse:
   batch-1の48キー中19キー (b001-b017, b019, b020) のexact (lo,hi) が
   cacheに存在 (=batch-1の19 LOSS行はcanonical chain内)・**b018 (WIN) は
   不在 (不消費どおり)**・**b021-b048の28キーは全て不在 (WIN/LOSS
   conflictなし・probedでもない)**。19+1+28 = 48 全キー簿記整合、
   かつclosure表unknown_now 29 = 19 known + 28 clean でない…のではなく
   unknown_now 29 = 1 (b018不消費) + 28 (clean) と機械整合する。
2. refresh-summary `38fc4e19…` worklist_first (40エントリ):
   probe_order 28 = class 16757 s5 528497 = **b018** (不消費WIN・本batch対象外)・
   probe_order 29..40 = class 16757 の12キー = **batch-1 packetの
   b021..b032 と (lo, hi, legal, s5_index, membership_class_count) 全字段一致**
   (機械照合済み)。orders 41..56 (b033..b048に対応) はworklist_firstの
   40エントリ外のため、makerは closure表unknown_now 29 と batch-1
   not_probed 28 + b018 1 の整合で代用する (下記G2/G6)。
3. closure-classes `6cc33dd7…`: rank 7 = class 16757・unknown_now 29・
   first_group_first 36・first_group_third 50・groups_served 5。
4. quarantine registry `results/n11-s5-evidence-quarantine.json`
   (`81d23160…`): active 2エントリ。28キーのexact pairはいずれもactive
   quarantine keyと不一致 (machine check)。
5. 本宣言時点で本セッションは solver を一度も実行していない。

## 3. スコープ・手法

実験dir: `research/experiments/n11-centralreply-closure-class16757-batch35-20261124/`。

- 手法: pinned runner `runbatch.sh` (sha256 `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84`
  ・batch-33/34 kitとbyte-clone) + pinned replica `jsreplay.js`
  (sha256 `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  ・byte-clone)。2-pass fresh-cold replay・budget 15,000,000・
  1 solver / 1 row / 1 process。
- 実行前にpublished val-gate 4行 (batch-34 kitの2 target × 2M/15M =
  `at2m-s5-1152921504606851072-536870946`〔nodes 2,000,000・result 0〕・
  `at2m-s5-1188950301626860544-536870912`〔2,000,000・0〕・
  `first-15m-s5-1152921504606851072-536870946`〔3,651,923・2〕・
  `second-15m-s5-1188950301626860544-536870912`〔5,040,200・2〕) を本環境で
  fresh再現し (budget,result,nodes) node-exact 一致が必須 (fresh実行は宣言後)。
- maker `make_batch35_keys.py` (本kit新規): fail-closed gates
  - G1: sources sha pins (7ファイル: batch-1 3・refresh-summary・closure-classes・canonical cache・quarantine)
  - G2: batch-1 audit `not_probed_unknown` == {b021..b048} (28キー)・
    status.log PASS/WIN行整合 (PASS 20行中 LOSS 19・WIN b018)・
    WIN key集合 == {b018}・batch-1 keys 48の(id, lo, hi, legal, s5_index,
    membership_class_count) 照合
  - G3: closure-classes rank 7 == class 16757 かつ unknown_now == 29 で
    29 == 1 (b018不消費WIN) + 28 (clean) と一致
  - G4: 28 cleanキー (とb018) のexact (lo,hi) pairがcanonical cacheに不在
    (same-lo コンテキスト計数はreportのみ・採用しない)
  - G5: 28キーがquarantine activeでない
  - G6: legal は batch-1 packet legal (Board再計算値origin) と
    worklist_first 12エントリ (b021..b032) の両方と一致 (手転写ゼロ)
  宣言前ローカル実行で gates PASS 3回byte-identical + tamper battery
  (pin drift・worklist field drift・cache hit・quarantine hit・not_probed
  drift・rank drift、全ABORT) を確認済みの構成でkit出版後はpublished bytes
  から同一手順を再実行する。
- **停止規則 (事前登録)**:
  1. determinism mismatch → runner HARD-STOP (rc=42)、以後のキー着手不可。
  2. budget枯渇 (result 0) → honest UNKNOWN。15M同条件の再探索は禁止。
     次ラダー (budget昇格) は将来の新規宣言が必要。
  3. **WIN-CONTINUE (事前登録・Part KN/CM先例・batch-34と同一)**:
     本drive実行前にclass 16757は既にb018不消費WINを持ち、
     「48全キーLOSSによる一括closure」は本budgetでは達成不可である。
     したがって WIN (result 1) が見つかってもdriveは継続し、
     28キー全てにhonest labelを完走させる。WIN行はstatus.log・rawに
     honest labelとして記録する (WIN-HALT rc=45で断片化するpublished
     runner byte-cloneを改变しない。ドライブの再開は残キーの
     再invocationで行う。実行protocolの変更ではない)。
- 消費規則: 本Partはprobeの完走とhonest labelの出版のみ。canonical
  cacheへの書込なし (adoptionは別adoption Part・pinned merger
  `90711961…` 専権。WIN行はさらに scrutiny owner C++第二実装 gate
  `9193f5b6…` 待ち)。クラス閉鎖・root被覆・securedの主張はしない
  (判定は後続の refresh再実行+独立監査が行う)。

## 4. 期待機械簿記 (事前登録)

- probed total: 0 → 28 (b021..b048)。**結果非予告** — WIN/LOSS/EXHAUSTEDの
  分布は実行後のhonest label。
- closure表・free_now・excluded_now・unknown・update8・greedy等の変化は
  本Partではderiveしない (adoption後のreauditが機械導出する)。
- nodes数・wall秒数はbookkeepingであり勝敗ではない。
- 実行quota: 28キー × 2-pass。batch-1の同クラス20キー (2-pass) が
  約10分で完走した実績から、本hostで概ね15-40分のsolver時間を予測する
  (キーごとのnodes次第・當て呼びではない)。timeout・環境リセットは
  誠実記録し、published runnerのTRUNCATED-RETRY guardでresumeする。

## 5. scrutiny owner C++ gate の現状 (不変)

Part DU宣言§4どおり: 採用ゲートはC++第二実装
`cpp/solvers/kyouen_dfpn_root.cpp` (pin `9193f5b6…`) だが、本実行環境に
C++コンパイラが存在せず (本セッションで再確認 2026-11-24T21:2xZ)、
パッケージ導入も禁止されている。よって本レーンはC++ gateを引き続き
実行できず、WIN行採用の専権はscrutiny ownerのまま不変。第三実装
(Part DU-b) は採用ではない。この事実は完了logに再記録する。

## 6. 出版形態 (宣言後に順次)

A) 宣言 (本note) → B) kit (scripts 3 + sources 7 + val-gate 8 byte-clone) →
C) outputs (status.log・raw 56・val-gate fresh .dv-host.out 4) を
**8キーごとのincrement出版** (Part DQ-DSで実地証明済みの耐sandbox-reset
規律) → D) batch-audit.json → E) README + MANIFEST-sha256 + 完了log。
全files commit-pinned fetch-back byte照合。

## 7. 並走との不接触

- fast lane (K1303 continuation完了・README bullet `ca42291b`)・
  PG(2,9)/cap-games lane (`792a7d43` 等)・moment/s-parameter系レーン:
  対象キー・class・文献が全く別で非接触。
- Part DU/DU-b published dirs (不変)。batch-1 (class 16757) published
  packet (不変・本kitのsources参照のみ)。
- 未採用WINプール (class 23101 ag001・1849 ag002・2251 ab028・5804×4・
  34908×4・34269×11・5343×46・16757 b018) の採用状態・scrutiny owner gate。
  EXHAUSTED 5行 (34908) の高budget再probe (別宣言必須)。

## 8. UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 16757 (本batchの28キーとb018を含む全メンバー) は
本Partの実行・出版のどの時点でもUNKNOWNのまま。** nodes数を勝敗や距離として
読まない。WIN/LOSS採用はscrutiny owner C++ gate 通過後の別adoption Part
(pinned merger `90711961…`) のみ。closure表・worklistはscheduling
bookkeepingでありclass statusを運ばない。
