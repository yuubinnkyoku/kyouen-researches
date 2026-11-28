# 宣言: Baer partition (Bruck) 検証の q=11・q=13 への拡張

- 日時: 2026-11-28
- 種別: 高速レーン (publish-then-execute・単一オーナー)
- 宣言時 HEAD: 60c712c0f22e04509fb31b90e053cf34dd7b62a8 (前段 kit+K1374+log commit)
- 前段: 宣言 `862293aa` + amendment `f359c5c5` + kit `60c712c0` (K1374, q=2..9)。

## 計画

1. 実装1 (GF(p^{2m}) 塔・前段 kit の baer_partition_impl1.py、生成元位数の
   O(ordE) 追加ループを >600,000 で skip するゲートのみ変更 — factor test
   (gamma^{ordE/f} != 1 for all prime f) は位数の完全検証として数学的に十分)
   を q=11, 13 に適用する。実装2 (gamma 探索が packed range p^{6m} を走査)
   は q>=11 でスケール外のため不使用 (正直な限界として記録)。
2. 各 q で前段と同一バッテリ: design 検査・Singer 商位数検証・軌道分割
   (q^2-q+1 軌道 × q^2+q+1 点)・Baer 基準 (全直線 1 または q+1 点・
   (q+1)-secant ちょうど q^2+q+1 本)・軌道対 union の全直線交差 >= 2。
3. 期待される新上界 (witness つき): **PG(2,121) <= 266 (2*(121+11+1)) < 363**、
   **PG(2,169) <= 366 (2*(169+13+1)) < 507**。
4. メモリ上限・実行時間で q=13 が完了できない場合は q=11 のみで正直に報告
   (失敗・未完は明記)。

## 主張の区別

- 有限機械検証 (q=11, 13 の全数) のみ。一般定理は前段どおり Bruck の引用。
- min の下界は主張しない。
- 標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・
  S2・全 closure class は全時点 UNKNOWN・verdict 不消費。

## 出版計画

- research/experiments/baer-partition-q11-q13-20261128/ (scripts + out + MANIFEST)
- K1374 への evidence addendum (同じ命題の検証範囲拡大のため同一K項目を更新)
- research/log/2026-11-28-baer-partition-q11-q13.md (完了log)
