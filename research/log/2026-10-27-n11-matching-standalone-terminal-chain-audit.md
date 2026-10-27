# 2026-10-27：14根再最適化の単独監査で終局証明を省略しない修正

開始時main `f9e555d7c0d34f74f1e7eb2bc2452c7fe3bdae72`。AGENTS.md、knowledge README、K0023、11×11の証明・再最適化実験・研究記録を確認。標準11×11空盤勝敗は**UNKNOWN**。

条件付き14根再最適化の `audit.js` を追跡すると、degree2・short13・short46・short18・n19 の5段階が、新しい9石WIN証明書を `terminal:false`（構造のみ）で受け入れ、8石WINへ逆伝播していた。専用 `verify.py` は先に終局再計算を実施していたが、`node audit.js` 単独実行では証明葉の真偽を保証しなかった。n20・targeted21の同種の問題は先行修正済み。

上記5段階の `proof.verify(rows,{terminal:true})` を必須化した。これにより各段階の単独監査でも、全合法9→10石子の終局まで二種類の整数幾何で再計算し、全て元先手WINと確かめてから8石WIN集合に採用する。以前の段階も `previous.audit(false)` から連鎖的に再監査される。未完探索、保存勝敗表、pn/dnを証明根拠には使用しない。

再現コマンド：`node research/experiments/n11-s5-post-n19-matching-20261027/audit.js --negative`。より広い最適化・独立交互閉路検査は `python3 research/experiments/n11-s5-post-n19-matching-20261027/verify.py --negative`。今回の修正は監査の信頼境界に関するものであり、計算量は増える可能性がある。変更後の専用CIは degree2 [40465754548](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40465754548)、short13 [40465754542](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40465754542)、short46 [40465754523](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40465754523)、short18 [40465754505](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40465754505)、n19 [40465754521](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40465754521) のすべてで成功した。

新規WIN/LOSS証明0件、7石・5石・二石root閉鎖0件。証明限定8石WIN4,089類、条件付き14根未証明250辺の既知値は変わらない。**標準11×11空盤UNKNOWN**。

`n11-s5-post-n19-matching-20261027/test_fail_closed.js` で、5段階すべてが `terminal:true` で検証器を呼ぶことを実行時に検査。さらに19子証明書の2行の状態数を +1/-1 と相殺して総数83,884を維持した改変を与え、構造検査 `terminal:false` は通過する一方、終局再計算 `terminal:true` が拒否することを確認した。`verify.py --negative` はこの試験を必須とする。[専用CI 40465920404](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40465920404) 成功。これは従来の単独監査で実際に見落とし得た改変を再現する回帰試験である。
