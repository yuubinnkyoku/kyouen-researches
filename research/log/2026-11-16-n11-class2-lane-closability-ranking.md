# 2026-11-16 n11 class2-lane head-1410 frontier closability ranking（ワークスペース喪失からの再実装）

- 長期レーン（自動実行）。成果導出時点の main HEAD: 4854d440…。出版直前の再取得で HEAD は 00e89b8f… に前進（K0865 census・K0866・two-token grid audit の並走出版を含む）。README・K0863 item・workflow yml は 00e89b8f 版に編集を適用し直した。
- 前回実行でローカルワークスペース（script・出力・corpus）を環境リセットで喪失したため、codeload zip 2.88GB（末尾 central directory 欠落）を local header 逐次走査で解析し 28,737 ファイルを CRC 検証付きで抽出（0 失敗）、reconstruct script 14 本を依存順に再実行（0 失敗）して cost-60c fold chain を再現（head 1410/174/6438/509109/4711/373023・head-1410 出力 3 blob が出版ピンと完全一致）した上で、closability ranking script を再実装した。
- script（30,821 bytes・stdlib のみ）は出版 cost-60c fold chain を runpy で再現し、theorem-applicability scan・cost-65j cover map・neighbor analysis を blob ピンで接合。D4 正準化と合法候補列挙は scan 出版実装＋新規整数外接円/直線実装の二重実装で、固定 100 行サンプルで bit-exact 交叉検証。前セッションで事前登録した期待値の全数値を assert で再現、2 回実行 byte-identical（約 11 秒）。
- S5 orbit 分類: own_closable 114 / cross_cover_required 57 / fully_sterile 3。fully_sterile は best coverable class-2（3 行/209・65k/70j/74h）・audit-blocked（10 行/698）・best class-4（18 行/1460）。第二候補（5 行/364）は cross_cover_required。best own-closable class-2 は 24 行/1704・any-class 最小 18 行/1238（class-1）・class-4 最小 60 行/4216。
- 行分類: unswept 6,390 / sterile 35（== scan census） / win_receipt_scheduled 9（pending cost-65j cover map・635 候補は sweep 不要） / transfer_partial 2（76c 76/15/61・69a 69/3/66） / win_pending 2（76d/77e・fold 未着地）。cost-65j 自身の行は head 1410 で解決済み。
- 遮断レバレッジ: 35 STERILE 行が 91 parent-incidence・60 orbit を遮断（3 orbit 遮断 22 行・2 orbit 12 行・1 orbit 1 行）。全 6,438 行で s6-s7 edge cost == 自行合法候補数（0 不一致・合計 509,109）。定理転送・掃済・65j 予約を除く実残 sweep 作業は 505,675 候補。どの 65j receipt（17 根）も STERILE 行を cover しない（機械確認）。
- 出版済み K0865（サンドボックス JavaScript census・commit 5ada304a）と全数値で一致: 3 unclosable parent の hex 完全一致・57 partial・114 残・STERILE 参照 91/12274・effRem 12183・partial top（rem 5−2・STERILE 済み cost 64/71・own candidates 61）も一致。K0865 が「bash 復旧後に実施」と保留していた python 再現に相当する（実装系も前提 corpus 再構築方法も異なる独立再導出）。
- 前セッション中は GitHub API（api.github.com の名前解決経路）が約 1 時間 404 を継続し push 未着地だった。今回 list_commits/get_commit/get_file_contents/push_files の全操作が回復していることを確認してから出版した。
- 本成果の出版はこの commit 自体（script 1・output 3・log 1・K0863 item 追記・knowledge README 更新・workflow trigger コメント、単一 commit 8 ファイル）。CI 監査 step は付けない（head-1410 ピンの verifier であり、head 前進時に望んで再導出を要求する設計）。
- solved 1410 は manifest 被覆の簿記。REFUTED-D10 は LOSS 証明ではなく、STERILE も LOSS 証明ではない。11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。

