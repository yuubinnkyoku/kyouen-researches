# 2026-11-18 five-row q=7 band-closure resume（高速レーン・環境復旧後の再開・較正と m=38,39 の決着）

## 概要

band-closure レーン（five-row-q7-band-closure-35-157-20261115・IN FLIGHT）は
2026-11-15 の実行環境長時間障害で m=50 が中断され、m=38, 39 と m=50..157 が
未実行のままだった。今回環境復旧後に**レーンを再開**し、再開時較正（決定性の
bit-exact 再現）を経て **m=38, 39 をともに UNSAT（完全な欠損極大非存在証明）**
で決着した。witness-free 幅集合が {19,...,37} ∪ {40,...,49} から
**{19,...,49}**（連続帯に接続）に拡大し、(5,7) の鋭い形は
**M_{5,7} = 19 または M_{5,7} ≥ 51** となった。掃引は引き続き m=50..157へ。

## 実施

- 着手前に最新 main（5852797c 以降を再取得）で records.jsonl が m=35,36,37,40..49
  の13幅のまま（他レーンの追記なし・並走衝突なし）・class-split レーンは m=37 まで
  （K0851）で m=38 以降の帯は本レーン専用であることを確認。
- **再開時較正（決定性の錨）**: m=35 の def-mode CNF を genfast3（blob sha
  24fa7ed7d7cb8c7101c8356b7ba77a3c7e62b29e・七行/六行レーンと同一バイナリ）で
  再生成し、meta が既存 record と完全一致（vars 9604・clauses 34349・curves 244）・
  md5 も既存設計と同一。kissat 4.0.4（md5 3a5eba830aa6008a604fcc9bbe99a325）
  再実行で **conflicts 2,809,004 が published record と bit-exact 一致**
  （process-time 112.5s vs 記録値 108.3s はホスト依存の wall 系・決定性の
  アンカーは conflicts）。生ログを `output/raw/kissat-5x35-q7-def-recal.txt`
  として保存。これで環境復旧後のスタック（node・genfast3・kissat）が
  2026-11-15 の記録生成環境と決定的に同一であることを確認した。
- **m=38**: genfast3 def-mode CNF（vars 10669・clauses 38171・**curves 271**
  は第三系全帯予測表 ts-census-fullband.json の 271 と一致）→ kissat
  **UNSAT (rc=20)・conflicts 2,337,347・90.7s**。5×38 欠損極大非存在の
  完全証明（1インスタンス）。生ログ `output/raw/kissat-5x38-q7-def.txt`。
- **m=39**: CNF（vars 11024・clauses 39445・**curves 280** は予測表 280 と
  一致）→ kissat **UNSAT (rc=20)・conflicts 2,257,859・90.1s**。5×39 欠損極大
  非存在の完全証明。生ログ `output/raw/kissat-5x39-q7-def.txt`。
- conflicts 系列（def-mode）: m=35: 2,809,004 → m=36: 2,653,429 →
  m=37: 2,464,961 → **m=38: 2,337,347** → **m=39: 2,257,859** → 
  m=40: 1,836,713。m=38, 39 は既存の漸減傾向を外挿した予想域
  （~2.3M）に乗っており、m=38 で +2.1M 台から m=40 の平台帯への
  遷移が連続的に埋まった（決定論的 per-width 完全証明なので外挿は
  参考·satisfiability 判定そのものは計算に依る）。
- records.jsonl は15行（m=35..37,38,39,40..49）に更新し、resume 用の
  sweep driver（scripts/sweep_driver_5xq7.sh・records.jsonl 重複回避・
  curves 予測表照合・230s cap・INDET 記録を含む）を scripts/ に追加。
- 生 kissat ログ3件（m=35 較正・m=38・m=39）を `output/raw/` 下に
  batch push（2026-11-15 の「生ログは環境復旧後に batch push する」の
  実行）。

## 境界の更新

- (5,7): witness-free 幅集合 {19,...,37}∪{40,...,49} → **{19,...,49}**
  （初の50幅連続 witness-free 帯）。集合形式:
  M∈{19,...,49} または ≥50。鋭い形（K0821 監査規約）:
  **M=19 または M_{5,7} ≥ 51**。
- m=35..49 の15幅はすべて def-mode UNSAT で各幅の完全証明。m=35..37 は
  class-split レーン（K0849/K0850/K0851）との独立符号化二重決着済み。
  上界 158（K0332・全称証明）は不変。

## 備考・レジューム

- 残る帯: **m=50..157（108幅）**。driver は `scripts/sweep_driver_5xq7.sh`
  （resume-safe・実行済み幅の重複回避込み）。conflicts の定点観測:
  m=44..49 は 1.36M..1.79M の平台帯・外挿では m=50 代も2〜3分/幅の
  見込みだが 230s cap を超えたら INDET を正直に記録し rowY=0/1/2 分割へ。
- 全幅 UNSAT が完走した時点で **M_{5,7} = 19 exact**（w=5 初・q=w+2 では
  (6,8) に次ぐ例）として K 項目化・research/knowledge/README.md の
  読解順序行を更新する（K0851/K0849 チェーンの関係更新も）。
- SAT 幅が出た場合は即停止・witness を dual-verify して下界更新として記録。
- push 前の最新 main 再取得・fast-forward 競合時の再取得+再pushは
  2026-11-15 の class-split レーンの運用手順に同じ。
