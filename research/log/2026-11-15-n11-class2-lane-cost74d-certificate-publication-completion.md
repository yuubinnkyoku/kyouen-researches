# cost-74d WIN7証明書15件の出版完了 — 20/20 blob照合・claim closed

前回sessionでfile_system実行環境の障害（Koyeb 503/DNS、2026-11-14T22:54Z〜）により3/19で中断していたcost-74d WIN7証明書の出版列を、環境復旧後に完遂した。

## 復旧sessionでの再抽出（全件byte-identical）

repo-verbatim pipeline（`class4_child1_cert_extractor_exact.ts` FBS=1<<20・default KILL_BIT7 kill table・`legal_candidates.py`・LC_ALL=C sort -u・header 2行、scriptsは全7件ともmainのgit blob shaと照合済み）で、pending 10 bits（69/80/92/100/2/28/102/109/112/116）を1件ずつ再抽出した。**全件、障害前のinterim目録（`class2-lane-cost74d-certificate-hash-inventory-20261115.json`）のmd5/sha256/git blob shaにbyte-exact一致**。キャリブレーションとして既公開のbit118も再抽出し公開版と完全一致、bit12/66/68/91も再抽出し全15 bitsで一致した。

- **bit102は単一プロセス再抽出で同一74,238行・29,752,097節点**（障害前の2分割の和と一致）
- **bit80の正確なextraction_nodesは13,115,852**（interim目録の「〜9.417M pending」は部分ログ由来の誤りと判明、マニフェストで訂正記載）

## 二重独立検証 15/15 PASS

復旧sessionで全15証明書に二重独立検証を再実行: BigInt検証器（`verify_win7_certificate_bigint_independent.mjs`、3x3余因子展開・engine非依存）**15/15 PASS**、Number Bareiss検証器（`verify_bit7_win7_cert.ts --consumed-out`）**15/15 PASS**（sub-roots = 敵合法初手数と全件一致・consumed union missing/extra 0/0・終局石数 [13,17]・行sorted-unique）。

## 出版 — 20/20 remote blob照合

16ファイルを(4/19)..(19/19)の1コミット1ファイルでpushし（bit69→bit116）、remote 20ファイル全てのgit blob shaをローカル目録と照合（**20/20 byte-exact**）。bit91はcost-72b bit85のD4重複（canonical `00000000000080811202000020000000`、変換 index 5）のため本文はpushせず、既公開の証明書（blob `c99ef87964f4770e7dab365ea42ad070b8c6495d`）で裏付けた（repo precedent: cost61d bit22 = cost71b bit1）。

**最終マニフェスト** `class2-lane-cost74d-win7-certificates-20261115.json`（32,772 bytes、blob `0f6e7860796b999c6ab3b41d43931881085ad09f`、commit `5d37fab7`）: 15/15 WIN7 bits certified、計723,630行・sub-roots 883・visited 1,541,140・terminal 250,132・edges 1,380,013・extraction nodes 186,044,401。claim `class2-lane-cost74d-inflight-20261115.json` をcompletedに更新（commit `7cae50e3`）。

## 障害の実録

- push実行プログラムが16 MiB sandbox memory limitでpush_files実行**後**に中断することが6回（bit69/80/92/100/102 part1/part2）あったが、いずれもremote着地をblob sha照合してから次に進めた。欠損・ truncationなし
- four-six-row lane（並走）とのfast-forward競合2回は同一内容retryで解決、「Reference cannot be updated」もretryで解決
- read_file pagingとpushを同一ブロックで行うとmemory限界に近づくため、push後は必ずremote listingのblob shaで着地検証する運用を確立

## 意味と残作業

証明書出版は74d sweepの15 WIN7 rootのreceipt被覆の裏付けを強化するものであり、frontier計数は不変（74d fold 1,163→1,179、cost-72b fold→1,188はraw sweep receiptとして既にchain headに織り込み済み）。**証明書は各7石rootの深さ10以内の先手勝ちのみを証明する**。次の未claim最安子はcost-74第二子 `00000000000000809142000000000000`。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4はいずれも引き続きUNKNOWN。**

成果物: [最終マニフェスト](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-win7-certificates-20261115.json)、[interim目録](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-certificate-hash-inventory-20261115.json)、[claim](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-inflight-20261115.json)、[sweep audit](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-sweep-audit-20261115.json)。証明書14本体は同output/`class2-lane-cost74d-certificates/`（bit91は`class2-lane-cost72b-certificates/bit85-root-00000000002000809102000002000000.cert`）。
