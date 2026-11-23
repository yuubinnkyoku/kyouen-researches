---
id: K1244
title: "2トークン残余ゲーム y=18族の全称検証: 正本検証器 verify_y18_universal.py part1 12チェック全 PASS（K1242 は observed のまま・昇格はpart2）"
kind: computation
status: computed
topics: [grundy, residual-games]
aliases:
  - "universal verifier part 1 for the two-token y=18 residual family H(R;(x,18);z): raw-engine anchored 12-check machine, overall PASS with 6,354,790 comparison points and bad 0"
  - "closed-form identity grid, deep-tail rows, option decomposition raw anchor, type machine with clip window 2y+2=38 sentinel 39 and 523,398 types (series: y=14: 281,912 -> y=15: 335,658 -> y=16: 394,686 -> y=17: 457,645 -> y=18: 523,398), tightness probe showing clip 37 has 1,012 confluence violations (first (60,100,100)) so 38 is tight (14-family streak y=5..18: 12/14/16/18/20/22/24/26/28/30/32/34/36/38)"
  - "census anchor z=0..79, x=18..70, R<=x+z+19 over both raw engines via bounded-memoization twins (published code object rebound to an LRU-capped recursive cache, cap 1,600,000) run as separate commands C11ordered/C11canonical (438,840 points each engine, 53 x-rows per z, ~19 s each) and fail-closed merged in the C11 mode with recomputed expected counts (points 438,840 / merge 110,682 / tail 4,240 per engine)"
  - "merge corollary x<=z-19 implies single_token(x+18,z,R) verified at 1,121,822 points (census merge rows first non-empty at z=37, 4th consecutive family whose probe box contained zero merge rows) and tail corollary R>=x+z+19 implies (x+18) mod 2 verified at 192,210 points, both with 0 mismatches"
relations:
  - type: extends
    target: "K1242"
    note: "K1242（y=18族 fit・cand18・出版時 observed）の正本監査段階 part1。A子=x==18 なら cand17(z,18,R-1)（合流子 {17,18}≡{18,17} の多重集合同値・x>=19 は cand18(z,x-1,R-1)）・B子=出版 cand17（K1240 全称・K1241 part1/part2機で proved 昇格済み）・C子=1 xor cand18(z-1,x,R-1) の12チェック。observed→proved の昇格判定は part2（C1d・census_rows.py 第三実装 C11r）で実施する"
  - type: depends_on
    target: "K1240"
    note: "B子の逐語転写元・K1240 の全称証明（y=17族・K1241 機で observed→proved 昇格済み）。cand17 ブロックは出版 verify_y17_universal.py part2 正本（commit ab23d120・SHA-256 4253cf29…）からブロック内 Y→Y17 改名（3,465 bytes・改名を除きbyte照合・出版 cand17.py〔K1240 fit・commit 6ca80e0e〕とも二重にbyte一致・両ソース byte一致）。y=18 における使用範囲は x>=18 行で K1240 の定義域 x>=17 の内側"
  - type: depends_on
    target: "K0832"
    note: "残余ゲームHの定義と単一トークン閉形式のraw anchor（C1b・merge corollary）"
  - type: extends
    target: "K1241"
    note: "y=17 全称 part1/part2 機械（K1241）と同型の12チェック構成を y=18 定数へ適合（マージ行 x==18・clip 38・census x=18..70=53行・C7 seed 20261182・C8 の x=17 拡張整合行・tail x+z+19）。機械組み立てscriptは出版せず転写marker+check_transcriptions_y18.py の二重正本方式"
