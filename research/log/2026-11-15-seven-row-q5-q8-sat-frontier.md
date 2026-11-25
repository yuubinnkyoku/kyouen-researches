# 2026-11-15 seven-row q5..q8 SAT frontier（高速レーン）

## 実施内容

seven-row-q5-q8-sat-frontier-20261115（IN FLIGHT claim 97153337 の執行・第2回）。
7行 q≤w 族の witness 帯前線（(7,5) 7×33・(7,6) 7×28→7×30・(7,7) 7×27・(7,8) 7×25）を
sat3.js streaming census（sat2 と9対照 byte-identical・rowfixed q5 は新規バイト一致較正 2/2）+
kissat 4.0.4 で掃引。第1バッチ（cdd25a11..25d4ca02）に続き、900s cap の
バックグラウンド実行（setsid nohup 2並列・1コマンド ~290s wall 制限の回避）を追加。

## 結果

1. **(7,5) 7×33 SAT**（rowY=0 分割・655,159 conflicts・835.7s・cap 900）:
   27石単一欠損 witness rows [3,4,4,4,4,4,4]・js+py 2系統検証 PASS。
   第1バッチの全4ミラークラス 250s INDET（399,206/399,144/344,970/345,432・
   クラス間抵抗ほぼ一様）は **cap 250s→900s の延長で SAT に解決**。
   **M_{7,5} ∈ [34, 1142]**（下界 33→34・上界 K0318 U=1142 不変）。
   m=34 への空列延伸は cell (33,0) 未遮断（not-maximal）で失敗。前線は 7×34。
2. **(7,6) 7×28 SAT + 7×29 空列延伸**（第1バッチ・本バッチで統合反映）:
   34石単一欠損 witness rows [5,5,5,4,5,5,5]（rowY=3・442,479 conflicts・137s）。
   同一34石が7×29でも 2系統検証 PASS → **M_{7,6} ∈ [30, 862]**（下界 28→30）。
   m=30 は cell (29,3) 未遮断で延伸失敗。rowY=3 は 280s 929,785 に続き
   **900s cap でも INDET（1,569,306 conflicts）**・rowY=0/1/2 は 250s INDET
   （796,125/822,483/847,765）— 全4クラス cap 内未解決・不在主張ではない。
   前線は 7×30。
3. honest negatives（全4ミラークラス走査の完了）: (7,7) 7×27 rowY=0/1/2 250s INDET
   （2,186,370/2,243,432/2,095,752）で既存 rowY=3（262s・2,242,940）と合わせ4クラス完走。
   (7,8) 7×25 rowY=0/1/2 250s INDET（3,613,768/3,717,333/3,678,867）で既存 rowY=3
   （250s・3,534,747）と合わせ4クラス完走。いずれも不在主張ではない。
4. 空列延伸は全家族前線 witness からは1幅も延伸せず（(7,6) m=28 witness の
   m=29 が唯一の例外）。cap 延長は (7,5) m=33 で有効だった — クラス間抵抗が
   ほぼ一様な前線でも k×minpos 分解の前に cap 延長を試す価値がある観測。

## 証明・検証の状態

- 各 SAT は完全符号化インスタンスでの witness 有限証拠（js: sat.js verifyConfig +
  py: verify_witness.py Python Fraction の2系統検証・records.jsonl に記録）。
- INDET は cap 到達の honest negative で不在主張ではない。
- M_{7,q} の確定値ではなく境界の更新。上界は K0318 代入（1142/862/708/651）。
- 11×11 空盤の勝敗等の無盤面問題には影響しない（固定幅 witness 帯の更新）。

## 運用メモ

- 900s 実行は setsid nohup バックグラウンド2並列で実行（1コマンド ~290s wall
  上限の回避策）。cap 到達時の conflicts は実行速度依存で変動しうる
  （bit-exact 主張は cap 内完了インスタンスのみ）。
- 環境リセット1回（23:58頃・bash 環境が一時利用不可）: 成果は全て文脈内記録で
  喪失なし。CNF md5 はリセット後再生成で全件一致。
- 生 kissat ログ（q5-m33 900s SAT・q6-m30 900s INDET）は環境復旧後の
  後続バッチで追記予定（records.jsonl の cnf_md5・conflicts が正本記録）。

## コミット

- 97153337 IN FLIGHT claim / cdd25a11 第1バッチ / 35d01cbd 第2バッチ（生ログ）/
  90103f3d 第3バッチ / 25d4ca02 第4バッチ / 本コミット: 900s バッチ + 統合反映
  （mwq_stabilization.csv・fixed-width README・K0827・本 log）。
