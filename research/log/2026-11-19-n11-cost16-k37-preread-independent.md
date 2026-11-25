# 2026-11-19 N11 cost-16 k37 preread 独立検証script出版 — 第二導出系列（bit-mask交差エンジン）で出版済みrank-37 preread JSON（blob `b98ed685…`・34 checks）の全欄を機械再導出し全一致・rank-35/rank-36回帰欄も出版k35/k36 preread JSON本文欄と三方一致・rank-36 preread main欄に初めて第二系譜による欄単位検証を付与（従来はProxmox同一script再現のみ）・k32→k37のera接続鎖（quint b_only 8,797/10,833/13,004/14,599/17,434/20,156・quint zero 192,579/226,503/265,252/310,033/359,558/415,741・triple b_only 2,992/3,296/3,622/3,970/4,361/4,758）を機械導出で確認・33 verification checks 0 failures・二重実行byte-identical

## 位置づけ

rank-37 preread出版（`900f68c3`/`98321003`/`510f0827`/`ad120f9f`・preread JSON 34 checks all pass）の直後に位置し、k37 preread logのレジューム項3「k37 preread独立検証script（k32〜k35パターン）の出版」を別レーンで先行履行した。k=35 prereadまでの独立検証script（`verify_cost16_k35_preread_independent_20261118.py`・commit `41c4cf12`・30 checks）と同じ役割を、k=37に対して果たす。

## 出版物

