# sat3 streaming census で (7,4) 帯の SAT 探索をアンブロック — m=28..35 全幅 SAT・K0827 帯4系統検証完了

Date: 2026-11-15
Lane: 高速レーン（seven-row-q4-q6-witness-frontier-20261115 の後続）
Experiment: research/experiments/seven-row-q4-extension-band-sat3-20261115/ (main push済み)

## 概要

frontier レーンで記録した **sat2.js 全三つ組censusのメモリ壁**（7×28 q=4 で OOM
rc 137・node heap 2560MB）を、節ストリーム出力版の **sat3.js** で解消した。
これにより K0827 構成的延伸帯のうち tsVerify のみだった **m=28..35 を SAT + 2系統検証
に昇格**し、(7,4) の witness 帯 m=4..35 が全て4系統検証済みになった。

## sat3.js（sat2.js との差分は3点・encode core は verbatim）

1. 節のストリーム出力: `enc.clauses[]` への全節保持 + `toDimacs()` の GB 級結合文字列
   （OOM 主因）を廃止し、chunk flush でディスクに直接書く。ヘッダは最後に前置。
2. 円の初遭遇処理: circMap 挿入順 = 三つ組列挙順でその場で counter を emit
   （clause 順・変数番号とも sat2.js と同一）。
3. 円の点走査を O(w) 化: 全点走査の代わりに行ごとの2次方程式整数根求解
   （row-major 昇順保持・点集合は全点走査と同一）。正規化キーの Set のみ保持。

### 検証

- **byte-identity**: 9対照（def/cap+seq/cap+tot/lex/rowY・w=4..7・q=4..6）で **9/9 cmp MATCH**。
- **meta一致**: (7,22,4)/(7,23,4)/(7,23,5) の curves/vars/clauses が公開 record と完全一致
  （本コンテナでは sat2 が 7×22 で既に OOM するため byte-diff 不可、end-to-end 再現で代替）。
- **kissat較正**: (7,5) m=23 → 1,200 conflicts **bit-exact**。
- **witness再現**: (7,4) m=22..27 → 全幅 0 conflicts・**石配置 6/6 公開 witness と完全一致**。

## 結果: m=28..35 全幅 SAT（200s cap・生成3.1〜5.2s）

- conflicts 36/59/249/94/256/537/214/160（m=28..35）。m=35 は 5,510,073 clauses・CNF 103MB。
- 全 witness 20石・**行マルチセット {3,3,3,3,3,3,2}**（K0827 構成的 config CA/CB と
  同一マルチセット・配置は独立の certificate）・js+py 2系統検証 PASS。
- **m=35 lex=H,V,HV 別符号化でも SAT**（314 conflicts・2系統検証 PASS）。

## 位置づけ

- **(7,4) witness 帯 m=4..35 が全幅4系統検証済み**（kissat SAT + jsVerify + pyVerify + tsVerify）。
  m=22..27 は SAT witness = 構成 witness（石配置まで一致）、m=28..35 は互いに独立の証明。
- M_{7,4} ∈ [36, 1929] 不変。前線 7×36（未実施・不在主張ではない）。
- sat3 により **(7,4) の m≥36 SAT 探索が生成~6s/幅で実行可能**になった
  （UNSAT 主張には 200s cap 超の長時間実行か構造論証が必要）。
- q≤w 全般（例: (7,5) 7×33+・(7,6) 7×28+・(7,7)・w=5,6 の q<w 族）の SAT 探索にも
  そのまま適用可能。q≥w+1 の genfast3 とは補完関係。

## 知識反映

- K0827: evidence/scope 更新 + artifacts 2件追加 + 追記セクション。
- results/fixed-width/mwq_stabilization.csv: (7,4) 行の census 壁記述を
  「sat3 で解消済み」に更新（下界36・前線7×36は不変）。
- results/fixed-width/README.md: (7,4)-(7,6) 段落に sat3 の記述を追記。
