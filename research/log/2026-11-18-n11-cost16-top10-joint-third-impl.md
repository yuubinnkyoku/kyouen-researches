# 2026-11-18 N11 cost-16 parent top-10 joint（45組み合わせ）第三実装クロスチェック全一致

## 成果

31行cost-16 parent `00000000000000003800000008001000` の **出版済みtop-10 joint membership（45組み合わせ・A/B分離・commit `537a4458`）を第三実装（published `PmLazy` をimportしない独立 `MyPm` 再帰カウンタ + 独立に配線した公式）で全45組み合わせ再計算し、joint_A・joint_B・joint・shared_row の全フィールドで 0 不一致** を確認した。anchor（錨）検証を先行させ、その後 joint 45 combos を slice 分割で実行した。

- script: `crosscheck_top10_joint_third_20261118.py`（anchors / slice N / finalize の3 mode・checkpoint resume付き）
- output: `output/crosscheck-top10-joint-third-20261118.jsonl`（6 anchor record + 45 combo record）・`output/crosscheck-top10-joint-third-20261118.json`（finalize検証JSON・9 checks all PASS）

これにより top-10 joint の全数値（生存曲線k=2厳密点 262,073,639,571,350,318 含む）は **出版実装・validate11全列挙（11行）・第三実装（31行直接）の3独立経路** で確定した。

## 手法（第三実装の独立性）

- **カウンタ**: published `PmLazy`（帯域内 forward-chain + band memo）を一切使わず、除去行集合を引数に取る素朴な再帰 `MyPm(V∖…)` を実装（memo dict・集合はfrozensetではなくsorted tupleで正規化）。各 anchor・combo で fresh memo を使い、memo履歴非依存性も各計算で独立に実証。
- **公式の独立配線**: 互いに素ペア joint_A=Σ_s w1[s]·pm(V∖e1∖e2∖{s})、joint_B=Σ_z W(z)·pm(V∖e1∖e2∖{z}) + Σ_{d,x<y} w(d,x)w(d,y)·pm(V∖e1∖e2∖{d,x,y})（W(z)=Σ_{d∈e1∪e2} w(d,z)）、行共有ペア joint_A=0・joint_B=pm(V∖(e1∪e2)) を published script を読まず仕様logから独立に実装。
- **anchor 6 section（全PASS後に関節計算へ）**: per-row pm 31/31（fresh memo 3,524,561状態・17.4s）・1-type a/b 3点（(0,1)/(15,19)/(28,30)・出版a_part/b_partと完全一致）・direct B_d 2点（row 18=18,319,351,945,126,110・row 2=23,475,415,507,703,040・出版b_slicesと完全一致）。anchor用memoは約3.52M状態でcgroup上限内。
- **slice実行**: combo 0-11 / 12-23 / 24-35 / 36-44 の4 sliceに分割（~130秒のkill窓回避・各invocation後にcheckpoint JSONLをscratchへsnapshot）。combo単体のfresh-memo木は 514,223〜4,793,114 状態・1.9〜25.0s（45 combos合計 622.1s）で、slice共用不要の小さい計算（出版時の観察と一致）。

## 結果

- **45/45 combos で match=True**（joint_A・joint_B・joint・shared_row 全フィールド）。不一致 0 件。
- shared-rowペア 22/45 で全て joint_A=0 を第三実装でも機械確認。
- finalize 9 checks all PASS: anchors.all_pass / combos.count_45 / combos.set_match / combos.all_match / shared_row.joint_A_zero(22) / bounds.mate_capacity_10x / bounds.joint_le_min_membership / survival.k1_share / survival.k2_value。
- **k=2生存点を第三実装値のみから再導出**: m1+m2−joint(0,1) = 262,073,639,571,350,318（出版値と厳密一致）。k1 share は 4.597501506…%（出版表記 4.5975% は4桁丸め）。
- 二重実行: finalize出力は **byte-identical**（sha256 `86374030…`・timing欄はJSONL側のみでfinalize JSONには含まれない）。
- 入力pin: phase A出力 git blob `fe4b4b55…`・B16 slice出力 git blob `883275fb…`・出版joint JSONLはcommit `537a4458` のものを照合対象として使用。

## 構造観察（第三実装が出版値と一致して確定）

- **(5,9) と (7,8) が完全に同一値**（joint_A=4,627,678,114,070,406・joint_B=1,480,220,003,763,750）: rows_a∪rows_b がどちらも {1,4,18,19} であり、互いに素ペアのjoint公式は e1∪e2 のみに依存する（joint_Aの和の範囲・W(z)の定義・第2項のdの範囲がいずれもunionで決まる）ため。2つの実装が独立に同一値を返し、union-only構造の実装間での追加裏付けとなった。45 combos中に同一値のグループはこの1組のみ。
- 実装間差異として有意な不一致・系統的ズレは皆無で、今回の不一致0は「第三の核」による実質的な独立再現と評価できる（カウンタ・公式配線・入力読み込みが全て独立）。

## 実装上の教訓（デバッグ段階で発見・anchor以前に捕捉）

1. **行選択述語の反転**: `not (mask>>s)&1` は立っていない行を選ぶ誤り（正: ビットが立っている行を選ぶ）。anchor段階のper-row pm照合が即座に検出し、joint計算前に修正。**anchor先行の段階的照合が公式・カウンタ双方のバグを下流に流さない**ことを再実証。
2. `rl[0]` を tuple化したままweight表引数に渡す型ズレ（正: 生のリスト）もanchor段階で捕捉。
3. **チェック側の過度な厳密性**: 当初 `100*k1/total == 4.5975`（float厳密一致）を書いたが、実際のshareは 4.597501506…% で出版の 4.5975% は4桁丸め。`round(share,4)==4.5975` に修正。**出版側の丸め表記と検証側の厳密値の粒を揃える**ことは検証script設計の定番注意点。

## 実験的事実（運用）

- 1 invocation 280s timeout + slice snapshot の運用で、~130秒kill窓・1.04GB cgroup制約の下で45 combosを4 slice（+finalize）で完走。中断してもcheckpoint JSONLからresumeで損失なし。
- comboあたりの計算は slice 3（後半・(5,9)/(6,8)/(6,9)等の重い除去）で 13.6〜25.0s に達するが、それでも単invocationに多数収まる。共有memoの効果は出版時観察どおり限定的で、独立検証にはfresh-memo per combo が最も単純かつ安全。

## 解釈上の注意

joint membershipは代替最小cover計画の組合せ数であって探索コストでもverdictでもない。本クロスチェックはcover計画の組合せ論の数値の独立性確認のみを主張する。REFUTED-D10・STERILE は LOSS 証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。
