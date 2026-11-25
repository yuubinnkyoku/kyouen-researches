# Part CH (2026-11-23): batch-28 (class 5343) 1-LOSS行 aa003 canonical adoption + re-audit — declaration, status, and note-loss incident disclosure

単一オーナー: n11中央応答レーン (Part CH継続セッション)。本logは Part CH の宣言・完了status・
note消失インシデントの開示を恒久記録するものである。

## 0. 要約

- Part CHは、Part CD (batch-28 drive-2) で出版された解決済み単一LOSS行 aa003 (s5 index 104943,
  nodes 4,070,373, 2-pass node-exact @budget 15M) のみを、Part BZ canonical cache (6,293行
  `9115be9e…`) に pinned byte-copy fail-closed union merger (`90711961…`) 経由で採用した
  (merged 6,294行 `3124461b…`, WIN 158 / LOSS 6,136)。採用パケットはloss-only 1行であり
  **full != loss**。WIN 4行 (aa001/aa002/aa006/aa007) は不採用 (verdict不消費)、
  EXHAUSTED 2行 (aa004/aa005) はhonest UNKNOWNのまま、fileless 47キー (aa008..aa054) は
  UNPROBEDのまま。
- class 5343 unknown_now 54→53 (rank 27→19。rank 19..26 の8クラス
  {5687, 12643, 31600, 10968, 23964, 25835, 30565, 5690} の+1シフトは純粋なranking churn、
  closure table membership 不変 left=[]/entered=[])。flips=[]・newly_free=[]・
  free_now 38→38・update8 resolved 133→134 (新規解決集合=={104943}のみ)・joint greedy
  38,295不変・probe worklist 64,747→64,746・per-root free/uncovered不変
  (root 27 baseline 119/119含む)・individual greedy union movers roots {4, 49}。
- 実験dir 14ファイル (README + MANIFEST-sha256含む) はmain出版済み。最終commit `387419b4`
  (E2) pinned HEADでのfetch-back 14/14 byte一致 (2026-11-23 継続セッションで実施)、
  README/MANIFEST-sha256もbyte同一を確認。
- tamper battery 12/12検出 + post-restore green (pin層・semantic層・manifest unpinned gate、
  実効性assert込み、extractor独立2-pass raw mismatch表示含む)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・
  class 10968・class 23964・class 5343 (54キーすべて・aa001..aa007を含む) は本Partの実行・出版の
  どの時点でもUNKNOWNのまま。** nodes数はbookkeepingであり勝敗ではない。WIN採用は引き続き
  scrutiny owner C++第二実装 gate (`9193f5b6…`) のみ (本レーンは代行しない)。本Partは
  loss-only 1行のcanonical adoptionであり、class 5343の閉鎖・root被覆・securedの主張を
  一切しない。unconsumed closure WIN候補は33キーのまま (aa006=32番目, aa007=33番目が追加済み)。

## 1. 出版commit一覧 (すべてmain・fetch-back byte検証済み)

| Part | commit | 内容 |
| --- | --- | --- |
| 宣言 | `72f403f8` | note amendmentコミット (コミットメッセージに宣言全文を含む。ただしREADME自体は未反映 — §3参照) |
| A | `894d6fd9` | scripts 4: make_increments_b28loss1.py `1a79f5a6…` + s5_union_merge.py `90711961…` (Part BZ正本・変更なし) + compare_deltas_b28loss1_adoption.py `86fbc570…` + reaudit/scripts/refresh_adoption_b28loss1.py `729ef020…` |
| B | `0c511f40` | increment `dc857bfd…` (1行) + increments-manifest `017c7c30…` (schema `b28loss1-increments-manifest-v1`, full_packet_eq_loss_only=false) + merge-audit run1/2/3 `5e8d6909…` ×3 byte一致 |
| C | `ae766957` | merged cache 6,294行 `3124461b…` (WIN 158 / LOSS 6,136; BASE 9115be9e 6,293行 + aa003のみ; fnv gate 0e0a266a / 259,574 bytes) |
| D | `b75823dd` | reaudit 3出力: refresh-summary `76cad2a1…` / closure-classes `baa2db13…` / per-root-coverage `75e59441…` (probe-worklistはregenerateするが「not published by design」により未出版) + decomp-deltas `975a9cc6…` |
| E | `41310db2` | README + MANIFEST-sha256 (14ファイルpinned) |
| E2 | `387419b4` | MANIFEST-sha256内increments-manifest sha pin手転写ミス修正 (`ae79952`→`ae97952` 2文字転置。直前fetch-back `sha256sum -c` が検出、BZ typo-fix先例に準じ開示。実ファイルは不変、正しいsha `017c7c30…ae97952225aaa71`) |

