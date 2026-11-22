# s_12/s_13 SAT 両側判定レーン（2026-11-22）: SAT機材、lex-leader瑕疵の発見と修正、較正ラダー、10×10十石witnessの格子同型類（2類→5類）

単一オーナー宣言: [2026-11-22-s12-s13-sat-stabilization-single-owner-note](../../log/2026-11-22-s12-s13-sat-stabilization-single-owner-note.md)（commit `71408dda54`）。
目標は標準 q=4 共円（正方形 n×n 盤・禁止四点組=共線または共円）の最小極大安全サイズ s_n について、

- n=12 at-most-10: SAT なら s_12≤10 witness（K1206 の「s_12≤10 witness 未発見」を更新）、UNSAT 完了なら s_12=11（K0320/K1206 と合わせ精確値）
- n=13 at-most-11: SAT なら s_13≤11 witness、UNSAT 完了なら s_13=12

のいずれかを決めることであった。**結果: いずれの側も単発 ~270-280s 予算内では決着せず（INDET、不在不主張）。**
その過程で、(a) SAT 符号化 v2 の D4 lex-leader 鎖に重大な瑕疵（軌道完全遮断）を発見し、機械検査済みの修正版 v2.1 を作成、
(b) 修正版により s_7=7 を両側から再導出（較正）、(c) 10×10 の十石極大安全配置について**既刊2類と非合同の新規3類**を発見・3系統検証した。

## 0. 成果と非主張の要約

主張（computable・機械検証済み）:

1. **10×10 十石極大安全配置の格子同型類が既知で2類→5類へ**。SAT model から得た3配置
   （v2-draft primary および v2-draft --shuffle=7、v2.1 primary）は、安全性・極大性が
   Python 整数・Node BigInt・census 直結の3系統で独立検証済み
   （tamper=1石除去は両幾何検証器が rc=1 で拒否）。格子同型（D4×整数平行移動）で K0038 の十石 witness・
   K0034 の別十石 witness のいずれとも非合同、相互にも非合同。
   十石 witness 全体の分類ではない。s_10=10（K0034）の値は不変。
2. **lex-leader 鎖の瑕疵と修正（方法論）**。v2-draft の鎖は標準 lex-leader を実装しておらず、
   A ≤lex g(A) を満たすベクトル（n=4 全列挙で 36,808 個/8,548軌道中）を棄却し、
   **一部の D4 軌道を完全遮断する**（n=3: 30/102 軌道、n=4: 3,195/8,548 軌道に受理代表元なし）。
   したがって v2-draft の UNSAT 結果（n7k6 2ショット等）は **s_7≥7 の根拠として使用できない**。
   修正版 v2.1 は受理言語が厳密に A ≤lex g(A) と一致し（n=3,4 全列挙、n=5..13 サンプリング、
   d-鎖全列挙照合 6,300 対 0 不一致）、全軌道に受理代表元が残る。
3. **s_7 = 7 の SAT 両側再導出（v2.1、較正）**。n=7 at-most-6 が UNSAT（default と --shuffle=42 の独立2符号化で一致）
   かつ n=7 at-most-7 が SAT。証明書なしのソルバ信頼境界（kissat 4.0.4・DRAT ログなし）かつ有限対象であり、
   K0031（s_7=7）の独立機材による再現として位置づける（値の更新ではない）。

非主張（INDET・不在否定なし）:

- s_12≤10 witness は未発見。s_12≥11 は未証明。s_13 同様。n12k10（v2.1 270s）・n13k11（v2-draft 280s）とも INDET。
- 既知の s_12≤11 witness（K0320）の SAT 再探索は 3ショット（default/--unsat/--shuffle=13）いずれも cap 内未達。
  n=13 の 12石 witness（K0320）も 1ショット未達。難度曲線として記録するのみ。
- gap-1 UNSAT（n8k7・n9k8・n10k9）も同予算では全て INDET（下記ラン表）。
- 11×11 空盤・二石 root・S2・class 1/2/4 は非接触（UNKNOWN のまま）。mwq CSV・T 値は不変。

