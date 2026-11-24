# Part CP takeover 完了log: batch-30 (closure class 34269) drive-2 — 25/50キーで誠実打ち切り (インフラ二重故障・事前登録stop rulesによるhard-stop) (2026-11-24)

publish-then-execute規約どおり、takeover宣言
`research/log/2026-11-24-part-cp-takeover-batch30-drive2-declaration.md`
(commit `87e19b5a`・observed HEAD `4d70d1d1`・fetch-back byte一致 sha256
`722ed3cd…`) → A′ `1edab9ed` (session script + val-gate 4 sidecar) →
B checkpoint1 `dd660ce7` (ac005..ac021 34 pass + sidecar 1 + status.log 30行) →
B checkpoint2 `9f754b3d` (ac022..ac029 16 pass + racing sidecar 2 + status.log 44行) →
C `8e1a0b9b` (README + MANIFEST-sha256 139行) → 本完了log。
**verdict不消費・11×11 UNKNOWN担保不変**。

## 接管 (takeover) 正当化と継承 (要約・全文は宣言note)

Part CP drive-2宣言 `7aaa0525` (2026-11-23T21:56:11Z) 以降3時間30分以上
batch-30系commitなし → Part U/Z/CG/CI takeoverと同一基準で宣告session消失と判定。
kit全pin再検査 (jsreplay `84585617…`・runbatch `f591f8c2…`・make_batch30_keys
`61fab4f7…`・drive1_local_step v2 `e7b627a8…`・batch-keys `79fbd166…`・
MANIFEST 72エントリ fetch検証 fail=0・drive-1 outputs 9件pin表完全一致) のうえ
takeover。原drive-2宣言の未出版session script (`95c3f15b…`は継承不能) を
published v2からの最小delta (WIN-HALT wave論理3箇所除去のみ) で再作成し
`466f475fc16c810882100a4c2291787cb77da7b6a74a18c2a646a14ef5d899c9` を宣言で
事前登録 (A′ commitで出版・fetch-back照合済)。

## 実行protocolの実績

1. **takeover-host val-gate fresh 4** (宣言後・2回実施): at2m 2キー
   (result 0・nodes 2,000,000 x2)・first-15m 3,651,923・second-15m 5,040,200。
   published baselines 4/4 node-exact (wall_s比較外)・`# replay_done` x4。
   なお at2m-1188950…とsecond-15m…の2 sidecarはpublished baselineと
   byte-identical (sha `eeafe3ac…`/`91dffdec…`)。不一致ならhard-stopは不発火。
2. **drive-2 waves**: runbatch直起動・2キー x 2 worker・inner timeout 260
   (外側290s)。TRUNCATED-RETRYはrunner guardが次invocationで回収
   (ac006 p2で1回・設計どおり)。

## 成果 (drive-2新規probe 25キー・batch-30全体では29/54キーprobed)

すべて2-pass fresh-cold・budget 15M・status.log append-only 44行
(drive-1分9行 (重複2行含む) + drive-2分35行)・clean 23キーはp1/p2 node-exact (`# replay_done`全pass付き):

- **WIN 3** (drive-2新規・honest label・verdict不消費): ac020 9,765,071 /
  ac026 3,036,572 / ac027 2,593,751。3キーともWIN-HALT行とPASS行の
  2行ペイロードで記録 (WIN-CONTINUE設計どおりwave継続)。
  batch-30全体のWINは5 (drive-1のac002 10,752,246 / ac003 8,036,766込み)。
- **LOSS 18** (drive-2新規clean・honest label):
  ac005 7,941,333 / ac007 6,320,372 / ac008 3,722,379 / ac009 14,494,291 /
  ac010 4,730,437 / ac011 3,413,023 / ac012 6,067,761 / ac014 8,535,077 /
  ac015 6,725,969 / ac016 3,000,128 / ac017 10,672,726 / ac018 6,927,463 /
  ac019 10,173,232 / ac021 9,916,865 / ac022 3,441,401 / ac023 8,979,741 /
  ac024 9,826,442 / ac025 3,428,856。
  (下記incident area 2キー ac028 5,087,946 / ac029 9,204,933 もLOSS label
  観測だがverdict不消費。drive-1のac001 5,635,468 / ac004 5,816,333込みで
  batch-30全体のLOSS labelは22。)
- **EXHAUSTED 2** (honest UNKNOWN・same-condition再probeなし):
  ac006 15,000,000 / ac013 15,000,000 (両pass nodes=15M一致)。
- **残25キー ac030..ac054 はfileless UNPROBEDのまま** (UNKNOWN・drive-3は別宣言)。

## 誠実記録 (incidents — 両方とも実験事実として出版)

1. **実行環境リセット (1回目・01:26Z頃)**: 3-wave連続loop実行がbash外側300s
   上限を超過し環境リセット・ローカル作業dir全損 (01:32-01:35Z時点で
   `/home/user/kr-exec`不在を機械確認)。**published証拠 (宣言 `87e19b5a`)
   だけが証拠の設計が実働**: commit-pinned raw fetchでkit 78 file復元・
   MANIFEST検証 fail=0・drive-1 9件pin再照合・val-gate fresh 4再実施
   (4/4 node-exact)・drive-2をac005からやり直した。失われた労働は
   ac005/ac006の2キー分のみ (再実行で同一値を確認: ac005 7,941,333 /
   ac006 15,000,000 [リセット前のローカル観測と一致])。
   **知見: 1 bash invocation = 1 wave厳守 (外側290sとinner 260sの設計どおり)**。
