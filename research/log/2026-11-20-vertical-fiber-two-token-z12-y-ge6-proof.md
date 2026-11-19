# z=12・y>=6 一様2トークン全Grundy分類（K1056）研究ログ

2026-11-20。高速レーン。作業開始時の最新mainは `7d191ed173371b702550f2bfbc9b2915bf3e4dbf`（K1055 README追記）。root `AGENTS.md` と `research/knowledge/README.md` を読み、現在の正本K項目・未解決範囲を確認した。

## 重複確認と選定

- K1043はz=12,y=5の全x切片、K1055はz=11,y>=6一様全Grundy定理。READMEと両正本は「z=12,y>=6はB=K1043・C=1 xor K1055で着手可能」と明示していた。
- A子は同じy行のx-1、B子はy=6でK1043・y>=7でy強帰納、C子はK1055で閉じる。依存が揃い、長時間root探索なしで全称化できるため、この一様族を優先した。
- `.github/workflows/knowledge.yml` と `refresh-knowledge-generated.yml` を確認したところ、K1055の独立検証器がknowledge integrity workflowに未登録だった。K1056と合わせて登録する。

## 導出

1. z=12,y=6..19、d=0..40の直接再帰でT/P候補を調査。値2は基本ラダーO[1,11]にd=2,6,10の前倒し点、d=13の掃引帯、d>=14のpinを加えた形になった。
2. 値1はd>=12で基底点O[13,2y+11]を持ち、これはy個の点 `{z+1,z+3,...,z+2y-1}`。d<12は過渡帯とy=6,d=0の対角縮退セルを別扱いにする必要がある。
3. A/B/C子の閉形式署名をparity別に圧縮し、d=0、d=1..11、d=12、d=13、d=14、d>=15のクラス表を得た。d=13の掃引帯はO[2y+13,S+12]、d>=14のpinは2y+13。
4. y=6基底とy>=7強帰納、各行内x外帰納を組み合わせ、全1<=R<=S+12を署名帯mexで閉じた。R=0は終局、R>=S+13はK0832一般tail。

## 監査

`verify_z12_y_ge6_proof.py` をPython 3.13.5で実行。2,892,040検査、不一致0。二回実行し、別作業ディレクトリからの別プロセス実行でもaudit.jsonはbyte-identical。

- verifier SHA-256: `4a02431098bea2f32684239a486482ed5eb3b04acc5ab243e8d85b7cbefbd895`
- audit SHA-256: `ceeed4db3e65f9e481b2fbaf632dd9237d3ac5cac245f48dce5bc86056df8cf8`
- audit（自己参照除外）SHA-256: `3ee74f79e6d2c9c2557d0b29eb45cca6358fc60db04dd27ed386a44af733340e`

監査は転写・実装照合であり、全称性の根拠は二段帰納と署名帯表。標準二次元盤への転送や11×11空盤の値は主張しない。

## main反映と限界

K1056、report、candidate、bands、band_derive、verifier、audit、logをmainへ直接反映する。K1043/K1055の現在の未解決記述、knowledge README、knowledge integrity workflow、generated-view refresh記録を同期する。K1055 verifierの未登録も同時に修正する。generated領域とroot READMEは直接編集しない。branch/PRは作成しない。

この実行環境からGitHubをcloneできなかった（DNS解決失敗）ため、repo全体の `uv sync --locked`、knowledge check、unittest、build.pyは未実施。ローカルPythonの独立監査は完了したが、CI成功はGitHub Actionsで確認するまで未完了とする。

次の候補はz=13,y>=6（B子K1045、C子1 xor K1056）で、同じ二段帰納を再利用できる。ただし着手時に最新mainで並走・重複を再確認する。