## 1. 宣言の受け入れ条件の達成状況

| 条件 | 状況 |
|---|---|
| 1. 較正ラダー s_7..s_10 の k=s_n−1 UNSAT / k=s_n SAT 再現 | s_7 は両側達成（v2.1）。s_8/s_9/s_10 は SAT 側のみ再現（witness+検証）。UNSAT 側（n8k7/n9k8/n10k9）は cap 内 INDET。**完了したのは s_7 のみで、精確値への寄与は s_7 再導出に限る** |
| 2. 決定性: CNF byte 再現（sha256 記録）・UNSAT は shuffle 2ショット一致 | 達成（n7k6 v2.1: default+sh42 とも UNSAT。CNF本体は非刊行だが scripts/cnf-sha256.txt に全件記録し (n,k,seed) から byte 再現可能） |
| 3. SAT witness の3系統検証+tamper | 達成（draft 5件+v2.1 4件の全9 witness、tamper 陰性対照は全件 rc=1 NOT-MAXIMAL-SAFE） |
| 4. 値更新は片側のみ | s_n の値更新なし（新 witness は分類成果であり s_10=10 は既刊のまま） |
| 5. 誤り検出時の訂正 | 2件。erratum-1: 初回 n9k8/n10k9 を --time なし（SIGTERM で切れる）で実行した運用ミス → n9k8 は cap 付きで再実行・n10k9 は破損として無効行とした（ログ参照）。erratum-2: **v2-draft lex-leader 瑕疵**（本README §3）。draft の UNSAT は取り下げ、v2.1 で再導出した |

## 2. 決定述語と符号化

決定述語（v1/v2/v2.1 共通）: 「|S| ≤ k かつ safe（禁止四点組の4点すべてが S に入らない）かつ
maximal（S 外の各点 e は、e を含む禁止四点組 q で他の3点がすべて S に入るもので攻撃される）」を充足する配置の存在。
SAT model は witness（s_n ≤ k）を符号化し、この符号化での UNSAT は「≤k 石の極大安全配置は存在しない」（s_n ≥ k+1）を意味する。

- 変数: 石指示子 x_c（N=n²個）、被覆補助、対称性破り鎖、Sinz カウンタ。K0057 アンカーで検証済みの
  census.mjs が起動毎に禁止四点組カタログ F（共線 D + 非共線共円 C）を再構築し fail-closed で照合する。
- v1（enc_sat.mjs）: safety 4リテラル（S1）+ t_q 一方向被覆（S2: t_q→「q 内の非石は高々1」、S3: x_e ∨ 各 t_q）+ Sinz（S4）。
- v2/v2.1（enc_sat2.mjs）: t_q を (q,e) 対ごとの z_{q,e} ≡「q の e 以外の3点が石」完全 Tseitin に置換（伝播強化）し、
  D4 の7非自明変換 g に対する lex-leader（LX）を追加。
  --shuffle=<seed> はリテラル番号の決定的置換（充足可能性不変の第2符号化）。
- **v2-draft と v2.1 の差は LX 鎖のみ**（§3）。CNF ハッシュ表（cnf2=draft、cnf3=v2.1）で区別する。
- Sinz カウンタは one-way だが exact-count 意味論で健全（|S|>k を根絶）。安全・被覆は列挙ベタ打ちで
  モデル到達時の意味は z 定義通り。充足方向の健全性は model から取出した配置の独立検証で直接確認する
  （verify_witness.py / verify_witness.mjs / check_model2.mjs）。

## 3. lex-leader 鎖の瑕疵（フォレンジクス）と修正版の機械検証

v2-draft の LX 鎖は、各位置で d_c を「strict 減少（A_c=0,B_c=1）のときのみ」強制する誤った向きの
forward 句（-d_{c-1} -A_c B_c d_c 等3句）を用いていた。この鎖の受理言語は:

