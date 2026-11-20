# y=10 two-token パラメトリック全称証明 — part2（C1d・census・K1141 observed→proved 昇格）

- 日時: 2026-11-20 (UTC)
- 実験dir: `research/experiments/vertical-fiber-two-token-y10-parametric-allz-proof-20261120/`
- 位置づけ: [part1 出版](2026-11-20-y10-parametric-allz-proof-part1.md)（12チェック
  6,265,496 点・全 PASS・3回 byte-identical）が残した part2 工程の実行。
  単一オーナー宣言は [y=10 skeleton single-owner note](2026-11-20-y10-two-token-skeleton-single-owner-note.md)
  が保持（宣言 2026-11-20T10:25:00Z・fit・preflight・part1/part2・昇格出版まで
  同一宣言。着手前に最新 main を再取得し y=10 レーンへの他オーナー着手がない
  ことを確認済み）。

## 実施内容

1. **C1d アンカーの事前検証（組み込み前・fail-closed）**:
   6つの published uniform closed form（z=8: K0999/K1000・z=9: K1001・
   z=10: K1002/K1011・z=15/16/17: K1065/K1077/K1087）を検証器に転写する
   前に、y=10 行を生両エンジンで検証（各 z0・x=10..45・R<=x+z0+30・
   計 15,336 点・H_ordered/H_canonical/cand10 の三者一致・不一致 0）。
   この事前検証が A17/K1087 転写初稿のバグ（value17 の T 先行評価順を
   崩して d>=19 行で P 判定を先に返す・(z=17,x=29,R=1) から 170 点
   不一致）を捕捉した。出版正本は修正後のみ。z=15/16/17 の (y,d) 過渡
   セルと S<17/S==17 分岐は y=10 で到達不能（S=x+10>=20）。
   低R単一トークン縮約 R<=z+6 も事前照合（x=10..159・不一致 0）。
2. **正本検証器 part2**: verify_y10_universal.py に C1d を組み込み
   （アンカー関数 A8u..A17u は出版検証器の (x,y,r) parametric 形を保持・
   y=10 で評価。出版 SHA をコメントで記載）。全チェック指定実行
   （C1 C1b C1d C2 C2b C3 C4 C4t C7 C8 C9 C11 C12）:
   **総 6,406,346 照合点・全チェック不一致 0・overall PASS**。
   C1d 140,850 点（アンカー 130,950 + 低R縮約 9,900）・マージ系
   1,494,591 点・tail 系 274,835 点・型機械全走型 123,543・C4t clip 21
   再掃引の confluence 違反 4,736〔初違反 (60,84,84)〕は part1 と不変。
   約75秒/run。
3. **3回実行の byte-identical 確認**: 同一 cwd 2 回＋別 cwd への隔離
   copy 1 回の計 3 回で audit.json が byte-identical
   （SHA-256 `41b7a315f0e7240390ccfc80f30488350549a835029c97559ff85ba9806bf8cf`）。
   検証器 part2 正本 SHA-256
   `f9169449309dcd25aaba8d6379d4289167f61eb3895b031e45ff9e80c46c05e4`（1,110行）。
4. **census_rows.py y=10 版**: y=5..9 と同型の生 tuple 二重再帰で
   z=0..79・x=10..70・R<=x+z+12 の 4,880 行（451,400 点・値0点 225,680・
   状態数 5,118,827・約18.4秒）を計算・行ごとの Thue-Morse 指数・T/P
   集合・tail を抽出（tail アサート R>=x+z+11 の (x+10) mod 2 全行成立）。
   census.txt（831,928 bytes・4,880行+空行80・SHA-256 `7aec116d…`）は
   第三実装として閉形式 cand10 と全 451,400 点で独立照合・不一致 0。
5. **K1141 observed→proved 昇格**: AGENTS.md「同じ命題の status 更新は
   同じ K 項目」に従い item を同番号で proved 昇格（title・scope・
   evidence・relations〔generalizes K0999/K1000/K1001/K1002/K1011/
   K1065/K1077/K1087 追加〕・artifacts〔proof dir・census・part1/part2 log〕
   を更新）。README bullet は observed 表記から全称証明表記へ同じ行で
   更新。knowledge.yml CI に K1141 verify/census の 2 step を追加
   （K1138 census step の直後・アンカー置換 1 回）。

## 昇格で確定した横断観察（y=1..10 全称表から）

- 基底点 y 点仮説 {z+1,..,z+2y-1}: y=10 で 10 点が全 z 確定（第10例）。
- tail 開始族式 x+z+y+1 と tail 値 (x+y) mod 2: y=2..10 の 9 族連続で全称確定。
- マージ命題 x<=z-y-1 → single_token(x+y,z,R): y=1..10 で全称確定（K1141 が
  y=10 版を全称系として昇格・監査上も 1,494,591 点独立照合）。
- clip 窓族式 2y+2: y=5..10 の 6 族連続 tight（y=10 は clip 21 で 4,736 違反・
  K1135 予想系列 6 連続的中）。
- 前倒し pin 格子公式 pin=z+(d+3y)/2: y=5..10 の 6 族統一。
- 最終 pin 行 d=y の追加値1点 2y+z+1: y=6,8,9,10 の 4 例（y=10 は偶数 y 初例）。
- 偶 z 対角行 d=-y の値1全欠如: y=8,9,10 の 3 族連続。
- pin 行 d 範囲の遷移（y=9 で互い違いに寄った奇z [-y+4,y]/偶z [-y+2,y-2]）
  は y=10 でも族式なし・一般証明は今後の課題のまま。

## 未解決（次工程候補）

- 横断法則（基底点・tail 開始・マージ・clip 窓・pin 格子・対角行規則）の
  y>=11 への一般証明レーン（これまで毎族の機械化を繰り返してきたが、
  y<=10 が全て確定したので補題化・一般証明を開く価値が出た）。
- y=11 族の同型機械化（skeleton survey・fit・B子=K1138 ではなく K1141 の
  cand10 を使う初の族・着手時は新しい単一オーナー宣言が必須）。
- 3トークン以上・固定幅・q点版安定化長・11×11 は範囲外。

## trust 境界

全称性は選択肢分解の健全性・正確な mex 恒等式・有限型空間の完全性
（raw錨・恒等式グリッド・型 confluence・シェル/多様体/probe・出版切片
転写アンカー・独立 census。K1023→K1138 と同一構成）による。
Lean ではない。C1d アンカー切片の正しさは K0999/K1000/K1001/K1002/
K1011/K1065/K1077/K1087 の主張。標準 11×11 の空盤勝敗・二石 root・
S2 {59,60} には一切言及しない。

## 出版物（本コミット列）

- part2-a: 実験dir（verify_y10_universal.py part2 正本・census_rows.py・
  output/audit.json〔part2 版〕・output/published_run.txt〔part2 3回目
  実行の標準出力〕・report.md に part2 節を追記）＋本 log。
- part2-b: output/census.txt（831,928 bytes）。
- part2-c: K1141 item observed→proved（同番号更新）。
- part2-d: knowledge README の K1141 bullet 更新（同じ位置で observed→
  proved 表記に書き換え）＋knowledge.yml K1141 CI audit step 2件。
