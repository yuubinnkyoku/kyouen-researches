# セッションログ: n=7〜9行掃引 → SAT単独 K_7/K_8 確定 → 双対Sinz v2修正 (2026-11-22、高速レーン)

- 単一オーナー宣言: commit `46efd957` (宣言時HEAD `9e10cd06`・13:04Z)。宣言ノート: [2026-11-22-n8n9-rows-k10-exactlyk-sat-single-owner-note](2026-11-22-n8n9-rows-k10-exactlyk-sat-single-owner-note.md)。
- 実験: [n7n8n9-sat-alone-kn-closures-20261122](../experiments/n7n8n9-sat-alone-kn-closures-20261122/README.md)。K項目: [K1229](../knowledge/items/K1229-n7-n8-sat-alone-k-closures-and-rows-extension.md)。

## 時系列 (UTC)

- 13:04 宣言出版。pinned enc_sat2 v2.1 + 新規双対Sinz at-least-kリフト (atleast_lift.mjs) によるexactly-k行掃引を較正から開始。較正ラダーが既刊値と全直撃: n4k7 SAT/n4k8 UNSAT・n6k11 SAT (K1225出版行464のwitness一致)・n6k12 UNSAT・n7k8 SAT (行463witness一致)・n7k6 UNSAT (s_7=7/K1224整合)。
- 行掃引: n7 k=9..14・n8 k=10..15・n9 k=10..17 がすべてSAT (2ショット)。全witnessをdecode→verify_witness.pyで検証し SAFE+MAXIMAL・石数一致・違反0 (計45 witness)。
- 運用事故2回: bash呼び出し300s上限超えで実行環境リセット (11:47Z頃・13:35Z頃)。/home/user/work 消滅 → 作業キットを永続マウントへ移設して復旧。「1回のbash呼び出し ≤ 1ソルバ実行 (cap ≤250s)」を厳守。
- n7 k=15 exactly UNSAT×2 (12-13s)。n8 k=16 exactly INDET (240-250s)・n9 k=18 exactly INDET (200-250s)。
- 13:5x compaction後のresumeで並走状況を確認: 同日13:41Zに[K1228](../knowledge/items/K1228-n3-n6-safe-size-histograms-sat-crosscheck.md) (n3-n6 SAT単独確定) が並走レーンにより出版済み — 本レーンのn≥7スコープは非重複と確認。[K1169](../knowledge/items/K1169-n8-ge16-partition-fresh-complete-search-verification.md) (11-20) がn8-ge16を分割完全探索で閉鎖済み。n9上界判定は[2026-11-20のn9-ge19レーン](2026-11-20-n9-ge19-k9-upper-decision-single-owner-note.md)が所有。
- **バグ発見**: n7 ge15 (safe-at-least) のshuffle 2ショット目が0秒SATISFIABLE → 既知のK_7=14と矛盾。調査: (1) no-lex版CNFで11石/38空点の割当が全節を0違反で充足することを機械確認、(2) 原因 = **双対Sinz逐次カウンタのj=1開始節 (x_i, U(i,1)) (i≥1) の欠落** (atleast_lift.mjsにも同一欠落)。セル0が石のときカウンタが不活性化しat-least-k半束縛が空文化 (純緩和: models(pre-fix) ⊇ models(post-fix))。**pre-fix UNSATはa fortiori有効・pre-fix SAT判定は単独では無価値** (ただし全SAT witnessは独立検証済みで証明書として有効)。両スクリプトをv2に修正。
- v2較正: 2^16全数地面真理 (safe 5,811・極大 {5:176,6:688,7:64}) と全一致 — sa ge-k k=1..12 (SAT⇔k≤7)・exactly-k k=1..8 (SAT⇔5≤k≤7)・両ショット。
- v2本体: n7 ge15 UNSAT×2 (default 4.86s/200,082c・s42 5s) → **K_7=14 SAT単独確定**。n8 ge16 UNSAT×2 (199.2s/5,646,514c・181.96s/5,245,460c) → **K_8=15 SAT単独確定** + K1169の別手法交叉。陽性対照: n8 ge15 SAT (1.18s)・n9 ge17 SAT (3.85s)、witness検証済み。閉包のexactly-k UNSAT行 (n4k8・n6k12・n7k6・n7k15) もv2で2ショット再実行。
- n9拡張: fresh探索 ge18 INDET (240s/6,118,159c)。W9の8 D4像の単位節注入対照: 恒等像 SATISFIABLE・他7像 UNSATISFIABLE (LX鎖が非正準像を正しく棄却) → 符号化は健全でge18 CNFはSAT、INDETはkissat探索能力の限界。ge19 (ge19レーン所有) はINDET (240s/6,166,925c)。**K_9上界への主張は一切なし**。
- tamper対照 (受入条件3): 20 default witness × 全単石除去 計208件、すべて SAFE+NOT-MAXIMAL (viol=0, uncovered≥1)。
- 運用事故3: 単発shotの出力tag使い回しで default 記録を s42 実行が上書き (n7 ge15・n8 ge16)。決定的CNF (byte-identical再生成確認済み) のdefault shotを再実行して記録復旧 (n7k15_sa2_def 4s・CNF sha16 ef35ac9f…従来と同一 / n8k16_sa2_def 199.2s・faedc3ff…同一)。kissatは同一入力で決定的。
- 運用事故4: 14:5xZ頃にbash実行環境が一時利用不能に。永続キットの成果物は無事。そのため本出版は2段階とした: (1) README・session log・K項目の即時出版、(2) バルク出力 (scripts/・pinned文書/・witnesses/・verify/・tamper/・run_records・meta_records・MANIFEST) は環境復旧後に続刊する。続刊時には本logに追記する。

