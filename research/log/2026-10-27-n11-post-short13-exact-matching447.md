# 2026-10-27：短い9石WIN13類後の14根最小費用447

開始時main `702d146592d685fde27ab4d91168b206590f2e55`。AGENTS.md、knowledge README、K0023、K0414、直近の9石WIN13類の独立終局証明と14根の460辺最適化を確認。空盤UNKNOWN。

直前の証明で8石WINが83類増加し、固定14根の未証明7→8石辺は460→447になったが、再最適化前の447は上界のみだった。今回、既存の証明を終局まで再検証した後、全853個の7石候補を再列挙。既知8石LOSSを子に持つ67候補を除外し、786候補の未証明8石子数を費用として計算した。費用が下がった有効候補38類、最安費用が下がった共有組29、単独候補13。343組の共有候補と27個の単独候補を28頂点最小重み完全対応で最適化し、**447辺が条件付き14根方式の厳密最小値**と確認した。保存済み14根がそのまま最適。

14根の全合法548辺のうち証明済み101辺、未証明447辺・相異なる447類。証明限定8石WIN2,516類、既知8石LOSS338類、WIN/LOSS衝突0。9石WIN13類の187着手・相異なる10石183類は二種類の整数幾何で終局まで再検証し、改変拒否6件に成功。

再現：`python3 research/experiments/n11-s5-post-short13-matching-20261027/verify.py --negative`（networkx 3.4.2）。[専用CI 40410225550](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40410225550) 成功。コード・監査・CIは `research/experiments/n11-s5-post-short13-matching-20261027/` と `.github/workflows/n11-s5-post-short13-matching.yml` に保存。

この最小値は計算時間の下界ではない。7石WIN根14類、5石局面、二石rootの新規閉鎖0。**標準11×11空盤UNKNOWN**。
