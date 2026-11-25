# K1125 root 840500 証明書の別実行環境での再現確認

- 日付: 2026-11-20
- 対象: K1125（残余45行レーン WIN8-D10 root 840500）
- 実行時の main: `9d5f7877924ea4016f4c97d053b79af4b42e4c9e`
- 環境: Proxmox 上の専用 runner、Python 3.13.5、Node.js 22.15.0
- 位置づけ: 新しい探索・新しいreceiptではなく、出版済み証明書と三つの既存検証器を別実行環境で再実行した再現確認

## 実行方法

作業中の古い・未コミット変更を含む checkout は触らず、最新 main の detached sparse worktree に K1125 実験ディレクトリだけを展開した。証明書・入力・検証器はすべて当該実験ディレクトリ内の出版済みファイルを使用した。生成した監査JSONは `/tmp` に出し、出版済みファイルは変更していない。

## 結果

1. Python第三方法監査 `assemble_win8_audit_root840500.py` を、実験ディレクトリと別作業ディレクトリ複写の2箇所から実行。両出力は相互にbyte-identicalであり、出版済み `output/win8-cert-extract-verification-20261120.json` ともbyte-identical。19/19 gate PASS、監査JSON SHA-256は `06c65f7611b7fea17131d5e13b28792aee1b7d723e7b8cdb1cb3b54012282886`。
2. BigInt 3×3余因子検証器を再実行。出版済み `output/bigint-verification.json` の全項目と一致。戦略行29,468、sub-root 58、visited 59,990、winner-to-move 38,458、loser-to-move 11,722、応手辺52,360、終端9,810、終端石数[14,18]、missing 0 / extra 0。
3. Bareiss 4×4検証器を再実行。root-checkは石数8・loser mobility 58で出版値と一致し、58 sub-rootすべての統計JSONも出版済み `output/bareiss-stats.txt` と一致。証明書行集合との比較では、sub-rootごとの消費列38,458件に8,990件の重複がある一方、一意化したunionは29,468行で証明書の全行と完全一致（missing 0 / extra 0）。この重複は異なるroot初手の下で同じ勝者局面が共有されるためで、証明書内の重複行や矛盾ではない。
4. 証明書本体のSHA-256は出版値 `21ad61959f6b2ae13e2e24fd98842788c88ada50643ccfd1f88a459701d0cbcc` と一致。

## 解釈と限界

- 今回は既存の三検証器を別環境で再実行したものであり、第四の独立実装を追加したわけではない。ただし、Python第三方法の監査正本とBigInt/Bareissの数値・行集合の照合を、別runner上で再現できた。
- WIN8-D10証明書が証明するのはroot 840500のゲーム木だけである。S6親行の閉鎖はreceipt foldの別工程であり、本確認では行を1つも閉じていない。
- fold19（root 1009000）の単一オーナー作業は別途宣言済みだが、本確認では重複実行していない。FOLD_PREVERIFIED_CHAIN案も未採用のままである。
- REFUTED-D10はLOSS証明ではない。探索節点数・solved数を勝敗として読まない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4は引き続きUNKNOWN。
