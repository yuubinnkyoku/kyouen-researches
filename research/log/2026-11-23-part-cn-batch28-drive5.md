# Part CN completion: batch-28 (class 5343) drive-5 — 残23キー aa032..aa054 完走、batch-28 全54キー probed (2026-11-23)

Part CN完結。publish-then-execute規約どおり、宣言 `research/log/2026-11-23-part-cn-batch28-drive5-declaration.md` (commit `11f2b668…`・observed HEAD-before-push `35cc3702a…`) → A scaffold `e73425b4…` (148 files) → B outputs `86b49d57…` (52 files) → C README+MANIFEST `ffe47c3a…` (201 files pinned) → 本完了log。**verdict不消費・11×11 UNKNOWN担保不変**。

## 成果

1. **batch-28 (class 5343) 54キー完走 (ALL-DONE・fileless 0)**: 残23キー aa032..aa054 (s5_index 199717..199739・batch内最高s5帯) をWIN-CONTINUEで13 worker-invocation・約43分で完走。
   - drive-5新規行: **WIN 17** (aa033 3,347,117 / aa034 14,097,048 / aa037 14,239,714 / aa038 4,911,996 / aa039 11,349,776 / aa040 8,916,641 / aa041 10,283,599 / aa042 5,800,791 / aa043 12,069,965 / aa044 9,219,778 / aa045 12,371,943 / aa046 2,185,149 / aa048 10,553,343 / aa049 7,272,703 / aa051 7,662,388 / aa052 8,976,982 / aa054 13,227,570 nodes・いずれもresult 1・2-pass node-exact)・**LOSS 1** (aa036 955,659 nodes・採用候補のみ)・**EXHAUSTED 5** (aa032/aa035/aa047/aa050/aa053・honest UNKNOWN)。
   - **batch-28全体 (Part CB/CH/CJ/CK/CNを通じた合算)**: probed 54 = WIN 35・LOSS 8 (aa003採用済み + aa015/aa017/aa018/aa023/aa024/aa029/aa036採用候補のみ)・EXHAUSTED 11・fragment 0・fileless 0・MISMATCH 0。54キーすべて2-pass node-exact。
2. **val-gate 4/4 node-exact** (宣言後・本host fresh `.ck-host.out`): at2m×2 nodes 2,000,000・first-15m 3,651,923・second-15m 5,040,200 (wall 9/9/17/25s vs published 8/9/17/25s・wall_s比較外)。
3. **監査**: win-halt変種 `96867282…` は全54完了状態で設計どおりGATE FAILED (「batch fully completed…フル監査を適用」) → drive-4 README記載済みの既知設計 (WIN行単行照合) によりpublished full audit `656cac31…` も不適 (「aa001: status.log node count mismatch」) → **Part CB先例と同型の最小派生 `row_audit_batch28_full_v2.py` (`1f4b3ce9…`・EXACTLY 1 gate修正: WIN行照合を2行ペイロード (PASS行+WIN-HALT行) に変更・schema `…rowaudit-full-v2`) を作成・B commitで出版して使用**: PASS x3 byte-identical (json SHA-256 `00c32383…`・probed 54 = WIN 35/LOSS 8/EXHAUSTED 11)。tamper battery 4/4検出 (実効性assert込み・各probe復元cmp済み) + clean control byte-identical。
4. **出版コミット** (fetch-back byte照合): A 148/148・B 52/52・C 2/2 (MANIFEST 201エントリ・pins通り)。宣言のfetch-back検証はcommit-pinned raw URL + sha256。

## 誠実記録 (incidents)

1. **session-local `drive5_local_step.sh` のALL-DONE状態空キーバグ (発現1回・batchキー無傷)**: 残余計算 `print("\n".join(rem))` は `rem=[]` で単一空行を出力し、全54キー完了直後の14番目のinvocationで `runbatch.sh ""` (空キー) が起動した。結果: (a) status.logにkey idなしのjunk行 `P1-FAIL ` が1行追記、(b) `output/raw/.p1.out` (node ENOENT stack trace) が生成。**108個のaaNNN pass fileはすべて無傷** (row-audit全gate PASSで機械確認) で、いずれのbatchキーにも触れていない。junk行・artifactとも出版を維持 (append-only規約・非verdict行として両監査に無視される)。drive-4のpublished sessionスクリプト `ea0db83e…` も同型構造 (発現機会がなかっただけ)。次drive系sessionスクリプトでは修正必須 (`print("\n".join(rem))` を `if rem: print("\n".join(rem))` に)。
2. 宣言時に「worker timeout 285s→260s」の理由 (外側shell上限290sに対するinner先発火・環境リセット防止) は事前開示済み・予想どおり機能 (rc=124時にも外側timeoutなし)。
3. aa034/aa035のp2 truncated (sidecars 2 files・P2-TRUNCATED-RETRY 2行) はpublished completeness guardの設計どおり次invocationでp2のみfresh-cold再実行し完走。

## 解釈ガード (不変)

- WIN 35行はhonest WIN labelのみ (unconsumed closure WIN候補・採用判断はscrutiny owner C++第二実装 gate `9193f5b6…` のまま・本レーンは代行しない)。LOSS 8行のうちaa003はPart CH採用済み・残7行 (aa015/aa017/aa018/aa023/aa024/aa029/aa036) はadoption候補のみ (canonical cache反映は別adoption宣言・pinned fail-closed merger `90711961…` 経由のみ)。EXHAUSTED 11行はhonest UNKNOWN (same-condition再probeなし・予算引き上げは別宣言条件)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて) はどの時点でもUNKNOWNのまま。** nodes数・wall秒数を勝敗として読まない。被覆・secured・root勝敗の主張はしない。canonical cache (Part CH merged 6,294行 `3124461b…`) への書込は一切なし。closure table不変。

## レジューム (次回の着手前に必ず最新main再取得・hourly並走注意)

- batch-28はprobe完走。次回最有力:
  (a) **7-LOSS行 (aa015/aa017/aa018/aa023/aa024/aa029/aa036) のloss-only adoption Part** (Part CH aa003単行・Part BZ 6行の先例・pinned merger `90711961…` 経由・reaudit込みフルセッション規模・WIN行採用判断はscrutiny owner待ちで非接触)、
  (b) **adoption後のreaudit・class 5343簿記更新** (unknown_now・closure churn・greedy union等の機械更新はadoption Part内で実施)、
  (c) **EXHAUSTED 11行の高位予算再probeは別宣言条件** (15M→45M等は新規事前登録が必要・同一条件再probe禁止は不変)、
  (d) Part CG takeover (aa006/aa007 thirdimpl・宣言 `d5e9acc2` 18:01Z) のoutputs出版確認 (停滞時はtakeover規約)、
  (e) batch-29 Part CI (ab001..ab054・closure class 2251・scaffold `c6ae987a`) outputs確認 (宣言側セッション所有・長時間停滞ならtakeover規約)。
- session系スクリプトの空キーバグ修正を次drive系Partに必ず反映。
