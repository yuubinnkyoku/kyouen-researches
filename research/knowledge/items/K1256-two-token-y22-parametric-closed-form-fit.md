---
id: K1256
title: "2トークン残余ゲーム y=22族のパラメトリック閉形式 fit（有限probe box＋box外spot・cand22・observed）"
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases:
  - "two-token y=22 parametric closed-form fit, P22-fit"
  - "cand22 fitting and out-of-box spot verification (fitting stage, pre-universal; first-draft ZERO-correction agreement on all 119,567 probe points; even-y mechanical translation from the published FINAL cand20, the universally proved y=20 table (K1246 promoted, K1249 machine), Y=20->22; reverse rename verified byte-identical to the published cand20 code in both directions)"
  - "seed law 10th consecutive one-shot test passed (even-y pair series 12->14->16->18->20->22, 6-for-6; FOURTH consecutive proved-seed extrapolation after cand11->13 via K1143, cand18->20 via K1242, cand19->21 via K1243/K1248, cand20->22 via K1246); FIRST family with 11 pin rows on BOTH parities simultaneously (z-odd d==2 mod 4 {-18..22}, z-even d==0 mod 4 {-20..20}); MOST out-of-box pin rows in the series (3+3 = 6, series-first on EACH parity, raw-verified by spot deep rows (41,23)/(37,23)/(33,23)/(42,22)/(38,22)/(34,22)); FIRST 23-row consecutive-integer th sweep 23..45; 8th consecutive family with zero in-box merge rows (out-of-box merge regression 123 rows / 19,449 comparisons bad 0); K0915 z=6,y=22 PROVED-slice three-way cross-check: raw probe vs proved T_22/P_22 boxes vs cand22 on ALL 2,450 in-box slice points bad 0; total 182,042 comparison points bad 0"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（box外マージ回帰123行19,449比較・境界行(45,22)/(46,23)のspot照合に使用。y=22ではマージ領域x<=z-23の成立にz>=46を必要としbox z<=30内のマージ行は0行・8族連続のbox内マージ0行〔マージ領域はcensus幾何でも z>=46 が初非空〕）
- type: extends
  target: K1246
  note: seed。cand22初稿は出版cand20（K1246 promoted・K1249機体で全称確定・2トークン族の全称はy=1..20完結）のY=20→22機械翻訳（Y定数・in_T22/in_P22/cand22/b22 rename・docstring・行内コメント値5件の再計算のみでコード本体は全式Y式で1行も変わらず・逆renameが出版cand20コード本体とbyte同一になることを両方向で機械検証）で生成し、probe 119,567点に一発一致。証明済みseed外挿は4連続目（cand11→13〔K1143 proved当时〕・cand18→20〔K1242〕・cand19→21〔K1243〕・cand20→22）。偶数y機械翻訳連鎖12→14→16→18→20→22の第6リンク
- type: extends
  target: K1248
  note: 隣接奇数y族（y=21・K1255機体でobserved→proved済み・2トークン族の全称y=1..21完結）の次の族（第22族・偶数y型）。**全称証明済み範囲（y<=21）の外の最初の族**。対比データ点としてpin mod-4クラス交代（y=20: 0/2・y=21: 1/3・y=22: 2/0）・box外pin個数系列（y=21の3+2→y=22の3+3）・k=Y census偶奇形状分離（y=21の3行→y=22の4行偶数族形状{20,22}/{21}/{22}・y=16/18/20と同型の4データ点目）・band下端系列44→46・掃引長21行→23行。y=22全称段階のB子は出版cand21の逐語転写（x=22合流子{21,22}≡{22,21}でy=21族x=22行と同一状態）で**系列初の全称確定済みB-child**
- type: extends
  target: K1238
  note: even-y統一テンプレートの第7データ点（偶数y族式〔z-odd I行k=floor((d+3y+2)/4)の連続整数th掃引23..45・base行同式floor((d+3y+1)/4)・偶z I行k=floor((d+3y-1)/4)・pin格子統一式o_pin=(d+3y)/2・pin行数(y+2)/2とy/2の同時11・単一band則2y+2..x+22・偶z対角値1欠如・tail x奇行〕のy=22でのfit level継続観測）。20→22は宣言c0baada6配下の事前登録どおり
- type: extends
  target: K1143
  note: 「pinスロット=th-1」（奇z I行）と偶z base行2k+1 slot則（y=11..21の11族連続に続き12族目として奇z 11 pin行・偶z 11 pin行すべてで算術的に成立〔2k(d)=o_pin(d)と2k(d)+1=o_pin(d)が全pin行で恒等的に成立〕）
