# fold22（K1132）外部第二検証: 別実装検証機による出版byte再確認（2026-11-20）

## 位置づけ

K1132のfold22 receipt fold（root `00000000000000801202000000840500`・残余35行→32行のWIN8-D10 receipt fold）は、
Publisherレーンが単一コミット `ac7b8be685a720915515fba04ceb61d7d1e505ab` で出版した時点で、
3回実行・fold21出版機のpristine rerun gate・チェーン全段frontier再計算・K1125 19 gate全再検証までを確認ずみである。
fold24以降と異なりfold22の実験dirには出版社同梱の独立監査機（`verify_foldN_independent.py`）がなく、
fold23・fold24外部第二検証でfold22正本がチェーン入力として間接照合に使われてはいたが、
fold22 receipt自身の主張（open 6行閉鎖・closed edge cost 484・残余35→32・親delta・28 canonical行分類・
win16候補 5→4根）の値単位の独立確認はまだなかった。
本実験は、単一オーナー宣言
（[宣言ノート](../../log/2026-11-20-n11-fold22-external-second-verification-single-owner-note.md)・commit `01c0855fd935b1951d686294efbb9305a3e4f4d8`・
2026-11-20T20:46:23Z・受入条件6項目）の下で実施した**外部第二検証**である。
検証機 `scripts/verify_fold22_external_20261120.py` は、出版機（`fold_win8_root840500.py`）とも
fold21以下の出版チェーン機とも実装を共有しない第三実装である。stdlibのみを使用し、
D4座標変換（8変換の明示的座標写像）・4×4共円行列の余因子展開det4・survival-move規約に基づく
合法手再実装（任意の石3点組と共円/共線(det4==0)になる空点をblockedとする）・census親対応・
frontier統計・五親target連鎖をすべて書き下ろした。fail-closed設計で、
出力はソート済みkey・時刻を含まない決定論的な監査JSON 1点である（失敗時は監査未書込でexit 1）。

## 固定pin

出版byteはGitHubのpinned commitから再取得し（宣言時HEAD `9a1c7a98f39103013a0221f4f63fc10eba6a9061`
と検証確定時最新main `34c29854c64286bbb1792ff28dc1973aef341e20` の両方でbyte一致を確認）、
下記SHA-256を照合した。

- 出版receipt正本 `win8-root840500-receipt-fold-20261120.json`
  SHA-256 `f6e011f4a16e6fe257694c3cd3ed90490623f84e1c24113c3f55df68ba3e3488`（25,349 bytes・出版単一コミット `ac7b8be6`）
- 出版機 `fold_win8_root840500.py`
  SHA-256 `d5721408e7fb41e794175f3f3bb8b9d43fae13d18c244a831b81532aa9f1db1d`
- 出版生成機 `build_fold22.py`
  SHA-256 `a73995be2ac448f2e56f804b3263330513c5bcb8a9e4042661c56e1deb4d7085`
- 出版README SHA-256 `0e6861bf2970bead67ce77de9361e11a435cb27ee668e066a565a6fe808c29da`
- fold21 receipt正本 SHA-256 `9a4da2f61fb5010ebfbddf784cd76f5972b438c244fa29c1f96f2c3cde65cb39`
  （fold22機のpristine rerun gateの対象）
- fold21 出版機 SHA-256 `44399cc59ef088ad25e90411f4404dbd0bad8ff14bc7c8a50be1a91bcc04102b`
- K1125証明書本体 SHA-256 `21ad61959f6b2ae13e2e24fd98842788c88ada50643ccfd1f88a459701d0cbcc`
  （1,067,425 bytes・29,468行）
- K1125監査正本 SHA-256 `06c65f7611b7fea17131d5e13b28792aee1b7d723e7b8cdb1cb3b54012282886`

もう一方の入力tree Wは、本実験dir同梱の `scripts/reconstruct_inputs.py`
（SHA-256 `dfa50996463fe31000e2bc3b03e37dabe33981bf00708a29ae7634d4a6594a27`・固定Git参照引数つき）で
再構成する。fold22機の入力pin 55点（12 Git blob pin + 43 SHA-256 pin）をfail-closedで再照合し、
rerun gate用にfold21出版機・fold18/19/20出版機・fold18 preverified写しをSHA照合つきで配置する
（`fold21のchain入力（12 blob + 40 SHA-256）がfold22機の55 pinの部分集合である`ことを検証機が機械確認する）。

## 実施内容と結果

監査正本は `output/external-audit.json`
（141,752 bytes・SHA-256 `b4b082f8cb0aa943aad7458ae0c6eb179a27704c5ea781eb18907d869c97522c`・gate 1,463）で、
`all_gates_pass` は true である。gate内訳は P系 13（出版pin）・I系 63（W 55 pin + pin鎖整合）・
C系 1,358（別実装再導出）・X系 15（pristine再実行）・T系 14（tamper fail-closed）。
主な内容は次のとおり。

- **出版pin照合・W再構成（P/I系）**: 上記7正本 + 実験dir 4ファイルのSHA-256照合、
  W 55 pin全件再照合、fold21機pin表とのblob/SHA両面での部分集合確認。
- **pristine再実行4回（X系）**: 出版fold22機を `FOLD_PREVERIFIED_CHAIN` 不使用で実行。
  同一cwd 2回・隔離tree/cwd/HOME 1回・隔離+`PYTHONHASHSEED=random` 1回の全4回が
  returncode 0・receipt出力SHA-256出版正本 `f6e011f4…` とbyte-identical
  （各回はfold21出版機のpristine rerun gateとその内部のfold20→fold19→fold18系推移的再検証込み・
  1回あたり実測約7.9秒）。tamper 2件を含めると1検証機実行でfold22機6回起動。
