# n11 残余26行のWIN8-D10 receipt fold root 200003800200（fold25）

## 位置づけ

K1137の8石root `00000000000200003800200008180000` のWIN8-D10証明書を、五親S6 frontierの第32 receipt（fold25・第15 WIN8 receipt fold）としてfoldした。直前のfold24（K1140・候補A）正本を入力にし、K1137の証明書・監査正本・K1086掃引記録を再検査してから、証明書のD4被覆をfrontierへ適用する。

**これは行の閉鎖簿記であり、閉じたS6行のゲーム理論的勝敗を示すものではない。** WIN8-D10が証明するのは当該8石rootのゲーム木だけである。

## 固定した入力

- fold24 receipt正本: SHA-256 `c4ab76d3cb7eba5c1ab8e1830c43d17bf9a771f511b66e7e8573864f3f2402c7`
- fold24出版機: SHA-256 `f462733dbaa6a958680ce49ff85e056adf8756cc946fa5ac612442f2c47b4fc8`
- K1137証明書: 19,525戦略行、706,180 bytes、SHA-256 `7bd64a47bed13c25fe069b0b3563c06081639cd3d2ad09b28a1e6c65a41fa61d`
- K1137監査正本: 19/19 gate、SHA-256 `dafa177bf74fd528c34e9a858a83345df4cf8138c17f33ca0102c28840f28c04`
- K1086掃引正本（addtwo-greedy23-d10-sweep）: SHA-256 `3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced`
- runner v17 Git blob: `c132cc6425eee3feaeef1d697dd74f968cfedb59`

fold機械は12個のGit blob pinと51個のSHA-256 pin、計63入力を照合する。fold24出版機は隔離複写上でpristine再実行し、fold23・fold22・fold21・fold20・fold19の検査を推移的に通したうえで、fold24正本との一致を確認する（fold19はfold18 marker-reversible preverified写しを通す。fold10..fold23はSHA-256 pinとfrontier全段再計算でも検査する）。

## 結果

K1137の主張2行はfold24後の残余26行にすべて含まれ、28個のD4正準6石行のうち現在openな対象として再導出された。C(8,6)部分幾何には主張2行のほかにtarget外open 1行があるため、閉鎖は**主張2行＋余剰1行の計3行**で行われ、余剰は`extra_s6_rows_not_in_target`へ分離記録した。5親targetの簿記は主張2行のみで進む。

| 指標 | fold前 | fold後 |
|---|---:|---:|
| 5親targetの閉鎖行 | 86 / 112 | **88 / 112** |
| target残余行 | 26 | **24** |
| S6 manifest記録数 | 1,725 | 1,728 |
| 残存S6行数 | 6,123 | 6,120 |
| 残存S6 cost合計 | 485,213 | 484,997 |
| open classが必要とするS6数 | 4,431 | 4,428 |
| open classが必要とするcost | 351,661 | 351,445 |
| 親行incidence | 11,660 | 11,654 |
| 残存S5 orbit数 | 173 | 173 |

閉鎖した行とcostは次の通り。

- `00000000000000003800200008100000` — cost 79（主張・5親target内）
- `00000000000000a09002000080000000` — cost 65（主張・5親target内）
- `0000000000000080120a000000008000` — cost 72（余剰・target外・C(8,6)部分幾何に内在・unswept・c2×2需要行）
- 合計cost: **216**

4つの親行はすべてclass 2で、親行incidenceは合計6減少した。個別の行数は7→6、7→6、54→52、38→36。root合法手は42。K1097のWIN16候補は1根・主張1行まで減った。K1137のg19が記録する`residual_open_rows`はfold23残余29時代の監査時点の値であり、主張2行のopen性はその時点で固定検証済みである（本foldはfold24後残余26での再導出と二重に整合する）。

「S6 manifest記録数」は簿記上の件数であり、S6局面の勝敗数ではない。

## 独立検査と再現

- fold機械を3回実行（同一cwd 2回＋隔離W複写・別cwd・別HOME 1回・いずれもfold24 pristine rerun込み）。3実行ともreceipt正本は同一SHA-256 `5780f3875ed13554c6f58f269cdb587b792e0c9f930aba11c551a89e17a1074d`・実行ログもbyte-identical。
- 固定Git参照`60e5109efad…`から`reconstruct_inputs.py`でWを全入力pin照合付きで再構成し、`build_fold25.py`で機械を再生成・実行・監査するend-to-end再現も実施した。再生成機は既存機とbyte-identical（SHA-256 `e871b6f9faa899878ef9b67bd3ba2883eed0a3bd6f9a1c3a42d8f89fe849ac8e`）。
- `build_fold25.py` はfold24出版機からfold25機を生成し、置換アンカー・古い定数・pin件数（PINS=12・PIN256=51）・Python構文を検査する。
- 別実装の標準ライブラリPython監査器は**49/49 checks PASS**。座標変換と4×4行列式の24置換展開を使い、fold機械の幾何補助関数を流用せず、D4被覆・余剰行のwin16 footprint不属・親行incidence・cost・frontier差分を再導出した。
- 独立監査正本SHA-256: `7747afdc2f26bb6b6a8bd794f098dd6c41c73a7c3eadfcfdf8fb475d3930715c`（3個の独立Wすべてでbyte-identical）
- fold receipt正本SHA-256: `5780f3875ed13554c6f58f269cdb587b792e0c9f930aba11c551a89e17a1074d`

## 再現手順

Python 3.13以上を想定。入力再構成器は固定Git参照から必要ファイルを取得し、12個のGit blob pin・51個のSHA-256 pinと照合する。

```sh
python3 scripts/reconstruct_inputs.py /tmp/fold25-W
python3 scripts/build_fold25.py /tmp/fold25-W
FOLD25_W=/tmp/fold25-W python3 /tmp/fold25-W/fold_win8_root200003800200.py
python3 scripts/verify_fold25_independent.py /tmp/fold25-W /tmp/fold25-W/fold25/output/independent-audit.json
```

再構成元の固定参照は `reconstruct_inputs.py` の既定値（`60e5109efad…`）に記録されている。入力の取得先が変わっても、内容がpinと一致しなければ停止する。

## 限界

このreceiptが閉じるのは五親targetの2行（簿記上は余剰1行の併閉を含む3行）であり、その行の勝敗ではない。K1137のWIN8-D10証明書も当該8石rootに限られる。二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4、標準11×11空盤の弱解決は引き続き**UNKNOWN**。残余24行レーンの残るWIN8候補はK1139 root `0000000800000000380000000810000a`（mobility 58・主張1行・g19拡張済み）の1根のみで、fold26として着手には別の単一オーナー宣言を要する。
