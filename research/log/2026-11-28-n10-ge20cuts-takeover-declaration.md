# 2026-11-28 takeover 宣言: 停滞 n10 ge20_cuts / |S∩T|=j 場合分割レーンの引き継ぎ（単一オーナー）

## 背景: 先行所有権の確認と本レーンの位置づけ

- 10×10 20石安全集合の SAT 判定（K0141）は先行実験
  `research/experiments/n10-twenty-stone-sat-20261115`（2026-11-15 高速レーン・IN FLIGHT）が所有する。
  同実験の README は (a) plain ge20 CNF の45分 INDET、(b) ge20_cuts 単発実行の3回連続環境損失
  （13:41Z / 16:05Z / 17:26Z・いずれも結果未記録）、(c) 場合分割方式への転換と再開手順・
  md5 照合手順の公開、(d)「長期レーンへの移管も選択肢」と明記している。
- 2026-11-15T17:32Z 以降、同実験への新規コミットは 2026-11-25 の誤commit復元
  （7baa6542・内容復元のみ）のみで、判定の進展は12日間ない。
  2026-11-20 の別レーン宣言も本問題を「並走レーンが所有」として非対象にしている。
- repo には停滞レーンの takeover 先例（9c5bca70: 2026-11-21 wsearch35 レーンの単一オーナー
  takeover 宣言）がある。本宣言はこれに準拠する。
- 本セッションは先に `2026-11-28-n10-twenty-stone-sat-declaration.md`（e6d8c24a・plain ge20 の
  自前符号化による判定）を出版したが、その後この先行所有権を確認した。
  **first-published-priority に従い、本 takeover 宣言をもって先行レーンの手法・資産を引き継ぎ、
  自前の plain 攻撃は停止する。** e6d8c24a の自前符号化は独立較正資産として記録する。

## 自前 plain 実行の honest negative（停止時点の記録）

- 自前新規符号化（forbid.py / encode4.py・詳細は e6d8c24a 宣言どおり）:
  F_10=54,441 が K0057 の既刊値と一致（先行実験の独立再現）。7×7=6,364 / 8×8=14,564 / 9×9=29,152
  の既刊アンカー完全一致、n=4 (max 7) / n=5 (max 9) brute-force 全較正 PASS、
  19石証人 0/3,876 違反再確認。kissat 4.0.4 公式 linux-amd64（binary sha256 21da5d98…）。
- plain ge20 (seqleast, 2100 vars / 64,203 clauses): 270s cap で **INDET 6,655,245 conflicts**
  （24,688 conflicts/s）。長時間走（背景・selmax との CPU 共有）はそれぞれ
  ~764,708 / ~646,574 conflicts 時点で本セッションが停止（無 verdict）。先行レーンの45分 INDET と整合。
  **plain ge20 の無条件 UNSAT は本レーンでも未取得のまま（長期レーン課題として維持）。**
- CPU quota 実測: cgroup cpu.max = 1.0 CPU。kissat は同時1走のみ（先行レーンの排他運用則と同一）。

## 引き継ぎ実行計画（先行 README の再開手順をそのまま機械実行）

1. 作業dirに先行実験の4 script（build_n10_sat.py / build_n10_cuts.py / split_ge20cuts.py /
   n10_split_driver.sh）を main から取得し、MD5 照合・制御 K1-K4 を再実行 PASS させる。
2. base CNF `n10_ge20_cuts.cnf` を再生成し **md5 584087313e50ec614e3c35c1935d224e 照合**。
3. split_ge20cuts.py で10サブCNF（tj0..tj9）を再生成し、出版 `split_gen.log` の10 md5 と完全一致を確認。
4. driver（CAP=3300s・1走ずつ逐次・jsonl comma-anchored skip）を背景起動し、
   完了した record から**随時 main に出版**（環境リセット越えの resumability。
   先行 driver の KS path は本環境の binary に置換するのみで、CNF・判定は不変）。
5. 判定規約は先行 README「結果の解釈」どおり:
   - 全 tj UNSAT ⟹ base cuts CNF UNSAT ⟹ (X1)/(X2) 完全列挙の前提で **K_10 ≤ 19**、
     19石証人と合わせ **K_10 = 19**（K0035・K0141 の決着・新規 K 項目）。
   - いずれかの tj が SAT ⟹ 模型から20石 witness を復号・行列式独立検証の上 **K_10 ≥ 20** を出版。
   - 予算内に決着しない場合は INDET 記録のみ出版（不在主張はしない）。
6. 11×11 掃引・重い root 証明は実施しない。標準11×11空盤・19 central-reply roots・二石 root {60,27}・
   第三手 {100,108}・S2・全 closure class は全時点 UNKNOWN・verdict 不消費・conflicts は bookkeeping。

- HEAD pin: 9e401db4a76cfffc058f9a0c4d7bfb1d78b320f2（本宣言時点の main）
- 実行環境: 本セッション sandbox（ユーザーPC到達不可・GitHub API 出版のみ）
