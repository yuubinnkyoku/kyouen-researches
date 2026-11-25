# 2026-11-16：cost-65n win2証明書の独立盲抽出・byte-identical照合 — bit90/bit117両root51+49手・BigInt/Bareiss両verifier再実行PASS・manifest全統計一致

開始時main: `373bcdd9`（並走のcost-65n win2 certificates manifest出版直後）。対象は並走が08:24〜08:25Zに出版した**cost-65n child `00000000000000801202010000800000` の2 WIN7-D10証明書**（bit90 root `00000000040000801202010000800000` 1,285,412B・bit117 root `00200000000000801202010000800000` 721,989B・commits `57ab8ed5`/`15c9b66b`/`373bcdd9`）。本レーンは証明書バイト列を抽出前に一切読まず、**bit-89と同一手順の盲抽出→byte-identical照合→両独立verifier再実行→manifest統計照合**を行った。なお本検証の前に、同じ2 rootsのsweep独立再実行59/59 node-exact検証とfold投影事前登録（投影head 1441→1444/174/6404/506746/4677/370660・mim 1+2・3親delta）をcommit `0c237017`で出版済み（fold receiptは本log時点で未着地）。

## 検証内容（出力 `output/class2-lane-cost65n-win2-certificates-independent-verification-20261116.json`・schema `-v1`）

### 盲抽出（published generic blind driver + repo-verbatim extractor・empty kill table）
- 手の再列挙: `legal_candidates.py`（Bareiss 4×4・2026-11-14修正版）でroot mobility **51手（bit90）/49手（bit117）**を独立に列挙。証明書のroot行・receipt・manifestは抽出前に不使用。
- 抽出: `cert_driver65j.ts`（published generic blind driver・commit `a7ac1757`時点）→ repo-verbatim `class4_child1_cert_extractor_exact_v16.ts`（empty kill table = blind）を**4並列チャンク構成**（bit90: 12/13/13/13・bit117: 13/12/12/12）で実行。
- **両rootともfbt_drops 0・fatalなし・全手ok/capped=false**。extraction nodes合計 3,151,841（bit90 2,438,487 + bit117 713,354）。抽出所要は各チャンク3〜7秒。

### byte-identical照合（組立後比較）
- 組立: rows sorted-unique（Python byte順・並走assemblerと同一規約）+ `n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS` header + root行。
- **bit90**: 35,627 rows・1,285,412B・md5 `616b15e76809b3e31064986d804d29a5`・git blob `c2460e59` — 並走出版証明書（part1of2+part2of2連結）と**byte-identical**。
- **bit117**: 20,047 rows・721,989B・md5 `9a1e0abe9602b25e5a3dd0ae1bbf4b59`・git blob `ac0ea37d` — 並走出版証明書と**byte-identical**。

### 両独立verifierの本環境での再実行
- **BigInt検証器**（3×3余因子展開・repo importなし）: bit90 **51/51 sub-roots PASS**・union missing/extra 0/0・winner 47,526・loser 14,036・terminals 12,139 [13,17]・visited 73,701。bit117 **49/49 PASS**・union 0/0・winner 28,468・loser 9,004・terminals 6,753 [13,17]・visited 44,225。両root `root_safe` true。
- **Bareiss検証器**（`verify_bit7_win7_cert.ts --cert --root-check --subroots`・exit 0）: bit90 root check stones 7/loserMobility 51・rows 35,627・seen 73,701・terminals 12,139 [13,17]。bit117 stones 7/loserMobility 49・rows 20,047・seen 44,225・terminals 6,753 [13,17]。**BigIntと全統計量が一致**。
- **並走manifest**（`class2-lane-cost65n-win2-certificates-20261116.json`・`373bcdd9`）とのtotals照合: rows 55,674 ✓・sub_roots 100 ✓・winner_states 75,994 ✓・loser_states 23,040 ✓・terminal_count 18,892 ✓・cert_bytes 2,007,401 ✓ — **全項目一致**。

### chunking観察（実験事実）
extraction nodesはチャンク構成に依存する（並走の単一チャンク構成 3,539,855 nodes vs 本レーン4分割合計 3,151,841 nodes・−10.97%）が、**sorted-unique行集合と組立証明書はチャンク不変**。抽出器内部のmove間キャッシュ挙動に由来する計算量差であり、証明書内容・不一致ではない。

## 意義

1. cost-65nの2 WIN7-D10証明書が**第三者環境でbyte-exactに再現可能**と確定した。sweep独立再実行（59/59 node-exact・`0c237017`）と合わせ、cost-65n行のverdict・証明書・統計がすべて独立検証済み。以後の65n fold receipt着地時の監査は本recordをpinできる。
2. 4並列チャンク抽出が単一チャンク抽出と同一の証明書を生成することを確認 — 大規模root（51手超）の証明書抽出をCPU 4並列で安全に分散できる実測根拠。
3. 本レーンのfold投影事前登録（`0c237017`・投影head 1444/174/6404/506746/4677/370660）は並走fold receipt着地前に出版済み。着地時に全フィールド照合を行う。

## 解釈境界（重要）

- WIN7-D10証明書は2つの7石rootそれぞれから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。NOT-STERILEは勝敗決着ではない。
- solved 1441（→fold receipt着地後の1444投影は投影に過ぎない）はmanifest被覆の簿記。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4は引き続きUNKNOWN**。

## 今後

- 並走のcost-65n fold receipt着地時: 事前登録（blob `da2b2292`・commit `0c237017`）との全フィールド照合（投影head 1444/174/6404/506746/4677/370660・mim 1+2〔child cost 65・`00000000000020003800000008080000` cost 69・`00000000000100809002000000000008` cost 65〕・3親delta・hist delta `c2=2,c4=0` −3）。不一致の場合は実験事実として記録する。
- 次target（cost-66帯等census v4 ranking）は並走依存。本レーンは新規claimを作らない。
