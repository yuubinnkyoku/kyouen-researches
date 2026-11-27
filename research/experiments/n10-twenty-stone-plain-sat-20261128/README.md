# n10 20石 plain SAT 攻撃（独立第2符号化）— honest negative と独立較正資産（2026-11-28 高速レーン）

## 位置づけ

- 本実験は宣言 e6d8c24a（research/log/2026-11-28-n10-twenty-stone-sat-declaration.md）に基づき実行し、
  その後の takeover 宣言 cc152b71（research/log/2026-11-28-n10-ge20cuts-takeover-declaration.md）で
  先行レーン（n10-twenty-stone-sat-20261115）の手法に合流した。
  本 dir は **plain ge20（カットなし）の独立符号化による honest negative と較正資産**を保存する。
  K_10 の判定主体は takeover 先の |S∩T|=j 場合分割（先行実験 dir 参照）。

## 独立符号化（先行実験のコードは不使用）

- `forbid.py`: 4×4整数行列式 det[[x²+y²,x,y,1]]=0 による禁止四点組の全列挙（円・直線を統一）。
  F_n を n=4..10 で新規測定: 194 / 826 / 2,491 / 6,364 / 14,564 / 29,152 / 54,441。
  既刊アンカー（7×7=6,364・8×8=14,564・9×9=29,152）と完全一致、
  **F_10=54,441 は K0057 と先行実験の独立再現**（3系統一致）。
- `encode4.py`: 変数1..100、禁止四点組は4項否定節。基数制約は2系統:
  - seqleast: Sinz 型逐次 at-least-k カウンタ（下向き節込み・健全かつ完全）
  - selmax: セレクタ u（exactly-one(x,u)・u⟺¬x）+ Sinz at-most-(100-k)
  両モードとも n=4（brute force 最大7）・n=5（同9）の全較正点で SAT iff k≤max を完全再現。

## 制御

- K0035 の19石証人（WIT）: 全3,876四点組で禁止0違反（再確認）。
- k=19 (seqleast, 2000 vars / 63,705 clauses, md5 da6e34647ec9e7dcbc9cbeaa206da7c8):
  **SAT・12,433 conflicts・3s**。模型から**先行2系統とは異なる第3の19石安全配置**
  W3 = [0,2,4,16,17,18,32,35,36,49,50,51,61,64,78,88,89,93,99]（点番号 x+10y）を復号し、
  行列式独立検証で 0/3,876 違反を確認（k19_model.json）。
- k=20 (seqleast, 2100 vars / 64,203 clauses, md5 7c911d9e1e3b0de4e1678b038495ad8a):
  **INDET・6,655,245 conflicts @270s cap**（24,688 conflicts/s）— 判定未取得。
  selmax (md5 6423324745ac5241eaef21164979a8e6) の長時間走は ~646,574 conflicts で停止（無 verdict）。
  先行レーンの plain 45分 INDET（ge20_plain_indet.json）と整合。**plain の無条件判定は長期課題のまま。**

## 実行環境

- kissat 4.0.4 公式 linux-amd64（zip sha256 63282e51…・binary sha256 21da5d98…・先行レーン pin と同一）。
- cgroup cpu.max = 1.0 CPU 実測。単発 24,688 conflicts/s。
- CNF は size policy により非出版（md5 のみ記載・スクリプトで再生成可能）。

## 11×11 帰属

標準11×11空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・全 closure class は
全時点 UNKNOWN・verdict 不消費・conflicts は bookkeeping。
