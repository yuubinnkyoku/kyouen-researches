# 2026-11-21 four-row q=7 真の安定化長 M_{4,7}=13 閉包（closure レーン・K1182）

レーン: four-row (w=4) q=7 closure。K1177 frontier レーン（宣言 528ec960・初期掃引 d6b2c948・band extension 433a8135）の直接後続。単一オーナー宣言・受理条件は宣言note（commit db666081）のとおり fail-closed。

## セッションの目標と経緯

K1177 出版時点で M_{4,7} = 13 or >= 86（q=7 有限掃引 13..85・m=86 は sat2.js 符号化メモリ壁）。K0318 の証明済み一般上界 U_{4,7}=81 と組み合わせれば帯 [13,85] の有限排除＋[81,∞) の解析上界で全幅 m >= 13 が被覆され、m=12 witness が下界を与えることは宣言時から見えていた。本セッションはこの閉包を（a）K0318 再現（b）records 監査（c）genfast3 移植と較正（d）壁の先の直接掃引（e）出版の順で fail-closed に実行した。

## 実行記録

1. **K0318 整数最適化の独立再実装**（scripts/u_recompute.js）: curve_packing_fixed_width の閾値計算を独立に書き直し、既刊 JSON と全 30 エントリ一致（mismatches 0）。key values: U_{4,6}=103, U_{4,7}=81（Q=756, Y=65, Yform=crossrow, opt=(5,65), H=75 等）。正本 output/u_recompute.json・再生全文 output/k0318_regen_full.json。
2. **K1177 records.jsonl 機械監査**（scripts/audit_records.js）: 108 レコード。q=7 witness band {7..12} 全 SAT・witness 3系統検証つき、witness-free {13..85} 全 UNSAT rc=20・INDET 0、q=6 witness {6..15} SAT / witness-free {16..29} 全 UNSAT・INDET 0、capacity/lexH レコードの整合。problems 0（output/records_audit.json）。
3. **genfast3.js の w=4 移植と較正**: six-row-q8-band-closure-22-370-20261114 出版の genfast3.js を byte-identical（md5 12c2bd9c…）で移植（core は four-row sat2.js と同一 md5 282ae832…）。q >= w+2 の完全性論で q=7 >= 6 が w=4 で正当化される。較正: (4,13,7)/(4,20,7)/(4,16,6)/(4,85,7) の CNF が sat2.js 出版値と byte 一致、pinned kissat conflicts bit-exact（5446/3359/1980648/3759）。
4. **壁の先の掃引 m=86..88**: genfast3 生成（0.12-0.13s/幅・vars 7043/7180/7317）→ pinned kissat 4.0.4 すべて UNSAT（conflicts 5930/5191/6072・0.16..0.23s）。2 回の独立実行で conflicts bit-exact。(4,86,7) def-mode + `--lex=H` 交差符号化も UNSAT（conflicts 3677）。solve 生ログ 7 本を出版。
5. **witness 再検証**: m=7..12 の 6 witness を JS verifyConfig で再検証（PASS）。
6. **records 追記**（scripts/append_records.js）: K1177 dir の records.jsonl 形式に 4 レコード（m=86,87,88 def + 86 lexH）追記。108→112。追記後再監査 problems 0（output/records_audit_ext88.json）。正本スナップショット output/records_extended.jsonl（md5 fd43f36e…）。

## 出版（part 分割・すべて fetch-back 検証）

- 1/3 commit d177c568: K1177 dir records.jsonl 108→112 + frontier README 閉包注記（witness-free band 13..88・M_{4,7}=13 (closed)・次の作業の更新）。push 前に base 両ファイルの md5 突合・fetch-back 両 md5 一致。
- 2/3-A commit bbc5f4e2: closure 実験dir part1（README 報告書・宣言 note・genfast3.js・u_recompute.js・audit_records.js・append_records.js）。push 前に sandbox 読み取りで md5 全突合、commit stats で additions 行数全一致。
- 2/3-B commit b5723394: part2（u_recompute.json・k0318_regen_full.json・records_audit.json・records_audit_ext88.json・records_extended.jsonl 55,466B）。
- 2/3-C commit 144362e9: part3（live: solve 7本・gen 4本・witness 6本。CNF は出版しない）。
- 3/3: K1182 item・本ログ・K1177 事後閉包節・knowledge README K1182 bullet（本コミット群）。

## 結論と知識昇格

- **M_{4,7} = 13（closed・K1182・status proved）**。ゲーム帰結: 全 m >= 13 の全安全局面で g(S)=(24−|S|) mod 2・空盤 second-player-win（K0024 の飽和ゲーム値形式）。q=6 は未閉鎖（M_{4,6}=16 or ∈ [30,103]）。
- 他レーンへの移譲済み観察: (5,7) にも同一パターン適用可（five-row 帯掃引 19..157 完了時に U_{5,7}=158 と併せ M_{5,7}=19。所有権は five-row レーン・本レーンは不作業）。
- 残る自由課題: M_{4,7}=13 の自己完結的ブロッキング計数証明（M の値を変えない）。q=6 の [30,103] 74 幅（genfast3 census が q=6=w+2 で使用可能なため sat2.js のメモリ問題を回避した掃引が有望）。

## 制約の遵守

- 有限掃引と解析上界の役割分担を成果物すべてで明示し、有限実験を全称定理として過大主張していない（K1182 は K0318 の証明済み定理に明示的に依存）。
- 推定やヒューリスティックは本閉包の論法に含めない。INDET 0・rc=20 で UNSAT を主張。
- branch/PR は作成せず main 直接出版。push 競合・同時書込みは発生しなかった（push 前に毎回最新 main を取得し md5 突合）。