2. **Koyeb remote command失敗 → 孤児プロセス競合 (2回目・02:15-02:19Z)**:
   wave invocation中にインフラ応答失敗 ("Failed to execute Koyeb remote
   command"・command実行はremote側で継続)。retry側の新invocationと、
   存続していた孤児step/worker群が同一pass file (ac028/ac029計4 file) に
   競合書込み。status.log時系列: 02:16:52 TRUNCATED-RETRY x2 → 02:17:46
   `ac028 MISMATCH p1=15000000,2,5087946 p2=` (p2空) → 02:18:19 `ac028 PASS` →
   02:19:25 `ac029 MISMATCH p1=15000000,2,9204933 p2=` → 02:19:34 `ac029 PASS`。
   **機械判定**: (a) MISMATCH 2行はp2側が空欄 (= mid-write読取) であり
   値レベルのdeterminism divergenceではない (真のdivergenceは両側完全値で
   なければ論理上成立しない)・(b) 節点数は独立3書き込みで完全一致
   (ac028: p1/p2/sidecar 5,087,946・ac029: p1/p2/sidecar 9,204,933)・
   (c) 最終4 fileはcomplete pair (replay_done付・p1/p2 field一致) だが
   書込み環境が競合下にあったため**ac028/ac029を「incident area」**
   (verdict不消費) とする。sidecar 2件
   (`ac028.p2.truncated.021652.out` 312B / `ac029.p1.truncated.021652.out` 314B)
   はrename時点でmid-writeだったファイルにwriterが完了書込みした結果の
   complete pass (同一値) として保存・出版。
   **知見: インフラ失敗時はremote孤児プロセス存続を仮定し、同一workdir対して
   retry前にliveness確認 (proc/cmdline走査) が必要。session scriptへの
   flock化はdrive-3宣言の候補改善事項。**
3. **打ち切り判断**: pinned orchestrationの `grep MISMATCH` pre-checkが
   状態としてdrive継続を阻止。事前登録stop rules (MISMATCH rc=42 hard-stop)
   の意味論は変更不能であり、「pushの競合・同時書き込み・取得失敗が起きた際は
   無理に押し進めず記録して次回に回す」規約により、25/50キーで誠実打ち切り。
   runner直起動による継続も「stop rules不変」の精神に反するため行わなかった。

## 出版 (全fetch-back byte一致検証)

- A′ `1edab9ed` 5 file (script + val-gate sidecar 4) — script sha宣言値と
  fetch-back一致。
- B checkpoint1 `dd660ce7` 36 file (ac005..ac021 34 pass・sidecar 1
  `ac006.p2.truncated.014532.out`・status.log 30行) — 41 file照合 fail=0。
- B checkpoint2 `9f754b3d`: ac022..ac029 16 pass・racing sidecar 2・
  status.log 44行。commit-pinned fetch-back 19/19 byte一致 fail=0。
  (1回目のpushは並走commitとのfast-forward競合で失敗・最新main再取得後の
  再pushで解消・データ影響なし。)
- C `8e1a0b9b`: README drive-2節追記+成果/verdict文言修正 (旧README
  `94bf0517…` prefix無傷・出版README sha `544407f5…`)・MANIFEST-sha256
  拡張 72→139行 (drive-2 kit/outputs全行・README行は出版後shaに更新・
  全体sha `2b36d896…`・fetch-back byte一致)。
- 完了log: 本file (research/log/2026-11-24-part-cp-takeover-batch30-drive2.md)。

## レジューム (次回の着手前に必ず最新main再取得・hourly並走注意)

1. **batch-30 drive-3 (残25キー ac030..ac054)**: 別の単一オーナー宣言。
   宣言時に必要な事前登録: (a) status.logのMISMATCH 2行・TRUNCATED-RETRY
   2行のincident index化 (real divergenceでないことの機械根拠は本log§誠実記録2)・
   (b) ac028/ac029の扱い (現complete pairを採用するか fresh再probeするか)・
   (c) session script v3 (flock導入・MISMATCH pre-checkのincident-aware化)
   のsha事前登録。停止条件・budget 15M・2-pass fresh-coldは不変。
2. batch-29 (class 2251) は並走 (Part CI takeover drive-2完成 `140cf80c`) で
   54キーprobe完 (LOSS 53 + WIN 1 (ab028)・EXHAUSTED 0)。次候補:
   batch-29のLOSS 37行adoption (CU先例・scrutiny C++ `9193f5b6…` 通過後・
   pinned merger `90711961…`)・row-audit・ab028 WIN行はPart CZ
   (`161373f9` scaffold) が第三実装交叉検証中。
3. batch-31 (class 5804・Part CY `81bdf46a` 完了) の続き・batch-30全キー
   probe完了後のrow-audit (Part CV先例) は各別レーン。
4. **UNKNOWN担保 (不変)**: 標準11×11空盤・19 central-reply roots・二石root
   {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 10968・class 23964・
   class 5343・class 2251・**class 34269 (batch-30 54キーすべて・EXHAUSTED・
   incident areaキーを含む)**・class 5804・class 34948はどの時点でもUNKNOWNのまま。
   nodes数・expansions数・wall秒数を勝敗として読まない。被覆・secured・
   root勝敗の主張をしない。WIN/LOSS採用は scrutiny owner C++ gate通過後の
   別adoption Part (merger `90711961…` 経由) のみ。
