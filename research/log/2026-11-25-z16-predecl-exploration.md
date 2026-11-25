# z16 min>=11 (floor-11) 宣言前 census 探査 log — 高速レーン 2026-11-25 13:xx UTC

## 概要

K1320 (T-Z15, z=15 min>=10) 完了直後の観測系列継続として、次スライス
**z=16 min>=11 (floor-11)** の宣言前 census kit を出版した
(publish-then-execute・本 log は観測のみで主張なし・slot は宣言 lane が
取得する)。kit: `research/experiments/strip-z16-min11-20261125/`
(engine_block.py `582c93c1…` chain 同一 bytes / explore_z16pre.py
`87f3bb71…` / explore_z16pre.out `16b10d0b…` = 3 走 byte-identical /
README)。explore_z16pre.py は凍結済みの出版 `explore_z15pre.py`
(`3e2a8ab8…`) のテキスト差分改造 (z 15→16, j+16→j+17, floor 10→11,
9→10 段, s ∈ {0}∪{11..41}, strip m∈{11..15}, m=10-row in-band record
(R=27), spots m∈{16..19}, m=11 base spot, below-band (17;Y;17) census)。
差分は kit README に全開示。

## 観測 (すべて判定外・census 規模)

10 セルすべて s-only (multivalue 0・各 183 形状)。deviant 表:

| cell | deviants (s : value (direction)) |
|---|---|
| F16f11 | 16:1 (UP) — 単一 UP 点のみ, 尾なし |
| G16f11 | 14:0 (DOWN), 16:2 (UP) |
| E16f11 | 14:1 (UP) |
| D16f11 | 12:0 (DOWN), 14:2 (UP) |
| C16f11 | 12:1 (UP) |
| B16f11 | 12:2 (UP) |
| A16f11 / A2 / A3 / A4 | なし (4 段連続完全崩壊) |

- **死点化イベント (第 2 回・s=10 枠のみ) の実測**: z=15 の供給源
  位置 s=10 (C15f10/B15f10/A15f10) は床 11 未満で全滅し、z=16 の
  deviant 表に s=10 は 1 つも出現しない。s=12 と s=14 の供給源は
  存続するが、deviant 構造は rank を越えて再編される (E は s=12 を
  失い、D は s=14 UP を獲得、B は s=10 DOWN から s=12 UP へ交代)。
- **新規 s=16 deviant クラス** (F16f11 UP:1, G16f11 UP:2): 過去の
  どのスライスにも F/G 段の s=16 deviant はなく、宣言 lane が供給
  を導出する必要がある。
- **F 系第 7 形態候補**: z=15 の第 6 形態 (DOWN@14 + 穴@15 +
  s>=16 恒常 2 尾) は z=16 に引き継がれず、F16f11 の deviant は
  単一 UP 点 (s=16, 値 1) のみ、tail spots s∈{42..49} は全 10
  セル 80/80 一致 (F の尾は消滅)。below-band 子 H(17;Y;17)=v(s,17,17)
  は 183 形状 deviant 0 (K1320 補題 BB の z=16 対応物の完全崩壊
  観測) でありながら F 構造は前スライスと異なる生成経路になっている。
- **T-Z16 主張位置の census**: m∈{11..15}, parts>=m, arity<=3 の
  456 形状 0 違反 (累積 11→142 / 12→249 / 13→333 / 14→401 / 15→456)。
- **帯域内 m=10 行 z=16 記録 (R=27, co-token 10 許容, arity<=3)**:
  **130 形状 0 分離** — K1320 §6 残余 (m=10 行 z∈{16,17}) のうち
  z=16 に初の肯定的データ (z=15 の m=9 行 analog は 152 形状 0 分離)。
  A4 セル (j=10) は Y>=11 制限で完全崩壊 (183 形状 deviant 0)。
- strip spots m∈{16..19} 12/12 一致。m=11 base spot H(28;(11,11);16)
  = 0 = v(22,16,28)。

## 誠実記録

- 本 kit の構造メモ書きは最初「s=10 と s=12 の供給源が床 11 未満で
  死ぬ」と予測を誤記した (s=12 は 11 以上で存続)。census 出力の
  s=12 deviant 存続で着目し、**凍結・出版の前に修正した**
  (.out bytes は docstring を含まないため不変・3 走 determinism
  は修正後に出力を取り直して再確認)。
- 派生元 explore_z15pre.py (出版済み凍結) との全差分は kit README
  記載どおり。engine pin `bd5f22e4…`assert 合格を毎走で確認。
- 3 走 (既定 / PYTHONHASHSEED=1 / env -i 隔離 dir) すべて rc0・
  stdout byte-identical・約 15 秒/走。

## ハンドオフ (次の宣言 lane 宛け)

- 本 kit から T-Z16 (min>=11) の slot claim→宣言ノート (紙面証明は
  10 段梯子 j=1..10・C 手子 = 出版 K1320 z=15 セル表の厳密適合・
  底 a=11 子 = A416f11 完全崩壊観測・階段子 R=24=z+min・帯域下子は
  (17;Y;17) 崩壊観測)→verify 機体→公式実行 chain を開始できる。
  想定 battery: D1 183×10=1,830 点 / D2 strip 456 / D5 z=17
  v(s,17,17) 照合 / D8 analog / A4 j=10 供給線 (m=10 行 z=16 の
  帰結) は D3 analog と同様の直接 anchor または増分 anchor を
  検討 (K1320 独立検証 log の教訓)。
- 注意: A416f11 (j=10) の「in-band 3 番目」構造面白さ — z*(10)=18
  なので z=16・z=17 の 2 スライスが帯域内底子になる初ケース
  (z=15 のときは 1 スライスのみ)。m=10 行残余 z=17 も近い。
- **着手前必ず最新 main 再取得 (hourly 並走注意)**: 現在並走 lane が
  z15-min9 (K1321 仮) を進行中 (predecl kit `5ec6c35d`)。本 kit の
  z16 スライスと m=10 行 z=16 は直交だが、次 lane が m=9 行 z=16 に
  着手する場合は名称での衝突確認を。
- 標準 11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN・
  verdict 不消費・本 log の観測は定理でも全称主張でもない。
