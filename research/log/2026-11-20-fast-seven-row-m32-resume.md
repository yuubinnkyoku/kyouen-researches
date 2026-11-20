# 2026-11-20 高速レーン: K0827 未反映実験の反映と (7,6) m=32 class-split 再開

高速レーン (work/fast)。K0827 のアペンド運用に従い、実験 dir のみ出版され
knowledge へ未反映だった 2 記録を反映した。境界値はどちらも不変。

## 反映 1: 7×60・q=4 の 1 石移動近傍完全列挙負 (2026-11-16 実験)

seven-row-q4-width60-one-swap-20261116。base53 と foundB_7x59 の 2 seed から
1-for-1 全候補を完全列挙（各 1,142 候補・安全 276/313・safe-maximal 0）。
C++ 外積/整数行列式と Python 正規化整数方程式の 2 方式完全一致。
width-59 の 2-for-2 負記録と合わせ、2 seed の 0/1/2 等数交換近傍を閉じた。
局所負であり M_{7,4} ∈ [60,1929] 不変・不在主張なし。

## 反映 2: (7,6) m=32 class {3} class-split の較正と未決 (2026-11-18 実験)

seven-row-q6-m32-class-split-20261118。
(7,30,6) c3 対照 end-to-end bit-exact PASS（CNF md5・SAT conflicts 2,670,296・
witness 同一配置・2 系統検証）。本命 c3_7x32 は 2 回の実行環境障害で未決
（12.4M+ conflicts 到達・同一決定経路通過確認）。判定保留の honest record。
M_{7,6} ∈ [32,862] 不変・前線 7×32。

## 本日の再開 (2026-11-20)

- c3_7x32 の resume を単一オーナーとして着手（宣言 commit e30cec0a）。
  cap 14400s・kissat 4.0.4 デフォルトオプション・CNF md5 bc10c516… byte-exact
  再生成・kissat md5 3a5eba83… rel-4.0.4 asset 再照合。
- 判定 (SAT なら M_{7,6} ∈ [33,862]・witness は 3 系統検証後に反映、
  UNSAT なら class {3} 限定の負記録・不在主張ではない、cap 到達なら INDET)
  は実験 dir と K0827 に追記して反映する。
- 備考 (運用): 2026-11-20 19:0xZ に実験 README 一時的に破損 push が発生
  (commit c75767fa・公開 ISR の転写事故) → 直後に byte 復元した
  (commit e30cec0a)。復元は afd5046663 の blob から実施・内容は復旧済み。
