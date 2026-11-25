# 2026-11-21 three-row q=4 frontier (M_{3,4} レーン) セッション log

単一オーナー宣言: commit `72fdd106793151a72dcea5bcc9298577879188de`
（`2026-11-21-three-row-q4-stabilization-single-owner-note.md`・02:09Z push・宣言本文 02:14Z）。

## 経緯

- 並走状況の確認: 四行 q7 closure レーンが宣言ノート `db6660813b`（02:06Z）で
  M_{4,7} closure + genfast3 w=4 port + m=86..88 延長を先行クレームしていたため、
  当セッションの持っていた同一内容の staging は出版を譲渡した（重複回避・受入条件6項目
  具備を確認）。並走は 02:15-02:19 に K1182（M_{4,7}=13 閉包）として着地し、
  02:29 にはq6 m=30,31 の def-mode UNSAT 延長（records 112→114）も出版済み。
  これらは本レーンとは非接触。
- 本レーンは 3×m・q=4（repo に項目なし・K0070/K0071 の q=4 妹分）を取得。
  U 値を K0318 正本スクリプトで再計算し U_{3,4} = 69 = min(A,B) を確認
  （q=4 では d1 = C(2,3) = 0・cross_cost = C(2,2) − 1 = 0 で packing 改善なし。

## 実施内容

1. **census 交差検証**: sat.js buildCensus（JS）と K0318 curve_key リフト幾何による
   独立 Python census（pycensus.py）を m ∈ {4,5,6,7,8,10,13,16,20} の9幅で比較。
   **全幅 byte-identical**（禁止曲線数 29/50/86/141/221/434/982/1865/3693）。
   line は JS が (B,C,D) 3項・Python が (A=0 を含めた4項) を出力するため、
   正準化（先頭 0 の除去）の後に比較。
2. **witness band 掃引**: sat2.js（w=3 代入・改変なし）def-mode CNF を
   kissat 4.0.4（md5 `3a5eba83…`・公式 rel-4.0.4 linux-amd64 zip から再取得・
   pin 一致）で判定。m=4..11 は conflicts≈0 の即 SAT、m=12 (308)・13 (163)・
   14 (218)・15 (174)・16 (1,782)・17 (1,093)・18 (3,513)・19 (3,111)・
   20 (72,789・14s)・21 (2,322)・22 (28,675・10s) とすべて SAT。
   **witness band {4..22}・INDET 0。**
3. **境界の INDET**: m=23 plain は 250s cap で 1,348,967 conflicts、--lex=H は
   250s cap 1,482,744 conflicts、m=24 plain は 100s cap 481,364 conflicts、
   いずれも判定なし（アーキテクチャ的に kissat resume 不可・cap 下 conflicts は
   環境依存参考値）。初回は13幅一括バッチで 290s 外装 cap を超えて環境リセットを
   喰い、以降1幅/呼び出しに分割した（教訓として K1174/K1167 の運用知見と同じ:
   外装余裕と idempotent 増分が必須）。
4. **小盤全数分類**: brute34.py（安全集合を枝刈り DFS 全列挙・第三独立系）で
   m=4..8 の全極大安全配置を分類。m=4,5,6 では満容量極大が存在しないことに注意
   （全極大が欠損）。満容量 (3,3,3) 極大は m=7 で初出 64 個、m=8 で 976 個。
   最小 witness は全幅 5 石。
5. **検証**: 19 witness すべて sat.js verifyConfig (ok) + verify34.py (pass)。
   交差符号化 --lex=H で (3,12,4) 76 conflicts・(3,22,4) 178,116 conflicts の SAT を再現。

## verify34.py 初版バグと教訓

初版 verify34.py は極大性を「空点を含む禁止曲線の**全ての**点が石」と実装し、
安全性も「曲線の全点が石」方式で検査していた。kissat+verifyConfig の判定と
食い違ったことで発覚。正しい意味論は「曲線上の石数 ≥ q−1（極大性）・
≤ q−1（安全性）」。修正後 19/19 一致。すなわち:
- census 一致だけでは意味論（計数条件）の検証にならない。検証同士の食い違いは
  どちらかが壊れているという控制在用命令であり、単独実装の PASS より価値がある。
- 誤実装は witness を棄却する向きにのみ作用したため、採用した主張に遡及影響なし。

## 環境リセット被害と復旧

