# y=12 two-token パラメトリック全称証明 — part2（C1d・census・K1152 observed→proved 昇格）

- 日時: 2026-11-20 (UTC)
- 実験dir: `research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/`
- 位置づけ: [part1 出版](2026-11-20-y12-parametric-allz-proof-part1.md)（12チェック
  6,311,993 点・全 PASS・3回 byte-identical・commit 60622f35/258cd7b0/1093e075）が
  残した part2 工程の実行。単一オーナー宣言は
  [y=12 universal verifier single-owner note](2026-11-20-y12-universal-verifier-single-owner-note.md)
  が保持（宣言 2026-11-20T17:03:31Z・commit d345c645・part1/part2 両段階を保持範囲と
  明示・K1152 fit レーンは自宣言で全称段階を保持範囲外。着手前に最新 main を再取得し
  他オーナー着手がないことを確認済み）。

## 実施内容

1. **C1d アンカーの事前検証（組み込み前・fail-closed）**:
   6つの published uniform closed form（z=8: K0999/K1000・z=9: K1001・z=10: K1011・
   z=15/16/17: K1065/K1077/K1087）のアンカー関数 A8u..A17u を y=10 part2 正本検証器
   （SHA-256 f9169449…・監査 41b7a315…）から 238 行 verbatim で抽出し（`Y` は関数
   ローカル変数のみで y=11/y=12 ブロックと干渉しない）、検証器組み込み前に y=12 行を
   生両エンジンで 4 方照合（各 z0・x=12..45・R<=x+z0+30・計 14,484 点・
   anchor/H_ordered/H_canonical/cand12 全一致・不一致 0・z 別
   2,261/2,295/2,329/2,499/2,533/2,567・約 2.2 秒・
   `scripts/preflight_c1d_y12.py`・`output/preflight-c1d-y12.json`）。低 R 単一
   トークン縮約 R<=z+6（z=15,16,17・x=12..159）9,768 点も不一致 0。y=10 の
   同段階が K1087 転写初稿の評価順バグ 170 点を捕捉した実績に対し、本族は
   y=10 正本からの verbatim 再転写のため事前検証は初めから一致（bug 捕捉 0 も
   実験事実として記録）。z=15/16/17 の (y,d) 過渡セル・S<17/S==17 分岐は
   y=12 で到達不能（S=x+12>=24）。
2. **正本検証器 part2**: verify_y12_universal.py に C1d と C11r を組み込み
   （in-place 拡張・テンプレート再生成。part2 正本 SHA-256 e2092976…・49,295 bytes・
   1,287 行）。全チェック指定実行（C1 C1b C1d C2 C2b C3 C4 C4t C7 C8 C9 C11 C11r C12）:
   **総 6,902,613 照合点・全チェック不一致 0・overall PASS**
   （C1d 139,860 点〔アンカー 130,092 点＋低 R 縮約 9,768 点〕・C11r 450,760 点
   〔4,720 行〕・C4t clip 25 再掃引の confluence 違反 3,540〔初違反 (60,88,88)〕は
   part1 と不変・型総数 191,789・merge corollary 1,417,623 点・tail corollary
   232,510 点は part1 と不変のまま bad 0）。audit.json（3,673 bytes・SHA-256 6bca3fa2…・
   stage 文言 part2）。
3. **3回実行の byte-identical 確認**: run1（同一cwd）→ run2（隔離 tree/cwd/HOME +
   PYTHONHASHSEED=random・census_rows.py と両 census part も隔離側で再生成）→
   run3（同一cwd）の 3 実行で audit.json・census.txt・census-ordered.json・
   census-canonical.json が全て byte-identical（preflight json も 2 回
   byte-identical）。part1 出版 byte の census part 2 ファイル（195670f0…/af4111f8…）
   は part2 実行でも同一 byte を再生成。出版前の fail-closed 検査として census.txt の
   P 集合 1 桁改ざん（C11r 行不一致・rc=1・PASS 出力なし）と欠落
   （FAIL-CLOSED 明示）を捕捉・復元で clean PASS。
4. **census_rows.py y=12 版（第三実装）**: y=5..y=10 と同型の生 tuple 二重再帰で
   z=0..79・x=12..70・R=0..x+z+14 の 4,720 行（450,760 点・値0点 225,361・
   エンジン状態計算〔LRU misses〕6,121,227・約 13 秒・maxrss 約 556MB）を計算・行ごとの
   Thue-Morse 指数・T/P 集合・tail を抽出（tail アサート R>=x+z+13 の (x+12) mod 2
   全行成立）。census.txt（828,655 bytes・4,720 行＋空行 80・SHA-256 67e48cbe…）は
   C11r で閉形式 cand12 から再導出して全 450,760 点を独立照合・不一致 0。本実行
   ホストの 1 GiB cgroup 制約のみ LRU 上限 1,600,000 を明示キャップ（docstring 記載・
   y=5..y=10 出版版との差はこの 1 点のみ）。
