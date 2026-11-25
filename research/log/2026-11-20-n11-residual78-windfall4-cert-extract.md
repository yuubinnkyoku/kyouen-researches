# 2026-11-20 n11 長期レーン: windfall 4 WIN7-D10 root の証明書抽出と三重独立検証（K1065）

## 経緯

- K1063（resolve6）の「次の一手」1番: windfall 4 WIN root の証明書抽出
  （repo-verbatim extractor + 二重検証）→ receipt fold 候補。本実験で実行。
- 対象は class2-lane-cost65h child `00000000000000803202000000001000` の
  bit 40/43/99/118（raw root = c65h|1<<bit）。被覆 4 行と出典は
  resolve6 正本（SHA-256 e85d4bfb…）の `win_cover_detail.evidence` に従う。
- 抽出規約は resolve6 の宣言どおり corpus provenance と一致する raw
  (child, bit) で行い、証明書の root 行は raw root（bit 40/43 はそれ自身が
  D4 正準形、bit 99/118 は非正準形のため canonical root との写像を gate で
  検証して記録）。

## 何をしたか

- **抽出**: repo-verbatim `class4_child1_cert_extractor_exact_ms23.ts`
  （FBS=1<<20・MS=1<<23・CAP=1e9）を自作 driver
  `scripts/cert_driver_windfall.ts`（78c 系譜・fatal/fbt_drops≠0 は出力拒否）
  で盲実行（kill table 空）。moves は legal_candidates.py による独立列挙
  （48/58/52/56 手）。抽出ノード数 3,074,926 / 7,700,023 / 3,355,354 /
  6,137,302。行数 31,189 / 51,767 / 36,625 / 55,838。fbt_drops 0・
  全 move ok・uncapped・terminal [13,17]。
- **再現**: 全 4 根について抽出を 2 回実行し証明書 byte-identical・
  ノード数完全一致を確認。
- **検証 1**: `verify_bit7_win7_cert.ts`（number Bareiss 4x4・sub-root 分解）
  root check（7 石・loser mobility 48/58/52/56）+ 全 sub-root PASS +
  consumed union == strategy rows（missing 0 / extra 0）。
- **検証 2**: `verify_cost71c_win7_bareiss_independent.py`（純 python・
  exact 整数 Bareiss・全 loser reply 展開の完全 replay）。全 PASS・
  terminal {13,15,17}。
- **検証 3**: `verify_win7_certificate_bigint_independent.mjs`（BigInt 3x3
  cofactor・117pool 系譜と同一方式）。全 PASS・sorted unique・
  terminal [13,17]・root_safe。
- **runner v16 node-exact 再現**: repo-verbatim runner v16
  （depth 10・andclose=1・cap 1e9）で 4 bit を fresh 再解。
  1,105,860 / 3,269,824 / 1,114,855 / 2,307,338 nodes が出版 raw batch 行
  （batch3/4/7/8）と完全一致。pilot_d6 対照行 loss=false（3,402 nodes）合格。
- **記録**: `scripts/build_verify_record_20261120.py` が artifacts から
  全 50 gate を再計算して fail-closed で正本 JSON を組む。
  2 回実行 byte-identical
  （SHA-256 a3ca1b3dfd2fcdbd28fc88a6f993c4ff5ad81ee92d4a22800ff2f6477c476feb）。

## 結果（output/windfall4-cert-triple-verification-20261120.json が正本）

- 4 証明書（certs/*.n11・2 回実行 byte 一致）が三系統の独立検証器で
  すべて PASS。全 50 gate PASS。
- 4 根は「単一順 pending receipt 候補」から「certificate-backed receipt
  候補（fold 前）」に昇格。**残余 78 行は 1 行も閉じない**: 閉鎖計上は
  本証明書を入力とする receipt fold 記録（fold 機械の入力 chain 再構築を
  含む）が別途必要。fold までの被覆簿記は 39 live witness 計画が
  78 行を独立に完全被覆するため windfall 非依存のまま成立。

## 解釈規約（不変）

- 各証明書の主張は「この 7 石 root で second mover が to move のとき
  original first mover が必勝（全 loser 分岐が loser stuck の terminal
  13-17 石で終端）」という game-theoretic fact のみ。WIN7-D10 を
  被覆行の値や pn/dn・solved 数として読まない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 はすべて UNKNOWN のまま。**

## 次の一手

1. 4 証明書を入力とする receipt fold（4 行の閉鎖計上・fold 正本の
   入力 chain 再構築）。
2. 39 live witness の depth-10 両順序掃引（K1059 同一規約・pilot_d6 制御）。
