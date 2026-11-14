# 2026-11-14 高速レーン: SAフロンティア第3弾 — M_{6,5}≥29（6×28・22石）と新前線の抵抗

- 開始時点で最新 main を確認（HEAD dc41b02b・並走は class4-lane cost-78 sweep・
  3701-3899 census・sa-frontier2 第2弾で主題独立）。AGENTS.md・
  research/knowledge/README.md・K0811・mwq CSV・CSV/README 現状を再確認。
- K0811/sa-frontier2 のレジューム「(6,5) m=28 の長時間攻撃」を実施。
  SA 機は sa-frontier-extension-20261114 版を verbatim（census・独立検証器無改変）。
  新規ドライバ variant_attack.js（パラメータ明示・JSONL即時追記）と
  reverify.js（JSONL→別プロセス独立検証）を追加。
- 2×8 q=4 制御で K0796 を再発見（機材健全性確認）してから本番。
- **(6,5) m=28 を22石（2石欠損）で発見（seed 303・T0=1.5/mrf=0.45/sK=36・
  74秒）→ M_{6,5} ≥ 29**（旧28）。in-machine 独立検証 + reverify.js による
  別プロセス再検証とも safe+maximal PASS。並走 sa-frontier2 は同一 m を
  10 run・~10分で非発見と記録した直後で、パラメータ帯の違い（T0≥2.0 系のみ）
  による突破。非発見が不在を意味しないことの最も直接的な再実証。
- (6,5) で初の2石欠損witness（従来の23石は1石欠損のみ）。行構成 4,4,4,4,2,4。
- 抵抗（非発見の記録）: (6,5) m=29 計8 run・m=30 2 run・m=28 発見後6 run
 （21石未探索残）・(6,6) m=22 2 run（累計7）・(5,7) m=19/20 各2 run。
  全23 run・witness座標・検証詳細は実験 output/results.jsonl。
- SAT（K0810 機 verbatim）: 6×28 census 240直線+4,274円（SA機と一致）。
  6×28/6×22 の row-deficient SAT は単発280秒予算で決着せず —
  6×29 UNSAT（=M_{6,5}=29 確定）は長期レーン向け残作業。
- 反映: 実験 research/experiments/sa-frontier3-20261114/（scripts 2・output・report）・
  本 log・K0811 更新（下界28→29・coverage m=22..28・抵抗 m=29/30・artifact 追加）・
  mwq_stabilization.csv (6,5)行 29..658 更新・fixed-width README の bounds 行更新。
  1コミット1ファイル・読み戻し検証。
- 次の一手: (1) 6×29 SAT UNSAT（確定なら (6,5) は exact-threshold 化）、
  (2) 22石構造（深い欠損行1つ+満容量行5つ）の一般 w への構造族分析、
  (3) (6,6) m=22・(5,7) m=20 の長時間攻撃。
