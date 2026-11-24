---
id: K1279
title: "min>=7 クリティカルストリップ z=10 スライス: H(m+11;X;10)=v(ΣX,10,m+11)（F10 persistent-2 の死+G10 2-deviant 双方向同居+E10 条件付き・ghost 一致 2 スライス連続+D10 D ランク初 2-deviant+C10 反転吸収 2 スライス〔吸収値減衰〕+B10 完全崩壊 2 スライス連続+A10 A ランク初完全崩壊〔2 完全崩壊ランク同居〕+trivial 吸収底+m 帰納の全称証明・K1268 予想 C1 バンド m=7 行の z=10 セル確定）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=10 slice for min>=7: for every m>=7 and every nonempty finite multiset X with min(X)=m, H(m+11;X;10)=v(sumX,10,m+11); this fixes the z=10 slice of the strip for all m>=7 (the m=6 z=10 cell is out of band since z*(6)=10), and determines the z=10 cell of the K1268 Conjecture C1 band m=7 row (remaining m=7 row cells: z in {11,12})"
  - "z-ladder lemma structure at z=10: Lemma F10 (F10(s)=H(12;{1}+Y;10) decomposition-independent over all 3,657 decompositions, values 1/0/1/0/1/0/1/0/1/0 at s=0/3..10 with F10(s>=11)=0: the 2-family that had ARRIVED at z=9 as persistent-2 (K1277) DIES at z=10 -- the s=10 value 1 is the single upward deviant vs the sigma-collapse v(s+1,10,12) (5 shapes {(10,),(3,7),(4,6),(5,5),(3,3,4)}), and s>=11 sinks back; the oscillation wavelength of the F-rank 2-family shrinks to a single point for the first time), Lemma G10 (G10(s)=H(13;{2}+Y;10) = 0/1/0/1/0/1/0/1/1/2/1 at s=0/3..8/9/10/>=11; deviants vs v(s+2,10,13) are s=8 DOWNWARD 0<2 (family {(8,),(3,5),(4,4)}) and s=10 UPWARD 2>1 (census 4 shapes {(3,7),(4,6),(5,5),(3,3,4)}, 5 shapes over all decompositions adding (10,)): the first BIDIRECTIONAL 2-deviant coexistence in the G-rank, and the first F->G deviant CHAIN -- the F10(10)=1 upward deviant pushes the G10 mex up to 2), Lemma E10 (E10(s)=H(14;{3}+Y;10) = 1/0/1/0/1/0/1/0/1/0 at s=0/3..8/9 with E10(s>=9)=0; the sole deviant is s=8 UPWARD 1>0 (family {(8,),(3,5),(4,4)}) -- z=9's two deviant points s in {6,8} shrink to s=8 only; the recursion stays in the K1276/K1277 CONDITIONAL form, and the unconditional ghost form again COINCIDES with it over all 3,657 decompositions -- the SECOND consecutive slice of coincidence after z=9, strengthening the z-specificity of the z=8 break; general law open), Lemma D10 (H(15;{4}+Y;10), floored Y>=5, s-only with TWO deviants {6:0, 8:2} against v(s+4,10,15): s=6 DOWNWARD 0<1 (second consecutive slice after D9) and s=8 UPWARD 2>1 -- the first 2-deviant D-rank cell AND the first bidirectional coexistence in the D-rank; note the E10 s=8 upward deviant is NOT absorbed by the D10 mex but CRYSTALLIZES as the parent's own s=8 deviant, whereas at z=9 the E9(8) deviant had been absorbed into D9 -- absorption-vs-crystallization is z-dependent, open; loose floor tokens>=3 breaks at s in {8,10}), Lemma C10 (H(16;{5}+Y;10), floored Y>=6, s-only with the SINGLE s=6 UPWARD deviant C10(6)=1 > v(11,10,16)=0: the D10(6)=0 downward deviant mex-reversal absorption continues for a SECOND consecutive slice, with the absorbed VALUE DECAYING 2 (z=9) -> 1 (z=10); position is the same archetype as the out-of-band witness (5,6)@z=10), Lemma B10 (H(17;{6}+Y;10), floored Y>=7: FULL collapse B10(s)=v(s+6,10,17) over all 700 floored decompositions with zero deviants, second consecutive slice after B9; its C-child 1^v(s+6,9,17) cites the published cell table B9 rather than a strip theorem -- dependency hand-off T-Z8 (z=9, via B9) -> cell tables (z=10)), and Lemma A10 (H(18;{7}+Y;10), floored Y>=8: FULL collapse A10(s)=v(s+7,10,18) over all 460 floored decompositions with zero deviants -- the FIRST full collapse of the A-rank, and the first slice with TWO simultaneously fully-collapsing ranks (B10+A10), extending the full-collapse-rank march D->C->B->A; the A10 C-child 1^v(s+7,9,17) is exactly the published T-Z9 theorem position -- dependency deepening continues on the A side)"
  - "base structure: the m=7 base H(18;X;10) is TRIVIAL ABSORPTION (first observation of this type): the a=7 child is exactly the B10 theorem position v(s+6,10,17) which by the B10 full collapse is IDENTICAL to the stair child v(SUM-1,10,17), so the parent option-set {v(SUM-1,10,17), 1^v(SUM,9,17)} (C-child is the published T-Z9 m=7 position) matches the single-token side with NO deviants used anywhere in the base -- unlike the deviant-absorption bases of K1273 (z=5,m=4), K1276 (z=8,m=5), K1277 (z=9,m=6); the m>=8 step is option-set identity {v(SUM-1,10,m+10)} (a>m child exactly the K1264 stair window edge, a=m child the induction hypothesis on (m-1) at R=m+10=(m-1)+11) and 1^v(SUM,9,m+10) (published T-Z9), matching the single-token side exactly"
  - "boundary sharpness: min>=7 is necessary (m=6 z=10 is out of band since z*(6)=10, separating at exactly one point (6,6) parent 2 vs single 1 UPWARD over all 222 shapes -- the published K1277 witness re-recorded; m=5 z=10 out-of-band separates at exactly (5,6) parent 1 vs single 0, amplitude decayed from z=9's 2 vs 0 with sign preserved), and the NEW observation m=6 z=11 out-of-band separates at (6,6) parent 0 vs single 1 -- a DELTA-SIGN FLIP of the frontier witness (first observed; recorded next-lane). z=11 census registered as open (F11 310 deviants -- the F-rank table splits from v for the first time at scale, consistent with the death of persistent-2; G11 4, E11 7, D11 floored 1, C11 floored 2, D11_loose decomposition-dependent s=10; B11/A11 census-collapse candidates; z=11 strip m in {7..11} 96/96, m=6 band-out 95/96 at (6,6))"
