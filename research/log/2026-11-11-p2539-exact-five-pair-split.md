# 2026-11-11 p2539の五点削除・完全対変更を分割検査

開始HEADはac21587da7ca9f41202a2a1070395fcbe463d3bc、main。
AGENTS.md、knowledge README、現行K0693/K0702/K0706/K0727、最新logとexperimentを読んだ。
git fetch origin main、status、実行中プロセスを確認し、研究計算や新しいremote commitはなかった。
他者の未コミットequality_screen_200k.jsonは保持した。

K0727で残る原点あり・完全対一つ・exact五点損失の凍結UNKNOWN入力を、
元の完全対{6,2533}の保持と変更に分けた。B6=21なので末尾に[21]か[-21]だけを追加する。
共通親のbyte再構築と相補的二単位節を確認し、対象を重複起動していない。
双方100000 conflicts・proof-disabledで実行したところ、保持はUNKNOWN（100004 conflicts、97.85秒）、
変更はSOLVER_UNSAT（99424 conflicts、127.01秒）。両子終了値0を保存した。
同じ親UNKNOWNをそのまま再探索せず、新しい形状分割を使った。

入力監査は全節の独立schema、各38868幾何四点の整数行列式0を確認した。
16不正入力を拒否し、元の完全対を表す実point変数とsplitの128真理値割当ても確認した。
この段階の変更不能はソルバ主張であり、独立UNSATとはまだ区別して扱った。
変更側だけproof-enabledで再生成し、同じ99424 conflicts・116.76秒で483675行DRATを保存。子終了値0。
保持側のUNKNOWNは再実行していない。

独立schema・整数幾何・RUP限定検査と、抽出147349行LRATの空節修正版検査が受理された。
採用圧縮CNF/DRATを別処理で独立schema・幾何・RUPとともに再生し、受理された。
8574253 bytesの採用DRAT gzipはGit管理、生成元DRAT gzipと大きいLRAT raw/gzipはmanifest付きでローカル保持・Git除外。
検査器・コンパイラ一般の健全性やLean形式証明は主張しない。

共通種点1253点と変更先の完全対二点を保つ1259点部分集合への縮小で、完全対の位置も保たれる。
従って五点以下の削除による改善には原点と元の完全対の保持が必要となる。
同じ固定seedの五点削除必要条件を強める証拠なので、新しいKは作らずK0727を更新した。
以前のexperiment・log・raw evidenceは更新していない。
保持側はUNKNOWNであり、五点削除局所最適性も最大性も示さない。全体範囲1258..1271は不変。

次回は残る保持側の追加点が作る障害辺や削除集合の支持構造を評価するなど、未被覆層を構造化する。
同じretained入力を同じ予算で再実行したり、既排除の完全対変更や原点なしを再探索したりしない。
具体的には、各追加候補uについて、保存辺のうち残り三点がSにある四点を抽出し、
保持必須の{0,6,2533}を削除選択肢から外した三点以下の障害族を作れる。
その障害族を五点以下でhitできないuは改善に使えない。互いに素な障害を六つ示すだけでも必要条件による枝刈りになる。
これは次回の候補評価案で、今回hit数や除外点を計算・証明したという意味ではない。

uv sync --locked、knowledge check（709項目、error/warningとも0）、33 unittest（347.009秒）、buildが成功した。
生成物をstage後に再buildし、git diff --exit-code -- README.md research/knowledge/generatedは終了値0。
全frozen source、採用/生成元DRAT、保持LRAT、qualification、実子終了値のbindingを照合した。
scopeを限定したindexは44ファイル・採用証明一つで、experimentのindex blobは作業中raw bytesと一致した。
他者screen、__pycache__、大きいraw/gzip LRAT、生成元DRAT gzipはコミット対象に含めていない。
終了前のfetchでもremote追加はなかった。branch/PRを作らず、検証済みの自分の変更だけmainへ直接commitする。
pushや探索workflowの自動起動設定は変更しない。
