# fold13（root 9840004）単体の外部第二検証 — 実行記録（2026-11-21）

study log: 宣言から出版まで。対象は fold13 receipt fold
（第20 receipt・3番目WIN8 receipt fold・root `00000000000000003800000009840004`・
出版実験 `research/experiments/n11-residual65-win8-receipt-fold-root9840004-20261120/`）の
外部第二検証（単体ext2）。

## 時系列

1. **宣言（先行出版）**: `research/log/2026-11-21-n11-fold13-external-second-verification-single-owner-note.md`
   （commit `5a9e8142942786ffe1b2afa2be228caea3d3d18f`・fetch-back byte一致）。
   宣言 2026-11-21T01:00:00Z想定・宣言時点HEAD想定 `928ae7834e`。
   受入条件6項目（出版byte pin再取得・W再構成・検証機による値単位再導出・
   pristine再実行4回・tamper fail-closed・監査正本3実行byte一致）を規定。
   直近30コミットでfold13単体ext2の先行宣言なしを確認済み。
2. **W入力再構成（api.github.com非依存）**: K1175レーンで確立した静的raw URL
   固定commit設計を直接適用。fold13 receipt正本 `c2bf8051…`（20,416 bytes）から
   `source_blob_pins` 12 Git blob SHA-1 + `source_sha256_pins` 16 SHA-256 = 28 pinを
   機械読み取りし、再構成機 `reconstruct_fold13_inputs.py`（`1b54624f…`）で
   全pin fail-closed照合・W13配置。fold11機pin表（12+10）⊂fold12機pin表（12+13）⊂
   fold13機pin表（12+16）の部分集合性を機械確認。quota枯渇条件下で待機ゼロ。
3. **第三実装検証機の実行**: `verify_fold13_external_20261121.py`（`aeda41e1…`・
   57,284 bytes・stdlibのみ・乱数・時刻なし）。
   **gate 774全PASS**（P 12 / I 44 / C 673 / X 29 / T 16）・1実行約29秒。
   X section: fold13出版機pristine再実行4回（同一W 2回・隔離copytree W/cwd/HOME・
   隔離+`PYTHONHASHSEED=random`）すべてreceipt `c2bf8051…` とbyte-identical。
   各回の機内fold11 rerun（`d7bf2cd5…`）・隔離W複写上のfold12 rerun（`0f73795c…`）も
   byte一致。V section: fold11・fold12出版機を検証機側から隔離W複写上で独立実行し
   `d7bf2cd5…`/`0f73795c…` を再現（受入条件3の外側確認）。
   T section: tamper 2件（worklist @117,777 blob mismatch・K1108証明書 @777,777
   sha256 mismatch・1 byte XOR 0x01）がrc≠0・fold13/fold11出力とも未書込・WT内
   pinned fold12 record無改変でfail-closed捕捉。
4. **監査正本の決定性**: `output/external-audit.json`（81,632 bytes・SHA-256
   `4fe40fa254b4d2658bb0fadbc47dadb43c3d85214be8a9517b525693b416be81`）が
   同一cwd 2回＋隔離cwd/HOME+`env -i`+`PYTHONHASHSEED=random` 1回の3実行で
   byte-identical（cmp照合）。
5. **part1出版（3分割push・fetch-back 5/5 byte一致）**:
   - part1a commit `f2fe7d58e9`: 実験dir `research/experiments/n11-fold13-external-second-verification-root9840004-20261121/`
     の README.md（`ca7ead2b…`）・`scripts/reconstruct_fold13_inputs.py`（`1b54624f…`）・
     `output/reproduction.log`（`224272ee…`）
   - part1b commit `dffc4af0c1`: `scripts/verify_fold13_external_20261121.py`（`aeda41e1…`）
   - part1c commit `51d86169c1`: `output/external-audit.json`（`4fe40fa2…`）
6. **part2（本log・knowledge item K1176）**: part1と別commit。

## 受入条件対照（宣言6項目）

1. **出版byte pin再取得**: OK。pinned commitからfold13 receipt正本（`c2bf8051…`）・
   fold13機（`5c27f1ae…`・42,315 bytes）・出版README（`ca7ead2b…`）・fold12 receipt
   （`0f73795c…`）・fold12機（`706bfa7a…`）・fold11 receipt（`d7bf2cd5…`）・fold11機
   （`9b3e06c8…`）・K1108監査（`2e453a76…`）・K1108証明書（`5b114b9e…`・1,640,220 bytes）・
   K1097 refsolve（`2896deb0…`）を取得し全SHA-256照合。W pin 28件はreceiptから
   機械読み取りで確定し再照合。
