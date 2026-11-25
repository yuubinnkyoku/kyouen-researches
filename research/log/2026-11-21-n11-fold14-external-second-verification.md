# fold14（root 9090022）単体の外部第二検証 — 実行記録（2026-11-21）

study log: 宣言から出版まで。対象は fold14 receipt fold
（第21 receipt・4番目WIN8 receipt fold・root `00000000000000909002200080100000`・
出版実験 `research/experiments/n11-residual62-win8-receipt-fold-root9090022-20261120/`）の
外部第二検証（単体ext2）。

## 時系列

1. **宣言（先行出版）**: `research/log/2026-11-21-n11-fold14-external-second-verification-single-owner-note.md`
   （commit `2a6f14de952738a5b3177ef4a3468f0cf1cd33ab`・fetch-back byte一致）。
   受入条件6項目（出版byte pin再取得・W再構成・検証機による値単位再導出・
   pristine再実行4回・tamper fail-closed・監査正本3実行byte一致）を規定。
   直近コミット列でfold14単体ext2の先行宣言なしを確認済み
   （fold13宣言ノートの「fold14-16は各レーン個別宣言」記載どおり最初の宣言）。
2. **W入力再構成（api.github.com非依存）**: K1175/K1176レーンで確立した静的raw URL
   固定commit設計を直接適用。fold14 receipt正本 `ed3159fd…`（19,295 bytes）から
   `source_blob_pins` 12 Git blob SHA-1 + `source_sha256_pins` 19 SHA-256 = 31 pinを
   機械読み取りし、再構成機 `reconstruct_fold14_inputs.py`（`62a72b36…`）で
   全pin fail-closed照合・W14配置。HEAD pin `2a6f14de95`。
   fold11機pin表（12+10）⊂fold12機pin表（12+13）⊂fold13機pin表（12+16）⊂
   fold14機pin表（12+19）の部分集合性を機械確認。quota枯渇条件下で待機ゼロ。
3. **第三実装検証機の実行**: `verify_fold14_external_20261121.py`（`d966dad5…`・
   58,352 bytes・stdlibのみ・乱数・時刻なし・K1176検証機を土台にfold14固有の
   外科手術と定数差替で構成）。
   **gate 880全PASS**（P 12 / I 54 / C 772 / X 26 / T 16）・1実行約53秒。
   fold14出版機単体pristine runは約11.4秒（機内fold11 rerun・隔離W複写上の
   fold12/fold13 rerun gate込み）。
   X section: fold14出版機pristine再実行4回（同一W 2回・隔離copytree W/cwd/HOME・
   隔離+`PYTHONHASHSEED=random`）すべてreceipt `ed3159fd…` とbyte-identical。
   各回の機内fold11 rerun（`d7bf2cd5…`）もbyte一致。V section: fold13出版機を
   検証機側から隔離W複写上で独立実行し `c2bf8051…` を再現・機内fold11 rerun
   `d7bf2cd5…` byte一致（受入条件3の外側確認）。
   T section: tamper 2件（worklist @200,222 blob mismatch・K1109証明書 @888,222
   sha256 mismatch・1 byte XOR 0x01）がrc≠0・fold14/fold11 rerun出力とも未書込・
   WT内pinned fold13 record無改変でfail-closed捕捉。
4. **監査正本の決定性**: `output/external-audit.json`（91,543 bytes・SHA-256
   `fe6370f7e9cd30eaca7cc0ce3a61d39e9a6dd1eb47c8ba4f300e680f5d55b102`）が
   同一cwd 2回＋隔離cwd/HOME+`env -i`+`PYTHONHASHSEED=random` 1回の3実行で
   byte-identical（cmp照合）。
5. **part1出版（単一push・fetch-back 5/5 byte一致）**:
   commit `23de00dc7ad8d49747c9de9cc021fd35e542f77c`: 実験dir
   `research/experiments/n11-fold14-external-second-verification-root9090022-20261121/`
   の README.md（`0d3b4e06…`）・`scripts/reconstruct_fold14_inputs.py`（`62a72b36…`）・
   `scripts/verify_fold14_external_20261121.py`（`d966dad5…`）・
   `output/external-audit.json`（`fe6370f7…`）・`output/reproduction.log`（`5d28aa0e…`）。
   push前に各ファイルのUTF-16 code unit単位FNV-1a照合（fail-closed）を実施、
   fetch-back後cmpでbyte一致確認。
6. **part2（本log・knowledge item K1178）**: part1と別commit。

## 受入条件対照（宣言6項目）

1. **出版byte pin再取得**: OK。pinned commitからfold14 receipt正本（`ed3159fd…`）・
   fold14機（`7b88a565…`・46,844 bytes）・出版README（`25f9f08b…`）・fold13 receipt
   （`c2bf8051…`）・fold13機（`5c27f1ae…`）・fold12 receipt（`0f73795c…`）・
   fold12機（`706bfa7a…`）・fold11 receipt（`d7bf2cd5…`）・fold11機（`9b3e06c8…`）・
   K1109監査（`00836a6e…`）・K1109証明書（`b8a15f9a…`・1,082,873 bytes）・
   K1097 refsolve（`2896deb0…`）を取得し全SHA-256照合。W pin 31件はreceiptから
   機械読み取りで確定し再照合。
