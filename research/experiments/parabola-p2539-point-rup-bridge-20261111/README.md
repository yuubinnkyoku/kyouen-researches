# p2539: 60除外単位節を親CNFだけのRUPへ接続（2026-11-11）

採用時点の検証結果はK0727へ追加した。現在の正本はknowledge itemを参照する。
ここで検査するのは**60個の負point単位節の導出**であり、親CNFのUNSATではない。

## 対象と証明生成

親Fは`../parabola-p2539-five-pair-split-20261111/output/retained/input.cnf.gz`、
非圧縮SHA-256 `64496e29f631e4f4090c103e571490f7959a30558462d9b4992ec668633f561b`。
51570変数144546節で、原点と完全対{6,2533}を保つexact1259点・exact五点損失の入力である。
前回の60点リストは検査対象の選択にだけ使い、今回のRUP検査は幾何学的な除外命題を仮定しない。

各uについてF+[a_u]（a_u=36512+u）の子を別プロセスで実行した。
PySAT 1.9.dev21/Cadical195、proof-enabled、budget10000で、60子全てが終了値0・SOLVER_UNSAT。
最大実conflictsは144、生成DRATは合計697205行。最初のu=555を試した後は、既存結果を保持して他の59点だけを生成した。
親やpruned60の全体UNKNOWNを同条件で再実行していない。

## 仮定の除去

子証明の各追加節CをC∨¬a_uへ変換する。重複literalは除き、a_uを含む元節はliftすると恒真節なので省く。
削除行は省き、元の節を多く保持する。子の末尾空節は¬a_u単位節になる。

一般的な理由は次の通り。子のRUP追加Cを調べる仮定は¬Cとa_u。
親側でliftしたC∨¬a_uを否定すると、同じ¬Cとa_uが得られる。
以前のlift節はa_uの下で元の子節へ戻り、削除を省いて多くの節を残してもunit propagationによる矛盾は壊れない。
従って子の追加がRUPなら親のliftした追加もRUPで、末尾に¬a_uを導ける。
ただしソルバ出力の一般的健全性や変換実装だけは信用せず、実際のlift全節を親Fだけで独立検査する。

## 独立チェックとDERIVATIONの意味

固定DRAT-trimソース（SHA-256 `78026871882de3f2fee66034e549e9c1a0a9a5291abd817d06f611f9ba0f355d`）を無変更で使い、
`-f -U`によりforwardで全追加をRUP限定検査した。各点のlift証明と結合証明を検査する。
成功は`c VERIFIED derivation: all lemmas preserve satisfiability`と`s DERIVATION`の両行で判定する。
上流mainは最終UNSATだけ終了値0にするため、DERIVATIONの終了値1はこのモードでの正常な導出受理である。
終了値1だけで成功と扱わず、上記行・NOT VERIFIEDの不在・失敗行の不在を要求する。
**空節なし、refutationではない、全体UNSATを主張しない**ことをreceiptにも保存する。

native checkerのcontrolでは有効な単位節・非単位節の導出を受理し、偽の単位節・偽の二項節・RATだけの節を拒否した。
独立な小さなunit propagationと真理値総当たりによる回帰では、561個の仮定下の負例、574個のlift節を照合し、
4不正入力と、guardを外すと親の帰結でなくなる例を確認した。
一般的な仮定除去の論証と有限回帰・実checkerの受理は分けて扱う。

個別60本は`individual-summary.json`で独立に採用し、結合検査の状態とは分けている。
単純結合の初回検査は120秒でtimeoutとなり、例外とbyte復元した入力を`combined-output/plain-attempt.*`へ保存した。
各点の末尾で、親の節でも単位節でもない使用済みlift補助節を削除する形式へ変更した。
親の節と60個の目標単位節は削除しない。別の300秒上限で135.535秒後にDERIVATIONを受理した。
採用結合証明は`combined-output/all-units.rup.gz`で、追加696834行・削除696774行の計1393608行。
各点のlift証明・receiptは`audit-output/`のu別ファイルにある。
`replay.py`は親F・結合証明・manifestだけから、SATライブラリや子証明を使わず60単位節を再検査する。
元の子DRAT・実終了値・既存pilotも保存し、上書きしない。

## 結論と範囲

60個の負point単位節はFだけのRUP帰結となった。
従ってその60節を加えた前回pruned60 CNF（SHA-256 `ea0b35e2e934035cea98abc6f491f9312c11830d60347b8097e9eebe62fd8656`）は、Fと全モデルが一致する。
これは既知の幾何学的除外をCNF内の検査可能な導出へ接続した検証上の進展である。
Fまたはpruned60のUNSAT、五点削除近傍の局所最適性、新しい上下界は得ていない。

K0727の既存根拠から改善Tは原点と元の完全対を保ち、|S∖T|=5。
Tが60点中のuを含めば、(S∩T)∪{u}は1254点なので、これを含むTの1259点部分集合T'を選べる。
原点と元の完全対はS∩Tに含まれる。T'は安全性・種との1253共通点・uを保ち、Fのモデルへ拡張できる。
しかし今回Fから¬a_uが導かれるため矛盾する。この縮小論証でも60点の回避を支持する。

検査器・コンパイラ一般の形式的健全性やLean形式証明は主張しない。
既存のpruned60/budget100000のUNKNOWNと1258≤A(2539)≤1271は変わらない。

## 再現と継続

repo rootから新しい出力pathを使う。

```powershell
$exp='research/experiments/parabola-p2539-point-rup-bridge-20261111'
uv run --locked python "$exp/replay.py" --saved "$exp/combined-output" --output "$exp/replay-fresh.json"
uv run --locked python "$exp/regression.py" --output "$exp/regression-fresh.json"
```

元証明から一点の変換・個別検査は`verify.py --saved <exp>/output --points <u> --output <fresh-directory>`。
全個別結果からの結合と検査は`combine.py --saved <exp>/audit-output --output <fresh-directory>`。
元のverify.pyは初回の単純結合timeoutも含む凍結driverとして保持する。全体結合の再検査にはcombine.pyを使う。
子証明生成の再現は`uv run --locked --with python-sat==1.9.dev21 python <exp>/run.py --output <fresh-directory>`。
既存子directoryを発見したら再起動せず保持する。UNKNOWNの再探索ではなく、特定単位節の証明生成である。
次回はこのnative RUP導出を、将来のpruned CNFの完結証明に前置して親だけの証明へ接続できる。
今回はその後段の完結証明を得ておらず、同じUNKNOWNの全体探索を再実行していない。
