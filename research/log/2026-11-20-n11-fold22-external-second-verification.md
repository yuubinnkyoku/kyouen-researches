# fold22 receipt fold（K1132）の外部第二検証: 実行記録（2026-11-20）

## 経緯

- **宣言（2026-11-20T20:46:23Z）**: fold22外部第二検証の単一オーナー宣言ノートを
  [単一オーナー宣言ノート](2026-11-20-n11-fold22-external-second-verification-single-owner-note.md)
  （commit `01c0855fd935b1951d686294efbb9305a3e4f4d8`）として先に出版した。宣言時点のmain HEADは
  `9a1c7a98f39103013a0221f4f63fc10eba6a9061` で、fold22単体の外部第二検証の先行宣言なし
  （fold23宣言ノート `90ac8eed` が「fold22単体は別途宣言する」と予告していたが、
  その時点ではfold22単体の宣言は存在せず、first-published-priorityにより本レーンが取得）。
  受入条件は6項目を定めた（出版byte pin照合・W再構成55 pin・pristine再実行4回・
  別実装による全統計再導出・tamper 2件fail-closed・監査正本3実行byte-identical）。
- **出版byte pin照合**: fold22出版実験dir（単一コミット `ac7b8be685a720915515fba04ceb61d7d1e505ab`）の
  receipt `f6e011f4…`・出版機 `d5721408…`・生成機 `a73995be…`・README `0e6861bf…` の4点と、
  上流のfold21正本 `9a4da2f6…`・fold21機 `44399cc5…`・K1125証明書 `21ad6195…`・K1125監査 `06c65f76…` を
  GitHubのpinned commitから取得してSHA-256照合した。
- **W再構成**: 本レーン定義の `reconstruct_inputs.py`（SHA-256 `dfa50996…`）を宣言時HEAD `9a1c7a98…` で
  実行し、fold22機の入力55 pin（12 Git blob pin + 43 SHA-256 pin）をfail-closed再照合、
  rerun gate用にfold21出版機・fold18/19/20出版機・fold18 preverified写しをSHA照合つきで配置した
  （fold21 chain入力の55 pin部分集合性は検証機側で機械確認）。
- **手動確認段階**: 出版機をpristine実行（`FOLD_PREVERIFIED_CHAIN` 不使用・実測7.9秒）し、
  receipt出力が出版正本 `f6e011f4…` とbyte一致することを最初に確認した。
- **検証機執筆**: 上記を一括する第三実装の外部検証機 `verify_fold22_external_20261120.py`
  （SHA-256 `ca11cbbc…`・48,949 bytes・stdlibのみ）を執筆した。D4座標変換（明示的8写像）・
  det4余因子展開・survival-move規約の合法手再実装（石3点組と共円/共線の空点をblockedとする）・
  親対応・frontier統計・五親target連鎖・win16 footprint再照合を出版機と実装を共有せずに書き下ろした。
- **covered_n転写誤りの捕捉**: 検証機初版のfold14/fold15/fold19 covered_n打鍵定数に要約経由の転写誤り
  （3/2/9）があり、実行1回目で検証機自身のfail-closed gate（covered行数・frontier solved増分の
  再計算照合）が即捕捉した。実レコードは5/6/5で、K1158・K1160・K1164のpin転写typoと同じ防御パターンが
  「レコードからの一方向の打鍵定数」にも有効であることを確認した（修正版が出版正本）。
- **初期化バグ2件の捕捉**: X系隔離実行で `closed_history` のUnboundLocalErrorと隔離HOME markerの
  生成順エラーが出たが、いずれも検証機自身の実行段階で即座に顕在化し修正した（監査JSONには影響なし・
  失敗時は監査未書込のfail-closed設計どおり）。
- **全受理条件の成立**: gate 1,463全PASS（P 13・I 63・C 1,358・X 15・T 14）。
  tamper 2件（本レーン選択offset: worklist `inputs/worklist.csv` 1099・K1125証明書 21212の1 byte XOR 0x01）は
  returncode≠0・`input blob mismatch`/`input sha256 mismatch`・出力未書込で捕捉。
- **決定論性・参照独立性**: 監査正本 `b4b082f8…`（141,752 bytes）は同一cwd 2回＋隔離HOME・別cwd・
  `PYTHONHASHSEED=random` の3実行でbyte-identical。最新main `34c29854…` で再取得・再構成したWでも
  同一SHA-256を確認（fold22出版4ファイル・W全ファイルとも2参照間でdiff一致・
  最終版検証機で計4実行byte一致）。
- **出版（part1）**: 実験dir 5ファイル（README・reconstruct機・検証機・監査正本・reproduction.log）を
  単一コミット `4eb6cbf0519af177c077680835607975d4f82ac5` でmainへ直接反映し、
  fetch-back 5/5 byte-identicalを確認した。

## 結果

- fold22 receipt（K1132）の全数値主張が、出版社と実装を共有しない第三実装の検証機によって
  出版byteだけから再導出され、値単位で一致した。fold22 receipt自体が6行（主張3＋余剰3）を閉じたのは
  出版社の成果簿記であり、本項の成果はその外部第二検証の成立である。
- gate 1,463全PASS、監査正本 `b4b082f8…` は時刻を持たない決定論的JSONで、複数環境で再現可能。
- 実験事実として、fold22 receiptの `win_candidate_plan_impact.note` 列挙文がfold18 retired root
  （`00901010`・3主張行）を本文から落としているが、noteの数列
  `49-4-3-3-4-3-4-3-3-4-3-3-3 = 9` はfold18 retire込みの12 retire計40行を正しく加算している。
  再導出（fold11..fold21 retired 11根＋本receipt 1根・K1097 footprint 16根49行exactly-once・
  残り4根9行）はreceiptの数値主張と完全一致し、列挙漏れは表現上の省略で数値に影響しないことを
  機械確認した（fold18 retireのcounter事実はfold18 receipt `win_candidate_plan_impact` 自身が保持）。

## 限界

行は1行も閉じない（fold22時点の残余35→32行は出版社の既出版簿記であり、本検証は追加の行を閉じない・
pool 120,416根は不変）。本検証はreceipt簿記・機械決定性・
入力pin・fail-closed防衛の再検査である。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべて**UNKNOWN**のまま。
