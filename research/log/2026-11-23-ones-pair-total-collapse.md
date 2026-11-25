# {1,1}全R崩壊定理 run log(ones-pair total collapse・2026-11-23)

## 発見経緯

K1264(ミントークン階段定理)の出版完了後、同reportの未解決・次課題2
「{1,1}の無分離観察の全称化」を本レーンが引き取った。着手時点の構造分析で、
分離の障害である補題Zの窓(n<=z)が x=1 では窓外でも破れない理由(値域が
{0,1,2}に落ちる)に気づき、補題V1(x=1残余の完全特徴付け)の形で詰めた。
z=0ではB子/A子の値がn=1で丁度1点だけ乖離(2 vs 1)するが3ケースすべてでmexが
一致することを確認し、全称定理が閉じた。

## 実行順序(publish-then-execute)

1. **宣言前探査(宣言ノートに開示)**:証明骨子の解析的導出+probe_ones.py
   グリッド(K1264出版verifierのエンジン・閉形式ブロック逐語使用):
   補題V1 4,305点 bad 0・{1,1} 2,025点 bad 0(z 0..24, R 0..z+14で無分離)・
   {1}^t census(宣言前のものはt=1..6・z<=12)。
2. **単一オーナー宣言の出版**(commit 284d82c6):主張・証明構造・protocol
   (D0..D5・変異電池8種・決定性4回)・宣言前探査の全開示。observed HEADは
   336481d2(y23 fitレーン)。宣言publish直前に並走のK1254整理(aa316896)が
   挟まったが無関係。
3. **宣言後実行**:検証器 verify_ones_pair_collapse.py の構築(build_verifier.py
   による出版K1264機からエンジン・閉形式ブロックのsha256ゲート付き機械抽出・
   手転写ゼロ)→ audit PASS(総照合67,513点 bad 0)→ 変異電池8種すべて捕捉
   (6/1/380/720/14/1/1/1)→ 決定性4実行(同一cwd2+隔離cwd+env -i・
   PYTHONHASHSEED=random・別HOME)で output/audit.json がbyte-identical
   (SHA-256 1f18ae21...)。
4. **実験dir出版**(commit ffbd5b7c):report.md・verifier・build_verifier.py・
   probe_ones.py・output/audit.json の5ファイル。初回pushは並走コミット
   (b9b855dd・K1258 README bullet)によるfast-forwardエラーで1回失敗、
   再fetch後に再pushで成功。commit-pinned fetch-backで5/5 byte同一を確認。

## 誠実記録

- **宣言点数算術のドリフト3箇所**:宣言ノート(284d82c6)の総照合点70,595に
  対し実測は67,513。D3は本文protocol(400点+100点×3比較=1,500)に対して合計
  計算だけ4,500と3倍に誤算上。D4は本文どおりR 0..z+10を実装したのに点数予想
  計算だけR 0..z+11で行い1,700と出した(実測1,615)。D5はpublished_expect照合
  +1点を持つアンカー3件を均一5点と数え30とした(実測33)。本文protocolはすべて
  実装どおりで、ドリフトは点数算術のみ。実測値が正本。
- **run4 PATH事象**:env -i実行はPATH=/usr/bin:/binだとpython3が/usr/local/bin
  に届かず1回失敗。PATHへ/usr/local/bin追加で再実行・byte-identical確認。
- **{1}^3@z=0,R=3 の分離点**は宣言前探査の新観測(K1264出版側は同rowの
  z=1,R=3 witnessのみ記載)。

## 残務・次課題

1. 全R崩壊多重集合の完全特徴付け({1,1}以外にあるか)。
2. K1264課題の残3項(窓外第2段構造・max(z+min(X),2)統合窓鋭さ・アリティ>=3の
   一般条件)は非接触のまま。
3. z切片機・y族検証器のlowR帯チェックのK1264/K1265引用への置換実装(別レーン)。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は常に
UNKNOWNのまま。**
