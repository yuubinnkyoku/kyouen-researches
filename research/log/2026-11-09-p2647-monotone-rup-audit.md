# 2026-11-09 保存証明の削除を消したRUP監査

AGENTS、knowledge README、K0693/K0702/K0706/K0707/K0711/K0713と最新log・experimentを確認。
fetch時にorigin/mainの74a96456（別領域の独立misere検査）が追加されていたため、mainへmergeした。
初期未追跡の他者のshape出力2件は変更しない。研究計算の実行中プロセスはなかった。

前回の617秒のSAT探索を再実行せず、ローカルに保存された2127240行の112証明を再利用する。
同じ120秒のDRAT検査を再試行する代わりに、RATを禁止した追加のみのRUP反駁として検査する方針を選んだ。
削除は無視するが、全追加が元CNFの帰結であることをRUPで検査するので、古いDRATの削除不具合の再導入ではない。

新しい独立experimentへ検査器・ドライバ・回帰・出力を置いた。
prototypeでは重複literalを持つ節がunitであることを見落として正しいRUPを拒否した。
失敗した入力・期待値・旧prototypeのhashを保存し、parserで重複を除去して修正した。
毎回初期化するPython UPと全割当列挙を使う516件の回帰が成功。K0707の4偽証明も拒否。

加えて、CardEncを使わず保存された4入力の全節を独立なschemaへ照合した。
NONE=2を含む一般kのcounterも、prefix閾値の解釈と全節照合で確認した。
安全集合からモデルへの拡張可能性を説明でき、単なる小例のsolver一致より写像の根拠を強化した。
53886提供辺のgeneric整数幾何検査も再実行して成功した。

## 検査方式の切替

000/011/101は削除を消したRUP列としても受理され、それぞれ5326/61818/147006追加節。
112の全追加列の単調検査は約464秒でまだ進行中だったため、当該自分のプロセスだけを中断した。
中断理由と対象、非受理receiptを保存した。時間切れや偽証明判定とは区別する。
同じ対象を重複起動せず、その後にupstream DRAT-trimへ切り替えた。

upstreamのcommitとMIT licenseを含む原文を別experimentへ保存した。
Windowsでgetc_unlockedが未定義だったため、原文を変更せずビルド時macroでgetcへ対応させた。
同実装のRUP-onlyモードでもK0707の4偽証明を拒否し、resolution正例を受理した。
112を後ろ向きに監査し、DRAT/LRAT coreを抽出する。抽出できたcoreは独立した再生へ回す。

## さらに見つかったLRAT空節の偽受理

導入候補のlrat-check.cを制御例で調べると、SATである単位節1だけの入力に対して
1行の「2 0 1 0」を受理した。hintから単位1が伝播するだけで矛盾しないのに、
空節をpivot=0のvacuous RATとして受理する分岐が原因だった。
指定upstream原文と反例を保持し、K0714へ記録した。原版の受理を監査根拠に採用しない。
局所コピーにRUP矛盾のない空節を拒否する条件を入れ、5制御例で正例受理・偽証明拒否を確認した。
これは別ファイルdrat-trim.cの不具合の実証ではない。抽出coreは別RUP実装でも再検査する。

## 検証と再開checkpoint

uv sync --locked成功。knowledge checkは696項目、error 0 / warning 0。
共通unittestは33件・345.557秒ですべて成功。生成物はbuild.pyで再生成する。
修正後の4入力は、選択変数とcounter群の範囲分離も加えた新しいencoding-audit-reservationで再照合し成功。
古いencoding-audit.jsonは当時のreceiptとして残した。

112のupstream driverはnative検査の後、大きいcore出力をgzip化している。
2026-11-09 18:43 JST時点でPython PID 30328が実行中、native drat-trimプロセスは終了していた。
DRAT coreは326732609 bytes・1264432行、gzip42064451 bytes。
受理receiptはまだ永続化されていないので、ここでは受理・タイムアウトのいずれも断定しない。
core-drat-manifest-checkpoint.jsonは所在とhashだけを表し、受理証拠として使わない。
大きいDRAT/LRAT coreはGitから除外しローカルに保持する。元の107MB証明も保持している。
監査済み範囲1296<=A(2647)<=1323は維持し、1322へはまだ更新しない。

次回はまずプロセスとoutput/shape-112/audit.jsonを確認し、同じ対象の計算を重複起動しない。
現在のexec sessionは48988。driverの完了後、verifiedがtrueなら原版LRATを使わず、
replay_core.py --checker lrat --shape 112 --output FRESH.jsonで局所修正版による再生を行う。
必要なら--checker rupで別RUP実装も使えるが、大きい追加列は時間がかかるので同予算の重複を避ける。
新しい大きいcoreについては配布可否とmanifestを明示し、存在しないcheckoutで再生可能と書かない。
全4入力の幾何写像と受理された反駁が揃った時点で、K0711の同じ命題の上界を更新する。

sourceの最終byte監査で、upstream checkoutがGitの設定によりCRLF化されていることを確認した。
コンパイルしたbyteは保持し、CRLF→LFだけで指定commitのGit blobと完全一致することを別途確認。
provenanceへ両方のhashとGit blob IDを追記し、本文変更とは区別した。

LRAT coreの未圧縮サイズは2711546166 bytesと大きく、現在のdriverのgzip level 9は重い。
次の新規driverでは、旧コードを凍結した上でstreaming・低圧縮levelと段階ごとのreceipt永続化を優先する。
実行中のdriverのソースはhashの対応を壊さないため変更していない。
今のプロセスが終わるまで同じ監査・圧縮を再起動しない。

最終buildは696項目から6 viewsとREADME生成に成功。生成差分は正本に対応する分のみで、stage後の再生成差分は0。
自分の41 pathのsource/evidence byteとhash、upstreamの改行だけの差、偽空節の原版受理・局所修正版拒否を最終確認。
他者の未追跡2出力と大きいraw/coreをcommitへ含めない。
