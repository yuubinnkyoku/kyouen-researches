# 2026-11-18 n11 head-1410: partial-STERILE 57 parent の非STERILE remaining child 列挙・join完全再現 (2026-11-18)

## 背景

cost82e revalidation sweep出版（commit `beb41b19`）とコーディネーター修正クロスチェック出版
（commit `c63d9c86`）に続き、前回の「次の一手」にあった **partial-STERILE 57 parentの
cross-cover価値分析（非STERILE children経由）** に着手した。並走のSTERILEフィルタ付き
census再構築（head-1473 worklistへの除外適用）はこの時点でまだ未出版で、管轄重複は無い
（本作業はhead-1410 K0865 censusのpublished dataに対する検証側の列挙であり、censusの
再構築・ranking変更・sweepは含まない）。

## 成果（`n11-head1410-partial-parent-nonsterile-children-20261118/`）

`audit_partial_parent_nonsterile_children_20261118.py`（blob `6e4e0dfb942841d352a8a62be2504d74443e0cc5`）が
K0865のparent-row joinをraw worklistから独立再導入し、**16 checks all PASS・二重実行
byte-identical**。出力
`n11-head1410-partial-parent-nonsterile-children-20261118.json`
（blob `30c8fdc4e7212bafe271662d8dcf0bbbde35b63b`・411,533 bytes）。report.md同梱。

入力は全てmain上のpublished data（git blob pin検証・commit `c63d9c86`時点）:
K0865 census `9c251da3`・worklist CSV `2fee1d07`・S5 closability CSV `65215b65`・
ranking JSON `c39c547d`。

### 検証（既出版値の完全再現）

- 全6,438行でorbit-related parent数 == 出版open_parents（不一致0）。
- 174 parent全てでrem/cost/sterile数/sterile hex集合/sterile cost/effRem/effective_costと
  S5 CSV 5カテゴリ計数・分類名対応が完全一致（不一致0 parent）。
- global incidence 12,274・census totals 174/3/57/114/91/12,274/12,183再現。
- sterile_row_registry 35行のopen_parents list再現。91 sterile refsの1石拡張正準形構造
  （ref hex == canon(P|1<<b)・σ≠identityでもframe-free）・cost一致。前回crosscheckの
  18 refsチェックの全91 refs拡張。
- effective_worklist_top16全entryをjoinから再現。

### 新規列挙（どの出版にも無かったidentity）

- **57 partial parentの非STERILE remaining S6行の全数表**: 4,297 child-incidence /
  3,555 distinct行（unswept 3,542・win_receipt_scheduled 9・transfer_partial 2・
  win_pending 2）。K0863により、これらのparentが自前行集合から受けられるdepth-10
  receipt証拠はこの行集合に限られる。
- **per-parent最小cost行**: min 57 / median 66 / max 76。最小は
  `00000000000000003800000001800000`（cl4・rem 75・sterile 1）のcost 57行
  `00000000000000003800001001800000`。K0865 effective worklist第1位
  `00000000000000801202000040000000`（effCost 229・effRem 3）はmin child cost 76で
  最下位（effective cost順位とmin-child-cost順位は別測度であることを確認）。
- **共有候補**: 709行が2〜3のpartial parentに所属（2 parent 676行・3 parent 33行）。
  最小共有行はcost 59 `00000000000080809002000020000000`。33行の3-parent行は
  単一sweepで3 parentのD10候補に同時に到達する。
- **special 13行**: win_receipt_scheduled 9・transfer_partial 2・win_pending 2
  （4行が2 parent共有）。

## 解釈

non-STERILEはdepth-10 coverの必要条件でしかなく、sweepがWIN7-D10を返す保証は無い。
本成果は候補列挙とjoin再現であり、receipt・verdict・coverage進展ではない。
parent分類にゲーム理論的値の主張は無い。

## 制限

- engine実行なし。engine depth-10 verdict健全性とD4不変性は既出版verdictと同一の
  trust境界に依存する。
- **REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。**
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## フォローアップ（同日・同experiment）: own_closable parentとの重複

`audit_nonsterile_own_closable_overlap_20261118.py`（blob `4419fb9d984b662c5ede106ece308ad0a4de94e2`・
出力blob `92056ad9fb23a8d390e3a0d735b5558336f8b003`・6 checks all PASS・二重実行byte-identical）。

- 3,555行のうち **2,609行 (73.4%) が少なくとも1つのown_closable parentにも所属**。
  partial parent候補の大部分はown-closable閉鎖経路が消費し得る行と重なる。
- **946行がpartial-only候補**（どのown_closable parentにも非所属）。profile hist:
  np1_no1 2,454 / np2_no0 612 / np1_no0 301 / np1_no2 91 / np2_no1 64 / np3_no0 33。
  **33行の3-parent行は全てpartial-only**。
- per-parent own-share中央値60.9%。**57 parent中45 parentで最小cost候補がown_closableと共有**
  （12 parentの最小候補はpartial-only）。
- この追加も候補の簿記であり、sweep予定・closure・verdictの主張を含まない。

## 次の一手

- 並走のSTERILEフィルタ付きcensus再構築の出版を待ち、出版されたら検証側に回る
  （本auditのjoin再現・91 refs構造チェックはhead-1410系の検証に再利用可能）。
- min child cost順位表・3-parent共有行33行・partial-only 946行は、将来のcross-cover候補選択
  （coordinatorのcertificate候補集中）への直接入力になる。ただし実際のsweep優先度は
  class demand構造（{c1,c2,c4}需要）と突き合わせて決めるべきで、本表単独では
  決めない。
- 残pool 8行の再検証は引き続き「revalidation」ラベルのみ。
