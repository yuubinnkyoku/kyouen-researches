# b28 thirdimpl queue registry rev2: P1パッケージ8行の交叉検証完了反映 (純bookkeeping・solver実行なし)

- 2026-11-24T03:58Z (authoring time)
- 対象: `research/experiments/n11-centralreply-class5343-b28win46-thirdimpl-queue-registry-20261124/`
  (rev1出版 `69e391a3`・queue-registry.json `8c4216c6…`・README `00d1062e…`)
- 変更: Part DE完了 (`1eead030`・実験
  `n11-centralreply-closure-b28p1win8-thirdimpl-20261124`) を受けて:
  - queue-registry.json: P1 8行 (aa046/aa016/aa025/aa033/aa027/aa038/aa012/aa042) の
    thirdimpl state open→done (completion `1eead030`)・queue_state_counts
    thirdimpl_done_win 8→16・thirdimpl_open_win 33→25・thirdimpl_publications にDE追記・
    packages P1 にstatus done追記・revisionメタデータ追記 (rev2・rev1 sha明記)。
    新sha `e437af3745fa129734cc1edc76808b49b84d23036109bad6ff93c03c29602483`。
  - README.md: done 8→16 WIN行・open 33→25行の記述更新 + rev2注記。新sha
    `ac24536667a2fc875235642114249cf802626ab250d1d983e4fd501d4fb5bf6c`。
  - MANIFEST-sha256.txt: 上記2行更新。
- 機械検証: rev2 JSON valid・WIN行state計数 done 16 / claimed 5 / open 25
  (合計46・loss 8不変・exhausted 0不変)。open33_by_est_cost・P2〜P4 viewはrev1不変
  (rev1時点のコスト分割viewとして保存)。
- 本revはsolver実行・probe・cache書込なしの純bookkeeping。**verdict不消費**:
  対象8行はhonest WIN labelsのまま・adoptionはscrutiny owner C++ `9193f5b6…` gate
  通過後merger `90711961…` 経由の別adoption Part専権。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・10968・23964・class 5343 (54キーすべて) は本revの前後を通じて
  すべてUNKNOWNのまま。** nodes数を勝敗や距離として読まない。