2. **W再構成機**: OK。`reconstruct_fold14_inputs.py`（静的raw URL固定commitのみ・
   api.github.com非依存・全byte digest照合・fail-closed）。
   fold11/fold12/fold13機の配置SHA照合・3機pin表のfold14機pin表に対する
   部分集合性機械確認込み（F11⊂F12⊂F13⊂fold14の鎖）。
3. **pristine再実行4回**: OK。全回receipt出力SHA-256が出版正本とbyte-identical。
   加えてfold13出版機を隔離W複写上で独立再実行し `c2bf8051…` byte一致・
   機内fold11 rerun `d7bf2cd5…` byte一致（外側確認）。
4. **別実装検証機での値単位再導出**: OK（880 gate）。
   - base 6,438行（cost 509,109）→fold13適用後 6,184/489,813・solved 1,664・
     incidence 11,775・残余62・五親target 50/112までの10出版記録連鎖
     （fold4/fold56/fold7/fold8/fold9〔9th-12th〕/fs13〔13th-16th〕/fold10/fold11/
     fold12/fold13）を段ごとに再計算しpublished値照合。
   - root 8石・quadruple-free・D4正準・合法手50をsurvival-move規約再実装で独立再導出。
     C(8,6)=28 canonical行を2方法（8 D4像×C(8,2)=224操作 vs 28部分集合正準化）で
     再導出し分類 open-frontier 5/not-in-worklist 22/closed-before-this-receipt 1
     （`00000000000000003800000008003000`・fold13 receipt閉鎖行・二重閉鎖回避を機械確認）。
   - coverage 5行（K1109 g07主張4行＋余剰1行 `00000000000000889002400000000000`）・
     closed edge cost 373・影響4親（全c2: 22→20/23→21/67→64/63→60・
     合計10 row-closings・完全閉鎖0）・frontier_after 6,179/489,440・solved 1,669・
     incidence 11,765・needed 4,487/355,888・五親target 50→54・残余62→58
     （hex全列挙照合）・win16候補 13→12根（主張39→35行・retired 4根合計14行・
     残余23行不交差）を出版receipt正本の全該当field（controls boolean 29件・
     独立検証ブロック・解釈ガード5文を含む）と値単位一致で確認。
   - K1109 19 gate主要値（g06 probes 512,590/614,246・g13 nodes 6,102,650/6,102,650・
     g05 mobility 50〔gate名 g05_root_mobility_50〕・g07 gate名
     g07_k1086_root_claimed_coverage_4rows・証明書byte 1,082,873/行数29,942
     sorted unique・third_method terminal 10,239/visited 65,134/winner 42,115/
     loser 12,780/応手辺 58,084・terminalRange [14,18]・subroot mobility 50）と
     K1097 27 gate・root 9090022行の intrinsic==claimed==4行・
     49行exactly-once partition・残余23行不交差を再照合。
5. **tamper**: OK。2件ともfail-closed（rc≠0・出力未書込・WT内pinned record無改変）。
6. **監査正本3実行byte一致**: OK。`fe6370f7…`（91,543 bytes・880 gate・all_gates_pass
   true・時刻/絶対path/volatile排除の決定論的設計）。

## 実験事実

1. fold14は主張4行のWIN8候補として初のfoldであり、28 canonical行分類で
   closed-before-this-receipt行を初めて1行含むrootである（fold13 receiptが閉じた
   `00000000000000003800000008003000`）。同を行が本receiptのcoverage 5行に
   含まれないことを分類・coverage双方のgateで機械確認した（二重閉鎖回避）。
   K1109実験dir名の「residual65」は証明書抽出実験のseries名としてintentional
   （root 9090022抽出時点のfrontier残余65に由来）であり、fold14実験dirの
   「residual62」とは系列が異なる。
2. fold13 erratum対照の清潔パターンがfold14 receiptでも継続:
   `independent_verification.source_record` はK1109実験
   （`n11-residual65-win8-cert-extract-root9090022-20261120`）を正しく指す。
   この対照を監査JSONのobservations欄に記録した（文書フィールドの検査であり、
   receiptのbyteは変更していない）。
3. K1176検証機（774 gate）からの外科手術で、チェーン再構成をfold13レコードまでの
   10段に拡張し、coverage照合を主張4＋余剰1の計5行に、4親影響gateを全c2・
   10 row-closingsに、K1109 19 gate値・レシート定数群（合法手50・証明書29,942行・
   controls 29）を差し替えた。fold13機pin表（12+16）のfold14機pin表（12+19）への
   部分集合性を検証機I sectionでも再確認した。
4. tamper offset（@200,222/@888,222）はfold13 ext2レーンのもの（@117,777/@777,777）と
   独立に選んだ。いずれも出版社が未試験の位置である（K1109証明書は
   1,082,873 bytes内のoffset）。

## 解釈規約

本検証は検証の検証（簿記・決定性・入力pin・fail-closed防衛の再検査）であり、
行は1行も閉じない（fold14時点残余62→58行は当該receiptの既出版簿記・pool 120,416根は不変）。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数・coverage数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべて
UNKNOWNのままである。**