実験dir: `research/experiments/n11-centralreply-class5343-loss1-adoption-reaudit-20261123/` (14 files)
E2 pinned HEAD `387419b4` での最終fetch-back: 14/14 sha OK・README/MANIFEST byte同一 (2026-11-23)。

## 2. 宣言原文 (publish-then-execute)

Part CH宣言は元来 note (research/knowledge/README.md) amendmentとして出版する設計だったが
(下記§3のとおりそのpushは失敗)、宣言本文はコミット `72f403f8` のメッセージと本セッションの
ローカル正本に完全に保存されており、以下に原文を恒久化する。

> ### Part CH 宣言 (2026-11-23): batch-28 (class 5343) 1-LOSS行 aa003 canonical adoption + re-audit — publish-then-execute
>
> (observed HEAD-before-push: 336481d230aa082078cb2e8cae4318f3aa8edfd3 →
> push直前に最新mainを再取得しコミットメッセージにHEADを記録する。push直前にnote
> blob sha1ロック 7dbd917a6b392e19949f36aa8d2672651dcb4f0a (620,004 bytes版・Part CG
> 宣言適用済み) を再照合・fail-closedで更新する。対抗宣言なし (note内 Part CH /
> batch-28 adoption / b28loss1 記述ゼロを機械grepで確認済み)。実験dir
> `research/experiments/n11-centralreply-class5343-loss1-adoption-reaudit-20261123/` は
> push直前に404を再確認済み。)
>
> - **目的**: Part CD (batch-28 drive-2・class 5343) でpublishされた解決済み単一
>   LOSS行 aa003 (key `(1152921504741064704, 4228)`, s5 index 104943, result 2,
>   nodes 4,070,373, 2-pass node-exact @budget 15M) のみを、Part BZ canonical
>   cache (6,293行 `9115be9e…`) に pinned byte-copy fail-closed union merger
>   (`90711961…`) 経由で採用する。採用パケットはloss-only 1行であり
>   **full != loss**: 同batchの WIN 4行 (aa001/aa002 はPart CC第三実装交叉検証済み・
>   aa006/aa007 はPart CG交叉検証レーン宣言済み) はhonest labelのまま不採用
>   (verdict不消費・scrutiny owner C++第二実装 gate pin `9193f5b6…` が唯一のWIN
>   採用ルート・batch-14residual q042 / batch-26 l028 先例)、EXHAUSTED 2行
>   (aa004/aa005・result 0 nodes==budget 15M) はhonest UNKNOWNのまま、fileless
>   47キー (aa008..aa054) はUNPROBEDのまま。閉鎖・被覆・secured・root勝敗の主張を
>   しない。
> - **正直開示 (protocol偏移)**: 本セッションはdry-run準備から開始したため、
>   本amendmentの出版前にadopted packet・gate定数・期待機械簿記の導出を本hostで
>   実施済みである。publish-then-executeの実質 (スコープの事前固定・事後の
>   cherry-pick不可能性) は、本宣言に固定する (a) 実験dir構成、(b) 入力sha pin群、
>   (c) 採用行 (aa003単行) と不採用集合 (WIN 4・EXHAUSTED 2・fileless 47)、
>   (d) 期待機械簿記 (下記) のすべてを事前登録することで担保する。出版される
>   outputsはこれら宣言値とのbyte一致をfetch-back照合で機械検証する。宣言後に
>   実行するのは、(A)-(E)出版とnote status updateである。
> - **入力 (全件byte-pin)**: published batch-28 drive-2 kit 96ファイル (dir
>   MANIFEST-sha256.txt `2811b577…`), status.log `343097c2…` (17行),
>   row-audit-winhalt.json `3e86a32b…` (probed 7 = WIN 4 + LOSS 1 + EXHAUSTED 2
>   + fileless 47), BASE cache 6,293行 `9115be9e…`, Part BZ reaudit outputs
>   (refresh-summary `fca242cc…`, closure-classes.csv `14fc37c3…`,
>   per-root-coverage.csv `4218a6b4…`), pinned merger `s5_union_merge.py`
>   `90711961…` (Part BZ正本・変更なし), dependency-graph.json.gz `54f9c364…`,
>   repaired-joint-plan-update8.json `b658290a…`, independent.py `954d3a10…`,
>   s5_evidence_policy.py `78655e94…`, quarantine `81d23160…`。
> - **実行protocol (本セッションで機械実施済み・出版は宣言後)**:
>   (1) maker `make_increments_b28loss1.py` (kit 96/96 sha検証・status.log 17行
>   構造gate (WIN-HALT 4ペア+EXHAUSTED 2ペア+TRUNCATED-RETRY 4行 sidecar
>   absence gate)・aa003 2-pass node-exact・WIN 4行/EXHAUSTED 2行の
>   NOT-emitted gate・zero BASE overlap・quarantine 0) → increment 1行
>   `dc857bfd…` + manifest `017c7c30…` (schema `b28loss1-increments-manifest-v1`・
>   `full_packet_eq_loss_only` false)。x4 byte-stable。
>   (2) merger selftest PASS → BASE+increment merge x3 byte一致 (merge-audit
>   run1/2/3同一 `5e8d6909…`) → merged 6,294行 `3124461b…` (WIN 158 /
>   LOSS 6,136)。
>   (3) refresh `refresh_adoption_b28loss1.py` (Part BZ版 `0677e6eb…` からのdeltaは
>   CACHE path・CACHE_SHA_EXPECTED・docstringのみ) x3 + 隔離実行 (env -i・別tree)
>   byte一致 → refresh-summary `76cad2a1…` / closure-classes `baa2db13…` /
>   per-root-coverage `75e59441…` (+ probe-worklistはregenerateするが「worklist
>   not published by design」(BZ先例) により出版しない)。
>   (4) extractor `compare_deltas_b28loss1_adoption.py` (Part BZ版 `a3adc0da…`
>   からのdeltaは1-batch/1-adopted-row/4-WIN/2-EXHAUSTED/0-fragment構造への適応
>   のみ・gate logic設計はBZ先例継承・11 sha pin + manifest semantic gates +
>   probed 7キー独立2-pass再検証 + closure churn rank機械宣言 CHURN_RANK_EXPECT +
>   update8 delta=={104943} gate込み) x4 + 隔離実行 byte一致 →
>   decomp-deltas `975a9cc6…`。
> - **期待機械簿記 (事前登録)**: class 5343 unknown_now 54→53 (rank 27→19・
>   rank 19..26クラス {5687, 12643, 31600, 10968, 23964, 25835, 30565, 5690} の
>   +1シフトは純粋なranking bookkeeping。closure table membershipは不変
>   left=[]/entered=[]・anchor 23101/1849 (unknown_now 1/1) rank不変)・
>   excluded_now flips=[]・newly_free=[] (loss-only 1行はBASE未知コスト子全解決
>   クラスのみfree化しうるが該当なし・**class 5343はWIN 4行不採用+EXHAUSTED 2行
>   +fileless 47キーが残るためfree化しない**)・free_now 38→38・update8 resolved
>   133→134 (新規解決集合=={104943}のみ)・joint greedy 38,295不変・probe worklist
>   64,747→64,746・per-root free/uncovered不変 (root 27 baseline 119/119含む)・
>   individual greedy union movers roots {4, 49} (root 4: 5978→5977, root 49:
>   2811→2810)。
> - **tamper battery (scratch tree上・12/12検出 + restoration green)**: pin層
>   (increment sha / status.log sha (maker) / BASE cache sha / batch-keys sha /
>   raw tamper→maker kit MANIFEST sha gate) と、攻撃者がpin定数を書き換えた場合の
>   semantic層 (verdict反転 2→1→「non-LOSS verdict」gate・BASE append→
>   「scenario cache row count != BASE + 1」gate・batch-keys class_index反転→
>   row-audit picture disagreement gate・manifestはunpinnedのためWIN行nodes+1 /
>   full!=loss反転 / resolved_ids欠落がsemantic gateで直接検出・extractorの独立
>   2-pass raw mismatch表示を含む) の兩層を実効性assert込みで検証。battery後に
>   pristine restoreでmaker/extractorともgreen。
> - **出版 (宣言後・順次)**: A scripts → B outputs → C README + MANIFEST-sha256 →
>   note status update。全files commit-pinned raw URL fetch-back byte照合・
>   branch path URL (CDN stale) は使わない。
> - **不接触**: Part CG (batch-28 drive2win thirdimpl・並走所有) の実験dir・
>   outputs・進行、batch-28 drive-2 published dir (不変)・batch 1..27各published
>   dir (不変)、fast lane (y=23)・finite-field lane (K1254)・inversive/z19 lanes、
>   19root計画、unconsumed closure WIN候補33キーの採用状態、BASE cache
>   (`9115be9e…`) read-only不変 (merge先は新規別名cacheとしてのみ出版)。
> - **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
>   class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa001..aa007を
>   含む) は本Partの実行・出版のどの時点でもUNKNOWNのまま。** nodes数を勝敗として
>   読まない。WIN採用は引き続きscrutiny owner C++第二実装 gate (`9193f5b6…`) のみ
>   (本レーンは代行しない)。本Partはloss-only 1行のcanonical adoptionであり
>   class 5343の閉鎖・root被覆・securedの主張を一切しない。