02:13 頃（m=13..25 一括掃引の cap 超過）で実行環境がリセットされ /home/user/work
配下の器材を喪失（この時点で sat.js/sat2.js/kissat/curve_packing・初期掃引成果）。
全器材を pin から復元: sat.js/sat2.js は repo raw から（md5 0cc6021a/282ae832 一致）、
kissat は公式 zip から（3a5eba83 一致）、curve_packing_fixed_width.py は repo から
（a9575c0a 一致・K0318 commit 49891aaf 正本）。m=4..12 の掃引をやり直し、
conflicts が bit-exact に再現（0×8・308@12）することで pin 復元自体の較正とした。
器材・成果の現物は knowledge/kyouen-research/q34-lane-kit/ に退避済み。

## 成果の位置づけ

- **M_{3,4} ≥ 23**（witness band {4..22}・有限機械証明）。
- **M_{3,4} ∈ [23, 69]**（Γ 内 open・69 は K0024 引用値で q=4 では K0318 改善なし）。
- 小盤 m ≤ 8 の完全分類は本レーンが初出（満容量極大の初出が m=7 であることも新事実）。
- 標準 11×11 には無関係。node 数・solved 数を勝敗として読まない。

## 続報（第2パート・02:35-02:48Z）: m=23 判定 — witness band 4..23 に拡大

part3（knowledge README bullet）は 02:34 commit `5938f1b` で完了（fetch-back
byte-identical・658,163→659,492→661,848 bytes・既存 bullet 全保存）。
以降の追跡:

1. **m=25,26 の CNF 生成**: sat2.js（md5 282ae832・pin 器材）で plain def CNF を
   生成。m=25: 禁止曲線 7,258・vars 74,163・clauses 245,245。m=26: 曲線 8,182・
   vars 83,522・clauses 276,175（未実行）。
2. **m=25 plain は 115s cap で INDET**（507,461 conflicts・判定なし）。
   幅とともに難度が上がることを確認。
3. **row-split 部分問題の設計**: def-mode（不足行の存在）は「不足行 = 行0/行1/行2」
   の 高さ 3 の OR なので、--rowY=Y（行 Y 欠損を固定）で完全な case-split になる。
   行0 と行2 のインスタンスは V 鏡映（y→2−y）で同型なので行0 側のみで代表できる。
   --lex=H（列鏡映 lex-leader）は行配置を保存するため行固定との併用が健全
   （H は行ごとの石数を変えない）。plain 250s cap 1.35M conflicts 未決だった
   (3,23,4) をこの2分割に賭けた。
   生成: (3,23,4) row0+lexH（vars 57,742・clauses 191,141・曲線 5,633）・
   (3,23,4) row1+lexH（同サイズ）・(3,24,4) row0/row1+lexH（vars 65,667・
   clauses 217,355・曲線 6,413）。
4. **(3,23,4) row0+lexH は 140s cap で INDET**（1,001,203 conflicts・判定なし）。
5. **(3,23,4) row1+lexH が SAT**（**471,357 conflicts・106.83s**・rc=10・cap 285s
   に到達前に決着）。witness 抽出: 8石・rows [3,2,3]（中央行欠損; row1={18,19}）・
   coord `9:0,12:0,18:0,18:1,19:1,4:2,15:2,18:2`。
   - sat.js verifyConfig: ok（size 8）
   - verify34.py: safe=1・maximal=1・deficient=1 → **2系統検証 PASS**
   witness は plain board 上で直接検証されるため、**M_{3,4} ≥ 24 は witness 自身が
   証明**（部分問題の意味論への依存なし）。
6. **(3,24,4) row1+lexH は 285s cap で INDET**（1,159,627 conflicts・判定なし）。
   m=24 はなお未決。外側行欠損（row0）側の m=23 も未決で、m≥23 の外側行欠損
   witness の存在は open。
7. **予想の反証を記録**: 初版 item は「m=23 は不足行 21 空点の被覆破綻の候補幅」
   と予想として書いていたが、m=23 witness により反証。8石 (3,3,2) 被覆パターンは
   幅 23 でも成立する。band 終端は [24,69] 内・外側/中央行系で非対称の可能性。

### 更新後の standing claims

- **witness band m=4..23**（20幅全 SAT・INDET 0・全 witness 2系統検証 PASS）。
- **M_{3,4} ∈ [24, 69]**（上界は K0024 引用値・K0318 は q=4 で改善なし）。
- m=24, 25 は INDET（m24: plain 100s/481k・row1+lexH 285s/1.16M・m25: plain
  115s/507k・m23 row0+lexH 140s/1.00M・いずれも cap 下参考値）。witness-free 幅は
  0 幅のまま。