**script**: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/verify_cost16_k37_preread_independent_20261119.py`（33,473B・git blob `7fdcedae1f780d92b37ef4922fed1f51eee472a4`・sha256 `25e7764a…`・`py_compile` PASS）

第二導出系列として、preread script群のdict-accumulate/Counter系譜と**異なる分類コード経路**（bit-mask交差: d2 = 対毎ANDのOR、d3 = 三組毎ANDのOR、popcountでb_only/zero/disjoint判定）でpinned phase-B aggregate（blob `31bdefdb…`）から全構造欄を再導出する。エンジン健全性のため全C(37,3)=7,770組合せとrank-36/rank-37の新quint層全区間（C(35,4)+C(36,4)=111,265件、合計119,035比較）でCounter変種との全一致を別checkで保証。

入力pinは agg / k35 preread（`490fa3a0…`）/ k36 preread（`760aa396…`）/ k37 preread（`b98ed685…`）の4件（jsdelivr + raw fallback・`--local DIR`対応）。

## 検証結果（33 verification checks 0 failures・rc=0）

- **meta (4)**: k37 prereadのcheck_count=34/all_pass/schema `n11-cost16-k37-preread-20261119-v1`・宣言入力pin（aggregate/k35_preread/k36_prereadがexpectと一致）・k36 prereadのcheck_count=33/all_pass・unknown_status免責（11×11等はUNKNOWN・no verdict）。
- **engine (1)**: bit-maskエンジンとCounter変種が119,035比較で0 mismatch。
- **rank-35層 (5)**: 出版k35 preread JSON rank35欄とk37 preread rank35_regression欄の双方に対し、root/membership/A-B split（120,058,481,266,728,720 = 92,036,253,749,417,268 + 28,022,227,517,311,452）・prior hits {18: 15-sharer, 21: []}・4新層census {16/18}・{348/133/80}・{1,612/4,289/83}・{1,595/44,781/0}・二重行hist 3種・profile全1,595本 {3/2/0}・disjoint quad 83（union 8・累積1,195をC(35,4)全件再計数）・full C(35,3) {3,970/1,257/1,318}・C(35,5) {14,599/310,033/0}（hist {15:177,16:33,18:1112,19:273}ほか）・sextet C(35,6) all zero・era接続（14,599−1,595=13,004、310,033−44,781=265,252）が全一致。
- **rank-36層 (5)**: 出版k36 preread JSON rank36欄（**これまでProxmox同一script再現（`fc46f01e`）しかなかった部位に、権威の異なる第二系譜による欄単位検証を初付与**）とk37 preread rank36_regression欄の双方に一致。root [19,22]・membership 120,046,727,515,486,665・prior {19: 10-sharer, 22: []}・4新層census {10/25}・{391/63/141}・{2,458/3,919/168}・{2,835/49,525/0}・hist 3種・profile全2,835本・disjoint quad 168（累積1,363）・full C(36,3) {4,361/1,320/1,459}・C(36,5) {17,434/359,558/0}（hist {15:2785,16:545,18:9217,19:4887}）・sextet C(36,6) all zero・era接続（17,434−2,835=14,599、359,558−49,525=310,033）。membership単調減少 m35 > m36 > m37 も確認。
- **rank-37層 (14)**: 出版k37 preread rank37欄の全欄に一致。root `00000000080000003800000108001000` [8,19]・membership 119,973,409,932,394,637（A 91,996,175,553,485,330 / B 27,977,234,378,909,307・恒等式・m36未満）・prior hits {8: [23] 単一sharer, 19: [0,2,3,8,9,10,15,29,32,33,35] 11-sharer}・新pair 12/24（= 行8sharer 1 + 行19sharer 11）・新triple {397/100/133}（histに行8が8 recordで初出現）・新quad {2,394/4,589/157}（hist行8: 11）・新quint {2,722/56,183/0}（hist {15:339,16:71,18:1043,19:1269}・**行8・行21・行22とも不参加**）・profile全2,722本 {3/2/0}・単一sharer行8のtriple/quad限定二重行化（8 record/11 record/0）・disjoint quad 157（union全8・**累積1,520をC(37,4)=66,045全件bit-mask再計数で直接確認**・1,363+157）・full C(37,3) {4,758/1,420/1,592}（hist 16 bin全一致）・full C(37,5) {20,156/415,741/0}（hist {15:3124,16:616,18:10260,19:6156}）・sextet C(37,6)=2,324,784 all zero・era接続（20,156−2,722=17,434、415,741−56,183=359,558）・raw JSON exact整数序列化。
- **era鎖 (3)**: k32→k37の5段接続を機械導出で確認（quint b_only / quint zero / triple b_only の各系列。全段 full(n)−new(n)=full(n−1) が成立）。
- **回帰欄の系譜横断一致 (1)**: k37 prereadのrank35_regression欄・rank36_regression欄を、本レーンの機械再導出値と出版k35/k36 preread JSON本文欄で再帰比較（尤もなbookkeeping欄 `classifier_comparisons`/`mismatches` を除く）し、差分0・0。**3独立アーティファクト（k35/k36/k37 preread）+ bit-mask機械導出の四方で全欄一致**。

## 実行記録

- 実行: 純Python・1プロセス・CPU並列なし・入力はCDN pinned fetch。**33 verification checks / 0 failures**・rc=0・1回約2.5〜3分（full quint C(32..37,5) 6件・sextet C(35/36/37,6) 3件・disjoint_global C(33..37,4)・新層census idx 32..36をbit-maskエンジンで再導出）。
- **二重実行byte-identical**（cmp一致・出力3,629B）。
- rank-37定数は本検証の前に、前回ランでTS系譜による事前導出＋anchored-rep系譜（k36 preread scriptからの厳密機械変換・33 checks版）による独立script実行の両方で同一値を確認済み（並走レーン出版の34-check版とも全数値一致・差異はnote文面と追加check 2件のみ）。本検証で Third code path（bit-mask）+ 出版済み2 preread JSON本文との再帰照合まで含めた重層検証が完成。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4はいずれもUNKNOWNのまま。** 本検証はban回避代替最小cover計画の構造欄の独立検証であり、勝敗に関する何らのverdictも生成しない。

## レジューム引継ぎ（本レーン追加分）

- k37 preread独立検証は本出版で完了。次回は最新mainで k=37 本計算・crosscheck k37拡張の出版状況を確認のうえ、未出版なら着手（並走レーンが担当している可能性が高いので、まず出版有無の確認を必ず行う）。
- rank-38 rootの事前導出（pinned aggregate top50 index 37へのk37_facts flow適用）はまだ。着手時は本レーンのbit-maskエンジン流用でrank-38層のpreread定数を事前計算できる。