- type: related
  target: K0915
  note: z=6,y=22証明済み切片（全称証明）との交差検証。宣言で補助的と事前登録し、実行では出版T_22(x)/P_22(x)表を監査生成器へ転写してprobe box内z=6切片（x=22..49・R<=x+52）全2,450点の三点照合（生probe値vs証明済み分類・cand22 vs証明済み分類）をfail-closed gateで実施しbad 0。ラダー{1,3,5}・pin(22,6)@47〔d=16〕・(26,6)@49〔d=20〕・掃引x=29の{51,53,55,57}・定常R=51〔=z+2y+1〕・tail R>=x+29→(x+22) mod 2が宣言予想・K0915出版表・生値で完全一致。転写トラップ（tail下端O[x+30,∞)を一時x+31と誤転写→境界点11点のみを検出）はfail-closed設計の作動実例として帳簿に記録（独立裏付け・本項はobserved・2レーンの相互補強の記録）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/report.md
  role: proof
  note: fit段階の正本記録（119,567 probe点一発一致・box内tail assertion 27,528点・box外spot 43,026点（全11奇z pin行・全11偶z pin行の個別行選択・6 box外pin行(41,23)/(37,23)/(33,23)/(42,22)/(38,22)/(34,22)のR<=130生値照合・全選択行にx>=22機械preflight assert）・merge回帰123行/19,449比較・tail raw 78点・K0915三点交差検証2,450点bad 0・事前横断予想の判定表（全18行一致・amendment不要）・誠実記録5点（宣言前deep smoke開示・sandboxリセットからの再構成・K0915転写トラップ・pinned秒数337.0・対抗宣言確認手段の限界）・y=12..y=22横断判定・宣言値のsha256ピン）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/cand22.py
  role: verifier
  note: 閉形式の正本cand22（in_T22値2表・in_P22値1表・Y=22・偶数y型で値1無限帯・tailはx奇行）とprobe全点照合（119,567点・mismatch 0・overlap 0・初稿一発一致）。出版cand20のY=20→22機械翻訳でコード本体は1行も変わっていない（逆rename byte同一を両方向で機械検証・translate_y22.py・結果docstring確定版に対しても本体検証再実行PASS）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/probe_y22.py
  role: verifier
  note: 生二重再帰probe（正準降順multiset memoization・z=0..30・x=22..z+43・R<=x+z+46=2y+2拡張cap・1,147行119,567点を書き出す決定論的生成器・6回再生成byte-identical incl. 隔離tree+env -i+PYTHONHASHSEED=random・probe_rows.txt SHA-256 2380c951…）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/spot_y22.py
  role: verifier
  note: box外spot（全11奇z pin行・全11偶z pin行を個別行選択したdeep rows R<=130 46行・bigz z=31..40・x=y=22 edge・far d∈{44,55,66}・tail raw・merge回帰123行/19,449・LRU cap 1.5M決定的退避・3バッテリーで全ブロック集計とCacheInfo完全一致）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/make_audit_y22.py
  role: verifier
  note: 監査生成器（box幾何独立再計算ゲート（宣言機械事前算出1,147行/119,567点と厳密照合）・値ヒストグラム事前予想等価ゲート{0:58950,1:49478,2:11139}・逐行整合性ゲート・in-box tail depth 24点/行27,528点ゲート・in-box merge 0行ゲート・in-box pin格子観測ゲート〔8+8行・R=z+(d+66)/2〕・K0915出版T_22/P_22表転写によるz=6切片全2,450点三点照合fail-closedゲート・fail-closed・最終版3回実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/spot_chunk_rerun_y22.py
  role: verifier
  note: spot決定性再実行driver（sandboxの単一実行300秒上限と環境リセット下で、出版spot_y22.pyのmain()を一意マーカーでバイトスライスしdeep/bigz/edge/far/tailmergeの各ブロックをexec再実行。3バッテリーで全ブロック集計・LRU CacheInfo行が完全一致・pinned合計337.0秒）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/translate_y22.py
  role: verifier
  note: Y=20→22機械翻両方向検証器（翻訳生成と逆renameの出版cand20コード本体byte同一検証・docstring確定版に対する再検証含む）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/tamper_battery_y22.py
  role: verifier
  note: fail-closed改ざんバッテリ（20変種すべてcaught・leak 0・no-op 0・ANCHOR EFFECTIVENESS事前assert・復元byte検証・battery終了後のrestore再実行がaudit.json確定shaを再現）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/output/audit.json
  role: data
  note: fit監査正本（SHA-256 fecfc248…15b905b・自己文書化・probe/spot/merge/tail数値・sha256ピン〔probe_rows 2380c951…・cand22 7a62577b…・probe_y22 b525e64b…・spot_y22 d176336b…・spot_chunk_rerun f697a1d6…〕・宣言commit c0baada6記録・K0915三点照合2,450点bad 0・両偶奇11 pin行とbox外pin 3+3の族初の記録）
