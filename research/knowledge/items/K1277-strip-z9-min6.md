---
id: K1277
title: "min>=6 クリティカルストリップ z=9 スライス: H(m+10;X;9)=v(ΣX,9,m+10)（F9 persistent-2+G9方向反転+E9条件付き再帰の無条件一致+D9下向き反転+C9反転吸収+B9新完全崩壊セル〔初のストリップ定理依存ランク〕+mex吸収底+m帰納の全称証明・K1268 予想 C1 バンド m=6 行の完走・z*(6)=10 の最終セル z=9 を確定）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=9 slice for min>=6: for every m>=6 and every nonempty finite multiset X with min(X)=m, H(m+10;X;9)=v(sumX,9,m+10); this fixes the z=9 slice of the strip for all m>=6 (the m=5 z=9 cell is out of band since z*(5)=9), and CLOSES the m=6 row of the K1268 Conjecture C1 band completely (the last band cell z=9, with z*(6)=10; the m=6 row is now fully determined for z in {0..9}, the second completed row after m=5)"
  - "z-ladder lemma structure at z=9: Lemma F9 (F9(s)=H(11;{1}+Y;9) decomposition-independent over all 3,657 decompositions, values 1/0/1/0/1/0/1/0/0 at s=0/3..9 and 2 for ALL s>=10: the 2-family that had sunk at z=8 RETURNS at z=9 and persists for all large s -- the first non-sinking large-s family in the F-rank; deviants vs the sigma-collapse v(s+1,9,11) are the s=8 DOWNWARD 1<2 family {(8,),(3,5),(4,4)} plus the whole s>=10 UPWARD persistent-2 family 2>0), Lemma G9 (G9(s)=H(12;{2}+Y;9) = 0/1/0/1/0/1/0/1/1 at s=0/3..8/9/>=10; the R2-form collapse v(s+2,9,12) breaks at EXACTLY s=8 via {(8,),(3,5),(4,4)} DOWNWARD 0<1: a DIRECTION FLIP of the G8 s=8 upward deviant (first direction flip observed in the G-rank)), Lemma E9 (E9(s)=H(13;{3}+Y;9) = 1/0/1/0/1/0/2/0 at s=0/3..7/8/>=9; deviants {(6,),(3,3)} DOWNWARD 1<2 and {(8,),(3,5),(4,4)} UPWARD 2>0; the CONDITIONAL recursion {G9(s), 1^E8(s)} + ({v(s+2,9,12)}: some Y token >=4) now COINCIDES with the unconditional ghost form over ALL 3,657 decompositions at z=9 -- the E8 (3,3) break was z-specific, so the fate of the unconditional E-rank form depends on z (machine-checked, general law open)), Lemma D9 (H(14;{4}+Y;9), floored Y>=5, s-only with the SINGLE s=6 DOWNWARD deviant D9(6)=0 < v(10,9,14)=1 at Y=(6,): a DIRECTION FLIP of the D8 s=6 upward deviant -- the first downward deviant of the D-rank; loose floor (tokens>=3) breaks at s in {8,10}), Lemma C9 (H(15;{5}+Y;9), floored Y>=6, s-only with the SINGLE s=6 UPWARD deviant C9(6)=2 > v(11,9,15)=0 at the position H(15;{5,6};9), the SAME position as the published m=5 z=9 out-of-band witness (5,6); the D9 s=6 downward deviant is RE-IMPLEMENTED as the a=m child value and the parent mex flips it upward: the first DOWNWARD-to-UPWARD reversal absorption in the ladder, after K1276's C8 absorbed an upward deviant without breaking), and Lemma B9 (H(16;{6}+Y;9), floored Y>=7: FULL collapse B9(s)=v(s+6,9,16) over all 700 floored decompositions with zero deviants; the C-child of the B9 recursion is 1^v(s+6,8,15) which is EXACTLY the published T-Z8 theorem position H(15;{6}+Y;8) -- the first ladder rung whose recursion cites a published STRIP THEOREM rather than a cell table (dependency deepening: the fully-collapsing rank moves C7/C8 (z=7,8) -> B9 (z=9))"
  - "proof technique: K0832 case computation closes the F9/G9/E9/D9/C9/B9 cells from published z<=8 lemmas (F8/G8/E8/D8/C8 cell tables and T-Z8), with the E9 recursion kept in the CONDITIONAL form exactly as in E8 (the unconditional coincidence is recorded as an observation, not used in the proof). The m=6 base H(16;X;9) is deviant ABSORPTION: A'-child v(S-1,9,15)=0 (K1264 stair edge), a=6 child C9(S-6) in {1 (s=0), 2 (s=6), 0 (s>=7)}, C-child 1^v(S,8,15)=0 (published T-Z8 at the m=6 position); parent mex{1}=0 at the singleton X=(6,) and mex{0}=1 or mex{0,2}=1 for s>=6, matching the single-token side v(S,9,16) (the absorption point is X=(6,6), the same deviant-absorption archetype as the K1273 z=5 m=4 base and the K1276 z=8 m=5 base). The m>=7 step is option-set identity {v(S-1,9,m+9)} (a>m child exactly the K1264 stair window edge, a=m child the induction hypothesis C(m-1,9) = T-Z9(m-1) at R=m+9=(m-1)+10) and 1^v(S,8,m+9) (published T-Z8), matching the single-token side exactly"
  - "boundary sharpness: min>=6 is necessary (m=5 z=9 is out of band since z*(5)=9; the 222-shape m=5 z=9 negative record separates at exactly one point (5,6) parent 2 vs single 0 UPWARD -- re-recorded here), and the m=6 row roof is EXACTLY z=9 (the m=6 z=10 out-of-band record separates at exactly one point (6,6) parent 2 vs single 1 UPWARD over all 222 shapes -- a NEW witness), so the C1 m=6 band z<z*(6)=10 is fully consumed. The band-frontier witnesses now line up as s=6 shapes: m=4 (4,4) downward/(4,6) upward, m=5 (5,6) upward, m=6 (6,6) upward (law strengthened, not claimed). z=10 next-lane census registered as open (F10 4-deviant family, G10 7, E10 3, D10 floored TWO deviants s=6/8 -- first 2-deviant D-rank, C10 one s=6 upward, B10/A10 floored families collapse in census: full-collapse rank candidate for z=10)"
