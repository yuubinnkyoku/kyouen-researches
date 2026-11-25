# candidate-supply whole-record（K1075正本側）独立第二検証のpristine再実行第三検証 研究log

## 経緯

- 2026-11-21 の本長期レーン実行は、K1192（36root-three-ply frontier=K1084第二検証の第三検証）part3（commit `5487dad0`）の直後から続行し、
  residual72系の残る未着手第三検証枠からcandidate-supply whole-record分を選定した。
- 対象コミットのファイル構成を実機確認: commit `3e0d2df9`（2026-11-19T21:55:31Z・単一コミット）は実験dir 3ファイル
  （README `69db6635…` 9,065・検証機 `k1075_second_verification.py` `f808279d…` 35,127・監査正本 `753f9a07…` 16,462）+ 研究log `9724e961…` 3,331 を
  一括出版しており、宣言時現main HEAD `5487dad0` で4ファイルともpin byteと一致した。出版社レーンの単一オーナー宣言ノート
  （2026-11-20出版）が先行出版済みであることも確認した。
- 選定理由: candidate-supply whole-record第二検証はK1075正本（候補供給再構築の出版）の87 gate第二検証で、residual72系第三検証群の
  大きな未着手枠だった。検証機は純stdlib・生probe corpus再構成+記録同一性経路のみ（幾何レーンと非重複）で、軽量と推定された。
  コミット検索（candidate-supply第三 / K1075 third / whole-record pristine reexec の各クエリ0ヒット）と対象file path履歴
  （publish commit `3e0d2df9` の1コミットのみ）で第三検証宣言・実験の不存在を確認したうえで着手
  （fold11/17/18/19/23/25/26 ext2・round-5 refsolve・WIN8抽出・n9-ge19・n10 witness・five-row q7・four-row q6残・
  remo survivor・residual23 zero-triple・3行q4・four-row q6 band は宣言済み・着手禁止の他レーン作業）。
- **W 15入力の所在確認**: 検証機内PINS（15点）と対象README「実行方法」節の取得元記述を突き合わせて全点の正規pathを実在確認した。
  roots.jsonだけは実験dir直下（`n11-residual78-39livewitness-depth10-sweep-20261120/` 直下）にあり、probe記録は同dir
  `output/probe-records-w{0..3}.jsonl`。15点とも現mainで検証機内pin とbyte一致。
- **宣言前のbyte再生性予備実測（K1191運用の適用例）**: 合成input_dir（15正規名配置）で出版検証機をpristine実行すると
  rc=0・stdout `gates 87 all_pass True faithful True`・約0.07秒/回・出力監査が出版正本 `753f9a07…`（16,462 bytes）と
  byte-identical。→ 本対象は出版監査byte再生が成立しており、rerun受入条件3は当初からbyte一致条件で確定した（erratumなし）。
- tamper予備探針（battery前・探針環境）： 検証機は `sorted(PINS)` 読み取り順（fold10→fold9→k1075→probes-w0..3→r7second→
  resolve5→resolve6→resolve7→roots→sv17→sweep39→sweep39dead）でSHA照合し、最初の不一致で `raise SystemExit("pin mismatch for <name>")`
  （tracebackなし）となり監査JSONを一切書かない「監査不書込」型fail-closed。t1 sweep39dead.json @33,333（読み取り15番目=最終）・
  t2 k1075.json @44,456（読み取り3番目）の1 byte XOR 0x20がいずれもrc==1・stdout空・stderr末行文言で入力名特定・監査不書込であることを
  実測し、宣言に挙動予測と読み取り順を記載した。offset @{33,333,44,456} は既知の全レーン探針位置とすべて別位置。
- 宣言出版: commit `9e7ac2a1`（10,769 bytes・受入条件5項目・fetch-back byte一致・
  ref_a = 宣言時HEAD `5487dad0…`・ref_b = 宣言commit）。

## 結果

- harness `verify_k1075_third_20261121.py`（18,523 bytes・stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・
  byte決定的監査JSON出力・合成input_dir方式・検証機への引数は絶対path化）を構築。開発中のバグ1件はdry-run失敗で捕捉し修正した:
  検証機呼び出しに相対pathのinput/out引数を渡したままsubprocessのcwdを変更したため出力が書かれない（引数を絶対path化）。
- **4 batteryすべて111/111 PASS・監査JSON byte-identical**（SHA-256 `365fbdfc81d4d642a5a047e7cf50a531ebc9ded75a5d0ce778b354f2ce421798`・
  14,992 bytes・`cmp`完全一致）。B1 fresh base（1.4s）→B2 同一base全stage再実行〔pin/recon再取得込み〕（1.4s）→
  B1f fresh base独立capture（1.5s）→B3 隔離fresh base+全体`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`+別cwd（1.4s）。
