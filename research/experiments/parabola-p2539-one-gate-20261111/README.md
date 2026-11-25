# p2539: 空対から二点以上の追加が必要、さらに27点排除（2026-11-11）

採用時の正本はK0734。同じ1258点seed S（SHA-256 `454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb`）の五点削除改善を対象とする。
既存の221点除外と18点の正gate Eを使い、**Eからちょうど一点だけ追加する形状を独立排除**した。
従って改善にはEの少なくとも二点が必要。保存済み相互制約との結合で27点をさらに除外し、総除外は248点となった。
全体の五点削除改善や最大安全サイズは未解決。

## 新しい制限形状の一回の探索

保持側親Fは51570変数144546節、原点・元の完全対{6,2533}を保持し、exact1259点・exact五点損失を表す。
Fへ既存221負point単位節、Eの正18点OR、E内全153組の負二項節を追加した。
合計51570変数144921節。負二項節と正ORによりEの選択数を正確に1へ制限する。
これは従来の18個別point仮定で許されていた複数E点の追加を禁止する新しい形状で、同じ未知入力の反復ではない。

PySAT 1.9.dev21/Cadical195、proof-enabled、budget100000で一回だけ実行した。
実conflicts667・1.761秒でSOLVER_UNSAT、完結DRATを保存。launcher終了値0、timeoutなし。
CNF・proofの圧縮bytes、raw SHA、source SHA、実終了値と標準出力を保持した。

## 独立監査と別処理再生

`verify.py`は探索コードやSATライブラリをimportせず、親の全schemaと追加375節を独立解釈する。
親のpoint定義・exact点数・損失counterと、221単位節・正18点OR・全153負二項節の対応を照合した。
38868実四点をgeneric整数4×4行列式で確認し、固定DRAT-trimの-Uで完結証明を受理した。
`replay.py`でも、採用圧縮CNF/DRATから独立schemaとRUPを別処理再生し受理した。
受理は終了値0・s VERIFIED。部分導出DERIVATIONと異なり、この**制限形状の入力**の反証である。
元の親F単独や五点削除近傍全体のUNSATは主張しない。221除外節は以前の独立根拠を引き継ぐ。

初回auditは親schemaへseedをset型で渡したため、要求するsorted listとの型契約で拒否された。
呼出側を修正し、採用auditは新しい`audit-final/`へ保存した。ソルバや証拠の再生成は行っていない。
実CNFの6改変を拒否し、18変数の全262144真理値割当てでexact-oneの受理が18通りだけであることを確認した。

## 大きなTにも二点追加が必要

既存の必要条件より、改善Tは五点を失い、Fの固定点を保持し、221除外点を避け、T∩E≠∅。
|T∩E|=1と仮定し、その一点をvとする。
(S∩T)∪{v}の1254点を含むTの1259点部分集合T'を選べる。
T'は安全、損失5、原点・完全対保持、221点回避と|T'∩E|=1を保つため、今回の入力へモデル拡張できる。
独立反証に矛盾する。従って大きな改善Tにも|T∩E|≥2が必要。

## 保存済み条件付き排除から27点を追加排除

以前のgate-cover実験は、各非gate点uに対して18組{u,v}の負hitting証明または必要障害族の削除証人を保存している。
既除外221点以外にも、負証明で排除されなかったvが一つしかない点が27個あった。
u∈Tなら、他の17個のgate点はTに含められず、|T∩E|≤1となるため、今回の|T∩E|≥2に反する。
その27点を次に挙げる。

```
4 632 813 819 824 879 937 1018 1046
1316 1358 1478 1550 1657 1665 1721 1731 1742
1811 1895 1910 1929 1931 1941 1963 2096 2160
```

`qualify.py`は以前の圧縮証明書・独立監査・source hashを確認し、27×17=459個の負hitting証明を再検査する。
各点に唯一残るgate点はqualificationの`conditional_cover_details`へ保存した。
この27点について新たなSAT探索・native RUP導出は行っていない。
必要障害だけをhitする残存証人を安全集合に読み替えない。個別18仮定の以前のUNKNOWNと、今回のexact-one反証を区別する。
全体範囲1258≤A(2539)≤1271は不変。

## 再現と引継ぎ

既存出力を上書きしない新しいpathを使う。

```powershell
$exp='research/experiments/parabola-p2539-one-gate-20261111'
uv run --locked python "$exp/verify.py" --saved "$exp/output" --output "$exp/audit-fresh"
uv run --locked python "$exp/replay.py" --output "$exp/replay-fresh.json"
uv run --locked python "$exp/regression.py" --output "$exp/regression-fresh.json"
uv run --locked python "$exp/qualify.py" --output "$exp/qualification-fresh.json"
```

新しい形状の探索再現は`uv run --locked --with python-sat==1.9.dev21 python <exp>/run.py --output <fresh-directory>`。
次回はE内の独立未排除146組による正被覆や、exact-two-gate形状を評価できる。
今回排除したexact-one形状や、以前の18個別仮定を同じ条件で繰り返さない。
