# 2026-11-16：cost-60c sweep完走 — 60/60・1 WIN7-D10（bit 92）・bit-92証明書二重検証・fold head 1407→1410・bit-119 REFUTEDで70j行cross-cover失敗（負の事実）

開始時main: `834c7e2e`（70j erratum）。本レーンのclaim `a20fff85`・成果一式 `57f6678a` は前セッションでpush済み。その後並走の **class4-lane cost-87 STERILE sweep**（`a084431f`: 87/87 REFUTED-D10、`f2da19ff`: log + K0783）が同一lane dirに着地したが、best class-4 blocker S5 `00000000020000003800000080000000` の18行は閉じずSTERILE確定のみ（receiptなし・frontier不変・本foldとパス非競合）。その他 `650c699c`〜`8576c9a7`（K0861/z=5・CI）は別dir。本レーンはcost-70j/65k/74hの3 STERILE行（best coverable class-2 candidate S5 `00000000000000801202000000200000` の全残行）のone-stone-replacement隣接open行解析に基づくcross-cover試行。70j-child `00000000000000801282000000200000` の114個の隣接open行のうち最安はcost 60で、そのchild `00000000000000003800000008008020`（dual demand c1=1,c2=1,c4=0、lift parent = class-2 `00000000000000003800000008008000` 50/3551 と class-1 `00000000000000003800000000008020` 74/5399）は未sweep・未claimだった。**60合法候補のうちbit 119だけが70j行をcoverする**（これがcross-cover動機）。

## 実施内容

### 1. IN FLIGHT claim（commit `a20fff85`）
`class2-lane-cost60c-inflight-20261116.json` + `scripts/prep_claim_cost60c_20261116.py`（demand・両parent・60候補・covers をhead 1407で再導出）。

### 2. sweep完走（v16・depth 10・8バッチ・4並列・約2.5分）
- **60/60・1 WIN7-D10（bit 92）・59 REFUTED-D10・0 capped・総nodes 25,197,741**。pilot 8×3402（全batch d6制御 loss=false）・terminal全[13,17]・andclose全true。heaviest: bit86 2,508,161 / bit105 1,529,196 / bit66 894,539。
- **bit 119はREFUTED-D10** → 70j行（`00000000000000801282000000200000`）はこの隣接経由では閉鎖せず、openのまま。負の実験的事実のみ（LOSS証明ではない）。
- determinism rerun（batch5・fresh process）: verdicts/nodes/capped/terminalStoneRange全てnode-exact一致（ms以外）。v15交差（単一foreground invocation・pilot 5949）: bit 92 loss=true一致、反証anchor bits 119/0/120 loss=false一致。

### 3. bit-92 WIN7-D10証明書（二重検証済み）
- root `00000000100000003800000008008020`（=child|1<<92、D4-canonical `00000000000000801292200000000000`）: **27,547 rows / 45 sub-roots（=root loser mobility全法手）/ 804,782 extraction nodes / fbt_drops 0**。cert 996,758 bytes・md5 `d771ef8275a9889a22974310e5c1e411`・git blob `b35128897b07f03e4baa11583423453cb378e18d`。
- BigInt検証（`verify_win7_certificate_bigint_independent.mjs`）: union 0/0・45/45・terminals [13,17]・8,543 terminals・winner 38,090・loser 12,028。Bareiss検証（`verify_bit7_win7_cert.ts`）: 45/45 PASS。両者独立に全sub-root検証。
- 独立監査（`scripts/audit_cost60c_raw_sweep_20261116.py`・stdlibのみ・md5 `50cbf9d2…`）: 60候補独立再列挙bit-exact・raw batch blob pin・MS5 manifest検証への置換を含む全assert一発通過・再実行byte-identical。

### 4. 出版（commit `57f6678a`）
raw batch 1-8 + determinism rerun + v15 crosscheck + sweep audit + win7-certificates JSON（blob `f76cd7dd10364f8110389e6c3aa082d5dff20b83`）+ claim v2（completed・blob `5b9df50226f5420c03af39813c55b247992deaf6`）+ cert 996,758 bytes（17チャンク分割push）+ bigint/bareiss verify records + audit script + cert_driver60c。全てraw CDN（commit pin付き）でmd5照合byte-exact。

