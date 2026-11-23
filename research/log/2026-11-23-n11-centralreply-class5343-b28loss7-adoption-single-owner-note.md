# 単一オーナー宣言: batch-28 (class 5343) 7-LOSS行 adoption — Part CO（仮採番）publish-then-execute

- 2026-11-23T20:2xZ 初回出版。単一オーナー: 本Partのadoption实行体（Vibe長期レーン）。
- observed HEAD-before-push: `891c70e2a4deb1f92f00976289c161a8d73b8ce6`
  （K1272 lane の experiment outputs 出版。非接触。直前 `701064f1` inversive-plane
  handoff note・非接触、`4be51cb6` K1272 宣言・非接触、`952897e5` K1252 scope note・非接触）。
- 対抗宣言チェック: `research/log` の 2026-11-23 17:30Z 以降のコミット列
  （CJ 42cecf36 / CL 7a184e92 / CM 27217816 / CK ad269701 / CG takeover宣言 d5e9acc2 /
  CM完了 2102800b / CK完了 85d26a2c / CN宣言 11f2b668 / CN完了 13fe1cc6 / K-series各種）を確認。
  **batch-28 loss-7 adoption の宣言・实行・出版は存在しない。レーンは空いている。**
  Part CG takeover（aa006/aa007 third-impl、18:01Z宣言以降 outputs無く停滞）と batch-29/class 2251
  （Part CI, scaffold c6ae987a, outputs停滞）は本宣言と非接触（本Partは優先度判断により手を触れない）。
- 共有入力はHEAD `4be51cb6` でcurl fetch-back照合済み（8/8一致。以後の `701064f1`/`891c70e2`
  はresearch/log・K1272实验dへの追加のみで本Partの入力ファイル非接触）:
  BASE cache 3124461b…（Part CH正準6,294行）・CH reaudit outputs（summary 76cad2a1…/
  closure baa2db13…/per-root-coverage 75e59441…）・drive-4 kit MANIFEST 1e4024f8…（150ファイル）・
  drive-5 kit MANIFEST e2d81055…（200ファイル）・batch-keys af19208f…・drive-5 status.log
  ca1e98cc…・drive-5 row-audit.json（full-v2）00c32383…。

## 宣言作業（publish-then-execute）

**ADOPTED-CANONICAL = Part CH BASE（正準cache 6,294行, sha256 `3124461b14e4f73a7248cbf5b96c7ff59ebfdcc05258adeb9c81791d86cc461e`）
＋ batch-28 の7新規LOSS行**（class 5343; aa015/aa017/aa018/aa023/aa024/aa029/aa036;
s5 164462/170101/173654/193820/196053/199714/199721; nodes合計 38,784,669）を、
pinned byte-clone fail-closed union merger（`s5_union_merge.py`, sha256 `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`）
で採用する。配下はすべて实验ディレクトリ
`research/experiments/n11-centralreply-class5343-loss7-adoption-reaudit-20261123/`。

- aa003 は Part CH で採用済み。**再送しない**（incrementは7行のみ。manifestにBASE一貫ゲートを置く）。
- WIN 35行（aa001/aa002=Part CC third-impl検証済み、aa006/aa007=Part CG lane宣言済み・outputs停滞中、
  aa008/aa009=Part CM third-impl検証済み、他29行はunverified honest label）は**不採用**。
  採用可否は scrutiny owner C++ second-implementation gate pin `9193f5b6…` が唯一の経路
  （batch-14residual q042 / batch-26 l028 先例）。本Partは非接触。
- EXHAUSTED 11行は honest UNKNOWN（両pass 15M枯渇、re-probe無し）。不採用・不留保。
- よって **class 5343 は解放されない**（残46 = 35 WIN + 11 EXHAUSTED の s5 集合と完全一致することを
  機械ゲートで示す）。
- 統合後cache行数 6,301（WIN 158 / LOSS 6,143）。

## 公式实行プロトコル（宣言後に实行、全ステップこのhostでbyte再現）

