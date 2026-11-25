# 2026-10-25：11×11四石LOSS証明書の五石cache照合をD4 class単位に統合

開始時mainは `a16d78aee21dab5f9ace84d7514e12175ad1c77e`。AGENTS.md、knowledge README、K0023・K0329、11×11のcoordinator資料、S4検証器と直近のD4子集合共通化logを確認した。11×11空盤はUNKNOWN。

## 観察

直前の改良で、同一D4 classに属する四石raw edgeの合法五石子**集合の生成**は1回になっていた。しかしLOSS証明のcache照合は依然として各raw edgeに対して同じ集合を全走査していた。raw edge数をE、相異なる正準五石子数をCとすると、cache.getはE×C回であり、結果と欠落診断も重複していた。

## 変更と根拠

`dfpn_s4_manifest_verify.py` のLOSS枝で正準五石子集合を1回照合し、cache中のWINの有無・欠落の有無を集約して全raw edgeに反映する。cache照合は **E×C → C回**。cacheに存在する子の報告数 `n_ok` は従来の意味を維持し、`E × (C − missing)` とする。

この集約はD4変換が合法着手と勝敗を保存し、同一classの全raw edgeが**同じ正準五石子集合**を持つことによる。したがって、いずれかの子がWINなら全edgeがWINを含み、WINが無く欠落があれば全edgeが未確定、すべてLOSSなら全edgeがLOSSとなる。全子集合の再列挙・manifest完全性検査・不正な子の拒否・cache矛盾拒否は従来どおり行う。

例：raw edge 2本・正準五石子103類ならcache照合206→103回、raw edge 4本・106類なら424→106回。これは**cache参照回数の削減**であり、検証器全体の実行時間や証明局面数の改善を実測したものではない。

## 確認と再現

- 旧ループと新しい集約式を、raw edge数1〜8、子数1〜125、全LOSS・WIN混入・欠落・WINと欠落混在の計4,000合成条件で比較し、WIN/LOSS/UNKNOWNのedge集計と`n_ok`がすべて一致。
- 実11×11の四石class `{60,0,1,2}` に対して、全子LOSS・1子欠落・1子WINの3条件で`main()`を実行し、cache参照回数が正準子数に一致する回帰試験を追加。
- 再現：`python3 -m unittest discover -s research/experiments/n11-search-methods/scripts -p 'test_dfpn_s4_manifest_verify_cache.py'`。
- **リポジトリ内回帰試験とCIの成功は現時点で未確認**。合成条件での集計同値と、実盤面回帰の追加を区別する。

二石rootの新規閉鎖なし。新たな勝敗証明なし。**標準11×11空盤の勝敗はUNKNOWN。**
