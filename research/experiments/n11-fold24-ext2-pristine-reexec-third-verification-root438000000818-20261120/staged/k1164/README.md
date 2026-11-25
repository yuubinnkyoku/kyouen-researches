# fold24（K1140）外部第二検証: 別実装検証機による出版byte再確認（2026-11-20）

## 位置づけ

K1140のfold24 receipt fold（root `00000000000000043800000008180010`・残余29行のWIN8-D10 receipt fold）は、
出版社レーンが単一コミット `fc4c18fdddb4072667ad019d3218a066e313ff4e` で出版した時点で、
5回実行・生成器からの機械再生成byte一致・同梱独立監査（46/46 checks）までを確認ずみである。
本実験は、出版社以外の実行主体による**外部第二検証**として、
第三実装の検証機を新規に書き、出版byteだけからfold24 receiptの全数値を再導出して照合したものである。
単一オーナー宣言は[宣言ノート](../../log/2026-11-20-n11-fold24-external-second-verification-single-owner-note.md)（commit `434d53f3e3`）
に先に行っており、宣言時の受入条件7項目はすべて達成した。

検証機 `scripts/verify_fold24_external_20261120.py` は、出版機（`fold_win8_root438000000818.py`）とも
同梱独立監査機（`verify_fold24_independent.py`）とも実装を共有しない別実装である。
stdlibのみを使用し、D4座標変換・4×4 incidence行列の余因子展開・親行対応・frontier統計を
明示的な座標写像から再実装した。fail-closed設計で、出力はソート済みkey・時刻を持たない
決定論的な監査JSON 1点である。

## 固定pin

入力は2点だけである。出版byteはGitHubのpinned commitから再取得し、下記SHA-256を照合した。

- 出版receipt正本 `win8-root438000000818-receipt-fold-20261120.json`
  SHA-256 `c4ab76d3cb7eba5c1ab8e1830c43d17bf9a771f511b66e7e8573864f3f2402c7`
- 出版機 `fold_win8_root438000000818.py`
  SHA-256 `f462733dbaa6a958680ce49ff85e056adf8756cc946fa5ac612442f2c47b4fc8`
- 出版同梱独立監査正本 SHA-256 `49f330c6e0f73c0a58fdd9b21c215c38fc3a594d35f1d617b1324468c4a3387b`
- 出版再現log SHA-256 `cb01749a9b52e7ed4392dc2d25cf008e805b0ca17b40a25537680e9d1df0e5b2`
- 出版 `reconstruct_inputs.py` SHA-256 `f4e1fa8e69b10c07d9eec7f0b798458b0e73a97308bd418b622d1e9542873591`
- 同梱監査機本体 `verify_fold24_independent.py`
  SHA-256 `e0dbebe463a5f0f4e652779905658301d3b9e4b1506e80b581bce673d1f102aa`
- K1091掃引記録 SHA-256 `edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25`
- runner v17 git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`

もう一方の入力tree Wは、出版済み `reconstruct_inputs.py` を固定Git参照 `b91e85a99f0480f084835bdff51533d0cf5feaa8`
で実行して再構成した61入力pin（12 Git blob pin + 49 SHA-256 pin）である。
検証機はWの61 pin全件をfail-closedで再照合する。検証機自体の打鍵定数は
テンプレート（`verify_fold24_external_20261120.py.tpl`・プレースホルダ `__PINS__`/`__PIN256__`）に
pins.jsonの12/49定数を注入して生成し、生成後の検証機を出版的byteとして扱う。

## 実施内容と結果

検証機の実行で得た監査正本は `output/external-audit.json`
（36,605 bytes・SHA-256 `c7e10332df04a4f1e5af7b1cbc5ec487a5c15ca7851edba102b7b3679feb7c24`・gate 800）で、
statusはPASSである。主な内容は次のとおり。

- 出版pin照合（P系 5 gate）と入力pin（I系 65 gate: 12 Git blob + 49 SHA-256 + base 6,438行再構成）。
- 出版機のpristine再実行4回（X系 20 gate）: 同一環境2回、隔離tree/cwd/HOME 1回、
  隔離+`PYTHONHASHSEED=random` 1回。全実行のreceipt SHA-256が出版正本 `c4ab76d3…` と一致。
- 同梱独立監査機の再実行（V系 4 gate）: 出力46/46 checksが出版監査正本とbyte-identical。
- 別実装再導出（C系 545 gate）: base 6,438行→fold23 frontier 6,126行/485,438 costの再構成、
  C(8,6)=28部分幾何のD4正準行を2方法（C(8,2) 2石除去×8 D4像の完全合成28と部分集合のD4正準化28）で再導出、
  主張3行（closed cost 225）・余剰0行の再決定、親delta 4親class 2計6、
  frontier_after 1,725/6,123/485,213/4,431/351,661/11,660、五親target 86/112→残余26行。
  全fieldが出版receipt正本の該当fieldと一致。
- 解釈ガード（E系 155 gate）とtamper検査（T系 6 gate）: worklist `inputs/worklist.csv` offset 777と
  K1136証明書 offset 12345 の1 byte XOR 0x01改変2件が、いずれもreturncode 1・監査未書込でfail-closed捕捉。
  2つのoffsetは出版社検査済み位置とは別に本レーンが選んだ。

監査正本は3実行（同一cwd 2回＋隔離cwd/HOME＋`PYTHONHASHSEED=random` 1回）でbyte-identicalである。
出版準備時にもう1回既定環境で再実行し（実測49.5秒）、同一SHA-256を再確認した。
実行記録は `output/reproduction.log` に置いた。

追加の実験事実として、検証機初版のK1091掃引pin定数にSHA転写typo（`deda…`→正 `ded0…`）があり、
fail-closedのpin gateが実行前に捕捉した。修正後の検証機が本正本である。
第三検証系で先行するK1158・K1160と同じ防御パターンがここでも有効だったことを記録する。

## 再現手順

```
python3 reconstruct_inputs.py <W_dir>          # 固定Git参照から61入力pinを再構成
python3 verify_fold24_external_20261120.py <W_dir> <pub_dir> <out_json>
```

`<pub_dir>` はfold24出版実験dir（出版byte 5点と同梱監査機を含む）である。
検証機は単一プロセス・直列で約50秒（実測49.5秒・user 39.4秒）で終了し、
`<out_json>` が本README記載のSHA-256と一致すれば再現成立である。

## 限界

本検証はreceipt簿記・機械決定性・同梱監査・fail-closed入力の再検査であり、
S6行・五親target行を1行も閉じない。fold24 receipt自体が3行を閉じたのは出版社の成果簿記であり、
本検証はその外部確認である。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべて**UNKNOWN**のまま。
