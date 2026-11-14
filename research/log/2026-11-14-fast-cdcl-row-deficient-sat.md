# 2026-11-14 高速レーン: fastsat CDCL開発 — 6×12 q=8 最小極大 ≤38・6×22 の2石欠損witness

## 経緯と目的

K0810の自作CDCLは (6,8) m=18 cap=41 や 6×12 q=8 cap=38 などが単発予算で未決着だった。
pysat/kissat の導入は本サンドボックスで禁止（pip/uv ともパッケージ導入不可・g++/make も無し）のため、
Node.js で書き下ろした競争的CDCL `fastsat.js` を開発した
（repoの codeload 展開も不要・DIMACSだけでK0810機と直結する設計）。

## 成果

1. **6×12 q=8 cap=38 が SAT** → 最小極大サイズ ≤38（従来 ≤39）。
   38石・行構成 7,7,7,6,7,4・census不使用独立検証 PASS・model は全20,842節を充足。
   133,524 conflicts/99.4s。第1設定（vdecay=0.95/base=512）は 366,683 conflicts で未決着、
   第2設定（vdecay=0.995/base=8192）で解決 — ソルバ設定間の非単調な難度差を記録。
2. **6×22 q=5 に22石（2石欠損）行欠損極大witness**（行構成 4,4,4,2,4,4）。
   2石欠損の既知最小 m を 28→22 に更新。旧CDCLが 80,747 conflicts/180s かかった盤を
   fastsat は 3,382 conflicts/11.2s。
3. 抵抗（非不在証明）: 6×29 q=5（2設定・17,798 conflicts）・6×28 q=5（2設定・10,939 conflicts）・
   cap=37（373,080 conflicts）。

## 検証プロトコル

- 制御: 2×8 q=4 SAT（K0796再現）・2×9 q=4 UNSAT（M_{2,4}=9 制御）。
- fuzz: 450題（nv≤15・全列挙照合・重複リテラル/unit込み）0不一致・SAT modelは元節リストで独立検証。
- 相互: 乱数3-SAT 60題（nv 20..40）をK0810旧CDCLと判定一致 60/60。
- 実装バグ2件を実際に捕捉: (a) DIMACSパーサの配列参照バグ（全節空化）、
  (b) reduceDB compactionがunit節にガベージ第2watchを付け、無関係リテラルの偽化で
  偽衝突→偽UNSAT化するバグ（6×22 で4025 conflicts後に発現。衝突節完全偽のtripwireで検出）。
  修復後fuzz全通過。UNSAT時のDRAT出力は実装済みだが、今回はUNSAT未取得のため未使用。

## レジューム

1. 6×29 q=5 行欠損 SAT/UNSAT（M_{6,5}=29確定の唯一の欠け。現ペースでは10^5-10^6 conflicts規模 —
   予算分割か符号化改良・または並列ポートからの再開設計が必要）。
2. cap=37（UNSATなら 6×12 q=8 最小極大=38確定・DRAT証明+チェッカ整備が前景）。
3. (6,8) m=18 cap=41・(6,6) m=22・(5,6) m=19・(5,7) m=19,20・(6,7) m=20 への適用。
4. fastsat は repo `research/experiments/sat-fastcdcl-20261114/scripts/` にある
 （md5 391254070c897f4bd824b457b20e3b05・push後remote一致確認済み）。

11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN のまま
（本成果は固定幅Mと最小極大の話で無盤面勝敗に無関係）。
