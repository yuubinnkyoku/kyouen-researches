# 2026-11-14 高速レーン: フロンティア長時間実行 第2報 — 6×30/6×23 直接SAT確認（新同型類）と実行環境アウテージ

前回（94b0296d・6×12 q=8 最小極大=37 確定）の続き。背景: 並走の extend6 深除去レーン
（f46dda3e・eca2325e・b8e0427e）が同日に 6×30 q=5 23石2件・6×23 q=6 29石8件の
witness を発見し、境界を M_{6,5} ∈ [31,658]・M_{6,6} ∈ [24,495] に更新済み
（K0815 第5弾）。本レーンは独立系統（kissat 直接SAT・欠損行単一節・lex無し）で
同じ前線を確認し、さらに前線外側の直接探索をキューした。

## L2: 6×30 q=5 — SAT・第3の同型類（extend6 witness と非同型）

kissat 4.0.4（--time=1800・102,400 vars/357,033 clauses）で **SAT**。
23石 witness（行構成 4,4,4,4,4,3・conflicts 4,001,401・decisions 38,950,217）を
ちょうど予算境界で発見。JS census 不使用検証器・Python 別実装の2系統で
safe+maximal PASS。**H/V/HV の全等距変換で extend6 の2件（行構成 4,4,4,4,3,4）
のいずれとも非同型** — 第3の同型類。
M_{6,5} ≥ 31 の独立確認（境界の変動なし・既に extend6 で [31,658]）。
成果物: encoding-symmetry-kissat-20261114/output/L2_c630_def.json（push済み）。

## L3: 6×23 q=6 — SAT・第9の同型類（extend6 witness と非同型）

同符号化・--time=1500 で **SAT**。29石 witness（行構成 4,5,5,5,5,5・
conflicts 919,243・2分弱）を2系統検証 PASS。
**既知8件（行構成 5,4,5,5,5,5）のいずれとも非同型** — 第9の同型類。
M_{6,6} ≥ 24 の独立確認（境界の変動なし）。
witness JSON は実行環境アウテージで未push（kissat は同一CNFでbit-exact決定的
なため再実行で復元可能・下記レジューム参照）。

## 符号化メモ（両witnessの意味論）

L2 witness の石数 23 = w(q−1)−1 = 6×4−1 と等しく、L3 の 29 = 6×5−1。
いずれも「欠損1行」のギリギリ容量。extend6 の列挙が到達したのは
base witness 近傍のみであり、直接SATはそれ以外の同型類を容易に発見する —
プール相対列挙と直接SATの探索空間が実質的に異なることを示す観測。

## 実行環境アウテージ（2026-11-14 11:40 UTC 頃〜）

L4（5×22 q=6・欠損行単一節・--time=1500）が約1330秒/14.7M conflictsまで
進行した時点で実行環境が一時利用不可となり、bash/filesystem系ツールが全滅。
L4 の verdict（UNSAT なら 5×22 の完全不在証明・SAT なら M_{5,6} ≥ 23）は
未取得。バックグラウンドキュー（L4〜L8・L9〜L11）も停止。
GitHub API 系ツールは生存しており、L2 成果の保護pushは完了。

## レジューム（次回実行）

1. bash 復旧後、krwork（kissat バイナリ・scripts/・results/）の生存確認。
   消失時は kissat 4.0.4 公式バイナリ（arminbiere/kissat rel-4.0.4）を再取得し
   sat2.js で CNF を再生成（いずれも決定的・DIMACSは同一bytes）。
2. キューの再実行（全CNF再生成前提・順序は情報価値順に変更可）:
   - L3re: 6×23 q=6 --deficient 1500s（2分で終了・witness JSON 復元）
   - L4: 5×22 q=6 --deficient 1500s — 前回1330s/14.7Mで未決着の再挑戦
   - L9: 6×31 q=5 --deficient 1800s — extend6 第5弾後の新前線（uOverflow 99.8%の
     陰性しかなく直接SATが最強の攻撃手段）
   - L10: 6×24 q=6 --deficient 1500s — 同上（uOverflow 99%の陰性のみ）
   - L5: 6×21 q=7 --deficient 1200s / L6: 6×19 q=8 --deficient 1200s
   - L7: 5×19 q=7 --deficient --lex=H,V,HV 1200s（K0738–K0759 occupancy 列挙
     UNSAT の SAT 側交叉確認・UNSAT 期待）
   - L8: 5×20 q=7 --deficient --lex=H,V,HV 1500s（K0816 の交叉確認・UNSAT 期待）
   - L11: 5×23 q=6 --deficient 1200s（5×22 が UNSAT だった場合の gap check）
3. 運用メモ: pgrep は無いので /proc スキャンで待機。バックグラウンドは
   setsid nohup … & で起動。postprocess.js の prefix 命名を L4_c522_def 形式に統一。
4. 並走 lane との書き込み衝突に注意（CSV・K0815 は fetch→編集→即push）。

## 現在の境界（本セッションでは変動なし・extend6 と本レーンで一致確認）

M_{6,5} ∈ [31,658]・M_{6,6} ∈ [24,495]・M_{5,6} ∈ [22,249]・
M_{6,7} ∈ [21,402]・M_{6,8} ∈ [19,371]・M_{5,7} ∈ {19,20} ∪ [22,158]。
6×12 q=8 最小極大 = 37（前回確定）。
