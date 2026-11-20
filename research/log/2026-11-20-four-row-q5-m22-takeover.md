# 2026-11-20 (4,22,5) class-split掃引 takeover (高速レーン)

## 状況認識

- M_{4,5} の前線は 4x22（K0857 で 4x21 witness-free 確定・M_{4,5} = 21 or >= 23・上界 U=140）。
- m22 掃引レーンは 2026-11-15 17:13Z に開始されたが 17:55Z の README追記を最後に停止。
  records 5行（ctrl SAT 375,415 bit-exact・c0k3p0/p1/p2 の600s INDET・c01 UNSAT 451.0s/5,022,943）。
- 2026-11-20 時点で5日間更新がないため takeover を決定（着手直前に最新main HEAD 77e6658a を再取得・
  他レーンの同一 (w,m,q) 着手なしを確認）。

## 較正（本takeover環境での実測）

1. 陽性対照 (4,20,5) class{0} k3 p1: CNF md5 362034b210d89ed3a25d34072995f3a6 byte-exact、
   kissat 4.0.4 SAT 375,415 conflicts bit-exact（19.4s・1コア専有）。
2. sat4 k-aware（m22版・2026-11-15導入のk=2上限修正入り）: (4,21,5) c0k3p0 --x2=1 が旧sat4と
   byte-identical CNF（md5 13749780ebd7467aca0a7b2e3ea7e163）。k=2 --x2=21 はk-aware版のみ生成。
3. kissat は公式静的バイナリ md5 3a5eba830aa6008a604fcc9bbe99a325（前レーンと同一）。

## 実行計画

- 単一オーナー・1インスタンス逐次・CAP=900s。
- batch AB: multi 6 (c02,c03,c12,c012,c013,c0123) + k2 22 + k1 22 + k0 2（sweep22fast と同じ
  「安価なクラスを先に」順序）。INDET の multi は krow-pin 分割で追分解する。
- batch C: c1k3p0..p10 直接（m21では38〜314s・×1.5-2予測）。
- batch D: c0k3p3..p10 直接。INDET は x2 分割へ。
- batch E: x2 分割 c0k3p0 b1..20（20枚）・c0k3p1 b2..20（19枚）・その他INDETバケット。
  さらに抵抗するサブバケットは第3石 x3 分割（sat4ka 拡張）で追分解予定。
- 決着・INDETともに records.jsonl に append してbatch pushする。
- 全 UNSAT なら 4x22 witness-free: witness-free幅集合 {21,22}・M_{4,5} = 21 or >= 24。
  SAT が出たら witness band m=5..22 に拡大・M ∈ [23,140]。いずれも K へ昇格する。

## 判断の根拠

- x2 分割の完全性は K0857・sweepp0x2gen.sh の規約（exhaustive disjoint・case分析として完全）。
  m21 では深cap抵抗バケットも x2 1枚 <=185s に落ちた実績。
- k3 直接試行の連続INDET (p0/p1/p2) が m21 の p0/p1 パターンと整合するため、
  cap 到達前に x2 へ直行する判断は記録済みのINDETと矛盾しない。