- **別実装再導出（C系 1,358）**: base worklist 6,438行（総cost 509,109）→ledger/globalFold→
  previousCostFold→firstFold tarball→secondThird→fold4→fold56→fold7/8→ninth-twelfth→
  windfall4(thirteenth-sixteenth)→fold10..fold21に至る全frontier連鎖（globalFold base再構成＋21記録適用段）を独立再計算し、
  fold21適用後open frontier 6,136行/486,243 cost・solved 1,712・incidence 11,683・
  残余35行・五親target 77/112行を再構成（`fold9 frontier_after solved 1635`等の各段published値と全一致）。
  K1125のroot `00000000000000801202000000840500` は石8・四つ組共円/共線0・D4正準を独立確認し、
  合法手58をsurvival-move規約の再実装で再導出。C(8,6)=28部分幾何のD4正準行を2方法
  （(A) 8 D4像×C(8,2) 2石除去224操作の完全合成と (B) C(8,6)=28部分集合のD4正準化）で再導出して
  集合として一致（D4同変性の実測確認）、28 canonical行の分類 open-frontier 6/not-in-worklist 22/
  closed-before 0を再決定。閉鎖6行のうち五親target内主張3行（K1089 claimed == K1097 footprint
  `intrinsic == claimed`・exactly-once 49行分割の一部）と余剰3行への分割、closed edge cost 484、
  4親delta（すべてclass 2・14→11・51→48・47→44・69→66・計12）、
  frontier_after 6,130/485,759・solved 1,718・incidence 11,671・s6_needed 4,438・cost_needed 352,207、
  五親target 77→80行・残余35→32行・win16候補 5→4根（主張12→9行）を再計算し、
  出版receipt正本の全該当field（coverage行単位のcost/demand/parents・controls 70 boolean・
  独立検証ブロック・解釈ガード5文を含む）と値単位で一致。K1125監査19 gateの主要値
  （uncapped probes 736,409/878,391・third-method 58/9,810/[14,18]/59,990/38,458/11,722/52,360・
  証明書1,067,425 bytes・29,468行sort -u・header行）とK1097 refsolve footprint 16根49行も再照合。
- **tamper 2件（T系）**: 本レーンが選んだ出版社未試験offset
  `inputs/worklist.csv` byte offset 1099 とK1125証明書 byte offset 21212 の1 byte XOR 0x01改変を
  Wの隔離複写上で実施し、それぞれ `input blob mismatch`・`input sha256 mismatch`・
  returncode≠0・出力未書込（rerun gate到達前の入力pin段でのfail-closed）を確認。
  隔離複写のため本番Wは無改変（事後にblob/SHA再照合）。

監査正本は3実行（同一cwd 2回＋隔離HOME・別cwd・`PYTHONHASHSEED=random` 1回）でbyte-identical、
さらに宣言時HEAD `9a1c7a98…` と最新main `34c29854…` の2つのpinned refから独立再構成したW双方で
同一SHA-256 `b4b082f8…` を確認した（最終版検証機で計4実行byte一致・W/pubは2参照間で全ファイルdiff一致）。
検証機1実行は実測約34.4秒
（user約28.5秒・fold22機6回起動込み）。実行記録は `output/reproduction.log` に置いた。

### 実験事実

- 検証機初版のfold14/fold15/fold19のcovered_n打鍵定数に、要約経由で転写した誤り
  （3/2/9 → 実レコードは5/6/5）があり、検証機自身のfail-closed gate
  （receipt記録のcovered行数・frontier solved増分の再計算照合）が実行1回目で即捕捉した。
  修正版が本正本である。K1158・K1160・K1164のpin転写typo捕捉と同じ防御パターンが
  「要約転写された定数」に対しても有効であることを記録する。
- fold22 receiptの `win_candidate_plan_impact.note` の列挙文はfold18 retired root
  （`00000000000000801202000000901010`・3主張行）を本文列挙から落としているが、
  同noteの数列 `49-4-3-3-4-3-4-3-3-4-3-3-3 = 9` はfold18 retireを含む12 retire計40行を
  正しく加算している。本検証の再導出（fold11..fold21 retired 11根 + 本receipt 1根、
  K1097 footprint 16根49行exactly-once・残り4根9行）はreceiptの数値主張と完全一致し、
  「列挙漏れは表現上の省略で数値に影響しない」ことを機械確認した。

## 再現手順

```
python3 scripts/reconstruct_inputs.py <W_dir> <pub_dir> [<git_ref>]
python3 scripts/verify_fold22_external_20261120.py <W_dir> <pub_dir> <out_json>
```

`<pub_dir>` はfold22出版実験dir（出版byte 4ファイル）。`reconstruct_inputs.py` のデフォルト
Git参照は `34c29854c64286bbb1792ff28dc1973aef341e20`（宣言時HEAD `9a1c7a98…` でもbyte一致済み）。
検証機は単一プロセス・直列で約35秒（実測34.4秒・user 28.5秒）で終了し、
`<out_json>` が本README記載のSHA-256 `b4b082f8…`（141,752 bytes・gate 1,463）と一致すれば再現成立である。

## 限界

本検証はreceipt簿記・機械決定性・入力pin・fail-closed防衛の再検査であり、
S6行・五親target行を1行も閉じない。fold22 receipt自体が6行（主張3+余剰3）を閉じたのは
Publisherの成果簿記であり、本検証はその外部確認である。WIN8-D10証明書は当該8石rootの
ゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべてUNKNOWNのまま。**