## 規約の帰結 (K1221と同じ型の事故として)

- SAT較正はdefaultショットの「witness復号+k一致+独立検証」まで (UNSAT側は2ショット一致+緩和方向の吟味)。
- at-least-k束縛は「束縛が実質化するサイズ (既知witnessが早期セルに石を持つ等)」でも既知witnessの**単位節注入対照**で受入言語を確認する。
- n4較正を透過した機構: n4では最小極大サイズ5とat-most-k底により、欠落があってもexactly-k結果が Lucky に一致する。小盤較正だけではこの種の欠落を検出できない。

## 非主張

- K_7=14・K_8=15は値更新ではなく第三手法 (SAT) による再確定 (既知値: K0029表・CYCLE5完全最大探索)。
- 有限盤のみ・実装/符号化/kissat trust込み・形式証明ではない。
- K_9の上界・K_9=18確定への主張なし (ge19レーン所有)。fresh探索で18石witnessに240sで到達できないという負の知見のみ記録。
- 標準11×11空盤・二石root・S2・closure classは非接触 (UNKNOWNのまま)。

## 出版記録 (2026-11-22追記)

- `da55127b`: 実験README (research/experiments/n7n8n9-sat-alone-kn-closures-20261122/README.md) のみで構成したREADME文書単体を出版。
- `f7209a3f`: 本session log + K項目 [K1229](../knowledge/items/K1229-n7-n8-sat-alone-k-closures-and-rows-extension.md) (直前のmain追いかけ確認後に非競合で到達)。
- `3e284f85`: K0029 (n1-n9最大安全サイズ既知値) への節追記「2026-11-22 SAT単独再確定 (値は不変)」。
- `51c10da7`: research/knowledge/README.md 末尾へK1229要約bulletをappend-onlyで追記 (取得正本497,056 bytes + 追記1,648 bytes = 498,704 bytes。fetch→追記→pushを同一実行内で完結)。
- 上記4コミット間に並走レーンの割込みなし (list_commitsでHEAD列を確認)。
- **続刊 (bash実行環境復旧後)**: scripts/8点・pinned文書4点・output/ (witnesses・verify・tamper・run_records・meta_records・brute_truth・brute_n4・w9_d4_cells・sa/) ・MANIFEST-sha256.txt を実験dirへ分割push。完了次第本節へ追記する。
