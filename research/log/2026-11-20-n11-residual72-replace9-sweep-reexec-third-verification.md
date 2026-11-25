# 残余72行 代替9根掃引再実行第二検証（K1149）pristine再実行第三検証（2026-11-20）

## 経緯

1. **最新main確認**: K1149（残余72行 代替9根掃引18 probe再実行第二検証・出版 commit `7ab77aa1`・検証機 `77cdd9e3…`・出版監査 `27fc420c…` 11,242 bytes・24/24 gate・item側の二重採番〔six-row K1149〕には関与しない）の第三検証が未着手だったため本レーンが宣言して着手。K1157（K1156第四幾何の第三検証）は前段で出版完了済み（part3 commit `87f56932`・fetch-back cmp一致）。
2. **単一オーナー宣言**: commit `c3c4dd28b48ccf4f5782ddb9f1a81e46d24e4787`（2026-11-20T16:01:30Z 宣言時刻）で宣言ノートを先行出版。
3. **採番の紆余曲折**。当初は仮番号K1158で進めていたところ、並走のK1147外部第二検証レーンが宣言 `887e594d`（15:21:00Z）の下、16:06:42Zにcommit `3298cc3ae7`（K1158 item+log part2）を出版してK1158を取得した。AGENTS.md後着優先規則により本レーンはK1159へ再採番し、実験READMEのK番号参照をK1159に修正した（`K1158` の混入なしを確認済み）。push直前3点確認（knowledge README grep `items/K1159-` 0件・item path 404・list_commits 0件）でK1159の空きを確認。
4. **staging**: K1149の入力一式（検証機・runner v17固定コピー〔git blob `c132cc64…`〕・出版掃引機・出版volume・出版probe-records・上流6正本 K1085/K1086/K1089/K1091/K1095/K1097・出版監査）をpinned commit `87f56932` のraw CDNで取得して本実験dir自体をstaging rootとし、`--root .` で再現可能な自己完結dir 17ファイルを構成した。
5. **harness**: `verify_k1149_reexec_third_20261120.py`（SHA-256 `ec55f78a…`・18,525 bytes・Python stdlib+Node.js runner・fail-closed）をK1153/K1155/K1157系譜で作成。pin 13点の独立pin（検証機内部fail-closed pinと二重）→ pass A新規再実行（本tree・4 workers）→ pass B新規再実行（隔離tree/cwd/HOME・入力複写）→ 出版掃引機pristine再assemble → 検証機assemble（fresh両パス＋pristine volume）→ `PYTHONHASHSEED=random` assemble → tamper gateの順に実行し、監査JSONはsorted keys・時刻/wall時間なし。
6. **全gate PASS**: pass A 18/18 probe完走・nodes総計 3,574,172 == 出版値・12.8秒。pass Bも18/18同一（約12.9秒）。pristine再assembleは出版正本 `e8f5d674…` とbyte-identical。assembleは出版監査 `27fc420c…` とbyte-identical（24/24 gate）で、`PYTHONHASHSEED=random` でもbyte-identical。tamper（`input/k1097.json` offset 500 XOR 0x01・改変後 `7cc71c5f…`）は returncode 1・records未書込でfail-closed捕捉。harness監査正本 `7e0824cc…` 7,700 bytesは同一cwd 2回+隔離cwd/隔離HOME 1回の3実行byte-identical（harness全体1回約25.4秒）。
7. **part1出版・fetch-back**: 実験dir 17ファイルをcommit `76ef33b2cf84a6fc5b837784ea1a80c987820962`（16:11:16Z）で出版し、同commitのraw CDNから再取得して17ファイル全てcmp byte一致（17/17）を確認。当初のpart1 pushの呼び出し結果は実行環境の中断で受け取れなかったため、再開時にlist_commitsで着地有無を確認してから再pushした（pushは1回のみ着地・二重出版なし）。
8. **part2・part3**: item（frontmatterはtitle・aliases全値を引用符化しknowledge integrity censusのクラスA障害〔plain scalar内のASCII ": "〕を予防）と本研究ログを出版し、続けてknowledge README末尾bulletを最新HEADから再取得して追記する。

## 解釈規約

loss=true（uncapped）はdepth-10内必敗のprobe事実の再現であり、証明書抽出の資格を本検証は与えない（抽出は宣言 `63877ffd2e` の別レーン管轄）。loss=false（uncapped）はREFUTED-D10 probe事実の再現でありLOSS証明ではない。nodes数・solved数を勝敗として読まない。WIN8-D10 candidateは証明書ではない。本検証は残余行を1行も閉じない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。** 残余20行（pool P⁗ 120,416根）は全行open。

## 引継ぎ

- 次回は着手前に最新main再取得。fold26（`23bffdd4e4`）・refsolve第5ラウンド（`ace38772d9`）・WIN8-D10証明書抽出（root `00000000010000809002000040002001`・`63877ffd2e`）はいずれも他レーン宣言済みのため着手禁止で、着地したら正本の第二検証（要単一オーナー宣言）が最優先。
- K1147レーンのK1158（8根被覆判定の第三検証・散在5実験dir入力のstage再構成とbasename依存性の発見）との相互整合確認は未実施で候補。
- 同系譜第三検証で未着手の対象は、K1149以降に新規出版された各検証実験（着地の都度READMEと採番を確認してから）。
- 器材 `/home/user/work/kv1149/`（harness・staging R/・監査out/）と `/home/user/work/k1159/`（part2原稿）は環境リセットで消失可・全成果はrepo出版済み。


## 追加監査・訂正（2026-11-21）

K1159 part1/part2の説明にある「K1149検証機内部pinとの二重照合」という表現は、K1146掃引機本体については正確でなかったため訂正する。K1149第二検証機 `verify_replace9_reexec_20261120.py` の `SWEEP_MACHINE_SHA256` は63文字 `d163b2a120ac46abee40d0b9a32269bce14a73901a85a80e595b7d2512bcd41` で、AST上の読み出しはline 886の監査metadataのみ、`gate(...)` からの参照は0件。公開監査の同項目も同じ63文字である。K1149のpristine gateは再assemble出力とvolumeのSHAを比較するだけで、機械ソース自体はpinしていない。なお `SWEEP_RECORDS_SHA256` は検証機内部で照合されている。

K1159第三検証harnessはK1146公開commit `e9ea153bc469aa551689a5d275773553852f3342` の機械本体を正しい64文字SHA `d163b2a120ac46abee40d0b9a32269bce14a73901a85a80e5925b7d2512bcd41` で独立pinし、pristine再assembleを出版volumeとbyte一致させている。したがって出所確認の不足はK1159側で補われており、18 probe×2パスの再実行結果や24/24監査再現を無効にするものではない。

追加監査器 `audit_k1149_machine_pin_gap_20261121.py` は8/8 gate、監査正本 `k1149-machine-pin-gap-audit-20261121.json`（SHA `b491e45092befcd490633cfa0e822c7063ef04eea14e078307221be84b9c38a6`）は同一tree 2回＋隔離tree 1回でbyte-identical。K1159第三検証harness自体も再取得後3回実行し、監査SHA `7e0824cc11c997882d6b01f528b0ac53205de3ce95891c901bf9da6eb29b7e43` と3回ともbyte一致した。

この訂正は証明書抽出・receipt fold・行閉鎖を追加しない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWN。**