D1. maker（`scripts/make_increments_b28loss7.py`）×4 byte-stable:
    両キット全ファイルsha検証（150+200）、全54キー2-pass node-exact、
    status.log絵図（drive-4 61行はdrive-5 109行のbyte-prefix、最終verdict行
    `2026-11-23T19:24:56Z aa054 WIN-HALT`、junk 行 `"P1-FAIL "`（末尾スペース、
    read_text().splitlines()で解析・strip禁止）をちょうど1行）、truncated sidecar 8の不採用、
    aa003 BASE一貫ゲート、7行のみ生成。
D2. merger selftest + merge ×3 byte-identical（出力tmp命名のため出力名は63B短縮名
    `merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-20261123.cache`）＋ merge-audit 3通。
D3. refresh（`reaudit/scripts/refresh_adoption_b28loss7.py`）×3 byte-identical
    ＋隔離实行（`env -i`・別tree・PYTHONHASHSEED=random）。
D4. extractor（`scripts/compare_deltas_b28loss7_adoption.py`）×4 byte-identical＋隔離实行:
    17 sha pin（両drive kit MANIFEST含む）＋キット全文件再検証、manifest・両row-audit意味ゲート、
    全54キー独立2-pass raw再検証（drive-5）、6キーはdrive-4 cross-drive一致（aa036はdrive-5のみ）、
    aa003 BASE一致 (2, 4070373)≡raw、scen==base+7、verdict count 6294(158/6136)→6301(158/6143)、
    holder算術（union 21、5343 own=7、他20クラスown=1）、metrics pin、PRC IG movers pin、
    closure pin → `output/decomp-deltas-b28loss7-adoption.json`。
D5. tamper battery（`scratch tree`、Part CHの12種踏襲＋manifestゲート拡張）: pin層
    （increment/BASE改変/verdict flip/keys改変=sha側で捕捉）と semantic層
    （attacker-repin後の non-LOSS混入・BASE append・class flip・manifest改変）で
    fail-closed作動を確認し、復旧後に緑復帰。
D6. 出版順: A= scripts 4（maker/merger byte-clone/refresh/extractor）→ B= increment+manifest+merge-audit×3
    → C= merged cache → D= reaudit outputs（summary/closure/per-root-coverage; probe-worklistは設計どおり非出版）
    ＋ decomp-deltas json → E= README + MANIFEST-sha256。
D7. 各push後にfetch-back sha256照合。競合・同時書き込み・取得失敗時は無理せず記録して次回实行に回す。

完了時: `research/log/2026-11-23-part-co-b28loss7-adoption.md` 完了log、
kyouen knowledge `KNOWLEDGE.md` 冒頭エントリ更新。

## 宣言前探査の全開示（規約に従い、宣言前に本hostで实行・観測した数値を全て列挙）

本セッションの採番 Part CO 宣言に先立ち、以下を**宣言前**に实行済み（全て決定論的・再現済み）:

1. キット取得・検証: drive-4 150ファイル + drive-5 200ファイルの全sha256検証パス（manifestと一致）。
2. maker自前实装→4回 byte-stable:
   increment `increment-b28loss7-20261123.cache` 7行
   sha256 `bd5ef7d7632816006bd5a74349bf703a8dd3251e3a550a33e7ae7a0253abe382`、
   manifest（schema `b28loss7-increments-manifest-v1`）
   sha256 `b47e07ca90b0166d22c681a3136a60500d7a4f8671b1e77b656a1b34c7c02192`。
   その過程で **drive-5 manifest sha を手転写した際の1文字ドリフトを maker の fail-closed
   kit-integrity ゲートが機械捕捉**した（検証 before-run 失敗→修正→緑。採用値は sha256sum からの機械転記）。
3. merger selftest PASS → merge ×3 byte-identical:
   scenario cache（6,301行, WIN 158 / LOSS 6,143, 259,886B）
   sha256 `854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d`、
   merge-audit-run1/2/3.json 同一 sha256 `06f25f00624070acde241dbc605dca17bf46ea7fbf30ab17fb7c2d094d3885aa`。