artifacts:
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/README.md
  role: document
  note: "実験README（機械構成・転写marker検証〔出版y17機はmarker保持のためEND marker行で打ち切る抽出〕・12チェック結果表・bounded-memoization twin設計〔~1.0GiB cgroup host〕・3回決定性〔2同一cwd+1隔離tree/cwd/HOME+env -i+PYTHONHASHSEED=random〕・fail-closed 9種〔T1/T2 census FAIL-CLOSED・T3-T8改ざん全捕捉・T9深部tail窓のbad 0は K1240 tail内部点の拡張整合性観察で真の境界(17)シフトは40 bad捕捉〕・組み立て機のregion-splice欠陥をC1が出版前に捕捉した誠実記録〔1,229 bad・出版bytesは修正後〕・宣言noteのcensus merge予測スリップ 105,651→実測110,682 の誠実記録・再現コマンド・解釈規約）"
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/verify_y18_universal.py
  role: verifier
  note: "正本検証器（part1・12チェック・38,212 bytes・SHA-256 14373419…・961行・@@TRANSCRIPTION marker 3ブロック・y=13..y=17 と同一手続き）"
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/scripts/check_transcriptions_y18.py
  role: verifier
  note: "転写二重正本検証（engine 1,957 bytes・cand17 3,465 bytes 二ソース一致〔出版y17機ブロックと出版cand17.pyの両方とY→Y17改名差分のみで一致・sources_agree〕・cand18 3,211 bytes〔出版cand18.py driver省き verbatim〕・構造アンカー抽出・repo root は AGENTS.md 探索・SHA-256 80fc9c31…）"
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/output/audit.json
  role: audit-output
  note: "part1フル12チェック監査正本（SHA-256 c090be81…・total_points 6,354,790・total_bad 0・型523,398・3実行byte-identical・corollaries merge 1,121,822 / tail 192,210 全bad 0）"
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/output/published_run.txt
  role: log
  note: "part1正典run transcript（転写検査→census両部→フル12チェック・rc=0・3回決定性・fail-closed 9種・誠実記録）"
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/output/census-ordered.json
  role: audit-output
  note: "census ordered部（SHA-256 af284ab7…・438,840点・bad 0・merge 110,682・tail 4,240）"
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/output/census-canonical.json
  role: audit-output
  note: "census canonical部（SHA-256 9c817177…・438,840点・bad 0）"
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/output/transcriptions-check-y18.json
  role: audit-output
  note: "転写検査結果（engine/cand17二ソース/cand18 全equal・overall PASS・隔離側でも再実行PASS）"
- path: research/log/2026-11-23-y18-universal-verifier-single-owner-note.md
  role: log
  note: "単一オーナー宣言ノート（commit 1d46f883・検証器run前に出版・観測HEAD c15b1c3f・y=19 fitレーンとの非接触合意〔対抗はy=19 fitのみ〕・事前横断予想〔clip 38 tight・census幾何・型総数〕・K1244仮採番・part1持範囲+part2継続保持の宣言）"
- path: research/log/2026-11-23-y18-universal-verifier-part1.md
  role: log
  note: "part1実行記録（選定・経緯・組み立てregion-splice欠陥の捕捉と修正の誠実記録・出版記録・part2への引き継ぎ）"
scope: >-
  κ=1残余ゲームHの2トークン族X=(x,18)、全z>=0・全x>=18・全R>=0 の全称命題
  （K1242）に対する正本検証のpart1として、実行・出版された12機械チェック
  （C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12・総6,354,790照合点・全bad 0・
  3回実行byte-identical・fail-closed 9種）。昇格判定（K1242
  observed→proved）はpart2（C1d出版固定z切片アンカー事前検証・
  census_rows.py第三実装のC11r・フル14チェック監査）で実施するpart1の
  段階（part2は同一単一オーナー宣言 1d46f883 の継続として後続実行）。
  系のマージ命題y=18版（x<=z-19）とtail（R>=x+z+19→(x+18) mod 2）は
  part1のcorollary掃引で1,121,822 / 192,210点 bad 0。標準11×11の空盤・
  二石root・S2 {59,60}・class 1/2/4は範囲外かつUNKNOWNのまま。
  3トークン以上・y>=19族・固定幅・q点版も範囲外。
