# 11×11 中央三石の四石応手：既存五石確定勝敗の逆向き再利用（2026-11-07）

## 新しい被覆結果（保存済み証拠からの有限計算）

三石位置 S={59,60,61} の四石目合法手は110、SのD4安定化群による軌道は30（先行log参照）。`research/experiments/n11-central-19-cover-20261031/output/s6sweep/s5_verdicts.json` の `first_win_s5`（78位置）から、Sを含む五石位置を選び、S以外の2石の各々を四石目候補として逆向きに抽出した。

**少なくとも1つの確定「元先手勝ち」五石子を持つ四石位置は50個、D4軌道では27個。** 四石局面の次手は元先手なので、合法な勝ち五石子が1つあれば四石親は元先手勝ち。対称性で軌道全体に拡張できる。残る未被覆軌道の代表四石目は **5, 23, 27 の3個**。先行の「既知1軌道・未確定29軌道」は、既存の五石証拠を逆向きに活用していなかったための過大評価であり、**27/30軌道に既存証拠からの勝ち手が存在**する。

この結論はK0675の五石勝敗分類を前提とする条件付きの親局面への論理的持ち上げである。今回、終局証明書を独立に再実行したわけではない。残る3軌道の勝敗はUNKNOWNであり、三石親自体の勝敗もUNKNOWN。特に、三石局面では第二手が四石目を選ぶため、27軌道の元先手勝ちだけでは全応手を覆わない。

## 再現（Python標準ライブラリのみ）

```python
import json
from pathlib import Path
p = Path("research/experiments/n11-central-19-cover-20261031/output/s6sweep/s5_verdicts.json")
data = json.loads(p.read_text())
S = {59, 60, 61}
def orbit(i):
    x, y = i % 11, i // 11
    return min(y*11+x, y*11+10-x, (10-y)*11+x, (10-y)*11+10-x)
parents = {}
for h in data["first_win_s5"]:
    bits = int(h, 16)
    cells = {i for i in range(121) if bits >> i & 1}
    if not S <= cells: continue
    assert len(cells) == 5
    for i in cells - S:
        parents.setdefault(i, h)
covered = {orbit(i) for i in parents}
assert len(parents) == 50
assert len(covered) == 27
assert covered == {0,1,2,3,4,11,12,13,14,15,16,22,24,25,26,33,34,35,36,37,38,44,45,46,47,48,49}
assert {5,23,27}.isdisjoint(covered)
print("direct parents", len(parents), "covered orbits", len(covered))
```

合法な四石目110個と全30軌道の完全性は `research/log/2026-11-07-n11-s3-central-triple-d4-stabilizer-30-orbits.md` の整数行列式コードで再検査できる。五石子は既存の合法局面データに由来し、親四石局面も合法性の下方閉包により合法。

**重要**: 「元先手勝ち」は五石局面で手番の勝ちを意味しない（五石では第二手の番）。K0675の固定側の勝敗定義を保持すること。
