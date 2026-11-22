# n11 central-reply batch-14 residual (class 23101) 10-LOSS canonical adoption reaudit (Part BC, 2026-11-22)

単一オーナーとして本hostが実行した、batch-14 residual (class 23101) の
残り10 LOSS行 (q043..q052) をcanonical exact-S5 verdict cacheへ計上する
採用・再監査実験 (Part BC declaration = note Part BC amendment)。

Part AW (batch-14 residual 完走: 残10キー全部が2-pass node-exactで解決、
10 LOSS / **WIN 0** / 枯損 0 / 不一致 0・23,252,550 nodes/pass・第三実装
交叉検証 Part AX済み) の直接後続。Part AV (batch-17 class 10661採用・
出版commit `23bda9ba`・fetch-back byte検証済み) の直後の採用で、
**full == loss**: residual batchにはWIN行も枯損行も1行も存在しないため
(「不在のgate」として機械検証)、採用パケットがそのまま完全解決
residualパケットであることがmanifest上機械表明される。class 23101自体は
batch-14 (Part AQ) のq042 WIN-HALTで**q042がunconsumed WIN**として残って
いるため、本採用で閉じることはなく、**閉鎖・被覆の主張は一切しない**
(すべて機械表明・機械検査):

1. increments maker (`scripts/make_increments_residual10.py` = published
   Part AS maker `b6094f0b...` のresidual adapt・row-audit 10行一致gate・
   q042 s5 745184除外gate・batch-17 s5交積0 gate搭載) をpublished
   residual raws (Part AW publication commit `cb94f808`) から再実行し、
   10 LOSS行 increment (sha256
   `c3f201a678bc33462728fe633a38fc68f794da49a965c789acf01407cf850cf8`,
   manifest sha256 `f7287b7b...`, schema
   `batch14residual-loss10-increments-manifest-v1`) を導出。
   3回実行・byte一致。gates: 3-way (p1/p2/status.log) node-exact +
   `# replay_done` 完了ガード、batch-keys (sha256 `d4fada68...`)
   legal/(lo,hi) 照合、published row-audit.json (sha256 `6b40b131...`)
   一致・総ノード23,252,550/pass、status.logのWAVE-END q052 stop=0
   all-10-done停止行・10キーのBASE cache (post-AV canonical 6,172行
   `a5540811...`) 不在 (0 hits)・quarantine 0・q042 s5 745184は
   increment・manifest内に出現しない除外gate。
2. sha-pinned fail-closed union merger (`90711961...`, byte-copy pin,
   selftest PASS) で採用前canonical cache 6,172行 (`a5540811...`,
   Part AV正本・本publication commit固定raw fetchでbyte同一再検証済み)
   にincrementをmergeし、**canonical cache 6,182行** (WIN 158 /
   LOSS 6,024, conflict 0, duplicates 0, sha256
   `0b594f7e14d7eb67263d38a3daa2816e1fd0b73b23403f9b58ca2917225f877a`,
   254,396 bytes) を新path
   `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-20261122.cache`
   に出版 (本repoの次のcanonical exact-S5 verdict cache)。merge 3回実行・
   byte一致・merge-audit 3回byte一致 (sha256 `6a9a53a3...`)。
   merge後のBASE 6,172行cacheはbyte不変を再検証。
3. Part AV refresh機 (`1b49cc07...` = published正本) のadapt
   (docstring文言 + canonical cache path + cache sha期待値の3ハンク) =
   `reaudit/scripts/refresh_adoption_23101resid.py` (sha256 `d6bb2374...`)
   を3回直列実行 (~66s/回)。4出力ともrun間byte一致:
   refresh-summary `5f3a09c6...`, closure-classes `52ec3d4b...`,
   per-root-coverage `1f54065a...`, probe-worklist `fe71be60...`
   (3.75MB, Part AH/AO/AP/AS/AV先例どおり不出版・sha記録のみ)。
4. delta extractor `scripts/compare_deltas_batch14residual_adoption.py`
   (published Part AV extractor `92d83671...` のresidual adapt +
   churn修正: closure候補表のgraph+再計算statusからの**全行row-exact
   独立再構築**を両worldで実施しpublished CSVとの一致をgate、
   全classのunknown集合減少量==increment universe交積の全体減算gate、
   churn退出/新規を記録量として格上げ) を3回実行・byte一致
   (sha256 `62de8c1692a8a4cf9ee4146fae1f64cf42aafbd8a57d27014260e66fdbd5e593`)・
   全gate PASS。delta json schema
   `n11-batch14residual-adoption-decomp-deltas-v1`。

## 結果: class 23101はunknownのまま・閉鎖主張なし (分類の前進)

-機械確定 (refresh再実行・extractor全gate PASS・`decomp-deltas-batch14residual-adoption.json`):
  class 23101のscenario-unknown費用子は**ちょうど{745184}**
  (q042のunconsumed WIN子・key `1152921505747697664:1032`。BASE cache・
  increment・scenario cache・quarantine・両index-verdict mapのすべてに
  不在を機械gate済み)。free_now 37→**37不変**・unknown 34,499→
  **34,499不変**・excluded_now 23→**23不変**・flips 0・new_free 0
  (未知→free_now無し・期待値計算と一致gate)。per-root coverage
  変更行0 (root 27 baseline 119/119不変)。update8新規解決 +0・
  remaining 31,779不変・groups_free_now 127不変。
- closure候補表のchurn (best-option簿記): 退出 {22149}・新規 {23965}・
  23101はrank 1のままunknown 11→1。他5クラス (23777/23960/23962/
  23964/23966) がそれぞれunknown childを1ずつ失う (全体減算gate)。
  採用10キーはgraph上23101のほか複数クラスのcost child。
- 簿記量 (勝敗ではない): probe worklist 64,888→**64,872** (−16)・
  joint greedy 35,645→38,978 (**非単調・6パス局所探索の収束先差で
  あり退行ではない**: improveパス無しの素greedyは49,361→49,351と
  正しく減少・delta jsonの`joint_greedy_nonmonotonicity`字段に明記)。
  nodes数・worklist数・greedy数を勝敗として読まない。
- verdict不消費 (WIN側不変): 消費はresidual 10 LOSS行のみ
  (fail-closed merger経由)。q042 WIN行 (s5 745184) をはじめ
  **17 unconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/
  r002/q042 + AY v001/v002) は読み書きとも全く不接触**。採用判断は
  scrutiny owner C++第二実装 gate pin `9193f5b6...` のまま。
- 並走との不接触: batch-18 (AY残51キー)・batch-19選定・y=16 fastレーン・
  K1058レーン・Part BB/AV成果物には読み書きとも触れない
  (本3コミットは本実験dir配下のみ・BASE入力はpublished正本のsha-pin読みのみ)。
- 標準11×11空盤・19 central-reply roots・class 23101・全class・未知の全S5子は
  本Partのどの時点でもUNKNOWNのまま。
