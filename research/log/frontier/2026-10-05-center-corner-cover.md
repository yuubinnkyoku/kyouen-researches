# 2026-10-05: 中心・隅s4 coverの最適値を独立証明

開始時main: `754cd0710d448ab397aa0cd3cb1a941e5d7f5451`。
AGENTS、現在のknowledge、n11未解決項目、df-pn、s5永続cache、s4 manifest、
set-cover、adaptive coordinatorと旧ログを確認した。

候補は残余hypergraphの独立双子点圧縮、s4 coverの独立最適下界、root分解。
今回、MILPのoptimalラベルに頼っていたcover最適値を検査可能な厳密dualへ
変える方向を選んだ。勝敗探索を長時間回すより、再利用性と決着可能性が高い。

LPを診断用に一度解くと、n11のdualが62点の重み1/2だった。これは
中心・隅rootの主対角反射orbitから、非隅orbitごとに一代表を選んだ形である。
classに含まれる隅数で場合分けすると、非隅orbitを高々二つしか覆えない。
この観察を全称下界へ進めた。LP出力自体は証明として採用しなかった。

上界は全隅を先に覆い、残るorbitをmatchingで組む。円の水平行交点≤2を
使う次数評価でn≥9を閉じ、n5/7は具体有限証人を検査した。既存
`{center,corner,1,2}` classを含めてもn≥9の最適数は維持される。

結果はK0350へ昇格: 奇数n≥5で `ceil((n²+n−8)/4)`、n11で31class。
生成器は共通geometry、検査器は平行移動3×3整数行列式と独立D4を使った。
n3/5/7/9/11/13/15の全classへのdual制約を検査し、上界証人と一致した。
class削除、偽coverage、過大dual、重複classは拒否された。

各classの勝敗は新たに探索していない。n11空盤はUNKNOWN。
次は実cacheを入力するweighted/adaptive coverへの適用であり、単純class数の
最適性を速度改善へ読み替えない。
