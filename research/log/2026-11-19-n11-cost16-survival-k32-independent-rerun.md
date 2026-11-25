# 2026-11-19 N11 31行cost-16 parent 生存曲線 k=32: 完全独立第二実行の全値一致の記録（independent rerun）

## 経緯（並走出版の検出・上書きなし）

k=31本計算出版とrank-32 preread（commit `490a3e44`・preread JSON blob `6d49ab5bea27c967e15b482b33e376510c62b857`・31 checks all PASS）を起点に、当レーンは出版済みk31 script（blob `7a292ea91fd5c19758ed5b84cfda04a8a2caa155`）からの機械変換で k=32 本計算に着手した（着手時点で k32 本計算は未出版と確認済み）。計算はquadsをdrive_quads.shのfenceバッチ運転・quintsをdrive_quints.shで実行し、slice単位JSONL append＋done()フェンスにより完走したところ、**並走レーンがまさに同時刻に k=32 出版を完了していた**（script+log commit `62c29d080`〔22:38:57Z〕・result JSON `595f0a279`〔22:39:08Z〕・record JSONL `f8bd71fed1`〔22:39:20Z〕・log修正 `71d6f07c3e`〔22:39:40Z〕）。当レーンはpush直前のHEAD再取得でこの出版を検出し、**上書きせず**本rerun logのみを別pathで出版する（k23衝突・k24 rerunで確立した運用教訓の再実効確認）。当レーンの実行は「第二の完全独立実行」として、repo慣習（k23 3実行・k24 2実行一致）に従い出版版との全値照合を最優先とした。

## 当レーンの独立計算（要約）

出版済みk31 scriptをconvert_k32.pyで機械変換し、k32 scriptを生成（84,252B・git blob `137f1ec169982f4c018f56fd18f59c2b90269505`・sha256 `75544564b44b2ddef82f8d4cc7ab5c3ca2e3e6109e0cf16c5815a7567aa2e252`）。変換仕様は52 checks（k31の51 + 新check `quints.new_era_double_row_23_absent`）。classifyによる新census全数事前導出でk32 preread（commit `490a3e44`）のpair/triple/quad/quint/sextet censusと全一致を確認してから本計算した。実行: anchor 10/10 match・pairs 31/31・triples 465/465（12 slice）・quads 4,495/4,495（75 slice）・quints 2,010/2,010（b_onlyのみ格納）・cross 4系統×2全match・finalize **52 checks ALL PASS**・finalize二重実行byte-identical（当レーンresult JSON 1,055,230B・sha256 `e7050d2e58ff1be937a25fa08ec66343a152adf51f7d5e05712fa9e444f6afc7`・git blob `2c09748ab7ba8f0dd470350347d8e53a31471f99`〔未出版〕・JSONL 1,093,583B 7,019 records・sha256 `067d2bd621bc64b54ab26e835118bb145e08cb50c189612a5906facb62207316`・git blob `4e26abdd1304c8fb0211c1100ce52e3b943426f8`〔未出版〕）。schema `n11-cost16-survival-k32-20261118-v1`（出版版と同一）。

- **確定値（出版版と全て一致）**: kill(32) = 2,551,395,717,771,593,231（全最小cover計画 2,966,450,341,680,481,356 の86.008374%）・kill_A(32) = 1,973,582,768,304,605,600・kill_B(32) = 577,812,949,466,987,631（和恒等式機械検証済み）・marginal(32) = 25,276,899,310,145,517（m32 = 120,146,272,057,315,812 の**21.0384%**・k31ハブ帯44.03%から急落の低位20%台。preread予測〔「disjoint 24本でやや下振れ」〕に的中）・**B_survive = 82,850,100,919,559,337（2.792904%・過去最低・初の2.8%割れ）**・A_survive = 332,204,522,989,328,788。
- **新層I-E分解（出版log同一の数値を独立導出・厳密成立）**: marginal = m32 − Σ新j2（127,404,469,561,558,572 = m32の106.0411%: disjoint 24本で126,903,719,186,283,657〔本平均5,287,654,966,095,152 = m32の4.4010%〕＋shared 7本で500,750,375,274,915〔0.4168%〕）＋ Σ新j3（34,561,550,958,404,013）− Σ新j4（2,041,444,240,745,655）＋ Σ新j5B（14,990,096,729,919）。
- **構造（出版版と一致）**: 新pair 7 shared / 24 disjoint・新triple 275 b_only / 50 zero / 140 disjoint・新quad 1,878 b_only / 2,459 zero / 158 disjoint・新quint 2,010 b_only（新era累計8,797 = 6,787+2,010・b_only quint二重行 {15:1616, 16:304, 18:5111, 19:1766} に行23は不参加のまま）・full census C(32,3)=4,960（2,992/980/988）・C(32,5)=201,376（8,797/192,579/0）・**C(32,6)=906,192 sextet all zero（I-E quint打ち切り・k=26から8連続機械保証）**。**行23がrank-32で初めて二重行族に参加**（triple層9 record・quad層12 record・quint層0）。

## 交叉検証: 2つの完全独立実行の全値一致

当レーン計算と出版版（result JSON blob `6bf47e8745300ae6235180591978daf9d7fe09e5`・record JSONL blob `c4f06b23ad64ae97cb642b244f2d675cd0bf6903`・script blob `ba9592883a8f622d8bb7cfd6fe7c19a14febadc3`）の全出力を比較した結果:

1. **JSONL（7,019/7,019 records）**: key set・格納順序が完全に同一。**sec（wall-clock）以外の全field差分0・memo_states差分0**（joint_A/joint_B/joint/class/lineage/combo等も含む）。差異は298 recordsの`sec`値のみ（byte-identicalな行は6,721/7,019）。両ファイルの総容量が同一の1,093,583Bであることも含め、両実行が同一のrecord体系を独立に再生したことを示す。
2. **result JSON**: `values`（kill k=1..k32全点・A_survive・B_survive_full_singleton_ban・B_survive_share_percent）・`structure`（census・histogram・rank32_root〔root hex・rows・membership・A/B分割〕・preread構造値）・`total_minimum_covers`・`type_A_total`/`type_B_total`・`inputs`（31個のpinned入力blob pin: phase-B aggregate `31bdefdb…`・k13〜k31 result JSON・k32 preread `6d49ab5b…`）が**全て完全一致**。schema・lane・date・interpretation_guard・unknown_statusも同一。両実装が同一pinned入力31点を参照した同一計算であることを、入力pin層から出力値層まで機械確認した。
3. **finalize check体系の実装差**: 共通50 checkは**detail field含めてbyte-identical**・全PASS。row-23新事実の保証は両実装とも1本のcheckで行うが名前が異なる（出版 `quads.new_b_only_double_row_23_quad_layer_only` / 当レーン `quads.new_b_only_double_row_23_first_doubling`・**detailのhistogramは同一** {0:14, 1:2, …, 15:635, 16:31, 18:847, 19:315, **23:12**, 30:2}）。当レーン版はさらに `quints.new_era_double_row_23_absent`（detail {15:613, 16:65, 18:962, 19:370}: 新era 2,010本のquint二重行histに行23が不在であることを和2,010とともに保証）を持ち、check_count 51 vs 52の差はこの実装差のみ。
4. **テキスト系の文言差（数値影響なし・erratum対象外）**: (i) titleの後半文言: 出版版はfull quint層hist {15:1616, 16:304, 18:5111, 19:1766}を引用、当レーン版は新era 2,010本のhist {18:962, 15:613, 19:370, 16:65}（和=2,010に一致）を引用。両histogramとも両JSONの`structure`に実データで格納されており、文言上の参照先が異なるのみで事実の食い違いはない。(ii) `inputs`のk31 JSON key名（出版 `survival_k31_json` / 当レーン `k31_json`・pin値は同一）。(iii) preread注記key名（`preread_exact_integers` / `preread_exact_integer`・本文は同一趣旨）。(iv) 3件のstructure noteの言い回し差（rank32_root注記・triple/quad二重行hist注記。同一計算事実の表現差のみ）。
5. **wall-clock指紋の独立性**: JSONLの`sec`総和は出版版約0.74h・当レーン約0.77h、pair層最高値は69.7s vs 76.5s（secを持つrecord数も層ごとに同一の {pair 31, triple 415, quad 2,036, quint 2,010}）で、両実行が別々の物理実行であることを残差側から確認できる。

以上より **k=32 は、k23（3実行）・k24（2実行）と同型に「異なる変換系統から生成された2実装・2実行の全値一致」により二重に独立検証された**。

### 多重検証の補足

- anchor 10 record（k13 pair joint×2系統・k31出版disjoint record再錨付け）mismatch 0・cross 8 record（cross3/cross4/crossq4/cross5各2）published参照値と全一致。出版k32 scriptとの差異は実装の系統（変換表・文言生成・check体系）に由来し、計算の組合せ論的内容は全record値等価により同一であることが示された。
- k32 preread（commit `490a3e44`）は純Python正確整数であり、両実装ともload時にA+B==M32（92,121,445,452,103,947 + 28,024,826,605,211,865 = 120,146,272,057,315,812）をassert・preread_match.*全検証PASS。k31で問題となったNode丸めerratum系統の再発はない。

## erratum判定: なし

数値・check体系・入力pinは全一致であり、文言差はすべて両版とも事実として正しい表現差（上記4項目）であるため、正本側の修正を要するerratumは存在しない。k24 rerunで記録した「title誤記（k23文言残存）」型の取りこぼしは本rankでは不発生（title文言差は参照先の異なる正しい記述）で、機械変換時の文言field一覧grep教訓の実効が確認できた。

## 運用メモ

1. **push直前HEAD再取得が再び有効**: 出版検出は計算完了後だったため重複計算コストは発生したが、上書き事故は皆無。毎時運行の並走では k33 以降も着手前に直近実行の着手時間帯を考慮する。
2. **check体系の命名は変換系統で自律発散する**: 同一のrow-23事実が2実装で別名のcheckとして実装された。rerun照合はcheck名集合ではなく「名前基準の対応付け＋detail含む本体比較」で行うべき（utils化の価値あり）。

## 次段（次回レーン候補）

1. k32 crosscheck拡張: `cost16_survival_k13_k14_crosscheck_20261118.py`（現版 blob `b71a3211917057cd36cb4e1f9b006d7298cf7fa0`・42,522B）へのk32点追加（PINSに result JSON blob `6bf47e87…`〔commit `595f0a279`〕・record JSONL blob `c4f06b23…`〔commit `f8bd71fed1`〕・record層checks・quint census接続 8,797=6,787+2,010・era接続）で+checks出版。
2. k33本計算（preread出版済: blob `e4346ddd…`・commit `67068e07`・rank-33 (7,19)・m33 = 120,083,817,332,086,665）。着手前に出版済みでないかの確認を必須とする。k34 prereadも出版済み（`8dbb1bcb…`〔commit `2a14f351`〕・rank-34 (9,19)・m34 = 120,079,520,746,539,458）。

## 11×11 状態（interpretation guard）

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。生存曲線（kill/survive系列）はban回避の代替最小cover計画の組合せ数であって、探索コストでもverdictでもない。B_surviveの過去最低更新（2.8%割れ）もcover-plan組合せ論の度量であり、勝敗とは無関係である。REFUTED-D10・STERILE は LOSS 証明ではない。