5. **K1152 observed→proved 昇格**: AGENTS.md「同じ命題は同じ K 項目・新規採番なし」に
   従い item を同番号で proved 昇格（title・status・scope・evidence・relations・
   artifacts を更新）。knowledge README の K1152 bullet は fit 表記から全称証明表記へ
   同じ位置で更新。knowledge.yml CI に K1152 verify/census の 2 step を追加
   （K1141 census step の直後・アンカー置換 1 回〔y10→y12〕）。K1162 item には
   part2 artifacts（verify part2 正本・census_rows.py・census.txt・preflight・part2 log）を追記。

## 昇格で確定した横断観察（y=1..12 全称表から・y=12 が 12 族目）

- 基底点 y 点仮説 {z+1,..,z+2y-1}: y=12 で 12 点が全 z 確定（第12例・y=1..12 連続）。
- tail 開始族式 x+z+y+1 と tail 値 (x+y) mod 2: y=12 版が全称確定（fitning レベルの
  11 族連続に全称族が y=12 まで到達）。
- マージ命題 x<=z-y-1 → single_token(x+y,z,R): y=12 版（x<=z-13）が全称確定
  （監査上 1,417,623 点独立照合）。
- clip 窓族式 2y+2: y=5..12 の **8 族連続 tight**（y=12 は clip 25 で 3,540 違反・
  2y+2=26 が tight・part1 C4t）。
- 前倒し pin 格子公式 pin=z+(d+3y)/2: y=5..12 の **8 族統一**（d≡y mod 4（奇z）・
  d≡y+2 mod 4（偶z）・偶z pin 6 行は y=12 が全称確定した初例）。
- 奇 z I 帯行 th(d)=ceil((d+3y+1)/2) の連続整数掃引（13..25）と pin スロット
  (d+3y)/2=th-1 の mod 4 交替構造（y=11 と共通の th-1 型・y=10 は th-2 型）が
  全称監査で確定。
- 最終 pin 行 d=y の I[2y+z+1) 型: 7 族連続（y=6/8/9/10/11/12 全称確定+fit）。
- 偶 z 対角行 d=-y の値1全欠如: y=8..12 の **5 族連続で全称確定**。
- B 子に先行出版族の閉形式を逐語転写する構成: cand9（y=10 の B 子）・cand10（y=11 の
  B 子・K1141 全称）・cand11（y=12 の B 子・K1143 出版 fit）で 3 連。

## 未解決（次工程候補）

- 横断法則（基底点・tail 開始・マージ・clip 窓・pin 格子・対角行規則・(I 帯 th/shift) の
  y>=13 への一般証明レーン（y<=12 が全称確定したので補題化・一般証明を開く価値が
  さらに上がった）。
- y=13 族の fit（着手時は新しい単一オーナー宣言が必須・pin=th-1 型かの判定材料）。
- y=11（K1143）の part2 は y=11 レーン保留中につき本レーンでは着手しない。
- 3トークン以上・固定幅・q点版安定化長・11×11 は範囲外。

## trust 境界

全称性は選択肢分解の健全性・正確な mex 恒等式・有限型空間の完全性
（raw錨・恒等式グリッド・型 confluence・シェル/多様体/probe・出版切片転写アンカー・
独立 census。K1023→K1141 と同一構成・y=11 は K1143 part1 の同型機）による。
Lean ではない。C1d アンカー切片の正しさは K0999/K1000/K1001/K1011/K1065/K1077/K1087
の主張（y=12 行はその特殊例）。標準 11×11 の空盤勝敗・二石 root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4 には一切言及しない（すべて UNKNOWN のまま）。

## 出版物（本コミット列）

- part2-a: 実験dir（verify_y12_universal.py part2 正本・census_rows.py・
  scripts/preflight_c1d_y12.py・output/audit.json〔part2 版〕・
  output/preflight-c1d-y12.json・output/published_run.txt〔part2 実行記録追記〕・
  README.md〔part2 節追記〕）＋本 log。
- part2-b: output/census.txt（828,655 bytes）。
- part2-c: K1152 item observed→proved（同番号更新）＋K1162 item part2 artifacts 追記。
- part2-d: knowledge README の K1152 bullet 更新（同じ位置で全称証明表記に書き換え）＋
  knowledge.yml K1152 CI step 2件。
