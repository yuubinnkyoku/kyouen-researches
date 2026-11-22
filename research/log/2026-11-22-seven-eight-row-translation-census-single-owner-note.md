# 単一オーナー宣言: 七行・八行家族の純並進 census と targeted bounded surgery（2026-11-22 高速レーン）

- 宣言時刻: 2026-11-22T01:50Z
- 宣言時 HEAD: `646e9d3fdc`（2026-11-22T01:49:30Z を直前 push 前に再取得して確認）
- 実験 dir（予定）: `research/experiments/seven-eight-row-translation-census-20261122/`
- セッション log（予定）: `research/log/2026-11-22-seven-eight-row-translation-census-session-log.md`
- 対象: 七行 (7,4)/(7,5)/(7,6)/(7,7)/(7,8)・八行 (8,9)/(8,10) 家族の frontier 幅に対する
  (a) 既出版 witness の D4 像 × 全並進による被覆 census（R(S) 測定）、および
  (b) census argmax 配置（frontier−1 幅で first-uncovered が 1 cell の配置）周りの
  targeted bounded surgery（追加石を T-curve 上に置く完備クラス: 1R1A・2R1A・2R2A・必要なら
  3R2A-both-adds-on-T-curve）。

## スコープ（fail-closed）

1. census は既出版 witness（(7,4): m=53 base と 7×57 pair0/pair1・(7,5): m=33/winA/winB/winC・
   (7,6): m=30/m=31・(7,7): m=25/m=26・(7,8): m=24・(8,9): m=27/m=28・(8,10): m=25）を対象とし、
   浮動小数点を使わない BigInt 整数演算エンジン（円は格子点列挙可、直線は2次方程式判別式）で
   D4 像 4種 × 全並進の R(S)（左フラッシュ正規化で翻訳被覆できる最大幅）を測る。
2. エンジンは (6,4) m=46 anchor（K1211 出版 placements 340/340）で較正し、決定性
   （2回実行 byte 一致）を確認済みであること。
3. surgery は正の対照 3つ（winA→winC on 7×35 T=(34,0) / m30→m31 on 7×31 T=(30,3) /
   base53→pair0,pair1 on 7×57）を必ず通す。対照落ちの場合は本レーンの surgery 成果は出版しない。
4. 独立検証: hit は Python Fraction 検証器（新規に書く）と JS エンジンの相互検証、
   tamper 対照、および新 witness への census 再実行（R(S) 連鎖の確認）を含む。
5. 主張の形式: census の R(S) 表は「この witness の純並進では target−1 で止まる」という
   scoped な事実としてのみ出版。surgery hit は当該クラス・当該 T の近傍に witness が見つかった
   という scoped な下界更新として出版し、不在主張は一切しない。nodes・候補数を勝敗として読まない。
   11×11 空盤・二石 root・class 1/2/4 は非接触で UNKNOWN のまま。
6. 重複回避: (7,4) width-60 の 2R2A（two 2-for-2 neighborhoods）は既に出版 negative
   （CSV note）のため本レーンでは実施しない。(7,4) では 1R1A/2R1A（未実施クラス）のみ行う。
7. 並走レーンとの分離: six-row (6,5)/(6,6)/(6,7) の band extension・frontier crunch 各レーン、
   n11 class-2/s4bd/sixth-cost 各レーンの path・K item には触れない。K 番号は push 直前に
   404 確認 + README grep で重複回避する。

## 経緯

本宣言より前に、同一セッション内で census を完了済み（全 seed 出力は手元にのみ存在し未出版）。
surgery エンジン構築・対照実行・本番実行をこれから行う。成果はすべて 1. の実験 dir に集約し、
manifest-sha256.json を添付して出版する。
