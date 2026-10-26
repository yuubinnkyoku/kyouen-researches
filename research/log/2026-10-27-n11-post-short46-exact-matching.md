# 2026-10-27：短い9石WIN46類を反映した14根の厳密再最適化

開始時main `1ea05c1ed9cc9569cba2c5118436defba9aaa75d`。AGENTS.md、knowledge README、K0023/K0105、最新の9石WIN46類独立終局証明と14根の447辺最適化を確認。空盤UNKNOWN。

新規9石WIN46類、相異なる10石WIN葉755類を3×3差分行列式と独立4×4 Bareiss法で終局検証。専用CI [40417811825](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40417811825) 成功。逆向きに8石WIN362類を新規導出し、証明限定8石WIN2,516→2,878類、固定14根の確保辺101→151、未証明447→397辺（相異なる397類）。WIN/LOSS衝突0、改変拒否6件成功。

全853候補から既知8石LOSSで67候補を除いた786候補の残費用を再評価し、343共有組・27単独候補から28頂点の最小重み完全対応を解く。再最適化コード・独立監査・CIは `research/experiments/n11-s5-post-short46-matching-20261027/` に保存。最適値は専用CIの結果に従う。条件付き14根の費用は計算時間の下界ではない。7石・5石・二石root新規閉鎖0、標準11×11空盤UNKNOWN。
