---
id: K1258
title: "2トークン残余ゲーム y=23族のパラメトリック閉形式fit（observed・有限box+box外spot 合計194,899点 bad 0・全称は未証明）"
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases:
  - "two-token y=23 parametric closed-form fit, P23-fit"
  - "cand23 fitting and out-of-box spot verification (fitting stage, observed, NOT universal; first-draft ZERO-correction agreement on all 126,821 probe points; odd-y mechanical translation from the published FINAL cand21, the universally proved y=21 table (K1248 promoted, K1255 machine), Y=21->23; reverse rename verified byte-identical to the published cand21 code in both directions; translation chain cand11->13->15->17->19->21->23, 6th odd-y link)"
  - "seed law 11th consecutive one-shot test passed (odd-y series 6-for-6: 11->13->15->17->19->21->23; even-y series 5; FIFTH consecutive proved-seed extrapolation after cand11->13 via K1143, cand18->20 via K1242, cand19->21 via K1243/K1248, cand20->22 via K1246/K1256/K1257, cand21->23 via K1248); FIRST single-parity 12 pin rows (z-odd d==3 mod 4 {-21..23}, odd-y family formula (y+1)/2); FIRST odd-y family with 11 z-even pin rows (d==1 mod 4, (y-1)/2); MOST out-of-box pin rows in the series (4+3 = 7: FOUR on the z-odd parity — first family ever — and seven in total; raw-verified by spot deep rows (45,24)/(41,24)/(37,24)/(33,24)/(42,23)/(38,23)/(34,23), full R<=130 rows bad 0); FIRST 24-row consecutive-integer th sweep 23,25,25,...,45,45,47 (final th=2y+1=47 observed directly in-box); 9th consecutive family with zero in-box merge rows (out-of-box merge regression 117 rows / 19,005 comparisons bad 0, boundary rows (47,23)/(48,24) raw-matched in the deep block); K0917 z=6,y=23 PROVED-slice three-way cross-check: ALL 2,639 in-box slice points agree with both the raw engine and cand23 (auxiliary, PRE-DECLARED as outside the declared battery; zero transcription corrections needed — a one-shot full-point agreement); value histogram gate {0:62566,1:52845,2:11410} pre-declared and matched exactly; total 194,899 comparison points bad 0 (probe 126,821 + spot 48,995 + tail raw 78 + merge 19,005); the FIRST family beyond the universally proved range y<=22; first family verified with a 6-chunk bigz z-subrange driver after the whole-block run exceeded the 300s sandbox cap; z=32 slice gap (32,767 vs declared 36,190) caught by the declared-geometry cross-check BEFORE publication and closed (3,423 points bad 0)"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（box外マージ回帰117行19,005比較・境界行(47,23)/(48,24)のdeep spot照合に使用。y=23ではマージ領域x<=z-24の成立にz>=47を必要としbox z<=30内のマージ行は0行・9族連続のbox内マージ0行〔マージ領域は幾何でも z>=47 が初非空〕）
- type: extends
  target: K1248
  note: seed。cand23初稿は出版cand21（K1248 promoted・K1255機体で全称確定・2トークン族の全称はy=1..21完結）のY=21→23機械翻訳（Y定数・in_T23/in_P23/cand23/b23 rename・行内コメント値5件の再計算・selfcheck domain assert定数のみでコード本体は全式Y式で1行も変わらず・逆renameが出版cand21コード本体とbyte同一になることを両方向で機械検証）で生成し、probe 126,821点に一発一致。証明済みseed外挿は5連続目（cand11→13〔K1143 proved当时〕・cand18→20〔K1242〕・cand19→21〔K1243/K1248〕・cand20→22〔K1246/K1256/K1257〕・cand21→23）。奇数y機械翻訳連鎖11→13→15→17→19→21→23の第6リンク
- type: extends
  target: K1256
  note: 隣接偶数y族（y=22・K1257機体でobserved→proved済み・2トークン族の全称はy=1..22完結）の次の族（第23族・奇数y型）。**全称証明済み範囲（y<=22）の外の最初の族**。対比データ点としてpin mod-4クラス交代（y=21: 1/3・y=22: 2/0・y=23: 3/1）・box外pin個数系列（y=22の3+3→y=23の4+3・単一偶奇側4行と合計7行の両方で系列最多更新）・k=Y census奇偶形状分離の継続（y=22の4行偶数族形状に対しy=23は奇数族3行形状 d-set {22,23,23}・cand23意味論では3行ともk=Y=23・y=17/19/21と同型の5データ点目）・band下端系列46→48（11データ点目）・掃引長23行→24行（初の24行掃引）。y=23全称段階のB子は出版cand22逐語転写（x=23合流子{22,23}≡{23,22}でy=22族x=22行と同一状態）で**2族連続の全称確定済みB-child**