## 3. note消失インシデントの正直開示 (2026-11-23 継続セッションで発見・確定)

Part CHは「note (research/knowledge/README.md) への宣言追記 + status update」を出版形態と
していたが、継続セッションでの検証により以下が確定した。

1. **宣言amend pushは実質失敗していた**: コミット `72f403f8` (「note: Part CH
   declaration… amended note fnv1a32: 82fcff16 (627,945 bytes…)」) のコミットにおける
   `research/knowledge/README.md` は、親コミット `ffbd5b7c` のREADME (943,542 bytes) と
   byte同一 (`cmp` で一致) であり、宣言追記は反映されていなかった。amend版noteのblob
   `cb44122e…` はrepoのgit objectに存在しない (blobs API HTTP 404)。fnv1a32等のローカル
   検証は「ローカル実体」に対してはpassしていたが、pushされたGitHub側実体のfetch-back
   byte照合が宣言內で「to follow」とされたまま未実施であり、失敗を検出できなかった。
   宣言本文はコミットメッセージ全文として保存されていたため失われていない (§2で恒久化)。
2. **旧中央レーンnote史はmainから消失**: Part AM〜CG (2026-11-22〜23) の宣言・status
   全体を含むnote (blob `7dbd917a6b392e19949f36aa8d2672651dcb4f0a`, 620,004 bytes,
   8,256行) は、Part CH宣言前の時点で既にmainのREADMEから失われていた。現main README
   (946,801 bytes・469行・「items/Knnnnが正本」形式) との行集合共通は1行のみ
   (sort+comm による機械比較)。READMEは内容置換型push (create_or_update_file系は
   content全体置換) により並走fast lane系の版に置換されていた。