relations:
- type: extends
  target: K1276
  note: "K1276 が全称証明した z=8 スライス（min>=5）の次スライス z=9（min>=6・m=5 の z=9 はバンド外なので床は必然的に m>=6 に上昇）を証明する。証明は K1276 の出版 F8/G8/E8/D8/C8 表・T-Z8（C手子 1^v(Σ,8,m+9) と B9 C手子 1^v(s+6,8,15))を直接引用し、F9/G9/E9〔条件付き再帰〕D9/C9/B9 の 6 セル梯子で閉じる。K1276 audit の D6c z9_cells census（F9/G9/E9/D9/C9/B9 表・D9 s=6 下向き・C9 s=6 上向き・B9 崩壊観測）は本項の宣言前探査 P10 crosscheck（出版 audit pin 84605d3b…）で完全一致確認の上で主張に昇格した。engine は同一の出版 sha-gate 鎖から機械抽出、出版源は 9 つに拡大（K1276 機 cdc47219… を追加・9 方 byte 照合 + pin 照合）。z=8 の E8 で発見された条件付き再帰は z=9 でも条件付き式として採用（無条件一致は観測）。"
- type: extends
  target: K1270
  note: "K1270 の低z banded（z∈{0,1}）・K1272（z∈{2,3,4}）・K1273 T-Z5・K1274 T-Z6・K1275 T-Z7・K1276 T-Z8 との併せ技で m=6 行は z∈{0..9} 全確定となり C1 バンドの m=6 行が完走（残部ゼロ・z*(6)=10・m=5 行に続き 2 行目）。"
- type: related
  target: K1268
  note: "統合窓 sharpness から登録された予想 C1 の m=6 行を完走（バンド z<z*(6)=10 の全セル z∈{0..9} 確定）。z=9 ストリップ崩壊は全 m>=6 で全称証明され（m=5 z=9 帯外は (5,6) 上向きの 1 点分離・m=6 z=10 帯外は (6,6) 上向きの 1 点分離で上確認認）、C1 の予想帯と整合。残部は m>=7 の z∈{10..z*(m)−1}（m=7 は z∈{10,11,12} の3セルが最短残部）。"