relations:
- type: extends
  target: K1277
  note: "K1277 が全称証明した z=9 スライス（min>=6）の次スライス z=10（min>=7・m=6 の z=10 はバンド外 z*(6)=10 なので床は必然的に m>=7 に上昇）を証明する。証明は K1277 の出版 F9/G9/E9/D9/C9/B9 表・T-Z9（C手子 1^v(Σ,9,m+10) と A10 C手子 1^v(s+7,9,17)）を直接引用し、F10/G10/E10〔条件付き再帰〕D10/C10/B10/A10 の 7 セル梯子で閉じる（梯子が初めて 7 セル化）。K1277 audit の D6c z10_cells census（F10 4・G10 7〔(10,) 含む〕・E10 3・D10 2〔D ランク初〕・C10 1・B10/A10 崩壊観測）は本項の宣言前探査（先行出版 commit 7e079e6a）で完全一致確認の上で主張に昇格した。z=9 の F9 persistent-2 は z=10 で s=10 の 1 点を最後に死ぬ（振動波長 1 点化・初観測）。engine は出版 sha-gate 鎖から機械抽出、出版源は 9 つ（K1277 機 bf3c0c1c… を追加し 10 方 byte 照合 + pin 照合・PROVENANCE PASS・手転写ゼロ）。"
- type: extends
  target: K1270
  note: "K1270 の低 z banded・K1272（z∈{2..4}）・K1273 T-Z5・K1274 T-Z6・K1275 T-Z7・K1276 T-Z8・K1277 T-Z9・本項 T-Z10 の併せ技で m=7 行は z∈{0..10} が確定（残部は z∈{11,12} の2セル）。C1 バンド各行の進捗: m=5 行完走・m=6 行完走・m=7 行 z<=10 確定。"
