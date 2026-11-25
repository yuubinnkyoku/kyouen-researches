# n11-windfall4-receipt-fold-thirteenth-sixteenth-20261120

K1066 が三重独立検証まで済ませた windfall 4 枚の WIN7-D10 証明書
（第13〜第16 receipt。class2-lane-cost65h child
`00000000000000803202000000001000` の bit 40/43/99/118）を入力として、
K1057/K1060 系譜の five-parent S6 frontier chain に receipt fold
（被覆簿記）を適用した。branch/PR は作らず main に直接出版。

## 何をしたか

- **chain 再構築**: `fold/fold_thirteenth_sixteenth.py` が、出版済み
  pinned 入力（git blob sha1 12 件・sha256 4 件・K1066 証明書 4 枚）から
  worklist → ledger/globalFold → cost78c/79c → first → second/third →
  fourth → fifth/sixth → seventh → eighth → ninth-twelfth の全 fold chain
  を毎ステップ frontier 再計算付きで再構築し、第12 receipt 後の
  frontier 6,213 行 / cost 492,021・S6 solved 1,635 が出版値と一致する
  ことを gate で確認（fail-closed）。
- **receipt 適用**: 各 receipt について (a) 対象行が fold 前状態で
  open・chain 全体で未使用（disjoint）、(b) covered 行が D4 像と canonical
  frontier から再導出され、resolve6 evidence および K1066 出版記録の
  covered 行と三方一致、(c) 証明書 byte sha256 が K1066 正本
  （検証記録 SHA-256 a3ca1b3d…）と一致、(d) root 幾何（7 石）・
  legal move 数の独立再列挙一致、(e) K1066 の全 50 gate の再検、
  を確認してから閉鎖を計上。
- **親簿記**: 各 receipt は 5親target 行をちょうど 1 行閉じ
  （extra 行 0）。影響親は各 2 親、affected_unique_parents 5。
  fully_closed parent 0。

## 結果（fold/output/thirteenth-sixteenth-win7-receipt-fold-20261120.json が正本）

| receipt | bit | canonical root hex | 閉鎖行 | cost |
|----|----|----|----|----|
| 第13 | 40 | 00000000000000803202010000001000 | 00000000000000801202010000001000 | 64 |
| 第14 | 43 | 00000000000000803202080000001000 | 00000000000000801202080000001000 | 79 |
| 第15 | 99 | 00000000000000803800000008001200 | 00000000000000003800000008001200 | 76 |
| 第16 | 118 | 00000000010000803800000008100000 | 00000000010000003800000008100000 | 80 |

- **frontier**: 6,213 行 / cost 492,021 → **6,209 行 / 491,722**
  （solved S6 1,635 → 1,639、parent_row_incidence 11,826 → 11,818、
  s6_needed 4,513 → 4,509、cost_needed 357,882 → 357,583、
  remaining_s5_orbits 173 不変）。
- **5親target**: 34/112 → **38/112 行閉鎖**。残余 78 → **74 行**
  （正本 JSONの `five_parent_target_after.residual_row_hex_after` が
  74 行の完全リスト）。
- **39 live witness 計画への影響（観測）**: unaffected 35 本・
  1行のみ閉鎖 4 本・両行閉鎖 0 本。windfall 4 根で 4 witness の被覆が
  1 行に減るため、post-fold 再解決（resolve7 相当）で計画の再架構が
  必要。
- **決定論性**: stdlib のみ・約15秒・**4 回実行で出力 byte-identical**
  （出力 SHA-256
  `594137b1bd4298b97a560def4920399ac49d7c4bd3e5fbcb54d3e8aa42919873`、
  21,269 bytes）。
- **全 controls PASS**（正本 JSON の `controls` 16 項目）。

## 解釈規約（他の n11 項目と同一）

- fold は行被覆の簿記であり、REFUTED-D10 は LOSS 証明ではない。
  WIN7-D10 証明書が主張するのは各 7 石 root 個別の depth-10 内
  先手必勝のみ。
- 本項で閉じたのは残余 78 行のうち 4 行で、**74 行は未解決**。
  二石 root・空盤の勝敗は本項の対象外。
- **標準 11x11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 はすべて UNKNOWN のまま。**

## 次の一手

1. 残余 74 行の post-fold 再解決（resolve7: 最大 matching・singleton
   候補の再計算・witness 計画の再架構）。
2. 次 receipt 候補の供給（resolve7 の fresh-safe pool・singleton
   候補から、証明書抽出→独立検証→fold の順で 74 行を段階的に削る。