- d_{c-1}=1（鎖 open）の間は A_c=1,B_c=0 を禁止するが、**等ビットでは鎖が閉じ、以降の位置の制約が消える**。
- その結果 A ≤lex g(A) を満たす配置の多く（n=3 全列挙 274 個、n=4 で 36,808 個の member/gate 対）を棄却し、
- 決定的に、**D4 軌道によってはどの代表元も7つの全 gate を通れなくなる**:
  n=3 で 102 軌道中 30、n=4 で 8,548 軌道中 3,195 が完全遮断。lex-min 代表元が遮断される軌道も 3,783。

完全遮断軌道が存在する以上、述語を満たす軌道がすべて遮断された場合に UNSAT が述語のせいではなく
対称性破りのせいで出る。よって v2-draft の UNSAT（n7k6 default・sh42、v2n8k6/8k7 等の試行も含む）は
**すべて証明として無効**。なお SAT 方向は「amide 節を満たす配置 ≡ 述語を満たす配置」なので
model から取出した witness は修瑕の影響を受けない（独立検証で裏付け済み）。

修正版 v2.1 は標準 Crawford 型の完全二方向 Tseitin 鎖 d_c ⟺ d_{c-1} ∧ (A_c = B_c)（d_{-1}=⊤）で、
ブロッキング句 -d_{c-1} -A_c B_c（c=0 は -A_0 B_0 無条件）と合わせて受理言語が厳密に A ≤lex g(A) になる。
機械検証 lexchain_orbit_check.mjs（output/output/lexchain_orbit_check.json）:

| 検査 | 結果 |
|---|---|
| P1 デサイダ vs d-鎖全列挙（n=2,3,4・各300ベクトル×7 gate・両方式） | 6,300 対、draft 0 不一致 / v2.1 0 不一致 |
| P2 draft が A≤lex g(A) を棄却 | n=3: 274、n=4: 36,808 member/gate 対 |
| P3 draft の完全遮断軌道 | n=3: 30/102、n=4: 3,195/8,548（lex-min 遮断 3,783 軌道） |
| P4 v2.1 受理言語 == A≤lex g(A) | n=3,4 全列挙両方向 0 不一致。n=5..13 各150サンプル 0 不一致 |
| P5 v2.1 軌道被覆 | n=3,4 全列挙で完全遮断 0 軌道。n=5..13 サンプルで lex-min が全 gate 受理 |

（P4/P5 は lex-leader 定理の実装確認である。draft 版の検査も同スクリプトに含まれる。）

## 4. ラン一覧（kissat 4.0.4、単発 --time=270s 前後、CNF sha256 は下位表）

