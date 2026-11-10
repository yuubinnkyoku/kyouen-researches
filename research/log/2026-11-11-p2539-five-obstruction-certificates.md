# 2026-11-11 p2539の五点削除で使えない追加候補60点を独立排除

開始HEADは49d07bc6b3e5ae4e7afeb20038a24380fb3f4bfe、main。
AGENTS.md、knowledge README、現行K0693/K0702/K0706/K0727、最新logとexperimentを読んだ。
git fetch origin main、status、実行中プロセスを確認。研究計算や新しいremote commitはなかった。
他者の未コミットequality_screen_200k.jsonを保持した。

前回の引継ぎに従い、同じ保持側UNKNOWNを再探索せず、一点追加時の障害を評価した。
提供辺でuだけがS外となる四点は6514個、対象uは1281点。
保持必須F={0,6,2533}を削除選択肢から外した障害族について、最初の貪欲packingだけでも43点の下界が五点を超えた。
これは一時的な選別であり正本化せず、bounded hitting探索と保存証明木で全候補を評価した。

60点で五点以下のhittingが不可能、1221点では提供障害族に対する削除証人を得た。
正の削除証人は幾何学的改善とは扱わない。探索は計5073 nodeを訪問し、SATライブラリを使っていない。
独立verifierは探索コードをimportせず、元入力から障害族を再構成し、branchの全選択肢とpackingの互いに素性を確認した。
負の証明木はpacking306・branch123 nodeを受理し、6514四点全ての整数行列式0を実検査した。
総当たり2224例で正負の探索結果・証明木・削除証人を照合し、14改変を拒否した。
有限回帰、実証明木の受理、一般的なhitting-tree帰納健全性は分けて記録した。

Fを保つ安全集合Tにuがあれば、D=S∖Tはuに対応する全障害をhitしなければならない。
従って五点以下の削除による改善は60点を回避する。大きなTや複数点の同時追加でも条件は必要。
既存の五点削除必要条件の追加証拠としてK0727を更新し、新しいKは作らなかった。
提供辺の完全性、1221候補の実現可能性、五点削除局所最適性、全体最大性は示さない。
全体範囲1258..1271と元の保持側UNKNOWNは不変。

次回は60点の除外を採用する形で残り1221候補の二点同時追加障害や削除支持の共有を評価できる。
SAT入力へ負point単位節を加える場合、今回の幾何・hitting-tree由来であることを明記し、
元のCNF単独のRUP帰結として扱わない。同じUNKNOWN・同じ予算は再実行していない。

uv sync --locked、knowledge check（709項目、error/warningとも0）、33 unittest（348.280秒）、buildが成功した。
生成物をstageして再buildし、git diff --exit-code -- README.md research/knowledge/generatedが終了値0。
全source・証明書・幾何入力・引継ぎ論証と、K0727本文およびREADMEの60点一覧のbindingを照合した。
scope指定のindexは18ファイルで、experimentのindex blobは作業中raw bytesと一致し、他者screenや__pycache__を含めていない。
終了前のfetchでもremote追加はなかった。branch/PRを作らず、検証済みの自分の変更だけmainへ直接commitする。
pushや長時間探索workflowの自動起動設定は変更しない。