2. **W再構成機**: OK。`reconstruct_fold13_inputs.py`（静的raw URL固定commitのみ・
   api.github.com非依存・全byte digest照合・fail-closed）。
   fold11/fold12機の配置SHA照合・両機pin表のfold13機pin表に対する部分集合性機械確認込み。
3. **pristine再実行4回**: OK。全回receipt出力SHA-256が出版正本とbyte-identical。
   加えてfold12出版機を隔離W複写上で独立再実行し `0f73795c…` byte一致（外側確認）。
4. **別実装検証機での値単位再導出**: OK（774 gate）。
   - base 6,438行（cost 509,109）→fold12適用後 6,193/490,526・solved 1,655・
     incidence 11,790・残余65・五親target 47/112までの9出版記録連鎖
     （fold4/fold56/fold7/fold8/fold9〔9th-12th〕/fs13〔13th-16th〕/fold10/fold11/fold12）
     を段ごとに再計算しpublished値照合。
   - root 8石・quadruple-free・D4正準・合法手57をsurvival-move規約再実装で独立再導出。
     C(8,6)=28 canonical行を2方法（8 D4像×C(8,2)=224操作 vs 28部分集合正準化）で
     再導出し分類 open 9/not-in-worklist 19。
   - coverage 9行（K1108 g07主張3行＋余剰6行）・closed edge cost 713・影響5親
     （c4×3: 87→84/90→87/75→72・c2×2: 61→58/16→13・各3行closing・完全閉鎖0・
     合計15 row-closings）・frontier_after 6,184/489,813・solved 1,664・
     incidence 11,775・needed 4,492/356,261・五親target 47→50・残余65→62（hex全列挙照合）・
     win16候補 14→13根（主張42→39行・残余23行不交差）を出版receipt正本の全該当field
     （controls boolean・独立検証ブロック・解釈ガード5文を含む）と値単位一致で確認。
   - K1108 19 gate主要値（g06 probes 1,143,198/1,528,656・g13 nodes 4,109,768/3,075,922・
     g05 mobility 57・証明書byte 1,640,220/行数45,286 sorted unique・third_method
     terminal 17,333/visited 103,531/winner 66,627/loser 19,571/応手辺 91,337・
     terminalRange [14,18]）とK1097 27 gate・root 9840004行の intrinsic==claimed==3行・
     49行exactly-once partition・残余23行不交差を再照合。
5. **tamper**: OK。2件ともfail-closed（rc≠0・出力未書込・WT内pinned record無改変）。
6. **監査正本3実行byte一致**: OK。`4fe40fa2…`（81,632 bytes・774 gate・all_gates_pass true・
   時刻/絶対path/volatile排除の決定論的設計）。

## 実験事実

1. K1175レーンの静的raw URL再構成機設計（api.github.com非依存）の直接適用により、
   W13再構成はquota待機ゼロで完了。同設計がfold14〜16の単体ext2にもそのまま
   使えることを再実証した。
2. fold12 erratumパターン（receipt `independent_verification.source_record` の
   ステール参照）がfold13 receiptには存在しないことを確認し、監査JSONの
   observations欄にfold12側erratumとの対照として記録した。fold12 receiptのbyteは
   一切変更していない。
3. K1175検証機（655 gate）からの外科手術で、チェーン再構成をfold12レコードまでの
   9段に拡張し、coverage照合を余剰6行込みの9行に、5親影響gateをc4×3/c2×2・
   15 row-closingsに、レシート定数群（合法手57・証明書45,286行）を差し替えた。
4. tamper offset（@117,777/@777,777）はfold12 ext2レーンのもの（@96,300/@456,789）と
   独立に選んだ。いずれも出版社が未試験の位置である。

## 解釈規約

本検証は検証の検証（簿記・決定性・入力pin・fail-closed防衛の再検査）であり、
行は1行も閉じない（fold13時点残余65→62行は当該receiptの既出版簿記・pool 120,416根は不変）。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数・coverage数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべて
UNKNOWNのままである。**