4. refresh ×3 byte-identical: refresh-summary.json
   sha256 `4727fb2b991d78107a67aa3ef2bf533be042907214216f8d363a23f884228179`、
   closure-classes.csv `9d3965d94db9fc8005fda1cd24aadf1b515a799e5558448a391489cd24caa85d`、
   per-root-coverage.csv `8e6fb981ee637d896cbf6d378d0543db06d5552da725cba2fa24130cc6fd4809`。
5. extractor完成→×3 byte-stable PASS（实行約3秒）: decomp-deltas json
   sha256 `39b2802d78c7e2c8b54262bfc994d96ed123dcb02ac400f2abce388a2556c74e`、
   script sha256 `67b2b3c583d569b672a40ef4d8edc0d7d0086b74d8e6eeb3aef2d20406d1fbe2`。
   初回实行で genuine gate hit: churn 431クラス中3クラス（5596等）は
   **両側 excluded_now 安定のまま rank移動**する純粋ランキング移動であり、
   「両側unknown」を要求した初版ゲートが過剰だった。ゲートを「再計算状態不変
   （分布 pin {unknown: 428, excluded_now: 3}）」に修正して緑復帰した。
   宣言前探査で見つかった設計修正として開示し、修正後ゲートを公式实行に使用する。
6. 事前観測された事後採用数値(**全てextractorのpinとして事前登録し、公式实行で再検証する**):
   - class 5343: unknown 53→46、closure rank 19→4。class_status_counts 両側完全同値
     （excluded 390 / excluded_now 23 / free_now 38 / unknown 34,498）→ flip 0・新規free 0。
   - holder算術: 7キーの graph holder union 21クラス。5343 own=7、他20クラスは
     各1（6キー membership 4×6 + aa036 membership 3 = 27 = 7+20）。
     closure表中のunknown減算は 5232（102→101, rank 605→570）・11641（56→55, rank 69→47）・
     5343 のみで、他カラム完全安定。
   - closure表: 807→808行、left={12697 (721,106)}、entered={5233 (722,106), 5374 (412,91)}
     （5233/5374はholder。純粋ランキング/table再構成 bookkeeping）。
     stable-unknown rank churn 431クラス（428 unknown + 3 excluded_now、状態不変・非holder）。
     anchors 23101 (1,1) / 1849 (2,1) / 12643 (21,53) は両側で rank・unknown完全不変。
   - update8: resolved_among_baseline_requirement 134→141、新規residual **ちょうど7**
     {164462, 170101, 173654, 193820, 196053, 199714, 199721}、lost []、
     remaining 31,725→31,718。
   - joint greedy 38,295→38,310 (+15)、probe-worklist 64,746→64,828 (+82)、
     group_best 2,119不変、groups_free_now 131不変、win_hit_groups 0不変。
   - per-root coverage: 全root free/uncovered不変、roots_summary_moved 空。
     individual greedy movers のみ root 4: 5,977→5,949 / root 16: 2,972→2,971 /
     root 49: 2,810→2,803。root 27 baseline 119/119 両側不変。
   - キャッシュ側: in_universe 450→457、known_universe 473→480（+7）。
7. 出力ファイル名設計: 旧来の長い chain名は255B制限とmerger tmp命名（出力名+".tmp"）のため使用不能。
   短縮名 `merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-20261123.cache` を採用
   （extractor pinとmanifestに明記）。

この宣言前探査の数値は「宣言通りに公式实行が同じ値を機械再現すること」の検証対象であり、
それ自体が结諘ではない。

## UNKNOWN guarantee

本Partのどの時点でも、標準11×11空盤・19 central-reply roots・二石roots {49,60}/{59,60}・
S2 {59,60}・classes 1/2/4/10968/23964/5343（aa001..aa054全キー含む）は **UNKNOWN のまま**。
nodes数はbookkeepingであり決してverdictではない。本Partはいかなるroot-coverage/
closure/secured/root-outcome主張も行わない。 WIN 35行の採用判断にに一切触れない
（scrutiny owner pin `9193f5b6…`専権）。verdictは不消費。
