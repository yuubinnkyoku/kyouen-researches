# 2026-11-14 高速レーン — 7行 q=9/q=10 witness帯のkissat交叉確認・延長・(7,9) witness探索とK0820統合

## 背景

`seven-row-inband-families-20261114`（13:22 push・commit 32fdcac3）は
(7,10) witness m=10..18・fastsat def+lex UNSAT 帯 m=19..40・(7,9) witness m=9..14・
U_{7,q}/U_{8,q} 表を含むが、**K項目化・CSV行・log が一切ない未統合実験**だった。
また UNSAT 帯は単一カスタムCDCL（fastsat）のみの根拠で、repoの水準
（K0816/K0818/K0819 は kissat 主体）より弱い。本実行はこの確認・延長と
(7,9) 前線の推進・統合を1回で完了させた。

## 判断と作業

1. **符号化の健全性確認**: sat2.js の def 単一節（∨¬rowGe[y]）は
   「総石数 < w(q−1) ⟺ ある行 ≤ q−2」（行は長さ m ≥ q の直線で安全から各行 ≤ q−1）
   により行欠損存在の完全符号化。節は H/V/HV 不変なので def+lex=H,V,HV は健全
   （K0815 第4弾の「lex は UNSAT 側に有効・SAT 側に有害」の教訓どおり、
   (7,9) witness 探索は lex なしで実行）。
2. **(7,10) 帯の交叉確認**: m=19..40 の CNF を決定的再生成し fastsat を走らせたところ
   **全22幅で conflicts が元実験 results.jsonl と bit-exact 一致**（同一インスタンス性の較正）。
   kissat 4.0.4 が全幅 UNSAT。制御 2×8/2×9 q=4 も bit-exact（121/535）。
3. **(7,10) 帯の延長**: m=41..51 を fastsat+kissat 両方で UNSAT（ worst m=46: 15,399
   fastsat conflicts・m=36: 41,278）。→ witness-free 帯 {19..51}・M_{7,10} = 19 or ≥52。
4. **(7,9) witness 探索**: m=15..23 がすべて SAT（55石・m=15のみ54石）。
   全witnessを census 不使用 JS verifyConfig + Python Fraction の2系統で検証 PASS。
   → witness 幅 {9..23}（m=9..14 は元実験）・下界 M_{7,9} ≥ 24。
5. **(7,9) 不在帯**: m=24..33 が kissat def-nolex で全幅 UNSAT（43,743〜94,368 conflicts）。
   m=24/33 は def+lex 別符号化でも UNSAT。
   **負記録**: fastsat は m=24 を 60秒 cap で解けず（210k conflicts TIMEOUT）—
   (7,9) 帯は kissat 単独であり (7,10) 帯（2ソルバ一致）より根拠水準が一段低い。
   K0820 に明記。
6. **統合**: K0820 新設（kind: proposition, status: computed）・mwq CSV に
   (7,9) "{24},34..613"・(7,10) "{19},52..587" の2行追加・
   実験 `seven-row-q9-q10-bands-20261114`（scripts 3 + README + report + output
   records/summary/witness/kissat 生ログ）。

## 運用メモ

- 本セッションで実行環境リセット2回（290秒タイムアウトでワークスペース消滅）。
  両方とも決定的再実行で**全記録数値が bit-exact 再現**（fastsat 較正値・kissat
  conflicts とも）。この再現性の記録自体が K0820 の evidence に含まれる。
- リセットの原因は (7,9) UNSAT 帯への fastsat 275秒 cap 交差確認（1インスタンスが
  cap まで燃焼）。以後の教訓: **交差確認ソルバには短い cap（60秒）を設定し、
  TIMEOUT は正記録として残す**。
- (7,9)/(7,10) は w=7 の帳尻2ファミリー（q≥11 は分離帯で M=q−1 既証明）。
  残る w=7 の open は (7,4..8)。（8,q) は q=4..12 が open・U 表は既存。
- views再生成（generated/・root README）は統合レーンに委ねる（K0820 は
  generated 未反映・CSV/README は本コミットで更新）。

## 次の一手（レジューム）

1. **(7,9) 7×34 以降の不在帯延長**（kissat 単独・1幅あたり~40秒）。
   どこまで伸びるか。並びに (7,10) 7×52 以降（符号化時間が O(m^3) で増加）。
2. **(7,8)・(7,7) の同型調査**（witness 帯の端・不在帯の開始点。q=8 は
   U=651・(6,8) との比較が面白い）。
