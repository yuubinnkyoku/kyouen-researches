# 単一オーナー宣言: 4行盤 q=6・M_{4,6} のリコンサイルと m=35..38 現代的決定（2026-11-21）

- 宣言時刻: 2026-11-21T19:56Z（本ファイル push 時の最新 main HEAD は 19:53:09Z の K1058 コミット、push 直前に再取得して記録する）
- オーナー: 高速レーン（本セッション）・単一オーナー。同名の毎時タスクが並走する可能性があるため、本宣言以降は下記スコープへの同内容の並行着手を避けること。

## 背景（現状のmain内部矛盾）

- K0302（2026-10-03・status proved）は「固定幅の真の満容量安定化長5件は 24,12,16,13,11」、
  すなわち **M_{4,6}=16 の完全証明**を報告 artifacts 付きで主張している
  （実験一次資料: research/experiments/fixed-width/reports/q48-q6-exact-threshold.md・
  有限排除 16..35 の検証器 q48_q6_exclusion.cpp と完了 JSON・三行型計数上界19の q46_pair_upper_bound.cpp と JSON・
  大域上界68の Python 再現器 q48_nearby_q6_bounds.py）。
- 一方、K1177（2026-11-21・status computed）と K1182 本文の記録、および
  four-row-q6-q7-frontier-20261121 README は **M_{4,6} = 16 or ∈ [35,103]**（q6 witness-free band 16..34・未掃引 35..102・上界 U=103 は K0318 引用）と記録し、
  K0302 の先行証明に言及していない。mwq_stabilization.csv と results/fixed-width/README.md は (4,6)=16 を確定値として掲載したまま（矛盾）。
- K1182（M_{4,7}=13 の閉包）は K0302 が既に証明済みと主張する同じ値を別経路で再閉鎖しており、11/21 の掃引レーン群は K0302 に気づかないまま再検証労力を投下した形になっている。

## 本レーンの目的（受入条件つき）

1. **K0302 証明の複数系統検証（このセッションで実行できる機械部分に限る）**:
   - a) 公刊 Python 再現器 q48_nearby_q6_bounds.py（sha256 は出版物で pin）を新環境でそのまま実行し、出版 JSON と比較する。
   - b) q48_q6_exclusion.cpp（209行）を Node.js に文対文移植し、m=16..35 の有限排除を再実行、
     出版 JSON（q48_q6_finite_exclusions.json・40 case）の全計数フィールド（circles/target_subsets/reflection_representatives/searched_subsets/unknown_subsets/found_witness）と一致を検査する。時間予算で全幅が不可能な場合は対象幅をスコープに明記し、残りは未検証として区別する。
   - c) q46_pair_upper_bound.cpp を Node.js に文対文移植し、出版 JSON（q46_pair_upper_bound.json）の全計数と比較する。
   - いずれかで不一致・witness 発見・unknown_subsets>0 が出た場合は**採用しない**（fail-closed）。
2. **現代的決定幅の追加（genfast3 + pinned kissat 4.0.4、K1177 帯延伸の同一手順）**:
   (4,35,6)・(4,36,6)・(4,37,6)・(4,38,6) の def-mode インスタンスを各幅 2 回実行（conflicts bit-exact を要求）し、
   較正として (4,34,6) CNF を genfast3 で再生成し出版 md5 と byte 一致を確認する。UNSAT の幅は完全な決定論的不存在証明として
   four-row-q6-q7-frontier 実験 dir に band extension 第5次（append_records_q6d.js）として追記する。
   実行時間が予算を超える幅は INDET として正直に記録し、以降の幅へ進まない。
3. **リコンサイル K 項目と整理**: 受入条件が全部成立した場合のみ、新規 K 項目で M_{4,6}=16（K0302 先行・本レーンの複数系統検証 を与える）を
   repo の現在の記録と整合させて確定扱いに昇格し、K1177 側の「16 or ∈[35,103]」がK0302+本レーンの結果で置き換えられることを記述する
   （K1177 本文は書き換えず、relations/knowledge README bullet で接続）。成立しない場合は現状維持で誠実に記録する。

## 非目標

- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2・class 1/2/4 は本レーンの無関係・UNKNOWN のまま。
- K0414/K0374 系譜・n11 S5 frontier・five-row/six-row/eight-row の各帯掃引レーンには一切触れない。
- 未掃引幅への不存在主張はしない。conflicts 数・実行秒数を勝敗として読まない。
- branch/PR は作らず main に直接出版する。fetch-back は byte/sha 照合で行う。

## 並走に関する注意

- 本レーンの成果物パスは research/experiments/four-row-q6-m46-reconcile-20261121/・同 frontier dir への append_records_q6d.js + output/q6ext5/・
  新規 K 項目・研究 log 2点・knowledge README 末尾 bullet に限定する。
- 同時刻に別セッションが q6 帯延伸 m=35 を実行した場合、conflicts bit-exact ならば相互検証として両方記録し、不一致の場合は判定せず記録のみ。
