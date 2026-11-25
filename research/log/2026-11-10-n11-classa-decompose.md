# 2026-11-10 n11 best-S3壁のclassA完全分解 + S4-C発見

- 背景: K0685の鎖監査は120 S2のbest-S3 blocker分布（最小60〜最大115、合計13,244）を
  残した。q59ノートは壁のclassA/classB分解（32/13,212）を合計でのみ記録し、
  per-S2の内訳とclassAの構造的起源を未確定のまま次の一手3としていた。
- 実装: 純TS BigInt盤 + 4×4整数Bareiss（verify_five_terminal_loss7.pyと同一式）。
  W4(s4) を「s4 ⊂ FIRST_WIN78 の五石位置」に単紮化した（F ⊇ S4 のとき F\S4 は
  F の一般位置性から自動的に S4 の合法手であるため、S4ごとの合法子列挙が不要）。
  blocker_of(s3) = legal(s3) & ~fcov(s3) のビットマップ差分のみ。
- 再現: best_per_s2 分布 {60:2, 75:2, 106:1, 110:43, 111:8, 112:3, 113:49, 114:3, 115:9}
  ・合計13,244が旧計測（chain_blockers.py + audit_cache）と完全一致。
- classA完全分解（T1）: blockerのuniverse子は必ずSW16。classA>0は8 S2のみ
  （q ∈ {11,28,35,41,47,59,61,69}）、計32件。classA t の全リストはK0724参照。
  残り112 S2のclassA=0は3機構: (i) q universe不出現62件、(ii) q含む位置が
  全FW（50件、代表q=51）、(iii) best S3がuniverse外（10件）。
- S4-C発見: universe 94位置のうち5位置は S4-A/S4-B のどちらの子でもなく、
  すべて {51,59,60,61,x}（x ∈ {44,45,66,67,68}、全FIRST_WIN）。
  第三の四石親 S4-C = {51,59,60,61} が存在し、6番目の子 {51,59,60,61,69} は
  S4-Aと共有。S4-CはFW oracle上の先手勝ち四石位置（K0676型）。
- 限界: すべて78先手勝ちoracle下の条件付き計算。空盤・二石rootはUNKNOWN。
- 今後: 32 classA blocker S4のS6/S7照合、S4-C残り合法子のsweep、
  q56反映（repo書き込み403のため本日は未反映; K0723/K0724ともドラフト保存中）。
