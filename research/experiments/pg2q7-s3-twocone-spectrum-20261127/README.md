# PG(2,7) s=3 完全Grundyスペクトラム (2錐法)

- 宣言: `research/log/2026-11-27-pg2q7-s3-twocone-spectrum-declaration.md` (commit 98fed922, publish-then-execute)
- 完了log: `research/log/2026-11-27-pg2q7-s3-twocone-spectrum-completion.md`
- 盤: PG(2,7) (57点・57直線・各直線8点・F7)。s=3 共演ゲーム
  (安全集合 = 各直線上の点数 ≤ 3、通常プレイ、g(S)=mex)。
- 手法: 2錐拡張 (宣言の新規補題)。
  恒等式 (m≥3): **N_m(g)·C(m,3) = N3nc·D_m(g) + N3c·D'_m(g)**
  (N3nc=26,068 非共線3点組 / N3c=3,192 共線3点組 = 57·C(8,3))。
  錐A = 非共線3点組Fを含む全安全集合 (75,876,952局面・最大サイズ15)、
  錐B = 共線3点組F'を含む全安全集合 (52,197,741局面)。
  各錐でディスク層binary列挙 → ping-pong radix sort (lo,hi,idx) →
  ストリーミングボトムアップ mex DP (子はsorted配列の二分探索)。
  m≤2 と空盤は直接鎖計算。

## 主結果 (output/combined_fset0.json)

- 全安全局面数 (m=0..15): **15,387,092,450** (m≥3は 15,387,090,796)
- 最大安全サイズ: **15** (層15: 錐A 1,275 / 錐B 735 → N_15 = 78,204)
- Grundy値の範囲: **0..6** (最大Grundy 6 は m=8 に出現)
- g(∅)=1, g(単点)=0, g(2点)=1, g(非共線3点組)=g(共線3点組)=0
- サイズ別 Grundy 分布 N_m(g) は combined_fset0.json の grundy_tables。
  顕著な観察 (有限・この盤のみ):
  - m=4: 全 391,020 局面が一律 G=2
  - m=9: G=5 が出現 (764,835,120・全体の約30%)
  - m=13..15: G∈{0,1} のみ (鎖の収束)
  - 極大サイズは 9,11,12,13,14,15 に分散 (偶奇混在 → K1298 パリティ定理と整合的に G≥2 が実際に出現)
- 極大 (m≥9): N_9^max=26,068 (数値が非共線3点組の総数 N3nc=26,068 と一致する。構造的説明は未提出・偶然一致の可能性を残す open question),
  N_11^max=20,176,632, N_12^max=335,964,384, N_13^max=180,182,016,
  N_14^max=6,569,136, N_15^max=78,204。
  (K1365 の補集合双対 (極大安全↔極小t-fold blocking) との照合は今後課題。)

## 検証ゲート (全て PASS・fail-closed)

1. 整除性: 全 (m,g) で恒等式が厳密成立 (両fsetで全セル)。
2. 解析アンカー: N_3=29,260 / N_4=391,020 / N_5=3,988,404 に全一致
   (C(57,3) / C(57,4)−57·C(8,4) / C(57,5)−57·(C(8,4)·49+C(8,5)))。
3. F不変性: fset=1 (別F・別F') の全パイプライン再実行で combined JSON 全表一致。
4. 決定性: fset=0 錐A dp の再走で dp_result.json byte同一
   (output/determinism_verdict.txt)。
5. 独立Python (別構成のPG(2,7)実装・ビットマスクDFS): 両錐の層サイズ m=3..7 完全一致。
6. tamper電池 5種 (G値・層サイズ・アンカー・極大・総数の改変) 全て検出
   (output/tamper_battery.txt)。
7. 較正: two_cone.js は PG(2,3) s=3 (K1356) と PG(2,5) s=3 (K1361) の
   出版値に全セル一致。ストリーミングdp版 spectrum.js も PG(2,5) 全パイプラインで
   出版表を再現 (calibration/ 参照)。

## honest disclosure

- これは単一手法 (2錐+恒等式) による初測定。Grundy表そのものは
  恒等式による相互整合・アンカー・独立低層再現で強く支持されるが、
  全15.4G局面の第二完全実装による再現はまだ無い。
- 総数の外部アンカーは m≤5 の解析値 + 低層 (m≤7) の独立再現のみ。
- 11×11 標準盤・19 central-reply roots・root verdict は一切消費していない
  (全時点 UNKNOWN)。

## 実行方法

```
node spectrum.js enum nc 0 DIR/nc 7 3   # 錐A列挙
node spectrum.js enum c  0 DIR/c  7 3   # 錐B列挙
node spectrum.js dp nc 0 DIR/nc 7 3     # 錐A mex DP
node spectrum.js dp c  0 DIR/c  7 3     # 錐B mex DP
node combine.js DIR/nc/dp_result.json DIR/c/dp_result.json 7 3 > combined.json
python3 check_gates.py combined.json    # ALL GATES PASS
python3 verify_py.py                    # 独立低層検証 (要 /tmp/q7/combined.json)
```

- 実行環境: Node v22, RAM cgroup 1GB, 2 CPU。dpは m=11 (27.7M層) で
  ストリーミング+ソート分割によりメモリ峰值 ~450MB。
- run_q7.sh / run_q7_f1.sh が全工程を自動実行する。

## ファイル

- scripts/: spectrum.js (enum/dp), combine.js, two_cone.js (較正用メモリ内実装),
  check_gates.py, verify_py.py, run_q7.sh, run_q7_f1.sh
- output/: combined_fset0.json (主結果), combined_fset1.json (F不変性),
  dp_{nc,c}_fset{0,1}.json/.log (錐素表), determinism_verdict.txt,
  tamper_battery.txt, calibration/ (PG(2,3)/PG(2,5) 較正と錐サイズ事前測定)
- MANIFEST-sha256.txt: 全ファイルのsha256
