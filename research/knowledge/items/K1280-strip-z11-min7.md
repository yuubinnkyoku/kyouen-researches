---
id: K1280
title: "min>=7 クリティカルストリップ z=11 スライス: H(m+12;X;11)=v(ΣX,11,m+12)（F11 persistent-2 の再誕〔s=10 下向き単一 deviant 1<2・5 形状 + 尾 s>=12 恒常上向き 2>0〕+G11 単一 s=10 下向き+E11 E ランク初双方向〔s=8 下 1<2・s=10 上 2>0〕・条件付き再帰・無条件 ghost 一致 3 スライス連続+D11 単一 s=8 下向き〔loose 依存は s=10 に移動〕+C11 C ランク初双方向〔s=6 下 1<2・s=8 上 2>0〕・帯外 witness 双と同セル 2 点同居+B11 完全崩壊 3 スライス連続+A11 完全崩壊 2 スライス連続〔C手子=出版 T-Z10 位置〕+trivial 吸収底 2 スライス連続+m 帰納の全称証明・K1268 予想 C1 バンド m=7 行は残り z=12 の1セル化）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=11 slice for min>=7: for every m>=7 and every nonempty finite multiset X with min(X)=m, H(m+12;X;11)=v(sumX,11,m+12); this fixes the z=11 slice of the strip for all m>=7 (z=11 is IN the m=7 band since z*(7)=13), and leaves exactly the z=12 cell open in the K1268 Conjecture C1 m=7 row"
  - "z-ladder lemma structure at z=11: Lemma F11 (F11(s)=H(13;{1}+Y;11) decomposition-independent over all 3,657 decompositions, values 1/0/1/0/1/0/1/0/1/0 at s=0/3..10/11 with F11(s>=12)=2: the persistent-2 family that DIED at z=10 (K1279) is REBORN at z=11 as the permanent >=12 tail UP 2>0 vs the sigma-collapse v(s+1,11,13)=0 (census 310/330 shapes), plus the single s=10 DOWNWARD deviant 1<2 over the same 5 shapes {(10,),(3,7),(4,6),(5,5),(3,3,4)} -- the F-rank table splits from v along the whole tail for the first time), Lemma G11 (G11(s)=H(14;{2}+Y;11) = 0/1/0/1/0/1/0/1/1/0/1 at s=0/3..10/11 with G11(s>=12)=1: the z=10 TWO-SIDED pair shrinks to the single s=10 DOWNWARD 0<1 deviant (5 shapes, same family as F11's s=10 deviant -- the F->G deviant chain continues as a PUSH-DOWN instead of the z=10 push-up), Lemma E11 (E11(s)=H(15;{3}+Y;11) = 1/0/1/0/1/0/1/0/1/0/2 at s=0/3..8/9/10 with E11(s>=11)=0: the FIRST two-sided E deviant pair {8 DOWN 1<2, 10 UP 2>0}, conditional recursion (K1276/K1277/K1279 form), and the unconditional ghost form COINCIDES over all 3,657 decompositions for the THIRD consecutive slice (z=9/z=10/z=11)), Lemma D11 (H(16;{4}+Y;11), floored Y>=5, s-only: single s=8 DOWNWARD 0<1 deviant vs v(s+4,11,16); the z=10 pair {6,8} shrinks to s=8 only; loose floor tokens>=3 is decomposition-dependent at s=10 (position moved from z=9/z=10's {8,10})), Lemma C11 (H(17;{5}+Y;11), floored Y>=6, s-only: the FIRST two-sided C deviant pair {6 DOWN 1<2, 8 UP 2>0} -- C11(6) sign-FLIPS from the z=9/z=10 UPWARD history, and the deviant CELLS CO-RESIDE exactly with the TWO m=5 z=11 out-of-band witnesses (5,6) and (5,8) -- structural-line coincidence observed for the first time), Lemma B11 (floored Y>=7: FULL collapse v(s+6,11,18) over all 700 floored decompositions -- 3rd consecutive slice z=9/z=10/z=11; the C-child cites the published B10 cell table), and Lemma A11 (floored Y>=8: FULL collapse v(s+7,11,19) over all 460 floored decompositions -- 2nd consecutive slice, two fully-collapsing ranks co-residing 2nd consecutive slice; the A11 C-child 1^v(s+7,10,18) is EXACTLY the published T-Z10 m=7 theorem position -- the strip-theorem dependency deepens to z=10)"
  - "base and ladder: the m=7 base is TRIVIAL ABSORPTION 2nd consecutive slice (a=7 child == B11t(s) == the stair option exactly by the B11 full collapse, no deviant used), and the m>=8 step is option-set identity {v(SUM-1,11,m+11), 1^v(SUM,10,m+11)} with the a=m child on T-Z11(m-1) and the C-child on the published T-Z10"
  - "boundary sharpness (finite full enumeration claims): min>=7 is necessary -- m=6 z=11 out of band (z*(6)=10) separates at exactly one T-family shape (6,6) parent 0 vs single 1 DOWNWARD: the z=10 frontier witness (6,6) was 2 vs 1 UPWARD, so the DELTA-SIGN FLIP observed in the K1279 census is promoted to a sharpness claim here (first promotion of a sign-flip witness); m=5 z=11 out of band separates at exactly TWO shapes -- (5,6) 1 vs 2 DOWNWARD (sign flip from z=10's 1 vs 0) and (5,8) 2 vs 0 UPWARD -- the first DOUBLE-WITNESS m=5 slice. z=12 census recorded open (F12 8 deviants at s=12 single-point 1>0: persistent-2 DIES AGAIN; G12 12; E12 4 at s=10; D12 floored 2 {8 down,10 up} + loose decomposition-dependent; C12 1 at s=8; B12 1 at s=8 UPWARD -- the B full-collapse series z=9/z=10/z=11 BREAKS at z=12 for the first time; A12 0 -- A collapse 3rd consecutive slice; z=12 strip m in {7..12} fully collapsing in the observed census range)"
