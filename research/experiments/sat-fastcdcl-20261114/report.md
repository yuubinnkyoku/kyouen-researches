# 高速CDCL SATソルバ fastsat — 6×12 q=8 最小極大 ≤38・6×22 の22石2石欠損witness（2026-11-14）

K0810 の自作CDCL（単発予算で (6,8) m=18 cap=41 などが未決着だった）を置き換える目的で、
Node.js 上に書き下ろした競争的CDCLソルバ `scripts/fastsat.js` を開発し、
既知の制御・全列挙fuzz・相互検証を通した上で open 境界を攻撃した。

## ソルバ

- 2-watched literals + blocker、EVSIDS（binary heap、指数減衰 0.95/0.99/0.995 切替可）、
  1UIP学習、Luby restarts（base 切替可）、phase saving、LBD ベースのDB削減＋メモリ圧縮、
  DRAT proof 出力（UNSAT時に限る）、cell変数の初期アクティビティ/位相ブート
  （`--ncells --cellphase=0 --cellboost` — sequential counter の補助変数が決定変数として
  探索を乱すのを抑制する。効く: 6×22 で 3382→2466 conflicts）。
- DIMACS入出力のみでK0810機（`row_deficient_sat.js`）のcensus・符号化・census不使用独立検証器と
  そのまま組み合わせられる。CNF生成は `scripts/cnf_driver.js`、witness検証は
  `scripts/model_verify.js`（=K0808/K0810の独立検証器 verbatim 呼び出し）。

## 主結果

1. **6×12・q=8 の最小極大サイズ ≤ 38**（従来 ≤ 39）。
   cap=38（全石数≤38・安全・極大）が SAT。38石witness（行構成 7,7,7,6,7,4）は
   census不使用独立検証器で safe+maximal PASS、SAT model は元CNF 20,842節すべてを充足。
   133,524 conflicts / 99.4 秒。cap=37 は 373,080 conflicts まで未決着（不在証明ではない）。
2. **6×22・q=5 に行欠損（2石欠損）極大安全配置の22石witness**（行構成 4,4,4,2,4,4）。
   独立検証 PASS。2石欠損witnessの既知の最小 m が 28 から 22 に下がる
   （1石欠損23石witnessの m=22..27 帯と同じ盤に2石欠損も同居する）。
   3,382 conflicts / 11.2 秒（repo旧CDCLは同一盤に 80,747 conflicts / 180 秒）。
3. **抵抗の記録（非発見・不在証明ではない）**: 6×29・q=5 行欠損（2設定・計 17,798 conflicts）、
   6×28・q=5（2設定・計 10,939 conflicts・SAによりSATであることが既知）、
   6×12・q=8 cap=37（373,080 conflicts）。
   なお cap=38 は最初の設定（vdecay=0.95/base=512）で 366,683 conflicts 未決着の後、
   第2設定（vdecay=0.995/base=8192）で 133,524 conflicts で SAT —
   **ソルバ設定の非単調な難度差の実例**（K0811のSAパラメータ依存性と同種の教訓）。

## 制御・検証

- 既知結果の再現: 2×8 q=4 SAT（88 conflicts）・2×9 q=4 UNSAT（1,440 conflicts）。
- fuzz: 乱数CNF 450題（nv≤15・節長1..4・重複リテラル込み）を全列挙と照合 — 0不一致、
  SAT model はすべて元節リストに対して独立検証。
- 相互検証: 乱数3-SAT 60題（nv 20..40）をK0810の旧CDCLと判定一致 60/60・SAT model検証。
- 実装バグは実際に捕捉された: (a) DIMACSパーサの `cur.length=0` 参照バグ（全節が空に）、
  (b) unit節が reduceDB の watch 再構築でガベージの第2 watch を持ち、無関係なリテラルの
  偽化で偽UNSAT衝突を起こすバグ（6×22で4025 conflicts後に発現、衝突節完全偽の
  assertion tripwire で検出・修復、修復後 fuzz 450題 0不一致）。
- UNSAT時は DRAT proof を出力する設計だが、本実験の未決着インスタンスに
  UNSAT判定はまだない（DRAT独立検証は未使用・今回の成果はすべてSAT witness）。

## 残作業

1. 6×29・q=5 行欠損のSAT/UNSAT（M_{6,5}=29確定の唯一の欠け）— 現ペースでは
   10^5〜10^6 conflicts 規模の予算または符号化改良が必要。
2. 6×12・q=8 cap=37（UNSATなら最小極大=38確定）。
3. (6,8) m=18 cap=41・(6,6) m=22・(5,6) m=19・(5,7) m=19,20・(6,7) m=20 への適用。
4. UNSATが取れた場合の DRAT チェッカ（Node実装）の整備。

## 追加成果（第2実行・同日）

4. **5×19・q=6 に行欠損極大witness（24石・行構成 5,5,5,5,4）→ M_{5,6} ≥ 20**（従来 ≥19）。
   K0811 のSAが5 run抵抗した m=19。fastsat に `--seed` 機能
 （LCGで初期アクティビティに ≤0.01 のjitter＋補助変数の初期位相ランダマイズ）を追加した
   seed portfolio の seed=7 が 8,378 conflicts / 7.1 秒で解決。
   census不使用独立検証器で safe+maximal PASS・SAT model は元CNF全節を充足。
5. **抵抗の記録（非発見・不在証明ではない）**:
   (5,7) m=19 — seeds 1,2,3（base=8192）・11,12（base=4096）の5設定・各100-120秒・
   110,139〜124,512 conflicts すべて TIMEOUT（計568,576 conflicts）。(5,7) m=20 —
   seed=3・117,144 conflicts で TIMEOUT。(6,8) m=18 cap=41 — 3設定・計約440,000 conflicts 未決着。
6. seed portfolio の教訓: 同一インスタンス・同一ヒューリスティクスでも初期アクティビティ/位相の
   わずかなjitterで (5,6) m=19 が SA 5 run抵抗→8千 conflicts で解決するほど難度が変わる。
   cap=38 の設定依存性（第3節）と同種の非単調性であり、単発runの抵抗を
   不在の証拠として扱えないことをさらに補強する。
