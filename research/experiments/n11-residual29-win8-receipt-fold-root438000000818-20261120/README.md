# n11 残余29行のWIN8-D10 receipt fold root 438000000818（fold24）

## 位置づけ

K1136の8石root `00000000000000043800000008180010` のWIN8-D10証明書を、五親S6 frontierの第31 receipt（fold24）としてfoldした。直前のfold23（K1133）正本を入力にし、K1136の証明書・監査正本・K1091掃引記録を再検査してから、証明書のD4被覆をfrontierへ適用する。

**これは行の閉鎖簿記であり、閉じたS6行のゲーム理論的勝敗を示すものではない。** WIN8-D10が証明するのは当該8石rootのゲーム木だけである。

## 固定した入力

- fold23 receipt正本: SHA-256 `04f334ff0f6aa995375283e94afc0e83ced6bebfeefea47359a5090a338fad59`
- fold23出版機: SHA-256 `c908f6c02842a305d642dcbb6157d3dfd832350afcc59452b0c917b0277d0a8e`
- K1136証明書: 34,843戦略行、1,260,393 bytes、SHA-256 `dbcb0bae71b9e00570f66db601790380362c65aaad2e46911cd2b80119337004`
- K1136監査正本: 19/19 gate、SHA-256 `d065383428621e03cfda87c9b20834f3e425c8c0e58f30823ee36d20828aa90c`
- K1091掃引正本: SHA-256 `edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25`
- runner v17 Git blob: `c132cc6425eee3feaeef1d697dd74f968cfedb59`

fold機械は12個のGit blob pinと49個のSHA-256 pin、計61入力を照合する。fold23出版機は隔離複写上でpristine再実行し、fold22・21・20・19の検査を推移的に通したうえで、fold23正本との一致を確認する。

## 結果

K1136の主張3行は、fold23後の残余29行にすべて含まれ、28個のD4正準6石行のうち現在openな対象として再導出された。余分なopen行はなく、3行だけを閉じた。

| 指標 | fold前 | fold後 |
|---|---:|---:|
| 5親targetの閉鎖行 | 83 / 112 | **86 / 112** |
| target残余行 | 29 | **26** |
| S6 manifest記録数 | 1,722 | 1,725 |
| 残存S6行数 | 6,126 | 6,123 |
| 残存S6 cost合計 | 485,438 | 485,213 |
| open classが必要とするS6数 | 4,434 | 4,431 |
| open classが必要とするcost | 351,886 | 351,661 |
| 親行incidence | 11,666 | 11,660 |
| 残存S5 orbit数 | 173 | 173 |

閉鎖した行とcostは次の通り。

- `00000000000000003800000008002040` — cost 66
- `00000000000000043800000008080000` — cost 75
- `00000000000000043800000008100000` — cost 84
- 合計cost: **225**

4つの親行はすべてclass 2で、親行incidenceは合計6減少した。個別の行数は46→45、8→7、9→7、65→63。余分なS6行の閉鎖は0。K1097のWIN16候補は2根・主張3行まで減った。

「S6 manifest記録数」は簿記上の件数であり、S6局面の勝敗数ではない。

## 独立検査と再現

- fold機械を5回実行。4つの先行ログと、生成器から再生成した機械の追加実行ログはすべて同じSHA-256 `cb01749a9b52e7ed4392dc2d25cf008e805b0ca17b40a25537680e9d1df0e5b2`。
- `build_fold24.py` はfold23機からfold24機を生成し、生成物は別作業領域の機械とbyte-identical（SHA-256 `f462733dbaa6a958680ce49ff85e056adf8756cc946fa5ac612442f2c47b4fc8`）。生成時の置換箇所・古い定数・pin件数を検査し、PINS=12、PIN256=49を確認した。
- 別実装の標準ライブラリPython監査器は**46/46 checks PASS**。座標変換と4×4行列式の24置換展開を使い、fold機械の幾何補助関数を流用せず、D4被覆・親行incidence・cost・frontier差分を再導出した。
- 独立監査正本SHA-256: `49f330c6e0f73c0a58fdd9b21c215c38fc3a594d35f1d617b1324468c4a3387b`
- fold receipt正本SHA-256: `c4ab76d3cb7eba5c1ab8e1830c43d17bf9a771f511b66e7e8573864f3f2402c7`

## 再現手順

Python 3.13以上を想定。入力再構成器は固定Git参照から必要ファイルを取得し、12個のGit blob pin・49個のSHA-256 pinと照合する。

```sh
python3 scripts/reconstruct_inputs.py /tmp/fold24-W
python3 scripts/build_fold24.py /tmp/fold24-W
FOLD24_W=/tmp/fold24-W python3 /tmp/fold24-W/fold_win8_root438000000818.py
python3 scripts/verify_fold24_independent.py /tmp/fold24-W /tmp/fold24-W/fold24/output/independent-audit.json
```

再構成元の固定参照は `reconstruct_inputs.py` の既定値に記録されている。入力の取得先が変わっても、内容がpinと一致しなければ停止する。

## 限界

このreceiptが閉じるのは五親targetの3行であり、その行の勝敗ではない。K1136のWIN8-D10証明書も当該8石rootに限られる。二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4、標準11×11空盤の弱解決は引き続き**UNKNOWN**。
