# four-row q=7 自己完結ブロッキング計数証明（K1196） — 研究log

- 日付: 2026-11-21
- 担当: 本レーン（11×11長期レーン・固定幅副産物レーン・単一オーナー）
- 単一オーナー宣言ノート: `research/log/2026-11-21-four-row-q7-blocking-counting-self-contained-single-owner-note.md`（commit `80ebdec39e7b349e2d3f2b6c66b652b3936f4e91`・2026-11-21T07:36Z・宣言時 main HEAD `497f4e176e82d979e65084900acc4ee7d3c72c0e`）
- 成果物: `research/experiments/four-row-q7-blocking-counting-self-contained-20261121/`（part1 commit `4d00069c7a5900db815a0b83ad9f735c76013f2d`）・K item K1196・本log・K1182 relation 追記

## レーン選定

2026-11-21 の第三検証ラティス（ext2 全枠）と全着手済み課題（refuted50 第三検証・fold 系 ext2・q6 帯延伸・q34・m22・s11・vertical-fiber）は他レーン宣言済みで着手禁止。
K1182 の解釈規約に明示された自由課題「K0318 に依存しない自己完結的なブロッキング計数証明（M の値を変えないが証明の独立性を高める）」が未着手であることを確認し、
n11 に無関係（衝突ゼロ）のこの課題を取得した。

## 主定理（数学的証明・K0318/掃引非依存）

**定理.** w=4・q=7 の 4×m 盤（一般に 4 本の水平線上の点配置）で行欠損（欠損行の石数
r ≤ q−2 = 5）を伴う極大安全配置が存在するのは m ≤ 86 のときに限る。

骨子: 欠損行 R の空点（m−r 個）は水平線（行容量 6 に届かない）でも非水平直線
（格子点 ≤ 4）でも block できず、すべて blocker 真 円が担う。割当円 C_i の
R 内割当点 e_i ∈ {1,2}・R 内石 u_i は円×水平行交点 ≤ 2 より e_i + u_i ≤ 2、
blocker 定義（円上石 ≥ 6）より R 外石数 t_i ≥ 4 + e_i。
相異なる円は非共線 3 点組を共有しない（2 共有点以下・円は 3 点で一意）ため
Σ C(t_i,3) ≤ C(18,3) = 816（R 外石 ≤ 3×6 = 18）。各円で C(t_i,3) ≥ 10 e_i
（type-1: C(5,3)=10・type-2: C(6,3)=20）なので 10(m−r) ≤ 816 ⟹ m ≤ r+81 ≤ 86。

系: 機械掃引 [13,86]（K1177 の 13..85＋K1182 closure の genfast3 m=86・いずれも
既刊正本）＋本定理の [87,∞) ＋ m=12 不足極大 witness ＋ capacity 存在（13/16 witness・
幅単調性）により、**K0318 を使わず M_{4,7}=13 が閉じる**（第二 certificate・
K1182 の status/値は一切変更なし）。誠実な相対位置: 計数閾値 87 は独立には
K0318 の閾値 81 より 6 幅弱いが、既刊掃引 86/88 が埋めているため certificate 十分。
一般化参考値: q=6 は m ≤ 117（U_{4,6}=103 より弱い・M_{4,6} は閉じない）、q=8 は m ≤ 82。

## 機械検証・battery（part1 の内容）

検証機 `scripts/verify_blocking_counting_20261121.py`（23,986 bytes・sha256
`ee5d88e200a5ae15dfc426354e9f550efac3a45d1243f921c5db4b1155a93147`・stdlib のみ・
決定的・fail-closed: 監査は全 gate 通過時のみ書込・1 実行約 1 秒）。全 49 gate
（A 幾何補題 9 / B 計数 3 / C 掃引 certificate pin 7 / D m=12 witness 前提 15 /
E m=13 capacity 7 / F 組立 4）が ALL PASS。

- **A**: 補題の格子全域整数演算テスト（4×6/4×12/4×13 の全 3 点組。円×水平行 ≤ 2・
  同一 3 点組を載せる相異なる円なし collisions=0〔registered 1,884 3つ組〕・円上 3 格子点
  非共線・非水平直線 ≤ 4 格子点）。
