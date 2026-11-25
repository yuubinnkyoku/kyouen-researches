# 2026-11-20 n11 長期レーン: windfall 4 WIN7-D10 証明書の receipt fold（第13〜第16）

## 経緯

- K1063（resolve6）の「次の一手」: windfall 4 WIN root の証明書抽出
  （K1066 で三重独立検証まで完了）→ **receipt fold**。
- K1066 は「fold 記録が別途必要になるまでは閉鎖計上しない」と宣言して
  おり、fold 正本は今回が初出。fold 機械への証明書入力は K1066 の
  出版正本（4 枚の .n11、検証記録 SHA-256 a3ca1b3d…）のみを使用。
- 並走レーンが K1066 を出版済みのため、本レーンのローカル抽出・検証
  成果（cert-13thb..16thb、bits 40/43 は内容完全一致の独立再現で
  bits 99/118 は canonical root 版）は出版せず、観測としてこの研究log に一行観測として記録するのみ。

## 何をしたか

- `fold/fold_thirteenth_sixteenth.py` により、出版済み pinned 入力
  （git blob sha1 12 件・sha256 4 件・証明書 4 枚の byte sha256）から
  worklist → ledger/globalFold → cost78c/79c → first → second/third →
  fourth → fifth/sixth → seventh → eighth → ninth-twelfth の全 fold
  chain を毎ステップ frontier 再計算付きで再構築。第12 receipt 後の
  frontier 6,213 行 / cost 492,021 が出版値（K1057/K1060）と一致。
- 4 receipt を chain に適用。各 receipt で gate: 対象行が fold 前状態
  で open・chain 全体で disjoint、covered 行が D4 像・canonical
  frontier・resolve6 evidence・K1066 出版記録の三方一致、証明書
  byte sha256 一致、root 幾何（7 石）と legal move 数
  （48/58/52/56）の独立再列挙一致、K1066 の全 50 gate 再検。
- 決定論性: **4 回実行で出力 byte-identical**
  （SHA-256 594137b1bd4298b97a560def4920399ac49d7c4bd3e5fbcb54d3e8aa42919873）。

## 結果

- 4 receipt とも受領成功・extra 行 0。各 1 行ずつ閉鎖
  （第13 bit40: `00000000000000801202010000001000` cost 64、
  第14 bit43: `00000000000000801202080000001000` cost 79、
  第15 bit99: `00000000000000003800000008001200` cost 76、
  第16 bit118: `00000000010000003800000008100000` cost 80）。
  closed_edge_cost 計 299。
- **frontier 6,213/492,021 → 6,209/491,722**（solved S6 1,635 → 1,639、
  s6_needed 4,513 → 4,509、cost_needed 357,882 → 357,583、
  parent_row_incidence 11,826 → 11,818、remaining_s5_orbits 173 不変）。
- **5親target 34/112 → 38/112。残余 78 → 74 行**
  （74 行の完全リストは正本 JSON の
  `five_parent_target_after.residual_row_hex_after`）。
- 39 live witness 計画（resolve6）への影響（観測のみ）:
  unaffected 35 本・1行のみ閉鎖 4 本・両行閉鎖 0 本。windfall 4 根で
  4 witness の被覆行が 1 行に減るため、witness 計画の再架構が必要。
- parent_closure: fully_closed parent 0・affected_unique_parents 5
  （各 receipt 2 親）。

## 解釈規約

- fold は行被覆の簿記であり、REFUTED-D10 は LOSS 証明ではない。
  pn/dn・solved 数を勝敗や距離として読まない。
- 残余 74 行は未解決。二石 root・空盤の勝敗は本項の対象外。
- **標準 11x11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 はすべて UNKNOWN のまま。**

## 次の一手

1. 残余 74 行の post-fold 再解決（resolve7）: 最大 matching・singleton
   候補・witness 計画の再計算。39 live witness 計画の再架構を含む。
2. resolve7 の候補から次 receipt 候補を選び、証明書抽出→独立検証
   →fold の順で 74 行を段階的に削る。
