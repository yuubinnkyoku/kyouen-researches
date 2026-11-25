# 2026-11-16 n11 class2-lane: theorem-applicability scan 第二独立検証とcost-69h raw出版ギャップの特定

## やったこと

並走レーンが出版したK0863正準形verdict cacheスキャン（`research/experiments/n11-class2-lane-sterile-unclosability-20261116/output/theorem-applicability-scan-20261116.json`・着地commit `2d090b49`）を、第一実装とコードを共有しない第二実装で全体再導出し、全フィールドを機械照合した。あわせてスキャンが実装していなかった3つの追加検査（X4/X5/X6）を設け、cost-69hのraw出版ギャップを特定した。

## 手法（独立性）

- 4点concyclicity: Leibniz展開（S_4全24項・符号は転倒数）による4x4円行列式。第一実装はBareiss。
- D4正準化・合法候補列挙・harvest（claim/sweep/audit/raw分類・resolve_child・集計schema判別）・fixpoint転写・同位置agreement・STERILE census・check再導出: すべて独立に書いたコード。
- 入力固定: スキャン自身のsha256 manifest（1,279ファイル）を正本とし、commit `2d090b49`のraw CDN取得コピー1,279ファイルがsha256とgit blob shaの二重照合で正本一致することを確認してから再導出。manifest外のファイル（後に着地した入力進化）は読まない設計で、コーパスが進化した場合の再実行は「スキャン再実行+再検証」の単位で行う。

## 結果: VERIFICATION PASSED（46比較・全一致・2回実行byte-identical）

engine map 8,964（REFUTED 8,305・WIN 659・capped 0・source conflicts 0）・fixpoint（索引7,149・115転送・第2反復0）・bit規約win_roots照合6件・claim合法候補一致59件・raw_skipped_lines 1,117・69a bit 109回帰（via含む）・targets 133子のengine/transferred/open/claims全一致・unswept 5子・事前REFUTED 34・残open 293・同位置1,782組・矛盾0・STERILE census 35行（全件engine由来・転写由来0）・skipped files・出版8 check全件。出力JSON sha256 `899d5dee…`。

追加検査: X1（115転送すべてのcanon(child|bit)≡via根canon・verdict一致を直接再検証）・X2（転送bitは全て合法候補）・X3（WIN転送0・新receipt主張なし）。

## データ品質観察: cost-69h raw batch2/3出版ギャップ（verdict不変）

- child `0000000000000080120a000000200000`（cost-69h・2026-11-15 sweep）のraw batch2ファイルのbit集合 [9,10,14,17,19,20,21,22] が同一sweep監査のbatch-2記録 [9,10,12,14,15,18,22,23] と不一致。bits 17/19/20/21 は子の合法候補でない（circle完結root）。
- raw batch3ファイル（監査が参照・bits [24,25,26,28,29,30,32,33]）がmain上に存在しない。
- 結果として69hは12/69候補にraw行を持たないが、audit aggregateが全69候補を被覆しておりengine map・targets・全下流は完全。
- 影響分析: engine mapに非合法root 4件が混入（出版集計・本再導出の両方が8,964に含む）するが、circle完結位置はD4不変でありどの合法候補rootのcanonとも衝突しない（X5衝突∅を機械確認）ため、転送・targets・STERILE census・矛盾検出への影響はゼロ。
- X6（監査batch記録 vs rawファイル実bit集合）をcorpus全体に適用: **186バッチファイル中、不一致はこの69h batch2の1件のみ・欠落はbatch3の1件のみ**。他レーンのraw/audit整合は完全。
- 69hのsweep verdict（WIN bits 58/96・REFUTED 67・capped 0）は不変。raw batch2/3の再出版は記録整合性の残課題（並走レーンへの引き継ぎ）。

## 帰結

- スキャンの全結論（115 theorem-derived REFUTED-D10・69a 66候補への削減・76c 15/76事前確定・同位置矛盾0・STERILE 35行census）が第二実装で確定。運用上の事前REFUTED転写は信頼して使える。
- 検証器・出力JSONはK0863 itemのartifactsに追記済み。CI監査stepは付けない（入力manifestピンの検証器であり、入力進化後に望んで赤になる設計。運用はスキャン再実行+再検証を単位とする）。

## レジューム

canonical head 1410不変（本検証は行閉鎖・foldを含まない）。69aは並走in-flightのまま（着手禁止）。69h batch2/3のraw再出版が残る。REFUTED-D10はLOSS証明ではない。STERILE行はopenのまま。**11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4はいずれもUNKNOWN**。