- type: extends
  target: K1143
  note: 「pinスロット=th-1」（奇z I行）と偶z base行2k+1 slot則（y=11..22の12族連続に続き13族目として奇z 12 pin行・偶z 11 pin行すべてで算術的に成立〔2k(d)=o_pin(d)と2k(d)+1=o_pin(d)が全pin行で恒等的に成立〕）
- type: related
  target: K0917
  note: z=6,y=23証明済み切片（全称証明）との交差検証。宣言で補助的と事前登録し、実行では出版T_23(x)/P_23(x)表を監査生成器へ機械転写し、probe box内z=6切片（x=23..51・R<=x+54）全2,639点の三点照合（生probe値vs証明済み分類・cand23 vs証明済み分類）をfail-closed gateで実施しbad 0・転写修正0の一発全点一致。ラダー{1,3,5}・pin(23,6)@49〔d=17〕・(27,6)@51〔d=21〕・掃引x=30の{53,55,57,59}・定常R=53〔=z+2y+1〕・tail R>=x+30→(x+23) mod 2が宣言予想・K0917出版表・生値で完全一致（宣言の194,899点電池には含めない3方向独立整合・fit observedと全称証明スライスの相互補強の記録）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y23-parametric-fit-20261123/report.md
  role: proof
  note: fit段階の正本記録（126,821 probe点一発一致・box内tail assertion 29,450点〔25点深/行〕・box外spot 48,995点（全12奇z pin行・全11偶z pin行の個別行選択・7 box外pin行(45,24)/(41,24)/(37,24)/(33,24)/(42,23)/(38,23)/(34,23)のR<=130生値照合・全選択行にx>=23機械preflight assert）・merge回帰117行/19,005比較・tail raw 78点・K0917三点交差検証2,639点bad 0・事前横断予想の判定表（全行一致・amendment不要）・誠実記録5点（宣言前raw実行0回・sandboxリセットからの再構成・bigz z=32抜けの出版前捕捉・pinned秒数592.2/host依存・対抗宣言確認とK番号）・y=11..y=23横断判定・宣言値のsha256ピン）
- path: research/experiments/vertical-fiber-two-token-y23-parametric-fit-20261123/cand23.py
  role: verifier
  note: 閉形式の正本cand23（in_T23値2表・in_P23値1表・Y=23・奇数y型で値1無限帯・tailはx偶行）とprobe全点照合（126,821点・mismatch 0・overlap 0・初稿一発一致）。出版cand21のY=21→23機械翻訳でコード本体は1行も変わっていない（逆rename byte同一を両方向で機械検証・translate_y23.py・SHA-256 0d70a440…）
- path: research/experiments/vertical-fiber-two-token-y23-parametric-fit-20261123/probe_y23.py
  role: verifier
  note: 生二重再帰probe（正準降順multiset memoization・z=0..30・x=23..z+45・R<=x+z+48=2y+2拡張cap・1,178行126,821点を書き出す決定論的生成器・3回再生成byte-identical incl. 隔離tree+env -i+PYTHONHASHSEED=random・probe_rows.txt SHA-256 9668376a…・実行17.8s）
- path: research/experiments/vertical-fiber-two-token-y23-parametric-fit-20261123/spot_y23.py
  role: verifier
  note: box外spot（全12奇z pin行・全11偶z pin行を個別行選択したdeep rows R<=130 46行/5,980・bigz z=31..40・x=y=23 edge・far d∈{46,57,68}・tail raw・merge回帰117行/19,005・LRU cap 1.5M決定的退避・2バッテリーで全ブロック集計とCacheInfo完全一致・pinned 592.2s）
- path: research/experiments/vertical-fiber-two-token-y23-parametric-fit-20261123/spot_chunk_rerun_y23.py
  role: verifier
  note: spot決定性再実行driver（sandboxの単一実行300秒上限下でbigzはブロック単体も超過するため、モジュール定数BIGZ_ZSを6つのz部分区間〔31-32/32-33/33-35/35-37/37-39/39-41・z=31..40を1行1回ちょうど被覆〕に束ねてチャンク実行・z32抜けの交叉確認記録をdocstringに保存）