| インスタンス (n,k) | 符号化 | kissat preset / seed | 判定 | conflicts | proc秒 | ログ |
|---|---|---|---|---|---|---|
| (7,6) | v1 | default | UNKNOWN | 981,669 | 199.49 | n7k6.log |
| (7,6) | v1 | default | UNKNOWN | 1,251,398 | 239.20 | v1n7k6.log |
| (12,11) | v1 | default | UNKNOWN | 115,584 | 248.66 | v1n12k11.log |
| (7,6) | v2-draft | default | **UNSAT（無効・§3により取り下げ）** | 832,104 | 70.23 | v2n7k6.log |
| (7,6) | v2-draft | shuffle=42 | **UNSAT（無効・§3により取り下げ）** | 995,485 | 90.59 | v2n7k6sh42_unsat.log |
| (7,7) | v2-draft | default | SAT | 129,460 | 10.61 | v2n7k7.log |
| (8,6) | v2-draft | unsat | UNKNOWN | 1,049,526 | 199.01 | v2n8k6_unsat.log |
| (8,7) | v2-draft | default | UNKNOWN | 1,761,112 | 249.23 | v2n8k7.log |
| (8,7) | v2-draft | unsat | UNKNOWN | 860,533 | 149.37 | v2n8k7_unsat.log |
| (8,8) | v2-draft | unsat | SAT | 223,856 | 39.92 | v2n8k8_unsat.log |
| (9,8) | v2-draft | default | UNKNOWN | 639,594 | 134.77 | v2n9k8.log |
| (9,9) | v2-draft | unsat | SAT | 163,958 | 48.60 | v2n9k9_unsat.log |
| (10,9) | v2-draft | — | **無効: SIGTERM による破損セッション（統計として不使用）** | — | — | v2n10k9.log |
| (10,10) | v2-draft | unsat | SAT | 152,960 | 81.11 | v2n10k10_unsat.log.gz.b64 |
| (10,10) | v2-draft | shuffle=7, unsat | SAT | 179,356 | 90.87 | v2n10k10sh7_unsat.log.gz.b64 |
| (12,10) | v2-draft | default | UNKNOWN | 336,195 | 269.65 | v2n12k10.log |
| (12,10) | v2-draft | sat | UNKNOWN | 308,470 | 279.60 | v2n12k10_sat.log |
| (12,11) | v2-draft | default | UNKNOWN | 356,116 | 269.61 | v2n12k11.log |
| (12,11) | v2-draft | unsat | UNKNOWN | 299,988 | 279.60 | v2n12k11_unsat.log |
| (12,11) | v2-draft | shuffle=13, unsat | UNKNOWN | 264,228 | 268.29 | v2n12k11sh13_unsat.log |
| (13,11) | v2-draft | unsat | UNKNOWN | 165,578 | 279.51 | v2n13k11_unsat.log |
| (13,12) | v2-draft | unsat | UNKNOWN | 208,509 | 267.20 | v2n13k12_unsat.log |
| (7,6) | **v2.1** | default | **UNSAT** | 174,155 | 13.56 | v3n7k6.log |
| (7,6) | **v2.1** | shuffle=42 | **UNSAT** | 176,473 | 15.35 | v3n7k6sh42.log |
| (7,7) | **v2.1** | default | SAT | 284,653 | 24.09 | v3n7k7.log |
| (8,8) | **v2.1** | default | SAT | 192,114 | 27.27 | v3n8k8.log |
| (9,9) | **v2.1** | default | SAT | 151,738 | 33.87 | v3n9k9.log |
| (10,10) | **v2.1** | default | SAT | 2,143 | 4.37 | v3n10k10.log.gz.b64 |
| (10,10) | **v2.1** | shuffle=7 | UNKNOWN | 752,186 | 261.68 | v3n10k10sh7.log |
| (12,10) | **v2.1** | default | UNKNOWN | 351,702 | 265.39 | v3n12k10.log |

備考: 「--unsat」「--sat」は kissat プリセット。sh はエンコーダ --shuffle。v1/v2-draft/v2.1 は符号化版数。UNKNOWN=honest bounded negative（cap 到達）、不在・非存在は一切主張しない。
`.gz.b64` は base64(gzip(生ログ))（kissat model の v 行を含む、最も大きい3本のみ。~1.7MB→b64 ~690KB）。復元手順と生ログの sha256 は logs/NOTE-gz-b64.md とファイル先頭行参照。
UNKNOWN=honest bounded negative（cap 到達）、不在・非存在は一切主張しない。

## 5. 結果A: 較正ラダー（v2.1）

- **UNSAT 側（s_7 再導出）**: n7k6（v2.1 default・13.56秒・174,155 conflicts）と
  n7k6sh42（--shuffle=42・独立第2符号化・15.35秒・176,473 conflicts）がともに
  UNSAT。受理言語が厳密 lex-leader で軌道被覆が機械検査済みの同一鎖の2符号化での一致により、
  「7×7 に6石以下の極大安全配置は存在しない」= s_7 ≥ 7（kissat の UNSAT 健全性への信頼の範囲で）。
  v2.1 の完全二方向鎖は draft 版より条件付き伝播が強く、同一述語の探索コストは
  70.23秒/832,104 conflicts から 13.56秒/174,155 conflicts へ縮んだ（draft 版 UNSAT 2件そのものは無効 §3）。
