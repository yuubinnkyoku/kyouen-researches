# n11-residual78-seventeenth-win7-cert-extract-20261120

第17 WIN7-D10 証明書（root `00004000000000821082000000000100`）の盲抽出・二回実行byte一致・
三重独立検証、および発見元である 39 live witness depth-10 両順序掃引の
追加独立実行記録。branch/PR は作らず main に直接出版。

## 並走調整の事実（はじめに）

- resolve6（K1063）の `witness_full` 39 live witness 掃引について、
  並走 n11 レーンが commit `68b04984f22fe907120ded2deaf5b03182108fd7`
  （2026-11-19T20:32:07Z）で単一オーナー宣言を出版した。
- 本実行の掃引 worker0 は 2026-11-19T20:32:47Z に起動しており、
  宣言の push と本実行の開始は互いに不可視（同一分内の同時着手）であった。
  本実行は掃引を完了（78 probe 完走・全ゲート合格）した後、出版前に初めて
  当該ノートを検出した。本実験dir は掃引の「正本の座」を宣言dir
  （`n11-residual78-39livewitness-depth10-sweep-20261120`）に譲り、
  完全な掃引記録一式を本dir `sweep-records/` に追加独立実行の一次資料として
  保持する。
- 並走が 2026-11-19T20:48:18Z（commit `e47e418496`）に単一オーナー実行の掃引
  正本（`n11-residual78-39livewitness-depth10-sweep-20261120/`）を出版したため、
  出版前に両実行の生probe記録を突き合わせた。**両実行は78/78 probe
  (root×順序) が nodes・loss・capped すべて完全一致（node-exact）**で、
  runner v17 の決定性が二環境横断で確定した（独立二重実行監査成立）。
  両実行は同一の WIN root を検出し、Win以外の全root は REFUTED-D10 で一致。

## 掃引の結果（sweep-records/witness-39-live-root-depth10-sweep-20261120.json が正本）

- 対象: K1063 resolve6 `witness_full` の39 root（全7石・D4正準形・全safe・
  covered rows 和集合 == 当時の残余78行・matching 39）。
- 規約: runner v17（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）・
  depth 10・cap 30M・両AND順序（andclose 1/0）・pilot_d6 制御行
  （3,402 nodes・loss=false要求・全78 probe合格）・生整数hex child
  （child = root − 最小セットビット・canon_hex被せ禁止・K1046事故規約継承）。
- **WIN 1 / REFUTED 38 / CAPPED 0 / 順序矛盾 0**、78 probe 完走、
  総nodes 169,615,508、最大単一probe 14,249,420 nodes。
- WIN root: `00004000000000821082000000000100`
  （andclose1: loss=true・1,576,372 nodes / andclose0: loss=true・2,544,178 nodes・
  両順序 uncapped・terminalStoneRange [13,17]）。
  別プロセスでの determinism rerun は両順序 node-exact 完全一致
  （`sweep-records/determinism/`）。
- run1 worker0 は最初の bash 呼び出し終了時にプロセスグループ毎消滅した
  （sandbox 環境の性質。3 probe 記録済みの段階で driver はrecordsから再開、
  残りを完走。`worker0.log` に2回の "worker 0 starting" がその事実記録）。

## 第17証明書（certs/win7-root-00004000000000821082000000000100-20261120.n11 が正本）

- 抽出: repo-verbatim `class4_child1_cert_extractor_exact_ms23.ts`
  を `cert_driver_seventeenth.ts` から blind（kill table 空）で起動。
  60合法 loser first-move 全て・完全 winning strategy tree を抽出。
  sum 4,250,297 nodes・49,591行・fbt_drops=0・全 perMove ok/uncapped・
  terminalRange ⊆ [13,17]。**2回実行で証明書 byte-identical**
  （両者 sha256 `21dd2f0e9f0b8ec22e917fce5a732835098baf37570a227bebacacb4c13807c8`・
  1,791,541 bytes・49,593行）。
- 独立検証 1（TS・Bareiss 4x4 sub-root 分解・全 loser reply 展開）:
  60/60 sub-root PASS・seen 103,152・terminals 17,157・opponent_edges 90,499・
  consumed union == strategy rows（missing 0 / extra 0）。
- 独立検証 2（純 python・exact 整数 Bareiss・全 subtree 再帰展開）:
  60/60 PASS・visited_winner_states 150,963・union 0/0・terminal {13,15,17}。
- 独立検証 3（BigInt 3x3 cofactor・K1036 K1060 と同一方式）:
  60/60 PASS・rows sorted unique・union 0/0・terminal [13,17]・root_safe true。
- ゲート組立: `scripts/build_verify_record_seventeenth_20261120.py` が
  repo-root から resolve6/fold9 両正本の SHA pin とともに全成果物を
  fail-closed で再検査し `output/seventeenth-cert-triple-verification-20261120.json`
  （sha256 `c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc`）
  を組む。**全38 gate 合格・2回実行（別プロセス・別cwd）で byte-identical**。
  ゲートは resolve6・fold9 両正本の SHA pin に加えて単一オーナー掃引正本
  （sha256 `22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc`）
  の pin と分類・総nodes・最大probe の三方一致も含む。

## 被覆と残余行（fold10 待ち）

- resolve6 matching 上、本rootは残余行
  `00000000000000821082000000000001` と `00000000000000821082000000000004`
  を被覆する。fold9（第13〜第16 windfall receipt）閉鎖後の残余74行に
  両行とも未閉鎖で残っている（gate `covered-rows-in-residual-74`）。
- **本項はこれらの行を閉鎖扱いにしない**。行の閉鎖計上は fold10
  （第17 receipt を消費する receipt-fold 記録・被覆行は証明書幾何から
  「8 D4像 − 1石」joinで再導出）が必要。fold10 が成立すれば残余は
  74 → 72 となる見込み（fold 機械のゲートが再導出を要求する）。

## 解釈規約（他の n11 項目と同一）

- 第17証明書が主張するのは「この7石rootで second mover が to move のとき、
  original first mover が必勝（全 loser 分岐が loser stuck の terminal 13-17 石で終端）」
  という game-theoretic fact のみである。
- REFUTED-D10 は LOSS 証明ではない。pn/dn や solved 数を勝敗として読まない。
- witness root は条件付き depth-10 掃引計画上の発見であり、空盤や二石rootには
  一切言及しない。
- **標準 11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4
  はすべて UNKNOWN のまま。**

## 次の一手

1. fold10: 第17 receipt fold（fold9 機械 `fold_windfall4.py` の pin 差し替え・
   前段 fold9 正本・本項 gate record・本証明書を入力とする）。
2. 残余72行（fold10後）への resolve7 再照合・add-two-stones 拡張 census。
   （単一オーナー掃引正本との per-probe 照合は前述の通り出版前完了。）