- **B**: max {a+2b : 10a+20b ≤ 816} = 81 の 817² 全数値列挙、組合せ定数、閾値 87 整合。
- **C**: frontier records.jsonl の q7 射影（86 レコード・def 7..88 plain＋lexH 13/86＋
  capacity 13/16）sha256 pin・witness band SAT・13..88 全 UNSAT・INDET 0・
  conflicts pin（13:5446, 20:3359, 85:3759, 86:5930, 87:5191, 88:6072）。
- **D**: m=12 witness 23 石の全前提 instantiation（全 25 空点の block 確認・割当円 7 個の
  e/u/t 分類で t ≥ 4+e 全円成立・Σ C(t,3)=80 ≤ 816・3つ組 registry 80 非交差直接確認・
  10(m−r)=70 ≤ 80）。
- **E**: m=13 capacity witness 24 石の同型監査。**F**: 掃引帯+計数帯の組立・結論。

battery 4 実行（同一 cwd 3 回＋隔離 copytree・隔離 HOME/TMPDIR・env -i・
PYTHONHASHSEED=random 1 回）すべて監査 byte-identical（`audit.json` sha256
`4361837037034b632f79f2b6c9cef6f1ca3fc03a85d65e66b90acc810fefb277`・9,266 bytes）。
負の制御: witness byte 400 XOR 0x20 → rc=1・`GATE FAILED [g15_pin]`・監査未書込。
正の制御: records.jsonl に無関係 1 行追記 → rc=0・監査 byte 同一（append 不変）。

## 実験事実・知見（発見順）

1. 検証機構築中に 3 件の実装バグを検出・修正（いずれも battery 成功前に解消し、
   reproduction.log に実験事実として記載）: (i) 円正準化の d2 符号正規化漏れ
   （A2 gate が collisions=8,304 で fail → 円方程式の対称性補正を追加し collisions=0）、
   (ii) path 階層バグ（parents[3]→parents[4]）、(iii) gate id フォーマット
   文字列バグ。
2. 監査埋め込み設計: audit に records.jsonl 全体 sha を埋めると q6 追記で
   append 不変性が壊れるため、q7 射影 pin のみ埋め込む設計に変更
   （射影 sha256 `6a54fb4f84a4de3504c1969f1222b24cf2ba747bc3523586c6e70ca277f2ab6f`・
   86 records・実行時全体 sha は reproduction.log 記載）。
3. 計数上界の閾値 87 が K0318 の 81 より 6 幅弱い一方、q=7 に限って既刊掃引の末端
   （86・さらに 88）と正確に噛み合う。q=6・q=8 では計数単独では閉じない
   （117/82）。この「要素計数証明の閾値と掃引末端の噛み合わせ」が第二certificateの
   実用条件という知見を得た。
4. api.github.com の core quota は本実行でも枯渇気味（未認証）。fetch-back 照合は
   raw 固定 commit URL＋sha256sum で完結させた（K1195 運用と同一）。

## 出版（3部構成）

- **part1**（実験dir 4ファイル一括）: commit `4d00069c7a5900db815a0b83ad9f735c76013f2d`
  。push 直後に raw 固定 URL fetch-back で 4 ファイル sha256 照合・byte 一致
  （README `68c05e0a…`・verify `ee5d88e2…`・audit `43618370…`・reproduction.log
  `42009e49…`）。
- **part2**（本log＋K item K1196＋K1182 relation 1 件追記）: K 番号は push 直前 3 点確認
  （最新 items コミットは K1195、knowledge README grep で K1196 なし、K1194 が
  refuted50 レーンに想定〔K1195 の前例どおり温存〕）で **K1196 を採番**。
  K1182 へは relations に 1 件（type: related → K1196）のみ追記し、frontmatter その他・
  本文・status proved は byte 変更なし。
- **part3**（knowledge README bullet）: 最新 main の README を再取得し、並走 bullet を
  温存したうえで自 bullet のみ末尾 append。

## 位置づけと限界

本作業は K1182 の主張に第二 certificate を与えるものであり、既存の
verdict・records・witness は一切変更しない。M_{4,6}（q=6）は本項では閉じない。
行は 1 行も閉じない（n11 の fold/coverage 簿記に無関係）。nodes 数・conflicts 数・
solved 数を勝敗として読まない。REFUTED-D10 は LOSS 証明ではない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**（2026-11-21）