### 5. fold — head 1407 → **1410**（`scripts/recompute_frontier_cost60c_receipts_20261116.py`）
- 75e chain head 1407/174/6441/509300/4711/373023 をrunpyで再現（cost-75e fold scriptが内部でreconciliation chain全体をbyte-identical再現・3つの75e出力blob `5cd93de7…`/`2154bcb9…`/`08aaf318…` を再assert）。
- sweep再導出（8 raw batchから）・bit-92証明書再assert（manifest blob・md5・git blob・sorted-unique・BigInt/Bareiss）・root disjointness（1 root vs 717 folded roots = 713+4、raw/D4両方）・childが1407でgenuinely remaining（両lift parentがchild行をedge 60で保持、demand c1=1,c2=1,c4=0、70j行もopen）。
- **fold結果: 3行閉鎖（全てin-manifest marginal）** — child（edge 60）・`00000000000000801092200000000000`（edge 59）・`00000000000000801292000000000000`（edge 72）。**新head 1410/174/6438/509109/4711/373023**（needed計数は不変: 閉じた3行は全てc1>0のため、open_only需要計数・histogram共に無変化）。
- affected parents 4個: class-1 lift 74/5399→**72/5280**（child+59を喪失）・class-2 lift 50/3551→**49/3491**・class-1 shared `00000000000000801092000000000000` 79/6044→**77/5913**（59+72を喪失）・class-2 shared `00000000000000801212000000000000` 69/5448→**68/5376**（72を喪失）。
- 上位候補不変: best coverable class-2 3/209（3 STERILE行 65k/70j/74h 全てopenのまま）・second 5/364・audit-blocked 10/698・best class-4 18/1460。top-candidates CSVは75e版とbyte-identical（blob `08aaf31892680668e7e292848235a154eb746407`）。
- 出力3ファイル（再実行byte-identical確認済み）: fold JSON（blob `239a6cf432e53713514d583e3682e1bef6075968`・9,495 bytes）・ranking CSV（blob `a01cfd5340fa89c0eaf834dcb96000f9b04d20ae`・7,535 bytes・md5 `1edd03f2f63b8e6a308dd7ab1c4ee5cc`）・top-candidates CSV（md5 `83b42f4e1b491d87172d32cd28fdaa1c`）。

### 6. ワークスペース喪失からの全chain再構築（今回の副成果）
本fold実行前に実行環境がリセットされ、未公開のローカルスクラッチ（tmp-cost*抽出中間物）を含むワークスペースを喪失。**repoの公開成果物のみから作業環境を完全再構築した**: (a) lane全体の必要ファイル約4,000個をraw CDN（commit `57f6678a` pin）から再取得してsize/blob照合、(b) 公開済み `reconstruct_tmp_cost62a/63h/63i/63j/65m/67d/70g_*.py` を実行、(c) 未公開だった **tmp-cost58c と tmp-cost84a 向けに `scripts/reconstruct_tmp_cost58c_84a_20261116.py` を新規作成**（公開証明書からcert-receipt・consumed.txt・tsverify・bigintレコードを合法手再列挙付きで再生成、70gパターン準拠）、(d) 75e chainが全blob pin込みで一発完走（約10秒）し、1407 head再現を確認。**これにより11-13以降の全fold chainがmainの公開成果物だけから再現可能になった**（再現性の構造的改善）。

## 構造的事実

- best coverable class-2 S5（3/209）の3 STERILE行のうち、**70j行のcross-coverはcost-60隣接経由では失敗**（唯一のcover root bit 119がREFUTED-D10）。ただし70j erratum（`834c7e2e`）の通り、STERILE行は他childのreceiptからのcross-coverで閉鎖され得るため、「永久に不可能」ではない。
- cost-60c receiptは1 rootで3行を閉じた（child行 + 2つのin-manifest marginal、うち2行は複数parentの共有行）。WIN7 receiptのmarginal経由の複数parent同時閉鎖は75e bit-10と同型。
- solved 1410はmanifest被覆の簿記。REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。

## 次の状況

- 70j-childの次の未sweep最安隣接は **cost 62 `00000000000000801282020000000000`**（parents 73/5489 と 49/3360）。着手前にどの合法rootが70j行をcoverするか事前計算してからclaim→sweep→fold。65k-child最安隣接 cost 64群、74h-child最安隣接 cost 65 `00000000000000805222000000000000` も候補。
- 76c claimはin-flight（1407基準・着手禁止）。76d/77e fold着地後はこの1410 headとのreconciliation foldが必要（root disjointness対60c rootをassert）。
- 並走のclass4-lane cost-87 STERILE（`a084431f`/`f2da19ff`）はbest class-4 blocker S5 18/1460の全行をSTERILE確定したが行はopenのまま（frontier計数に影響なし、reconciliation不要）。best class-4 candidate S5はown-row-coverableカテゴリから離脱。
- 11x11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。