3. **(8,9)/(8,10) への拡張**（U=984/940。8行盤の census は w=7 と同程度に軽い）。
4. K0342 型 tail 評価（U=613/587 を大きく下げられれば M 確定に直結）。

**11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN**
（本成果は固定幅Mの話で無盤面勝敗に無関係）。

## 第2ラウンド（同日 15:00 頃）: 帯延長 24..60 / 19..60 と genfast.js（censusメモリ壁の解消）

1. **census メモリ壁の発見**: sat2.js の `S.buildCensus` は全点三つ組で円を列挙
   （circMap が C(n,3) エントリ）。7×51 (n=357・C=755万) は通るが **7×52
   (n=364・C=798万) で OOM (rc 137)** — q=9/q=10 とも m=52 で丁度壁に当たる
   （CNF自体は8k vars/29k節と微小・生成16秒→OOM は不連続に見えるが
   C(n,3) の平滑な3次増加がコンテナ上限 (~2.9GB) を 51/52 の間で跨ぐだけ）。
2. **genfast.js 開発**（scripts/genfast.js）: q ≥ w+1 のもとで「全 q点円の中心
   x座標は半整数」ことを利用（円と行の交点 ≤2 → q≥w+1 点の円は同一行ペアを
   持つ → その垂直二等分線が中心を通る）。各 u=U/2 (2m−1 個) について異行ペア
   (p,q) が中心yを厳密有理数で解き、pair-witness ≥12 の候補を整数精密スキャン。
   線は元のペア列挙をそのまま使用。**S.buildCensus を monkey-patch して sat2.js
   の符号化・dump を verbatim 再利用（drift ゼロ）**。曲線順序を厳密再現
   （線:最小2点順・円:最小3点順・線が円の先）。
   **検証: 12サンプルで sat2.js と CNF バイト一致**（(7,34,9)・(7,45,9)・(7,51,9)・
   (7,51,10)・(7,19,10)・(7,40,10)+lex・(6,21,7)・(6,22,8)・(5,21,6)・(5,22,7)・
   (7,30,9) cap+tot・(7,30,9) rowY）。7×52 生成 2.7 秒。q < w+1 は assert で拒否。
3. **(7,9) 帯延長**: m=34..45（lean1.sh/sat2.js）+ m=46..60（lean2.sh/genfast.js）
   全幅 kissat UNSAT（22,641〜46,865 conflicts）→ witness-free 帯 **{24..60}**。
   m=52/60 は def+lex=H,V,HV 別符号化でも UNSAT（25,855 / 19,373）。
   **M_{7,9} ∈ {24} ∪ [61,613]**。
4. **(7,10) 帯延長**: m=52..60 全幅 kissat UNSAT（888〜1,634 conflicts・極めて軽い）。
   m=52/60 は lex 別符号化でも UNSAT（1,033 / 1,020）。
   **M_{7,10} ∈ {19} ∪ [61,587]**。
5. 両 band とも「exact M 仮説（24/19）」はさらに強化。UNSAT conflicts は m に
   対し単調ではなく 22k〜94k の範囲で振動・難化傾向なし（q=10 に至っては
   ~1k で軽い）→ 帯延長は m=61..100+ も容易に続行可能（1幅~40秒）。
6. **統合（第2ラウンド分）**: report.md に帯延長 + genfast セクション追記・
   scripts README に lean2.sh/genfast.js 追記・summary.json 再生成
   （q9 50 records / q10 44 records）・K0820 の主張・artifacts・追記セクション
   更新・mwq CSV 両行 "{24},61..613" / "{19},61..587" に更新・fixed-width README
   の K0820 段落更新・log（本節）。

## 第2ラウンドのレジューム

1. m=61..100+ の帯延長（kissat 単独・lean2.sh・1幅~40秒・軽い）。
   100 まで行けば M 仮説の経験的裏付けは相当に強くなる。
2. (7,8)・(7,7) の同型調査（q=8 は U=651・(7,8) は q≥w+1 を満たし genfast が
   そのまま使える）。
3. K0342 型 tail 評価（U=613/587/651 を下げられれば M 確定に直結）。
4. (8,9)/(8,10) 拡張（genfast は w=8 にもそのまま適用可能・q≥9 assert 通る）。

**11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN**
（本成果は固定幅Mの話で無盤面勝敗に無関係）。