- type: related
  target: K1268
  note: "統合窓 sharpness から登録された予想 C1 の m=7 行 z=10 セルを確定。z=10 ストリップ崩壊は全 m>=7 で全称証明され、C1 の予想帯と整合。残部は m=7 の z∈{11,12} と m>=8 の z∈{11..z*(m)−1}（m=8 は z∈{11,12,13} の3セル）。"
- type: depends_on
  target: K1264
  note: "階段定理（空でない X・0<=R<=z+min(X) で H(R;X;z)=v(ΣX,z,R)）。母体の a>m 子・F10/G10/E10/D10/C10/B10/A10 セルの A手子評価に窓端ちょうどの等式として使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・中間枝 (R+z)%2。F10/G10/E10/D10/C10/B10/A10 梯子の全場合計算と単一側選択肢集合の算出基盤。"
- type: related
  target: K1273
  note: "底構造の分類（自明吸収 vs deviant 吸収）の交替系列への追加点: z=5 m=4 底（deviant 吸収）・z=8 m=5 底（deviant 吸収）・z=9 m=6 底（deviant 吸収・吸収点 X=(6,6)）に対し z=10 m=7 底は TRIVIAL 吸収（初観測・子に deviant を一切使わない）。これは z=9 の底の類型（deviant 吸収）から z=10 で交替したことを意味し、底の類型の継続性は open。"
- type: related
  target: K1272
  note: "出版 Lemma F（F セル表）系の z=10 延長が F10。F セル値の 2 系は z=6（s>=8→0）→z=7（s>=8→2）→z=8（s>=9→0）→z=9（s>=10→2・persistent）→z=10（s=10 のみ 1 を最後に死滅・波長 1 点化）と、周期 2 振動が z=9 で周期性を破り z=10 で消滅するまでの全歴史が確定した。"
artifacts:
- path: research/experiments/strip-z10-min7-20261124/report.md
  role: proof
  note: 機械監査の正本記録（D1-D9・D6c z=11 census・変異電池 B1-B14・決定性 4 実行・provenance・実行環境リセットと pin 照合復元の誠実記録）。証明全文は宣言ノート §2 にあり本 report は証明そのものではない。F10 persistent-2 の死・G10 2-deviant 双方向同居・D10 D ランク初 2-deviant ・C10 反転吸収 2 スライス〔吸収値減衰〕・B10+A10 2 完全崩壊ランク同居・trivial 吸収底・C1 m=7 行 z=10 セル確定を含む。
- path: research/experiments/strip-z10-min7-20261124/verify_strip_z10.py
  role: verifier
  note: "専用機体（SHA-256 8f29faf7263943f983e5589f16259d02c8c1d7761bea97d13676bed6d30ea768・57,191B・audit/tamper 両モード・engine block は出版 K1264/K1268/K1271-K1277 の9源から sha-gate 機械抽出・pin bd5f22e4…）。D1-D9 宣言 protocol（宣言総計 24,743点/44,548比較: D1 3,657/10,971・D2 330/991・D3 330/992・D4 1,650/4,950・D4b 1,078/3,234・D4c 700/2,100・D4d 460/1,380・D5 1,332/3,996・D6 90/270〔seed 20261129〕・D7a 17/85・D7b 75/225・D8 14,859/14,859・D9 165/495）と D6c census を実装。"
- path: research/experiments/strip-z10-min7-20261124/build_engine_from_published.py
  role: verifier
  note: "provenance sha-gate（出版 K1264・K1268・K1271・K1272・K1273・K1274・K1275・K1276・K1277 の9源から engine block を cut・10方 byte 照合（9源+本機体）+ pin bd5f22e4… 照合・PROVENANCE PASS・手転写ゼロ）。"
- path: research/experiments/strip-z10-min7-20261124/output/audit.json
  role: data
  note: "監査正本（SHA-256 9f9bff605c837407f9a39ab331fc16823e8e0206c4354dd0c56af004ea93f738・12,406B・宣言総計 24,743点/44,548比較 bad 0 と完全一致・meta.verifier_sha256 8f29faf7…・4実行 byte-identical・D6c census に z=11 次レーン観測（F11 310 deviant・G11 4・E11 7・D11 床付き 1・C11 床付き 2・D11_loose s=10・B11/A11 census 崩壊・z=11 strip m∈{7..11} 96/96・m=6 帯外 95/96 (6,6) 親0 vs 単一1〔Δ符号反転〕・m=6 z=10 帯外 (6,6)・m=5 z=10 帯外 (5,6)・E10 無条件 ghost 不一致 0）を記録。"
