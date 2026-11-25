# 2026-11-15 (4,21,5) 高速レーン: SA pin-sweep (環境停止下・sandbox のみ) と blocker 円ケース分割の設計

## 経緯

- 13:41Z の実行環境全面停止 (bash/file_system 不能) を受け、GitHub API
  (github_app) + run_typescript sandbox (純TS) のみで class-split の最難バケット
  c0k3p0/c0k3p1 の構造探索を実施した (成果: four-row-q5-m21-sa-pinsweep-20261115)。
- sandbox 制約を実測して回避した設計 (再利用用に記録):
  (1) 実行 ~60s 相当の process safety deadline、(2) メモリ ~16MiB、
  (3) Math.random / Date.now は recorded-ops 上限に触れるため自前 xorshift32
  (リテラル seed) + 固定 ITERS で予算管理。census は Map 禁止 ->
  正規化円係数 4 本配列 + sort + ランレングスの計数法
  (C(k,3)>=10 <=> k>=5 の判定と C(k,3) 一致の sanity check つき)。
  Node 参照実装 (scripts/sa21.js) は同一アルゴリズムで第二実装として検証。

## 発見・成果

1. census 再現: 538 円 (5/6/8点 = 180/340/18)、非共線3点組 89,228 — 既存記録と一致。
2. (20,0)/(0,0) を通る >=5点円は各19本、共通は
   g* = {(0,0),(4,2),(9,3),(11,3),(16,2),(20,0)} の1本のみ (6点・V対称)。
3. m=20 witness は 4x20 で safe・極大 (count-4 円15本 + 満杯行3本) — 較正 PASS。
4. p1 seed (m=20 witness の V 像 offX=0 移植) は 4x21 で U=1・未遮断 (20,0) のみ
   — surgery レーンの移植結果 (T'={(20,3)}) と一致。
5. SA 合計 ~11.3M iters (自由 2.0M+1.8M+1.2M・ピン掃引 83x12k + 86x13k・
   2段階 57x25k・深掘り 900k+900k+500k) で witness (U=0) に未到達。
6. 厳密な局所事実 (有限全列挙): p1 seed から深さ2 escape なし・
   U<=1 多様体は p1 seed / p0 ci79 / p0 ci31 すべてサイズ1 (孤立)。
   p1 seed の全隣接は U>=2 (フラグなし169 / バケット固定あり164)。
7. **blocker 円ケース分割の設計**: バケットを「(20,0) 石」(unit 1本) と
   「(20,0) 空」((g, 4-subset) ピン: p1 83 / p0 86) に完全分解 (計 84/87 インスタンス)。
   x2 分割と直交。sat4.js 方式の unit pin で実装可能。

## 判断・方針

- SA の負結果は witness 不在の証明ではないため、K 昇格・records.jsonl 更新は
  実施しない (実験 README + 本 log + summary JSON で記録)。
- push 直前に最新 main を再取得して class-split README に追記した
  (並走レーンが活発なため、fast-forward 競合時は再取得・再構成で対処)。

## 引き継ぎ (実行環境復旧時の優先順)

1. c0k3p1 deep (deepcap.sh v2, CNF md5 059fc19d...) 再 launch。
2. x2=4 対照の kissat SAT 実証 (sweepp0x2.sh 起動前の必須較正)。
3. blocker 円ケース分割 (sat5.js 相当: --gpin g,S) の実装と掃引。
4. sa21.js (Node) での大規模 SA 再実行 (sandbox 制約の外のスケールで、
   hill-climb (--anneal 0) と焼きなまし (--anneal 5) の比較も)。
