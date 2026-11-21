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