- path: research/log/2026-11-23-y22-two-token-skeleton-single-owner-note.md
  role: log
  note: fit段階の単一オーナー宣言ノート（commit c0baada6・probe実行前に出版・事前横断予想の全記録・対抗宣言チェック・box幾何1,147行/119,567点・総比較点182,042の出版前機械算出・逆rename両方向検証の事前登録・宣言前deep smoke 1回の誠実開示・fetch-back byte検証 SHA-256 b552094d…d6cce）
- path: research/log/2026-11-23-two-token-y22-parametric-fit.md
  role: log
  note: fit段階の実行記録（選定・宣言・経緯・系列初一斉達成3件・誠実記録5点・出版記録〔Commit A 3b69574e・fetch-back byte検証〕・次段階〔y=22全称はB子cand21逐語＝系列初の全称確定済みB-child〕）
---

# K1256: 2トークン残余ゲーム y=22族のパラメトリック閉形式 fit（observed）

## 命題（fit段階・有限範囲で確定・全称は未証明）

すべての z>=0・x>=22・R>=0 に対して H(R;(x,22);z) = cand22（`cand22.py` が正本・
z 偶奇別 T/P 集合表・Y=22・偶数 y 型で値1無限帯・tail は x 奇行・d = x-z・off = R-z）。
**本項の status は observed**: 検証は有限 probe box（z=0..30・x=22..z+43・R<=x+z+46）
+ box 外 spot（宣言電池合計 182,042 点比較・bad 0）であり、全称（全 z・全 x・全 R）は
次段階の別宣言（verify_y22_universal.py・K 番号は追って採番）で挑む。
コード本体は出版 cand20（K1246 promoted・全称確定）の Y=20→22 機械翻訳で 1 行も変わらず、
逆 rename が出版 cand20 コード本体と byte 同一になることを両方向で機械検証した
（translate_y22.py）。

## 主結果（宣言 c0baada6 配下・publish-then-execute）

- **初稿一発一致**: probe 119,567 点 mismatch 0・T/P overlap 0・値ヒストグラム
  0:58,950/1:49,478/2:11,139 が宣言の事前機械予想と厳密一致・値 3 なし。
  seed 法則 10 連続（偶数 y 6 連続）・証明済み seed 外挿 4 連続。
- **系列初一斉達成 3 件**: ①両偶奇同時 11 pin 行（初）②box 外 pin 各偶奇 3 行・
  合計 6 行（系列最多）③23 行 th 連続整数掃引 23..45（初）。
  いずれも偶数 y 族式（y=10,12,…,22）からの外挿どおりで、宣言で事前登録された。
- **K0915 証明済み z=6,y=22 切片との三点照合**（補助・宣言電池外）: 全 2,450 点 bad 0。
  指摘対象となる転写ミス（tail 下端 x+30→x+31）は境界点 11 点のみで fail-close 検出。
- **マージ回帰**: cand22 == single_token(x+22,R)（K0832）を box 外 123 行 19,449 比較 bad 0。
  y=22 は box 内マージ行 0 行（z>=46 必要）が 8 族連続。
- **決定性・fail-closed**: probe 6 回再生 byte 同一・audit 3 回 byte 同一・
  spot 3 バッテリー全統計一致・改ざん 20 変種すべて caught（no-op 0・leak 0・
  anchor 実効性事前 assert・復元 byte 検証）。

## 検証規模（宣言電池合計 182,042 点・bad 0）

| 検査 | 規模 | bad |
|---|---:|---:|
| probe box（1,147 行）全点照合 | 119,567 点 | 0 |
| box 内 tail assertion（24 点深/行） | 27,528 点 | 0 |
| spot deep 46 行 R<=130 | 5,980 点 | 0 |
| spot bigz 240 行 | 30,240 点 | 0 |
| spot x=y=22 edge 25 行 | 4,100 点 | 0 |
| spot far 18 行 | 2,628 点 | 0 |
| tail raw | 78 点 | 0 |
| merge 回帰 vs K0832 | 19,449 比較 | 0 |
| K0915 z=6 三点照合（補助・電池外） | 2,450 点 | 0 |

## 誠実記録

帳簿づけ 5 点（宣言前 deep smoke 1 回の開示・sandbox リセットからの出版参照による再構成
〔再生成 probe の byte 同一再現で検証〕・K0915 転写トラップ・pinned 秒数 337.0・
対抗宣言確認手段の限界）の正本は report.md・fit log に同じ。

## 範囲外の維持

標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は UNKNOWN のまま。
3 トークン以上・y>=23 族・固定幅・q点版は範囲外。 y=22 の全称（A子/B子cand21逐語
〔系列初の全称確定済み B-child〕/C子・clip 窓 2y+2=46 tight 判定）は本項の昇格条件であり
別宣言。y=23 fit の seed は cand21（K1248 proved）。
