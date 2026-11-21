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
