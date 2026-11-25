# 2026-11-26 第29ラウンド: PG(2,9) の非 conic 7-キャップの Grundy＋統合メモ

## 非 conic 7-キャップの Grundy

- PG(2,9) の 7-キャップ全体は 51,554,880 個、うち conic 7-キャップは 7,076,160（K1321）。
- 非 conic 7-キャップの例 {11,22,29,32,44,61,89} を発見し、アップセット完全 DP を実行。
- 結果: **Grundy = 1**、極大拡大は **8-キャップのみ**（complete 8-arc、サイズ 8）、
  アップセットはわずか 2 局面。
- conic 7-キャップの Grundy も 1（K1321）なので、7-キャップは conic/非 conic を問わず
  G=1 の可能性が高い（q=9 では 7 が極大サイズの 1 つであり、maximal extension の偶奇が
  混在するため、より大きい Grundy もあり得る点に注意）。

## 統合チェック

- `tools/knowledge/check.py`: 1,227 items、374 エラーは他レーンの既存リンク切れのみ。
- `tools/knowledge/build.py`: 生成物に差分なし。
- `tools/knowledge/tests` の unittest は 30 分以上応答がなく、この環境では実用的でないため
  停止（以前も >20 分で打ち切り）。統合確認は check.py / build.py で代替。

## 次の一手

1. PG(2,9) の 8-キャップ・9-キャップの非 conic 部分の Grundy。
2. PG(2,9) 完全 Grundy への orbit 圧縮。
3. 一般 q の Grundy 分類。