- **SAT 側**: n7k7（v2.1）の witness は K0031 の証人と格子同型（既知の再発見・陽性対照）。
  n8k8・n9k9・n10k10（v2.1）も SAT。v2-draft 時代の4インスタンスも SAT で
  model（witness）は独立検証済み（draft の鎖は充足方向に無害）。v2.1 の n10k10sh7 は cap 内 UNKNOWN（§4）。
- s_8/s_9/s_10 の UNSAT 側（n8k7/n9k8/n10k9）は cap 内 INDET（表参照）。

## 6. 結果B: 10×10 十石 witness の格子同型類（2類→5類）

primary witness `[[9,1],[1,2],[8,2],[9,2],[0,3],[3,4],[5,6],[9,6],[8,7],[2,9]]`
（v2-draft n10k10 SAT model から、canonical span 10×9）、
shuffle7 witness `[[2,0],[1,1],[7,2],[4,3],[5,3],[6,3],[3,4],[5,5],[1,6],[6,6]]`
（--shuffle=7 から、canonical span 7×7）、
v2.1 witness `[[6,3],[7,3],[0,4],[7,4],[8,4],[1,5],[2,5],[9,5],[2,6],[3,6]]`
（v2.1 n10k10 SAT model から、canonical span 10×4）。

既刊の明示 witness は2類である: K0038 witness（span 7×9）と K0034 本文の別witness `13 50 56 59 63 68 77 83 85 98`（span 10×9）。両者の正準形辞書式最小キー（D4 8像→min-corner 正規化→辞書式最小、K1206 classify.mjs と同一規約）は
`[[0,0],[1,0],[6,0],[1,4],[4,4],[1,5],[2,5],[0,6],[2,7],[0,8]]`（K0038-n10）と
`[[1,0],[4,1],[6,1],[2,2],[1,3],[6,3],[0,4],[3,4],[9,4],[6,8]]`（K0034-another-n10）で互いに非合同。

本レーンの3 witness の正準形キー:

| witness | canonical key | span | K0038 | K0034別 | 相互 |
|---|---|---|---|---|---|
| wit_n10k10 (draft) | `[[0,0],[0,1],[1,1],[8,1],[9,2],[6,3],[0,5],[4,5],[1,6],[7,8]]` | 10×9 | 非合同 | 非合同 | — |
| wit_n10k10_sh7 (draft) | `[[0,0],[5,0],[4,1],[2,2],[3,3],[4,3],[5,3],[6,4],[0,5],[1,6]]` | 7×7 | 非合同 | 非合同 | primaryと非合同 |
| v3wit_n10k10 (v2.1) | `[[1,0],[2,1],[2,2],[3,2],[3,3],[0,6],[0,7],[1,7],[1,8],[2,9]]` | 4×10 | 非合同 | 非合同 | 上の両者と非合同 |

よって 10×10 の十石極大安全配置の**既知の格子同型類は2類→5類**。機械可読正本は
output/classification.json（draft 5 witness 一括）と output/v3classification.json
（v2.1 witness も含めた正準形キー・対比較、scripts/classify_v3.mjs 生成）。

検証チェーン（両 witness とも）: 空点90点すべてが禁止四点組の第4点として blocked（covered 90/90・
violations 0）、4点組全件 safe、min|det|>0、Sinz/lex 条件を含む model 検査 PASS（check_model2・
アンカー gate 付き census 直結）。tamper（1石除去）は py/mjs 両検証器が rc=1 NOT-MAXIMAL-SAFE で
fail-loud 拒否。census.mjs 起動時アンカー検査（F/D/C/lines/circles = K0057 出版値）全件一致。
三点共線 triple は primary 5・sh7 5 個（証人が共円のみでなく共線でも攻撃している通常の構造）。
v2.1 ラン自身の witness（すべて decode→3系統検証 rc=0・tamper で py/mjs とも rc=1）:
n7k7 は K0031 witness と合同（**陽性対照**: 修正符号化が既知の s_7=7 witness を再発見）。
n8k8・n9k9 は draft 時代の witness と非合同の別配置（n=8 は全408カタログ（K0032）に属するとみられる
再発見対象であり、n=9 は s_9=9 の明示 witness として追加の検証済み例。新規性はここでは主張しない）。
n10k10 は **4.37 秒** で SAT（正しい鎖の伝播効果: draft 81秒→v2.1 4秒）し、上表第5類の witness を与えた。
n10k10sh7 は 270 秒 cap で UNKNOWN（shuffle 下の難度上昇の記録。draft sh7 witness は引き続き
SAT 方向の有効 witness である。不在・難の主張はしない）。
三点共線 triple 数: v3 witness は n7=3, n8=3, n9=3, n10=4（output/v3witness_features.json）。