- path: research/experiments/vertical-fiber-two-token-y23-parametric-fit-20261123/make_audit_y23.py
  role: verifier
  note: 監査生成器（box幾何独立再計算ゲート（宣言機械事前算出1,178行/126,821点と厳密照合）・値ヒストグラム事前予想等価ゲート{0:62566,1:52845,2:11410}・逐行整合性ゲート・in-box tail depth 25点/行29,450点ゲート・in-box merge 0行ゲート・in-box pin格子観測ゲート〔8+8行・R=z+(d+69)/2〕・K0917出版T_23/P_23表転写によるz=6切片全2,639点三点照合fail-closedゲート・fail-closed・最終版3回実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y23-parametric-fit-20261123/translate_y23.py
  role: verifier
  note: Y=21→23機械翻訳両方向検証器（docstringをインラインした自己完結型・翻訳生成と逆renameの出版cand21コード本体byte同一検証・cand23.py byte同一再生成を確認済み）
- path: research/experiments/vertical-fiber-two-token-y23-parametric-fit-20261123/tamper_battery_y23.py
  role: verifier
  note: fail-closed改ざんバッテリ（20変種すべてcaught・leak 0・no-op 0・ANCHOR EFFECTIVENESS事前assert・復元byte検証・battery終了後のrestore再実行がaudit.json確定shaを再現・T08は行120・T19はz-odd pinアンカーの一意化で%4==0行までマッチのy23適応点をコメント記録）
- path: research/experiments/vertical-fiber-two-token-y23-parametric-fit-20261123/output/audit.json
  role: data
  note: fit監査正本（SHA-256 dc646f24…57d3e004・自己文書化・probe/spot/merge/tail数値・sha256ピン〔probe_rows 9668376a…・cand23 0d70a440…・probe_y23 0e1786f4…・spot_y23 f5802732…・spot_chunk_rerun b1d60ad2…〕・宣言commit 6f79c81f記録・K0917三点照合2,639点bad 0・単一偶奇側12 pin行・box外pin 4+3・z32抜けのhonest record・status "finite fit + out-of-box spot verification; NOT a universal claim"）
- path: research/log/2026-11-23-y23-two-token-skeleton-single-owner-note.md
  role: log
  note: fit段階の単一オーナー宣言ノート（commit 6f79c81f・probe実行前に出版・事前横断予想の全記録・対抗宣言チェック・box幾何1,178行/126,821点・総比較点194,899の出版前機械算出・逆rename両方向検証の事前登録・宣言前raw実行0回の正直な開示）
- path: research/log/2026-11-23-two-token-y23-parametric-fit.md
  role: log
  note: fit段階の実行記録（選定・宣言・経緯・系列初一斉達成（単一偶奇側12 pin行・box外pin 4+3=7行・24行掃引）・誠実記録5点・出版記録〔fetch-back byte検証〕・次段階〔y=23全称はB子cand22逐語＝2族連続の全称確定済みB-child〕）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,23)について、z偶奇別のパラメトリック
  T/P集合表（閉形式cand23・出版cand21のY=21→23機械翻訳でコード本体不改変・
  逆rename両方向byte同一）がGrundy値0/1/2を分類するというfitレベルの命題
  （observed・有限範囲で確定）。証拠は宣言済み電池 合計194,899点比較・不一致0
  （probe box z=0..30・x=23..z+45・R<=x+z+48 の126,821点＋box外spot 48,995点＋
  tail raw 78点＋merge回帰19,005比較）と、宣言外の補助照合である
  K0917 z=6,y=23証明済み切片との三点照合2,639点 bad 0。全z>=0・全x>=23・全R>=0の
  全称は本項の範囲外で未証明（次段階verify_y23_universal.py・別の単一オーナー宣言）。
  系としてx<=z-24の単一トークン一致マージ命題y=23版とtail R>=x+z+24の(x+23) mod 2も
  fitレベル観測に留まる。標準11×11の空盤・二石root・S2 {59,60}・class 1/2/4は
  範囲外かつUNKNOWNのまま。3トークン以上・y>=24族・固定幅・q点版も範囲外。
