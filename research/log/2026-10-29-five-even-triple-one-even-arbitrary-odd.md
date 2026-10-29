# 2026-10-29 高速レーン：5中心・偶数三点型消去を「偶数型1種類＋任意の奇数型」へ拡張

既存の「奇数型全25種類」および「偶奇混在8種類以下」の結果を確認し、重複しない次の境界を検証した。

5中心クリーク、各中心に正の奇数枚の私有葉を持つ抽象分割グラフの通常Node Kaylesで、三点型T以外に正の偶数重複の非私有型が高々1種類なら、その他の型の正の奇数重複は種類数に制限なく許し、Tに2点追加しても根のGrundy数が不変。

K0336の同一link独立双子点の正の偶奇縮約で有限基底へ還元。Tを固定するS3×S2群で、偶数型25候補を8軌道に、残る24種類の奇数型選択を安定化群で縮約した。35,454,336代表を全件検査、重み付き総数419,430,400構成、不一致0。独立の名前付き頂点・閉近傍削除の直接mexと別の型別再帰を250組（前後500構成）照合し、全件一致。

一次資料・再現器：
- [説明・数学的還元・限界](../experiments/game-structure/five-even-triple-one-even-arbitrary-odd-20261029/README.md)
- [全件列挙](../experiments/game-structure/five-even-triple-one-even-arbitrary-odd-20261029/verify.cpp)
- [独立標本検証](../experiments/game-structure/five-even-triple-one-even-arbitrary-odd-20261029/verify_independent.py)

この定理は抽象分割グラフについての計算機援用の全称証明。整数格子実現性や11×11の空盤勝敗は主張しない。2種類以上の偶数非私有型は未証明。全体CI・knowledge正本への昇格・生成索引更新は未実施。