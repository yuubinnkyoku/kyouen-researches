# seven-row-q8-band-probe-20261115

**Negative record（正直な負の記録・非不在の主張ではない）**: (7,8) 帯
（M_{7,8} ∈ [25, 651]・K0825・witness 前線 7×25）の naive な def 単一節
OR 符号化による帯掃引（m=25..650 を def-mode kissat で一掃する高速レーン戦略）
の実現可能性をプローブした結果、**m=26 と m=45 の両幅で 200s cap INDET**
となり、掃引はこの符号化では実行不可能と判断した。掃引は行っていない。

## プローブ結果（genfast2.js def 単一節 + kissat 4.0.4・200s cap）

| 幅 | curves | vars/clauses | conflicts @200s | verdict |
|----|--------|--------------|-----------------|---------|
| m=26 | 702 | 27,070 / 97,003 | 3,034,922 | INDET (rc 124) |
| m=45 | 1,684 | 47,250 / 170,097 | 2,501,174 | INDET (rc 124) |

既知の難所と同水準で横這い: (7,8) m=24 def-OR 240s 3,829,302（K0825）・
m=25 rowY=3 250s 3,534,747（K0825）と同程度の conflict 密度。
curves 数は m 増加で増える（702→1,684）が困難度は下がらない —
(7,9)/(7,10) 帯（m=586 でも ≤4.6k conflicts）と対照的で、
q = w+1 では禁止曲線密度の増加が伝播を強化しない。

## 結論・次のレバー

- **naive def-mode 帯掃引（高速レーン戦略）は (7,8) には不適**。
  exact M_{7,8} の決着には (a) rowY 行固定分割（K0825 が m=24 で使用・
  ただし m=25 rowY=3 が 250s INDET）や 35 クラス deficiency 分割
  （K0818/K0819 機械）を各幅に適用する重装備レーン、または
  (b) K0342 型 universal tail bound で U=651 を大幅に下げる必要がある。
- 生成器コストの壁は別途存在: q=8=w+1 は genfast3（q ≥ w+2 限定）不可・
  genfast2 は O(m³)（m=45 生成 ~0.2s だが m=600 では ~400s/幅）。
- 本プローブは不在の主張ではない（INDET は非証明）。(7,8) の各幅の
  行欠損極大非存在は依然どの幅も証明されていない（witness-free 帯は空）。

## ファイル

- `output/records.jsonl`: 2 records（INDET・conflicts・cap 付き）
- `output/s7x26q8.kissat.txt` / `s7x45q8.kissat.txt`: 生ログ（INDET 打ち切り）
- `output/*.meta`: genfast2 生成メタ（vars/clauses/curves）