- 標準 11×11 は無関係・UNKNOWN のまま。REFUTED-D10 は LOSS 証明ではない。

### 増分出版（本 commit）

records.jsonl 26レコード化（+4: m23 row0 INDET・m23 row1 SAT・m24 row1 INDET・
m25 INDET）・wit_3x23_4.witness.json 追加・実験 README と K1183 item の
claims 更新（band 4..23・M ∈ [24,69]）・knowledge README の K1183 bullet 更新
（本ログも同 commit）。

## 続報2（HV 符号化較正と m=24 全分割掃引・02:50-03:05Z）

1. **HV 符号化の陽性対照**: V 鏡映（y→2−y）は中央行 y=1 を固定するため
   --rowY=1 との併用が健全。(3,23,4) --rowY=1 --lex=H,V が **SAT 173,883
   conflicts@40.21s**（lexH 単独 471,357@106.83s の 2.7 倍速）で
   **lexH 単独と同一 witness**（`9:0,12:0,18:0,18:1,19:1,4:2,15:2,18:2`）を再生
   → HV 符号化の健全性・有効性を較正。
2. **(3,24,4) --rowY=1 --lex=H,V は 285s cap で INDET**（1,230,473 conflicts・
   判定なし・V 対称でも決着せず）。
3. **(3,24,4) --rowY=0 --lex=H は 285s cap で INDET**（1,602,798 conflicts・判定なし）。
   **m=24 は plain + 全 row-split 分割（3種）が 285s cap で未決**。m=24 の決着には
   285s 超の cap、--cap=K（石数上限）併用、不足行石数 0/1/2 の2段階分割、
   あるいは並列分散が必要。M_{3,4} ∈ [24,69] は不変・m=25 も plain 115s cap 未決。
4. records.jsonl 29レコード化（+3: m23 row1-lexHV SAT 対照・m24 row1-lexHV INDET・
   m24 row0-lexH INDET）。claims は不変（[24,69]）。実験 README/K1183 item の
   m=24 探索記録と records 計数のみ更新（本コミット）。

## 続報3（行和63分割: m=23 外側行 witness と m=24 P(24)・05:20-06:55Z）: witness band 4..23 の終端確定

1. **行和分割の設計（session2 part1-4 出版済み・ここまでの経緯をまとめる）**:
   安全配置では水平線が禁止曲線（q=4 では同行4点で成立）のため各前行の石数は
   q−1 = 3 以下。よって行欠損極大 witness の行和3つ組 (r0,r1,r2) は
   {0..3}^3 ∖ {(3,3,3)} の63通り。**row-k piece**（sat3.js rowfixed-kex:
   --rowY=Y --kex=K で行 Y の石数を厳密に固定。行0・行1 × K∈{0,1} の4件で
   石数 {0,1} を含む48通りを殺す）と **row-sum piece**（sat4.js rspec:
   3行の石数を完全指定。残り15通りを12件で殺す〔lexH piece は V 鏡像 triple を
   同時に反証・V 不変性の機械検査つき〕）で63通りを exactly-once 被覆
   （partition_closure.py の機械検査・台帳 partition_closure.json・pending 0・
   uncovered 0）。sat3/sat4 は four-row lane 正本 sat2.js（md5 282ae832）の
   w=3 代入に piece 条件を加えた派生で、CNF 生成は決定論的。
2. **m=23 外側行欠損 witness（part1 で出版）**: 同型の48分割（row-k 2件 +
   row-sum 16件）で (2,3,3) piece が SAT。8石 witness・rows [2,3,3]・
   coord `5:0,21:0,9:1,12:1,15:1,10:2,12:2,13:2`（wit_3x23_outer_4.witness.json・
   sat.js verifyConfig + verify34.py 2系統検証 PASS）。**m=23 では中央行系・
   外側行系の両方で witness が存在する。**
3. **m=24 は witness-free（P(24)）**: 63分割16 piece が全 UNSAT
   〔決定打 (2,3,3) 2,671,271 conflicts@476.10s〕→ **witness band は 23 で
   終端・witness-free 幅は {24}**。P の単調性はないため m≥25 での witness 復活は
   否定されず、M_{3,4} ∈ [24,69] 不変（残る不確定幅は 25..68の44幅）。
4. **witness-free 判定の解釈規約**: m=24 は witness 検証方式ではなく
   台帳検査方式（63 triple の piece 被覆・verdict 機械検査）。SAT 側と違い
   witness を検証器に通す経路がないため、被覆の完全性（exactly-once・pending 0）
   が正しさの条件。
