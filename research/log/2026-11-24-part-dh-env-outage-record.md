# Part DH 執筆中での environment outage 記録 (2026-11-24T06:31Z 付近・実験途中の正直な事实記録)

Part DH (宣言 `f63c1654` → A1 `f8db8d87` (scripts 7 + input 14 + val-gate 8 + README) → A2a `de650462` (sources 38) → A2b `871af8cf` (sources 6)、計74ファイル全てfetch-back byte検証済み) 出版直後のローカル実行中に、sandbox実行環境が一時使用不可能になった (~/dfpart/kitdh への bash・read 全て RPC失敗 `The execution environment is temporarily unavailable`、約40分以上の再probeで復帰せず)。本記録は kit 出版物には影響しない。失敗・timeoutは実験事実として記録する (プロトコル)。**完了ではない・B/C commit は未実施**。

## 破損前までに机器検証済みだったローカル実行結果 (全て pinned出版物とnode-exact、ただしlocal fileの存続は未保証)

- D1 rules-gate: rc=0・quads 95,670 / triples checked 195,044 / mismatches 0。
- D2 val-gate fresh 4 (\`.dh-host.out\`): at2m×2 (result 0, nodes 2,000,000) / first-15m (result 2, nodes 3,651,923) / second-15m (result 2, nodes 5,040,200)。replay行は published baselines とreplay_done込みで一致 (wall_s のみ異なる=audit G7 設計どおり除外)。
- D3 negatives: ng1 GATE_FAIL (legal count mismatch: derived=87 declared=88) / ng2 GATE_FAIL (stone count mismatch: bits=5 declared=6)、rc=1 fail-closed 設計どおり。
- D4 anchors: k02a a/b (result 1 clean, expansions 9,106,337, ttHits 4,991,527) / l1a a/b (result 2 clean, expansions 7,660,202, ttHits 3,951,175)。双方 det-pair exact・published pins一致。
- D5 replica (per-key budget設計どおり): aa011 p1/p2 (12,424,953)・aa054 p1/p2 (13,227,570)・aa022 p1/p2 (14,044,375)・aa034 p1 (14,097,048) rc=0 で published node-exact。aa034 p2 以降 (aa037/aa032/aa028/aa021/aa050 の全パス) は未実行 or 未確認。

## 記録に値する埋め込みlesson (host測定・次回再実行の試算に使用)

- hostは2コア。replica (jsreplay) 単独時 ~194k nodes/s、2並列時 ~93k nodes/s/プロセス、4並列はTMO衝突 (rc=124 を3パス記録→2並列で再実行しgreen。status.logにhonest残置)。
- 300s bash cap内で aa050 (25,541,199 nodes・budget 30M) は 2並列でも ~277s/TMO=295ぎりぎり → 次回は aa021/aa050 の各パスはソロ実行推奨 (~120-140s/pass)。
- D6 thirdimpl: k02a 9,106,337 expansions ≈ 52s/pass実測 → aa050 est pass-one ~30M expansions ≈ ~170s/pass < wallcap240 (単独時)。18 run は2並列×少数で余裕。

## 次回実行への指示 (再現不能なlocal状態に重要証拠を残さない)

1. 最新main再取得 (hourly並走注意) → A1/A2 からkit 74 fileをfetch-back sha検証 (全pinは宣言log refs)。
2. maker再実行 (gates PASS確認・input再生成) → output/ は掃除して D1 からやり直す。中断時のlocal outputは信頼せず全再実行 (全valueはpublished pin側にある)。
3. D5は2並列上限・aa021/aa050はソロ。D6 wallcap240不変・D7 audit×3 byte-identical・D8 tamper (実行後auditに対して宣言済みbattery)。
4. 完了後 B (output) → C (README最終+MANIFEST) → 完了log。

verdicts不消費・11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 5343 (全54キー) はUNKNOWNのまま。9行のWIN labelsは引き続き unadopted honest labels。
