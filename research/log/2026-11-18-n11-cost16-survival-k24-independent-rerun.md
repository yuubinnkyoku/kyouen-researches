# 2026-11-18 N11 31行cost-16 parent 生存曲線 k=24: 並走実行の相互検証と正本JSON title誤記のerratum記録（independent rerun）

## 経緯（同一時限タスクの並走・上書きなし）

同一の時限タスク（長期レーン）の複数実行が並走する運用において、当レーンは k=23 の先行出版（commit `c0179112`・正本復元 `01c17daa`/`0a3d5788` 後）をpush直前のHEAD再取得で確認した後、k=24 拡張に着手した。ところが計算実行中（約11:03着手・約11:10完了）に別レーンが commit `b89cd0f5`（11:06:50）で同一の k24 出版を先行で完了し、続いて commit `d2805b7b`（11:08:02）で crosscheck script を k13..k24 に拡張して k24 JSON の pin（blob `a0955297355beef8b2cf2560afebb0001fcf880b`）を確定した。当レーンは push 直前の最新HEAD再取得でこの出版を検出し、**上書きせず**本 rerun log のみを別pathで出版する（k23時の衝突〔`32887705`/`be0366ac` 上書き→復元〕で確立した運用教訓の実効確認）。

## 当レーンの独立計算（要約）

出版済み k23 script（blob `46374ca4…`）を機械変換で k24 script に生成。変換時の事故: 識別子置換で `IDX24 = 22` の値更新を落とし smoke test の `load_top24` assert で即検出・修正（k22/k23時の usage行・rank root block 残存事故と同種・計算前検出）。計算前 smoke test で組立済み機構から k=1..23 の kill/kill_A/kill_B が出版 k23 JSON（blob `fc60c366…`）と全点厳密一致することを確認してから本計算した。

- **確定値（出版版と全て一致）**: kill(24) = 2,198,596,292,207,938,784（74.1154%）・kill_A(24) = 1,697,688,995,945,872,118・kill_B(24) = 500,907,296,262,066,666・A_survive = 608,098,295,348,062,270・B_survive = 159,755,754,124,480,302（5.3854%）・marginal kill = 62,646,884,579,080,928（m24 = 120,643,896,818,077,661 の51.9%・ハブ根で38.1%→51.9%へ反転上昇）。
- **marginal分解（出版logと同一の数値を独立導出）**: Σ新j2 = 65,242,312,179,900,681（m24の54.08%・disjoint 12本 = 64,490,584,883,588,994〔53.46%・平均5.374e15〕・行18共有11本 = 751,727,296,311,687〔0.62%〕）・Σ新j3 = 7,304,112,563,625,318（6.05%）・Σ新j4 = 58,812,622,721,370（0.049%）。**disjoint-partner法則の予測（ハブ根ならmarginalは50%台へ戻る）が的中**。
- **構造（出版版と一致）**: 新pair 23本（shared 11 / disjoint 12）・新triple 253本（b_only 164 / zero 62 / disjoint 27）・新quad 1,771本（b_only 371 / zero 1,400 / disjoint 0）・全 C(24,5)=42,504 個の 5-subset が構造的ゼロ（I-E quad打ち切り11度目）・triple census C(24,3)=2,024 = b_only 1,284 / zero 450 / disjoint 290。
- **検証**: 27 checks all PASS・finalize二重実行 byte-identical（当レーンJSON sha256 `af5981d6…`・git blob `ec69b452…`）・JSONL 2,051 records（pair 23 + triple 253 + quad 1,771 + cross 4）・cross mismatches 0（disjoint triple 2本MyPm・b_only quad 2本PmLazy・出版logと同一候補）。

## 交叉検証: 2つの完全独立実行の一致 + 正本JSON title誤記の発見

当レーンの計算と出版版（commit `b89cd0f5`）の全出力を比較した結果:

- **JSONL**: 2,051/2,051 record で key set・順序が同一。**値差分 0・memo_states 差分 0**。差異は wall-clock の `sec` field のみ。
- **JSON**: 数値・構造・checks フィールドは全点完全一致（kill系列・census・rank24_root・quints・A/B分割すべて）。テキストフィールドに2件の差異:
  1. **title（出版版が誤記・erratum）**: 出版 k24 JSON（blob `a0955297…`）の title は **k=23 の文言「Exact survival curve extended to k=23 … fifth non-hub root (6,15)」のまま**で、k24 への更新が機械変換で漏れていた。当レーン版は「…to k=24 … twelfth hub root (8,18) on row 18」。**影響は体裁のみ**: 全数値・`structure`（`rank24_root`・census・`quints_all_zero`）・27 checks は正しく、crosscheck 28 checks（network/local両mode・commit `d2805b7b`）も通過している。
  2. **ie_mechanism（当レーン版が旧文言）**: 出版版は「same A/B split identities as the k=14..k=23 publications」（更新済み・正）、当レーン版は「k=14..k=22」（機械変換の取りこぼし・意味は同じ）。

**erratumの取扱い**: repo規約（出版済みpin対象bytesは不変・crosscheck pin `a0955297…` が正本JSONを参照・cf. 11:00のk23正本復元）に従い、本erratumは本logへの記録のみとし、正本JSONの上書き修正は行わない。将来 k25 拡張等で正本JSONが再生成・再pinされる機会に併せて修正することが望ましい。なお reproduce 検証は title を読まないため、本誤記は後続のpin照合・再現性検証には影響しない。

また当レーンの k23 局所計算（JSON sha256 `7133be0d…`・JSONL 1,797 records）も正本（`3b208df9…`系の復元版）と全値一致しており、**k23 は3実行・k24 は2実行の完全独立計算が全値で一致**したことになる（k23 2実行目〔k23 rerun log `32887705` 系〕と当レーンの JSON は title 含め byte-identical）。

## 運用上の教訓（k23衝突時の教訓の追加確認）

1. **push直前HEAD再取得の実効性**: 今回は検出が計算完了後であったため重複計算のコストは発生したが、**上書き事故は完全に回避**できた（k23時は取得僅差で握りつぶした）。
2. **計算着手前の同題材出版確認が重複コストの削減に有効**: 当レーンは着手時に「k24 は未出版」と確認してから着手したが、先行レーンが同時刻に着手済みだった。同一時限タスクの毎時運行では、着手前確認に加えて「直前の実行の着手予定時間帯」も考慮する価値がある。
3. **機械変換の取りこぼしはテキスト系フィールドにも起きる**: k24出版版の title 更新漏れ（本erratum）と当レーンの ie_mechanism 更新漏れは、いずれも数値系assertを通過する。変換時の残存grepは値系（IDX・件数assert）だけでなく**出力JSONの文言フィールド一覧**も対象にすべき。
4. **IDXの値更新**: 識別子置換（IDX23→IDX24）だけでなく値（22→23）の更新も変換表に明示的に含めること（当レーンは smoke test assert で即検出したが、計算前のpy_compileだけでは検出できない）。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。生存曲線はban回避の代替最小cover計画の組合せ数であって、探索コストでもverdictでもない。REFUTED-D10・STERILE は LOSS 証明ではない。
