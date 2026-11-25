# 実行 log: K1314 下帯第2行崩壊 (T-BB2 + L-2/PB2) — 高速レーン 2026-11-25

前回 (K1314 セッション前半): compaction を挟みながら、宣言前探索の凍結
(explore_k1314.py/.out・WA..WG 全波 bad 0)、型付き子 D 座標 mex + 族 F1–F5 の
手証明骨格の完成、単一オーナー宣言ノートの出版、機体 14 電池の実装と公式 4 走、
変異 15 種の実測、成果物 25 ファイルの出版までが完了し、fetch-back 25/25 の
byte 一致で閉じた。本 log は出版 chain の全体を記録する (item/log/README bullet
は後半の本実行で出版)。

## チェーン (publish-then-execute)

1. **採番確認**:着手時観測 HEAD 99577d5f (Part EC reaudit の直交 commit のみ・
   knowledge 変更なし)。`K1314 repo:yuubinnkyoku/kyouen-researches` commit
   検索 total 0。
2. **宣言ノート出版 `7e597ba0`**:
   `research/log/2026-11-25-belowband-row2-single-owner-note.md`
   (§1 主張 T-BB2/L-2/PB2/L-BR2/L-0・typed 子・系 A–C・§2 手証明全文・§3 凍結
   探索・§4 機体宣言 14 電池+変異表 15 種・§4.5 主張の区別・§5 open 登録・
   §6 honest 経緯)。単一 commit・sha256
   37e71df6da00ac8ae47c292ef4cd38e84bae6269c7a1b1077b8dbe1168258d6。
   §6 記録: 凍結前の explore 初版は engine ブロックの provenance コメント 6 行を
   省いた bytes で起動 sha ゲートに fail したが、公刊 bytes (bd5f22e4…) に差し替え
   再実行して全波完走後に凍結した (値への影響なし・凍結 sha 6e95ac4b… が正本)。
3. **kit part A1 `6a324217`**: verify_k1314.py (sha256
   94cef6434662acad602a472f57dc1d7021fafbd6bd6680773d9b2f7bedde280f・
   engine pin bd5f22e4… startup ゲート内蔵・embed は K1138/K1282..K1313 chain
   と同一 bytes・14 電池 40,513 点・変異 15 種を事前宣言)。
4. **kit part A2 `3a8f0373`**: kit README.md + engine_block.py
   (582c93c1…・K1282..K1313 kit と同一 bytes) + predry 構成。
5. **kit part B1 `620265ee`**: explore_k1314.py (6e95ac4b…) / explore_k1314.out
   (197ca679…) 凍結出版 (WA (E,w) マージ census 345 cells・多値セル厳密特定・
   WB T-BB2 広域 census 27,467・WC 基底補題 fits・WD typed closure 5,007・
   WE witness 3,116・WF K0832 j 帯 1,524・WG seed 1314 random 400・全波 bad 0)。
6. **kit part B2 `eaa349c9`**: predry 4 走 (同一 cwd×2 PYTHONHASHSEED
   random/1 + 隔離 tree env -i×2 99/7)・全走 rc=0・stdout byte-identical
   sha256 4c2102c689e3b7848fcb1708a4a8c0f865e81d31c1a2118e4d8cbd598bee1240
   (約 4.1 秒/走)。
7. **公式 4 走 `f62a02a3` (part 1)**: kit bytes から同一 4 構成で実行・全走 rc=0・
   stdout byte-identical・宣言 predry sha と同一 (4c2102c6…)。counts
   [1440, 2646, 2970, 928, 4509, 2338, 851, 7026, 542, 9538, 2145, 2912,
   1968, 700] 総計 40,513 bad 0・engine_gate PASS。
8. **変異電池 15 種 (part 2a–d `80987915`/`c617fb74`/`fc1ab849`/`119638fe`)**:
   `--tamper-engine` rc=2 (mutated sha 0ea47a80…・pin 不一致) + 電池 flip 14 種
   (ty 1440 / d2 2646 / d3 2970 / ex 928 / tt 4509 / l2 2338 / pb 851 / ps 7026 /
   ce 542 / wa 9538 / ab 2145 / db 2912 / zz 1968 / rs 700) 全部 rc=1・宣言どおり
   の単一電池汚染 (bad 配列の非ゼロ成分がその電池の count と完全一致)。
9. **detcheck + MANIFEST `b32413b3` (part 3)**: detcheck.json (OFFICIAL-PASS・
   clean counts/bad 配列・engine sha・4 走 sha・変異 bad 配列を全 assertion
   検査後に書き出し) + MANIFEST-sha256 (24 files・自己除外)。
10. **fetch-back**: 成果物 25 ファイル (official 8 + tamper 15 + detcheck +
    MANIFEST) を FNV-1a 64 bit で照合・25/25 byte 一致 (rate limit 2 件は
    45 秒待ち再試行で解消)。

## 成果の要約

- **T-BB2 (定理)**: 全 n≥3・全 z≥0・全多重集合 X の下帯第2行 k=z+n−4 で
  H = [E odd] / 2 (E=z+n−3) / 1−[E odd] (E≥z+n−2)。例外は (1,1,1)@{0,1} の
  2 セルのみ。n をまたぐ正しいマージ座標は (E, w)=E+z+n−5 (多値セルは
  (−1,−3)→{0,1}・(−1,−2)→{1,2} のみ・例外セル由来)。
- **L-2 / PB2 (定理)**: n=2 の第2行 (plane 法の行 k=Z−2・壁行 k=−2)。
  PB2 の遠方場は L-2 に対して偶奇反転 (同一 k 行・異なる plane で則が異なる
  最初の実例・内部インターフェース)。
- **手証明**: 型付き子 (A-a/A-b/B/C・全子が R−1) + D 座標 5 行 mex 表 + 族
  F1–F5 直接計算 + 存在補題 E1–E4 + 単一 R 強帰納で完結。B 承継の typing
  (n−1=1→L-BR2, 2→L-2, ≥3→T-BB2) 完全確定。
- **意味**: tail (K1312) + 境界 (K1311) + 頂行 (K1313) + 第2行 (本次) + n=2
  第2行法令で全多重集合 n≥2 の k≥z+n−4 が完全確定。O-BBL2 の第2行層を解決、
  残余 open は k≤z+n−5 (O-BBL3)。
- **系**: K0832 3トークン過渡帯予想 A (j=0・常に 2 = T-BB2 の 2-line)、
  B (j=2・常に 2 = 公刊 T-DB)、C (j=1・2 ⟺ z=0 = 公刊 T-BB) を解決。
  統一予想 U (k≥1 スライス) は open 継続。

## 主張の区分

- 定理: T-BB2・L-2・PB2・L-BR2・L-0 (手証明が正本・宣言ノート §2)。
- census 40,513 点 (D1–D4, D6–D10, D12–D14) は機械的一貫性検査で証明の代替
  ではない。D5 typed 4,509 点は帰納段 mex の機械再現。D7/D8 は公刊閉形式・
  アンカーの転写検査。D11 は系 A/B/C の有限照合。
- 11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN・verdict 不消費。

## 次課題

1. 第3行 k=z+n−5 (n=3: k=z−2) の census (O-BBL3 入口・(E,w) 風マージの貫徹
   検査・plane z+1 第2行値からのボトムアップ可)。
2. 統一予想 U (K0832 k≥1 スライス) の O-BBL3 構造予想としての検証。
3. plane 摺り合わせ (PB2/L-2 型界面) の深層での再出現観測。