evidence: >-
  2026-11-23出版・単一オーナー宣言 1d46f883 配下:
  (1) 転写の二重正本検証: engine/cand17/cand18 の3ブロックが出版bytesと
  byte一致（cand17は出版y17機part2ブロックと出版cand17.pyの2ソースで
  一致・sources_agree・隔離側でもPASS）。
  (2) フル12チェック PASS: 総6,354,790点・bad 0（C1 23,940 / C1b 43,296 /
  C2 225,449 / C2b 19,492 / C3 1,305 / C4 585,189 / C4t 585,189〔probe〕 /
  C7 200,000 / C8 1,035,729 / C9 900,534 / C11 877,680 / C12 1,856,987）。
  宣言noteの事前機械算出と全照合点数で完全一致（宣言のpart1総計
  6,354,790どおり）。
  (3) clip窓2y+2=38 は tight: C4tで clip 37 が 1,012違反・最初 (60,100,100)
  で band bottom とともに歩く最初違反の系列が6観測目
  （y=13..17の5観測に (60,100,100) を追加・y=5..18の14族tight連続確定）
  （宣言の事前横断予想どおり違反>0でtight確定）。
  (4) census: z=0..79・x=18..70・R<=x+z+19・両エンジン各438,840点 bad 0
  （bounded-memoization twin・LRU 1.6M・~1.0GiB cgroup host・C11mode で
  FAIL-CLOSED検証の上 merge）。merge帰結は宣言どおり z>=37 で初めて非空。
  誠実記録: 宣言noteのcensus merge per-engine予測 105,651 は宣言側の
  算術スリップで、機の独立再計算値 110,682 が部品・監査の正本値
  （他の全予測値は一致）。
  (5) 決定性: audit/census parts/転写検査出力 3実行byte-identical
  （run1/run2同一cwd・run3は隔離 tree/cwd/HOME+env -i+
  PYTHONHASHSEED=random・転写検査と両census部品は隔離側で再生成し一致）。
  (6) fail-closed 9種: T1 census box改ざん・T2 census部品欠落は
  FAIL-CLOSED。T3 band下端・T4 steady pin・T5 merge境界（z-19→z-18）・
  T6 clip窓・T7 合流多重集合・T8 A子 の各改ざんを全捕捉。
  T9深部tail窓シフト(19,20,21)→(18,...)はbad 0で、これは出版cand17
  （K1240 proved）tail主張の内部点 R=x+z+18 における整合性（検出対象外）
  の観察として誠実記録し、真の境界外シフト(17,...)は C8 bad 40 で捕捉。
  (7) 誠実記録（組み立て段階）: 最初の組み立てbuildはregion-splice
  off-by-one（旧cand17候補regionがcand18ブロック後に残存し Y=17 が
  再代入）で、機のC1が即座に捕捉（1,229/23,940 bad・1族分の特徴ずれ）。
  marker一意性assertで修正し、出版bytesは修正後のみ。
---

## 12チェックの構成と実績値（part1）

y=17 機（K1241）と同一構成の12チェックを y=18 定数へ適合:
A子は x==18 の合流子 {17,18}≡{18,17} で cand17(z,18,R-1)、
B子は出版 cand17（K1240 全称・x>=18 行は定義域内側）、
C子は 1 xor cand18(z-1,x,R-1)、型機械 clip 2y+2=38・番兵 39、
census z=0..79・x=18..70（80*53=4,240行）・R<=x+z+19、
C7 seed 20261182、C8 の x=17 行は拡張整合行としてのみ。

**実績値: overall PASS・総6,354,790照合点・全bad 0・型523,398**
（系列: y=14 281,912 → y=15 335,658 → y=16 394,686 → y=17 457,645 →
y=18 523,398）。

## C4t tight と最初違反の歩み（14族連続）

clip 37（2y+1）で 1,012 型収束違反・最初違反 (60,100,100)。最初違反は
band bottom とともに歩む系列
（(60,90,90)→(60,92,92)→(60,94,94)→(60,96,96)→(60,98,98)→(60,100,100)）
6観測目で、**clip窓 2y+2 tight 判定は14族連続（y=5..18:
12/14/…/34/36/38）**に伸長した（宣言の事前横断予想どおり・違反ゼロなら
再審と宣言していたところ違反>0でtight確定）。

## 誠実記録

- 宣言noteのcensus merge per-engine予測 105,651 は宣言側の算術スリップ。
  機の独立幾何再計算 110,682 が両census部品・監査と一致し正本値。
  他の全照合点数（11チェック点数・総計6,354,790・census 438,840・
  tail行 4,240）は宣言どおり。
- 組み立て段階のregion-splice欠陥（旧cand17候補regionの残存→Y=17汚染）
  を機のC1が出版前に捕捉（1,229 bad・1族ずれ签名）。builderはmarker
  一意性assertで修正。出版bytesは修正後のみ。
- fail-closed T9の深部tail窓シフト(18)はbad 0: 出版cand17（K1240
  proved）tail主張の内部点ゆえ検出対象外。真の境界外シフト(17)は
  40 badで捕捉（y17のT5拡張整合性観察と同型の記録）。

## part2への引き継ぎ

part2（C1d 出版固定z切片アンカーの y=18 行〔preflight fail-closed〕
+ census_rows.py 第三実装 y=18 版（XMIN=18・XMAX=70・RBUF=20・ZHI=80）
の C11r）を同一単一オーナー宣言 1d46f883 配下で実施し、
フル14チェック監査3回byte-identical + fail-closed電池の上で
**K1242 を observed→proved に昇格する**（同一K番号・K1240前例）。
