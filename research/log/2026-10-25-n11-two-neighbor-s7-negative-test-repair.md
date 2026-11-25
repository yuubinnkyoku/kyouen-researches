# 2026-10-25：9石2根→7石被覆監査の負の試験を修復

開始時のmainは `defc8752855ef1732095f3addfce80b771cbfa16`。
`AGENTS.md`、`research/knowledge/README.md`、K0023・K0105・K0329・K0375・K0418、
11×11の最新のknowledge・experiments・logを確認した。標準11×11空盤は**UNKNOWN**。

[CI 40197046408](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40197046408)
は `Audit n11 two S9 neighbors against proof-only S7 coverage` の
`--negative` で失敗した（2026-10-25 13:29 UTC）。
正の監査は先に完了し、9石WIN 2根、相異なる10石WIN 58葉、
8石WIN純増16類、7石親純増56類、証明済み7→8辺純増128本、
**影響を受けた7石親64類の最小未被覆子49類**、
**新たに全子被覆した7石親0類**、WIN/LOSS衝突0を出力していた。
これは影響64類に限る不足数で、全7石局面の最小不足ではない。

失敗原因は `checkManifest()` が配列の件数と集合への包含だけを確認し、
重複を含む同件数の10石葉・8石親の入力を受理したこと。
通常のファイル読み込み関数 `keys()` はソート済み一意性を確認するが、
公開された `checkManifest()` を直接呼ぶ負の試験はその前提を満たさない。
`[first, ...array.slice(0,-1)]` の改変が拒否されなかった。

`audit.js` の `checkManifest()` 自体で、9石根・10石葉・8石親の
各配列に対し厳密昇順（重複なし）を要求するよう修正した。
これにより入力経路を問わず重複した証明書の検査を拒否する。
修正コミット：
[9c6cc39](https://github.com/yuubinnkyoku/kyouen-researches/commit/9c6cc39a45b0ab236a8dfe15b03148d4b4f8d84e)。

この記録時点では修正後のCI完了は未確認。
今回の修正は証明書の**改変拒否能力**の改善であり、
9石・8石の既存勝敗や新しい7石勝敗の確定ではない。
二石rootの新規閉鎖0。標準11×11空盤は**UNKNOWN**。