- type: depends_on
  target: K1264
  note: "階段定理（空でない X・0<=R<=z+min(X) で H(R;X;z)=v(ΣX,z,R)）。母体の a>m 子・F9/G9/E9/D9/C9/B9 セルの A手子評価に窓端ちょうどの等式として使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・中間枝 (R+z)%2。F9/G9/E9/D9/C9/B9 梯子の全場合計算と単一側選択肢集合の算出基盤。"
- type: related
  target: K1273
  note: "底構造の分類（自明吸収 vs deviant 吸収）の交替系列への追加点: z=5 m=4 底（deviant 吸収）・z=8 m=5 底（deviant 吸収）・z=9 m=6 底（deviant 吸収・吸収点 X=(6,6) の mex{0,2}=1）。D→C の反転吸収（D9 下向き → C9 上向き）は K1273/K1276 の吸収と異なり崩壊セル自体が deviant を持つ初の構造。"
- type: related
  target: K1272
  note: "出版 Lemma F（F セル表）系の z=9 延長が F9。F セル値の 2 系は z=6（s>=8→0）→z=7（s>=8→2）→z=8（s>=9→0）→z=9（s>=10→2 以後非沈没）と z=8 まで周期 2 の振動だったが z=9 で初めて周期性を破る（persistent-2・s の増大で沈まない族の初出現）。"
artifacts:
- path: research/experiments/strip-z9-min6-20261124/report.md
  role: proof
  note: 機械監査の正本記録（D1-D9・D6c z=10 census・変異電池 B1-B14・決定性・provenance・誠実記録）。証明全文は宣言ノート §2 にあり本 report は証明そのものではない。C1 m=6 行完走・F9 persistent-2・D9 下向き反転・C9 反転吸収・B9 完全崩壊〔初のストリップ定理依存ランク〕を含む。
- path: research/experiments/strip-z9-min6-20261124/verify_strip_z9.py
  role: verifier
  note: "専用機体（SHA-256 bf3c0c1c1b38a32bbcb7cf83129d4c5842a39aa99587cb342301ee66adab5cd2・50,229B・audit/tamper 両モード・engine block は出版 K1276 機等から sha-gate 機械抽出）。D1-D9 宣言 protocol（宣言総計 23,808点/42,662比較）・14変異電池 B1-B14（B1=318・B10=236・B11=570・B12=100 等）。"
- path: research/experiments/strip-z9-min6-20261124/build_engine_from_published.py
  role: verifier
  note: "provenance sha-gate（出版 K1264・K1268・K1271・K1272・K1273・K1274・K1275・K1276 の8源から engine block を cut・9方 byte 照合（8源+本機体）+ pin bd5f22e4… 照合・PROVENANCE PASS・手転写ゼロ）。"
- path: research/experiments/strip-z9-min6-20261124/probe_strip_z9_predecl.py
  role: verifier
  note: "宣言前探査機体（SHA-256 ac473d1297c6829e734d2359deec9d5f55c36a82cae43a181d04014947453a80・宣言ノート §6 P1-P12+crosscheck の再現・E9 無条件期待式の z=9 一致（不一致 0）検証ブロック込み・engine は出版 K1264 機から sha-gate cut）。宣言前探査の全開示規約の一次資料。"
- path: research/experiments/strip-z9-min6-20261124/probe_z9_predecl.json
  role: data
  note: "宣言前探査出力（SHA-256 726741d41789e464d79af11ce2ec6c7e4e56d0b1e992927eab02aeb26da65e0e・出版 K1276 audit の z9_cells census との完全一致（P10 match=True）・E9 無条件式不一致 0 件→条件付き式と一致（P8）を含む）。"
