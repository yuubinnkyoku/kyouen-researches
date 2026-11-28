# Baer partition (Bruck) 検証の q=11・q=13 拡張

- 宣言: `709c8515` (HEAD pin 60c712c0・publish-then-execute・単一オーナー)
- 前段: 宣言 `862293aa` + amendment `f359c5c5` + kit+K1374+log `60c712c0` (q=2..9)

## 結果

- **q=11 (PG(2,121))**: N=14763 点/直線・Singer 部分群軌道 111 枚 × 133 点・
  Baer 基準全軌道 PASS (per-orbit プロファイル {1:14630, 12:133})・
  軌道対 union 266 点 = t=2 witness (全直線交差 >=2・
  witness プロファイル {2:14497, 13:266}) → **PG(2,121) <= 266 < 363 = 3q^2**。
- **q=13 (PG(2,169))**: N=28731・軌道 157 枚 × 183 点・
  プロファイル {1:28548, 14:183}・witness 366 点
  (プロファイル {2:28365, 15:366}) → **PG(2,169) <= 366 < 507 = 3q^2**。
- design 検査 (点/直線数・直線サイズ 122/170・点次数・2直線交差 1 点
  (seed 固定 2,000 サンプル))・Singer 商位数検証 (gamma^N ∈ K* かつ
  gamma^{N/d} ∉ K*) 全 PASS。

## 実装・限界 (正直な開示)

- 実装1 (GF(p^{2m}) 塔) のみ。スクリプトは前段 kit と同一
  (baer_partition_impl1.py) から2点のみ変更:
  (a) factor_pp が 11, 13 をサポート、
  (b) 生成元位数の O(ordE) 追加ループを ordE > 600,000 で skip
  (factor test gamma^{ordE/f} != 1 (all prime f) は位数の完全検証として
  数学的に十分なため。q=2..9 の結果はループありでも検証済み)。
- **実装2 (GF(p^{6m}) 直接構成) は q>=11 で不使用**: gamma 探索が
  packed range p^{6m} (q=11 で 11^12 ~ 3.1e12) を走査するためスケール外。
  q=11, 13 は単一実装による検証 (design・Baer・位数の多重チェックあり)。
- 実行時間: q=11 で 57s、q=13 で 161s (Python 3.12・純 Python・決定的)。

## 再現

```sh
python3 scripts/baer_partition_impl1.py 11 out/impl1_q11.json
python3 scripts/baer_partition_impl1.py 13 out/impl1_q13.json
```

- 主張は有限機械検証のみ。一般定理は前段どおり Bruck の引用。
  min の下界は主張しない。
- 標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・
  S2・全 closure class は全時点 UNKNOWN・verdict 不消費。