5. **cover 構造分析（part2-4で出版済み）**: witness の被覆円の家族分類
   （families.json・A/B/C/D identity checks・analyze_cover.py/verify_families.py）・
   master 判別式の exact-rational 恒等検証（master_cover_identity.py・2,124 checks
   0 mismatch）・S/X/Y 剰余パリティ補題の機械完証明（parity_lemmas.py・
   witness 794円スキャン 0違反）。m=24 で被覆破綻が確定した今、これらを一般計数に
   繋ぐのが最有望の解析方向。
6. **第二環境での独立 bit-exact 再検証（part5/5 引継ぎ・本セッション）**:
   session2 が part4/5 (f)（06:03-06:04）で沈黙したため part5/5 を引継ぎ、
   m24 16 piece + m23 外側 18 piece + 較正 sat3 cal23 rowY=1 kex=2 piece
   （SAT 319,199 conflicts で wit_3x23 型 witness 再生・verify34 PASS）の計35 run を
   第二環境で同一 pin 器材から CNF 再生成（md5 台帳は records.jsonl 参照）・
   pinned kissat 4.0.4 で再実行した。**全ピースの verdict と conflicts が出版台帳
   （partition_closure.json・README/K1183 記載値）と bit-exact 一致**
   〔決定打 (2,3,3) m24 = 2,671,271@445.76s〔第一環境 476.10s〕・
   (3,2,3) = 1,117,137・(3,2,2) = 153,096・(2,3,2) = 121,085・
   m23 (2,3,2) = 94,415・m23 (2,2,3) = 133,939・
   m23 (2,3,3) SAT = 1,004,683@138.34s 等・35件全て〕。SAT piece は witness が同一再生
   （m23 (2,3,3) の再 run は published wit_3x23_outer_4 と同一 witness を
   bit-exact conflicts で再生）。決定論的 solver の全ピース conflicts の完全再現は
   CNF 再生成の byte 同一性の強い経験的証拠（数学的証明ではなく報告レベル）。
7. **交差符号化対照3件**: (2,2,2)（16,004 conflicts@9.41s）と (3,2,3)
   （1,724,972 conflicts@420.33s）を --lex=H 単独の別 CNF で再判定して同一 UNSAT
   〔primary は lexHV〕、m23 (2,3,3) の V鏡像 rspec (3,3,2) を別 CNF で再判定して
   SAT（487,095 conflicts@88.95s・witness `10:0,12:0,13:0,9:1,12:1,15:1,5:2,21:2`
   = published witness の V鏡像・rows [3,3,2]・sat.js verifyConfig + verify34.py 2系統 PASS）。**UNSAT 分割の符号化独立性の初の実証**（HV→H の対照）と
   **SAT piece の V鏡像転送の健全性の陽性対照**（台帳の V鏡像転送被覆の意味論が
   正しく SAT↔SAT で対応することの確認。UNSAT 側の V転送〔m24 (3,3,2) を
   (2,3,3) piece から殺す部分〕は直接の対照実験を欠くまま台帳の意味論に依存する）
   を成立させた。
8. **make_records.py の erratum・拡張**: part4/5 (f) で出版した旧版は
   V鏡像注記のフォーマットバグ（'(%d,2,%d)' に引数2つ→TypeError）で lexH piece
   を含む実行が落ちる状態だった。修正して ((%d,%d,%d), (c,b,a)) に直し、決定打
   (2,3,3) entry と交差対照3件を追加、さらに SAT verdict piece に witness 抽出
   （extract_witness.js）と2系統検証（verify34.py）を自動実行してレコードに
   witness_stones/witness_coord/verify_js/verify_py を含めるように拡張
   （SAT レコードが自己完結する。全 piece 2系統検証 PASS を確認してから
   records.jsonl を組立）。
9. **records 増分**: records.jsonl 29→67〔24 SAT + 35 UNSAT + 8 INDET〕。
   README.md・K1183 item・knowledge README の K1183 bullet（K1177 precedent の
   更新注記形式に準拠）を witness-free 幅 {24}・P(24) に更新（本コミット）。
10. **次課題**: (a) m=25 の同一16-piece 分割掃引〔決定打型 (2,3,3) piece は
    m=24 で 476s・m=25 では数倍が見込まれるため単独バックグラウンドで増分出版〕、
    (b) S/X/Y パリティ補題と家族分類の一般計数への昇格（m=24 破綻の証明的理解）、
    (c) 行→幅単調性（m=24 の反証が m≥25 に継承される条件・e.g. 列surgery）。