relations:
- type: extends
  target: K1279
  note: "K1279 が全称証明した z=10 スライス（min>=7）の次スライス z=11 を証明する。証明は K1279 の出版 F10t/G10t/E10t/D10t/C10t/B10t 表・T-Z10（A11 C手子 1^v(s+7,10,18) と m>=8 帰納の C手子 1^v(Σ,10,m+11)）を直接引用し、F11/G11/E11〔条件付き再帰〕D11/C11/B11/A11 の 7 セル梯子＋trivial 吸収底＋選択肢集合一致帰納で閉じる。K1279 audit の D6c z11_cells census（F11 310 deviant・B11/A11 崩壊候補）は本項の宣言前探査（先行出版 commit 10b8e96d）で表照合 match=True を確認の上で主張に昇格した。engine は出版 sha-gate 鎖から機械抽出、出版源は 10（K1279 機 8f29faf7… を追加し 11 方 byte 照合 + pin 照合・PROVENANCE PASS・手転写ゼロ）。"
- type: extends
  target: K1270
  note: "K1270 の低 z banded・K1272（z∈{2..4}）・K1273 T-Z5・K1274 T-Z6・K1275 T-Z7・K1276 T-Z8・K1277 T-Z9・K1279 T-Z10・本項 T-Z11 の併せ技で m=7 行は z∈{0..11} が確定（残部は z=12 の1セルのみ。z=13 は z*(7)=13 でバンド外前線）。C1 バンド各行の進捗: m=5 行完走・m=6 行完走・m=7 行 z<=11 確定〔残り1セル〕。"
- type: related
  target: K1268
  note: "統合窓 sharpness から登録された予想 C1 の m=7 行 z=11 セルを確定。z*(7)=13 により z=11 は m=7 バンド内（z=10 スライスに続き m=7 行に適用）。z=11 ストリップ崩壊は全 m>=7 で全称証明され、C1 の予想帯と整合。残部は m=7 の z=12 と m>=8 の z∈{12..z*(m)−1}（m=8 は z∈{12,13} の2セル）。"
- type: depends_on
  target: K1264
  note: "階段定理（空でない X・0<=R<=z+min(X) で H(R;X;z)=v(ΣX,z,R)）。母体の a>m 子・F11..A11 セルの A手子評価に窓端ちょうどの等式として使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・中間枝 (R+z)%2。F11..A11 梯子の全場合計算と単一側選択肢集合の算出基盤。"
- type: related
  target: K1273
  note: "底構造の分類（trivial vs deviant 吸収）の交替系列への追加点: z=10 m=7 trivial 吸収（K1279 初観測）が z=11 でも継続（2 スライス連続）。底類型の継続性は open。"
- type: related
  target: K1272
  note: "出版 Lemma F（F セル表）系の z=11 延長が F11。F セル値の 2 系は z=6→z=9 振動（周期 2）→z=10 死滅（K1279）→z=11 再誕（尾 s>=12 恒常 2）→z=12 census 再死（s>=13→0）と、恒常 2 の生死振動の全歴史が z 交替構造の観測資料として確定した（一般則 open）。"
artifacts:
- path: research/experiments/strip-z11-min7-20261124/verify_strip_z11.py
  role: verifier
  note: "専用機体（SHA-256 c02eb116d3387e0ba3de7dede34330f624393018033618f7ebe61f1fd2226aa0・59,617B・audit/tamper 両モード・engine block は出版 K1264/K1268/K1271-K1277/K1279 の10源から sha-gate 機械抽出・pin bd5f22e4…）。D1-D9 宣言 protocol（宣言総計 24,746点/44,557比較: D1 3,657/10,971・D2 330/991・D3 330/992・D4 1,650/4,950・D4b 1,078/3,234・D4c 700/2,100・D4d 460/1,380・D5 1,332/3,996・D6 90/270〔seed 20261131〕・D7a 17/85・D7b 78/234〔25 deviant/witness ペア+53 標準〕・D8 14,859/14,859・D9 165/495）と D6c z=12 census を実装。D6 の形状間エンジンクリア（value-transparent・宣言点数不変）は run log 開示。"