3. **git objectとして旧noteは保全**: blob `7dbd917a…` はblobs APIでbyte正確に取得可能
   (620,004 bytes, ローカルsha1再計算一致)。
   `curl -H "Accept: application/vnd.github.raw" https://api.github.com/repos/yuubinnkyoku/kyouen-researches/git/blobs/7dbd917a6b392e19949f36aa8d2672651dcb4f0a`
   で誰でも復元・検証できる。Part AM〜CGの実験成果自体は各実験dir・knowledge items・
   コミットメッセージに失われていない。
4. **repo方針との整合**: 現行AGENTS.mdは「research/knowledge/items/ が現在の知識の唯一の
   正本」「root README.mdは生成領域であり直接編集しない」「古いREADME・log・archiveの記述
   よりitems/を優先」を定めており、note追記は廃止された運用だった。よって宣言とstatusは
   このlog file (出典として残す) に恒久化し、READMEへの再追記は行わない。対抗宣言検索は
   本log出版前に「Part CH status / b28loss1完了」記述がmain knowledge・logに存在しない
   ことをgrep群で確認済み。

## 4. 実行環境の制約 (再現性のための正直な記録)

- 本セッションはgitなし環境である。GitHub操作は GitHub contents API (create_or_update_file /
  push_files相当) + raw URL fetch-back で行う。push後のfetch-back byte照合が唯一の最終
  検証手段であり、今回Part CHでそれを怠ったことが§3-1の検出漏れの直接原因である。以後
  note改変を含む出版は必ずpush直後にfetch-back byte照合を行う。
- ローカルの作業tree `/home/user/kr-exec/repotree/` は非gitの部分再構築であり、真のrepo
  状態はGitHub側から再取得すること。
- sandboxメモリ制限 (16MiB) 下での巨大ファイルの取り扱いは、file chunked read +
  自作UTF-8エンコード→FNV-1a32 (js/python両側照合) で行う (push_files引数組み立て時の
  実体取り違えリスクは§3-1の例で実証されたため、push直前のローカル実体sha再計算と
  push直後のfetch-back sha照合を必須とする)。

## 5. 次回候補 (Part CH以降)

1. batch-29選定はreaudit再実行後 (rank 35 class 2251・rank 36 class 34269が
   zero-collision clean候補)。
2. Part CG (batch-28 drive-2win thirdimpl・並走所有) の完成待ち・status回収。
3. batch-23 fileless 51キー、batch-24 fileless 49キーの将来probeは別宣言が必要。
4. aa006/aa007の第三実装交叉検証はPart CGが宣言済みのため非接触。
5. note消失インシデントの影響調査: 旧note (blob `7dbd917a`) に記録されたPart AM〜CGの
   うち、READMEだけでなく実験dirにも欠けている成果がないかの棚卸しは各Partの出版
   コミットとの照合で実施可能 (現時点ではPart BZ/CC/CD等の主要成果は実験dir + MANIFESTで
   fetch-back確認済み)。

## 6. UNKNOWN担保 (最終)

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa001..aa007を含む) は
2026-11-23 Part CH完了時点でUNKNOWNのまま。class 5343はWIN 4行 unconsumed +
EXHAUSTED 2行 + fileless 47キーが残るため閉じない。unconsumed closure WIN候補は
33キー。nodes数はbookkeepingであり勝敗ではない。