- rerun: 出版検証機pristine 4回/battery×4 battery（同一base 2・隔離copytree+隔離env 1・+`PYTHONHASHSEED=random` 1）で
  全回rc=0・stdout `gates 87 all_pass True faithful True`・出力が出版正本 `753f9a07…`（16,462 bytes）とbyte-identical・
  battery内4回間でbyte一致（検証機1回約0.07秒）。erratumなし。
- tampers: t1 sweep39dead.json @33,333（stderr末行 `pin mismatch for sweep39dead.json`）・t2 k1075.json @44,456
  （`pin mismatch for k1075.json`）がいずれもrc==1・stdout空・監査不書込（probe-local出力pathの事前不在+事後不在の両assert）・
  本番input W無改変再照合。**2つのstderr文言は互いに異なる入力を特定し、2入力pin gateが互いに独立して発火する**ことを
  1 battery内で実証（gate `tamper-independent-errors`・t1は読み取り15番目〔最終〕・t2は3番目のfailで読み取り順独立性を含む）。
- part1実験dir（README・scripts harness・output 監査正本・output reproduction.log・4ファイル）を単一コミット出版
  （commit `4c8c95aa`・fetch-back 4/4 byte一致）。
- part2として本item（K1193）と本logを出版。K番号はpush直前の3点確認（search_commits `K1193 repo:yuubinnkyoku/kyouen-researches`
  0ヒット・README最大K番号 K1192〔part3でbullet追記済み〕・HEAD `4c8c95aa`〔part1出版のまま並走なし〕）で採番した。
- **B3初回のPATH起 因失敗の記録**: B3（`env -i`隔離実行）の初回は `PATH=/usr/bin:/bin` にpython3が無く
  `env: 'python3': No such file or directory` で即失敗（battery全体としては失敗扱いにならず、同一baseのB1/B2と
  capture一致まで完了した時点での隔離巡の失敗）。python3の実在bin dirをPATHに渡してB3を再実行し、
  111/111 PASS・byte一致で受入どおり確定した。この失敗はbattery設計の実験的事実としてreproduction.log 再構築のうえ
  最終版に含めず、本logに記録として残す。

## 実験事実・知見

1. **「rerun受入のbyte再生性は宣言前に予備実測してから課す」運用の適用例（K1191知見）**: 本対象もbyte再生成立（erratumなし）で、
   K1192（t36）とあわせ連続2例が通常型。replace16 K1191のerratum型は今の所1例のみだが、運用は予備実測を必須としたまま維持する
   （対象ごとに変わるため）。予備実測1回+本battery 16回の計17回が出版監査とbyte一致。
2. **fail-closed設計はSystemExit不書込型（tracebackなし）**: 読み取り直後のSHA不一致で `raise SystemExit("pin mismatch for <name>")`
   が置き、監査JSONを一切書かない。stderr文言は入力名で決定的。fold10（gate-failed監査書込型）・resolve7/replace16/本対象
   （SystemExit不書込型）・t36（raise RuntimeError traceback型）の系列で、**文言がtracebackを含まない場合は末行=文言そのもの**であり
   gate記録が最も単純になる型であることを確認。
3. **W 15点（第三検証群で最多の入力数）でもreconが完動**: 2参照×15点のraw fetchとduplicate配置の再照合が全て機械gateで完結
   （61 gate）。入力点数はgate数に比例して増えるが、battery所要は検証機実行時間に支配されず約1.4秒で安定。
   第二検証出版（2026-11-19T21:55Z）から約1.6日で第三検証確定。
4. **隔離batteryのenv -iはPATHの実在確認を含めて手続き化する（運用知見）**: python3が標準PATH外（/usr/local/bin）にいる環境では
   `PATH=/usr/bin:/bin` の固定は失敗する。以後の隔離実験は `dirname $(which python3)` を含める。

## 解釈規約（不変）

- 本検証はcandidate-supply whole-record第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、探索・根の新規判定・
  行の閉鎖・候補universe再構築・receiptの再発行・幾何レーンの再検査は一切行わない。
- 幾何censusの重複率はDFPN節点数・共有表命中率・証明状態再利用性を測るものではない。nodes数・solved数・coverage数を勝敗として読まない。
  REFUTED-D10はLOSS証明ではない。witness根・候補供給は条件付きdepth-10掃引計画で証明書ではない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手

- residual72系の第三検証で残る未着手枠は **refuted50分（verifier 48,898 bytes・audit 38,056 bytes）** のみ。最新mainの宣言状況を確認のうえ
  各レーン個別宣言で着手する。（本Kのpart3としてknowledge README bullet追記〔K1193〕も単独コミットで出版する。）