- path: research/experiments/strip-z11-min7-20261124/build_engine_from_published.py
  role: verifier
  note: "provenance sha-gate（出版 K1264・K1268・K1271・K1272・K1273・K1274・K1275・K1276・K1277・K1279 の10源から engine block を cut・11方 byte 照合（10源+本機体）+ pin bd5f22e4… 照合・PROVENANCE PASS・手転写ゼロ）。"
- path: research/experiments/strip-z11-min7-20261124/output/audit.json
  role: data
  note: "監査正本（SHA-256 ea23d3f17cf268d57d3be3a1942545a086007ab530bd1efce35d43127bc8d671・12,350B・宣言総計 24,746点/44,557比較 bad 0 と完全一致・meta.verifier_sha256 c02eb116…・4実行 byte-identical〔同一cwd×2/隔離tree/env -i別HOME+PYTHONHASHSEED=random〕・D6c census 6,813/9,969 bad_engine 0 に z=12 次レーン観測〔B12 初破れ 1 (s=8 上向き 2>1)・A12 0・F12 8 再死・G12 12・E12 4・D12 2・C12 1・z=12 strip m∈{7..12} 崩壊観測〕・m=6 z=11 帯外 (6,6) 0<1・m=5 z=11 帯外 2 witness・E11 ghost 不一致 0 を記録）。"
- path: research/log/2026-11-24-strip-z11-min7-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit 13571ad6・sha256 1e12191a…・45,375B・publish-then-execute・F11/G11/E11〔条件付き〕D11/C11/B11/A11 + T-Z11 + 鋭さ (a)(b) の証明全文を機械実行前に先行開示・宣言前探査の全開示・宣言総計 24,746点/44,557比較の事前登録）。
- path: research/log/2026-11-24-z11-predecl-exploration.md
  role: log
  note: 宣言前探査記録（主張なし・先行出版 commit 10b8e96d・kit と共に機械実行前に全開示）。
- path: research/log/2026-11-24-strip-z11-min7.md
  role: log
  note: run log（選定→探査→宣言→機体→公式監査→出版→fetch-back 検証・宣言ノート sha 1e12191a…・audit sha ea23d3f1…・D6 per-shape clear・バックグラウンド実行の環境リセット失敗 2 度の誠実記録）。
scope: >-
  残余ゲーム H(R;X;z)（K0832/K1138系再帰・K0832 単一トークン閉形式 v）について、
  すべての m>=7・min(X)=m を持つ空でない任意の有限多重集合 X（全形状・全アリティ）に
  対して H(m+12;X;11)=v(ΣX,11,m+12) が成立するという全称命題（proved・F11/G11/E11〔条件付き
  再帰〕D11/C11/B11/A11 閉形式の K0832 場合計算 + 出版 z<=10 補題・T-Z10 引用 + 底 m=7 の
  trivial 吸収 + 選択肢集合一致 + m に関する帰納）。同一証明に含まれる数学的部品として
  Lemma F11（F セル z=11 閉形式表・分解非依存・全称・persistent-2 の再誕〔s=10 下向き
  deviant + 尾 s>=12 恒常 2〕）、Lemma G11（R2型セル閉形式・単一 s=10 下向き deviant・
  F→G 押し下げ連鎖・全称）、Lemma E11（E セル閉形式・E ランク初双方向 2 deviant・条件付き
  再帰・無条件 ghost 全分解一致〔3 スライス連続〕・全称）、Lemma D11（床付き D ランクセル・
  単一 s=8 下向き deviant・全称）、Lemma C11（床付き C ランクセル・C ランク初双方向
  2 deviant・帯外 witness 双との同セル同居・全称）、Lemma B11（床付き・完全崩壊
  3 スライス連続・全称）、Lemma A11（床付き・完全崩壊 2 スライス連続・C手子=出版
  T-Z10 定理位置・全称）も主張に含む。境界の鋭さとして m=6 z=11 帯外 (6,6) の
  Δ符号反転 witness（0<1 下向き）と m=5 z=11 帯外 2 witness 同居
  （(5,6) 1<2・(5,8) 2>0）を有限全列挙の主張として含む。K1268 予想 C1 の m=7 行は
  z∈{0..11} が確定（残部は z=12 の1セル・z=13 はバンド外）。z=12 スライス（B12 初破れ
  （s=8 上向き）・F12 再死（s=12 単点）・D12 loose 分解依存位置の変化・床 min>=7 vs
  min>=8 の選定）、F ランク 2 系の z 交替則（死→再誕→再死）、E ランク無条件 ghost
  一致の一般則、帯外 witness の符号反転時刻の一般則、C ランク deviant の符号史、
  loose D ランク分解依存位置の移動則、底類型（trivial 吸収）の継続性、
  m=5 帯外 2 witness 同居の一般則は open、11×11 盤面のいかなる勝敗も本項目の範囲外。