## 7. 結果C: s_12/s_13 と難度曲線（INDET）

n12k10（v2.1・270s）と n13k11（v2-draft・280s）は cap 内 UNKNOWN。--sat プリセット・shuffle 併用でも
改善なし。n9k8・n10k9（gap-1、v2.1/draft）も同予算未達。既知 witness（K0320）の再探索は
n12k11 で3ショット（draft: default/--unsat/--shuffle=13）・n13k12 で1ショットすべて cap 内未達。
この「n≥12 では witness 探索すら冷起動 CDCL で届かない」という曲線は、s_12/s_13 の SAT レーンで
単発270s級の予算を前提とする限り、分解（行ごとの石数固定・左端ピン等 K1217 式の2重分解、
あるいは Cumberland 級の込み入った inprocessing 設定と resume 相当の積み増し）が必須という
運用上の知見として残す。s_12/s_13 の値は本研究群の他の項目（K0320: 上界、K1206: 近傍の完備陰性）から不変。

## 8. 限定

- kissat は DRAT 証明を出力していない。UNSAT の正しさは「kissat 4.0.4 の実装健全性 + 独立2符号化一致」の
  信頼境界であって、検証可能証明書ではない（v2.1 の軌道被覆検査は符号化側の健全性のみを機械保証する）。
- v2-draft の全 UNSAT 試行は取り下げ済み（§3）。SAT model すべて独立検証済みであり出版 witness に影響しない。
- witness の「第3・第4類」は既刊2類との非合同の主張であって、十石 witness 全数の分類ではない。
- 有限計算であり、s_n への一般化・不狩知の不在はここから主張しない。

## 9. 再現手順

```sh
# 禁止四点組カタログは起動ごとに K0057 アンカー照合 (fail-closed)
node scripts/enc_sat2.mjs 7 6 --out=n7k6.dimacs --meta=n7k6.json        # v2.1
node scripts/enc_sat2.mjs 7 6 --shuffle=42 --out=n7k6sh42.dimacs ...    # 独立第2符号化
kissat --time=270 n7k6.dimacs > n7k6.log                            # s UNSATISFIABLE
# draft 版（アーカイブ）: node scripts/enc_sat2_draft_chain.mjs ...（cnf2 と byte 一致）
node scripts/lexchain_orbit_check.mjs --out=output/lexchain_orbit_check.json   # §3 の機械検査
# model からの witness 取り出し（v行 → JSON, KYOUEN_NVARS は meta の nVars）:
KYOUEN_NVARS=26191 node scripts/decode_model.mjs n7k7.log n 7 k 7 > wit.json
python3 scripts/verify_witness.py wit.json       # SAFE+MAXIMAL（整数4x4行列式・空点ごと証人）
node scripts/verify_witness.mjs wit.json         # BigInt Bareiss（列順序相違の第2系統）
node scripts/check_model2.mjs 10 10 <cells-csv>  # census直結の第3系統 + D4 lex-leader 記録
node scripts/classify_sat_witnesses.mjs          # 格子同型分類（アンカー: K0031/K0038/K0034別/K0320）
```

## 10. ハッシュとCNF非刊行

CNF 本体は非刊行（計~420MB）。scripts/cnf-sha256.txt に v1/v2-draft/v2.1 全 CNF の sha256 を記録し、
上記コマンドで byte 再現可能。MANIFEST-sha256.txt に本実験の全刊行ファイルのハッシュを記録する。