- path: research/experiments/strip-z9-min6-20261124/output/audit.json
  role: data
  note: "監査正本（SHA-256 9c0294e9dc413c422a88be17d64aa0325aad5236eca2bcb3885e8988473b79ae・10,217B・宣言総計 23,808点/42,662比較 bad 0 と完全一致・meta.verifier_sha256 bf3c0c1c…・4実行 byte-identical・D6c census に z=10 次レーン観測（F10 dev 4・G10 dev 7・E10 dev 3・D10 床付き 2 deviant〔D ランク初〕・C10 1 deviant・B10/A10 崩壊・z=10 strip m∈{7..11} 96/96・m=6 帯外 95/96 (6,6)・m=5 z=9 帯外 (5,6)・E9 無条件 ghost 不一致 0）を記録。"
- path: research/log/2026-11-24-strip-z9-min6-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit c9c91fca72fb1a4cf82029a5e13ccac919dc0f8e・sha256 b267fb69…・F9/G9/E9〔条件付き〕D9/C9/B9 + T-Z9 の証明全文を機械実行前に先行開示・publish-then-execute・宣言前探査 P1-P12 の全開示・宣言総計 23,808点/42,662比較の事前登録）。
- path: research/log/2026-11-24-strip-z9-min6.md
  role: log
  note: run log（選定→探査→宣言→機体組立→公式監査→出版→fetch-back 検証・実行環境 timeout リセットによる全滅と pin 照合での決定論的復元の誠実記録を含む）。
scope: >-
  残余ゲーム H(R;X;z)（K0832/K1138系再帰・K0832 単一トークン閉形式 v）について、
  すべての m>=6・min(X)=m を持つ空でない任意の有限多重集合 X（全形状・全アリティ）に
  対して H(m+10;X;9)=v(ΣX,9,m+10) が成立するという全称命題（proved・F9/G9/E9〔条件付き
  再帰〕D9/C9/B9 閉形式の K0832 場合計算 + 出版 z<=8 補題・T-Z8 引用 + 底 m=6 の
  C9 s=6 deviant mex 吸収 + 選択肢集合一致 + m に関する帰納）。同一証明に含まれる
  数学的部品として Lemma F9（F セル z=9 閉形式表・分解非依存・全称・s>=10 の
  persistent-2 family）、Lemma G9（z=9 の R2型セル閉形式・deviant は s=8 の
  {(8,),(3,5),(4,4)} 下向き ちょうど・G ランク初の方向反転・全称）、Lemma E9
  （z=9 の E セル閉形式・条件付き再帰期待式・deviant は s=6 下向き {(6,),(3,3)} と
  s=8 上向き {(8,),(3,5),(4,4)}・無条件 ghost 形は z=9 で全分解一致〔観測〕・全称）、
  Lemma D9（床付き D ランクセル H(14;{4}∪Y;9)・Y>=5 で s-only だが唯一の deviant
  s=6 下向き・D ランク初の下向き・全称）、Lemma C9（床付き C ランクセル
  H(15;{5}∪Y;9)・Y>=6 で s-only・唯一の deviant s=6 上向き・位置は出版 m=5 z=9
  帯外 witness (5,6) と同一・D→C 反転吸収の初観測・全称）、Lemma B9（床付き B ランク
  セル H(16;{6}∪Y;9)・Y>=7 で完全崩壊 v(s+6,9,16)・再帰の C手子が出版ストリップ定理
  T-Z8 の位置そのもの〔初の定理依存ランク〕・全称・本項目で初の全称証明）も主張に
  含む。K1268 予想 C1 の m=6 行は完走（z∈{0..9} 全確定・残部ゼロ・2 行目）。
  m>=7 の z∈{10..z*(m)−1}（m=7 は z∈{10,11,12} の3セル）、z=10 ストリップ・
  F10/G10/E10/D10/C10/B10/A10 閉形式、s=6 構造線の方向反転系列
  （D8↑→D9↓→C9↑→D10 2点↓→C10↑）の一般則、バンド前線 witness = s=6 形状法則
  （m=4 (4,4)/(4,6)・m=5 (5,6)・m=6 (6,6)）、完全崩壊ランク移行の一般則
  （C7/C8→B9→z=10 の B10/A10 候補は census 観測のみで open）、E ランク無条件
  ghost 形の z 依存性の一般則は open、11×11 盤面のいかなる勝敗も本項目の範囲外。