- path: research/log/2026-11-24-strip-z10-min7-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit 1682cd6764fa23a84c3d377abaf234bd329d60f4・sha256 16f5275d…・F10/G10/E10〔条件付き〕D10/C10/B10/A10 + T-Z10 の証明全文を機械実行前に先行開示・publish-then-execute・宣言前探査の全開示・宣言総計 24,743点/44,548比較の事前登録）。
- path: research/log/2026-11-24-z10-predecl-exploration.md
  role: log
  note: 宣言前探査記録（主張なし・先行出版 commit 7e079e6a・kit と共に機械実行前に全開示）。
- path: research/log/2026-11-24-strip-z10-min7.md
  role: log
  note: run log（選定→探査→宣言→機体組立→公式監査→出版→fetch-back 検証・実行環境リセットによる消失と pin 照合での決定論的復元・採番衝突（仮採番 K1278 が並走 lowz レーンに取得されたため K1279 に再採番）の誠実記録を含む）。
scope: >-
  残余ゲーム H(R;X;z)（K0832/K1138系再帰・K0832 単一トークン閉形式 v）について、
  すべての m>=7・min(X)=m を持つ空でない任意の有限多重集合 X（全形状・全アリティ）に
  対して H(m+11;X;10)=v(ΣX,10,m+11) が成立するという全称命題（proved・F10/G10/E10〔条件付き
  再帰〕D10/C10/B10/A10 閉形式の K0832 場合計算 + 出版 z<=9 補題・T-Z9 引用 + 底 m=7 の
  trivial 吸収 + 選択肢集合一致 + m に関する帰納）。同一証明に含まれる数学的部品として
  Lemma F10（F セル z=10 閉形式表・分解非依存・全称・persistent-2 の死〔s=10 の 1 点を
  最後に沈む〕）、Lemma G10（z=10 の R2型セル閉形式・2 deviant 双方向同居〔s=8 下向き・
  s=10 上向き〕・G ランク初・F→G deviant 連鎖初・全称）、Lemma E10（z=10 の E セル閉形式・
  条件付き再帰期待式・唯一の deviant s=8 上向き・無条件 ghost 形は z=10 でも全分解一致
  〔観測・2 スライス連続〕・全称）、Lemma D10（床付き D ランクセル H(15;{4}∪Y;10)・Y>=5 で
  s-only・2 deviant {s=6 下向き・s=8 上向き}・D ランク初の 2-deviant かつ双方向・E10 s=8
  deviant の結実〔非吸収〕・全称）、Lemma C10（床付き C ランクセル H(16;{5}∪Y;10)・Y>=6 で
  s-only・唯一の deviant s=6 上向き・D→C 反転吸収 2 スライス連続〔吸収値減衰 2→1〕・全称）、
  Lemma B10（床付き B ランクセル H(17;{6}∪Y;10)・Y>=7 で完全崩壊 v(s+6,10,17)・2 スライス
  連続・全称）、Lemma A10（床付き A ランクセル H(18;{7}∪Y;10)・Y>=8 で完全崩壊
  v(s+7,10,18)・A ランク初の完全崩壊・同スライス B10 との 2 完全崩壊ランク同居初観測・
  全称・本項目で初の全称証明）も主張に含む。K1268 予想 C1 の m=7 行は z∈{0..10} が確定
  （残部は z∈{11,12} の2セル）。m>=8 の z∈{11..z*(m)−1}（m=8 は z∈{11,12,13} の3セル）、
  z=11 スライス（F11 310 deviant・B11/A11 census 崩壊候補・(6,6) Δ符号反転 witness・
  min>=8 バンド）、底の類型（trivial vs deviant 吸収）の継続性、F ランク 2 系の波長短縮
  法則、双方向 2-deviant ランク同時発生（G10/D10）の一般則、E ランク無条件 ghost 形の
  z 依存性の一般則、完全崩壊ランクの A 移行と同居の一般則、バンド前線 witness の
  Δ符号反転時刻は open、11×11 盤面のいかなる勝敗も本項目の範囲外。
