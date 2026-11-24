# Part CY drive-2 incident amendment (2026-11-24): ad033/ad034 artifact-MISMATCH診断とdrive2b gate — publish-then-execute

単一オーナー: n11中央応答レーン (長期レーン・本セッション本host)。Part CY
drive-2 (宣言 `research/log/2026-11-24-part-cy-batch31-class5804-drive2-declaration.md`
・commit `21fef631`) の実行中に発生した MISMATCH 2行の診断結果と、その後の
運用修正 (drive2b) を正直開示する。**verdict不消費・11×11 UNKNOWN担保不変**。

## 1. インシデント時系列 (status.log・file群の機械再構成)

1. 02:16:0xZ: step invocation (ad033/ad034 dispatch) 開始直後に実行環境
   (Koyeb remote command) のインフラ障害が発生し、呼び出しは「filesystem changes
   not synchronized」でエラー返却。しかし workerプロセス群は実行を継続
   (zombie worker)。
2. 02:16:30Z: 再実行した step invocation が guard で zombieの書きかけ p1 を
   検出し `ad033/ad034 P1-TRUNCATED-RETRY` を記録・p1を fresh-cold再実行開始
   (sidecar `adNNN.p1.truncated.021630.out` に退避)。
3. 02:17:5x-02:18:0xZ: zombieの p1 passが完走しsidecar inode (rename先) に
   `# replay_done` を書いたのち zombieは p2 を開始 (`adNNN.p2.out` に header
   のみ書いた時点で稼働継続)。
4. 02:18:20/02:18:31Z: 再実行側 workerの fresh p1 が完走 (ad033 5,883,887 /
   ad034 4,885,748 nodes・いずれも result 2)。**p2存在チェックの時点で
   zombieが作成済みの headerのみの `adNNN.p2.out` が存在したため再実行側は
   p2を実行せず**、headerのみのファイルで p1==p2 比較 → `MISMATCH p1=… p2=`
   (p2 field 空) を記録して rc=42。
5. 02:18:36/02:18:51Z: zombie runbatch自身が完走した p2 と比較し
   `ad033/ad034 PASS` を記録して終了。以後プロセス残存なし (/proc 機械確認)。
6. 02:19:44Z: 診断後、pinned runner `runbatch.sh ad033 ad034` を再呼び出し
   (設計どおり完了pass skipping) し、両キー `PASS` を再記録。

## 2. 診断 (機械検証・全行為は正常動作)

- **非決定性の証拠はゼロ**: ad033/ad034とも、fresh p1・zombie p1 (sidecar)・
  zombie p2 の**3つの完了passが `replay,` 行 f6,7,8 (budget/result/nodes) 完全
  一致**:
  - ad033: 15000000,2,5883887 × 3
  - ad034: 15000000,2,4885748 × 3
- 2行の MISMATCH は「p2 fieldが空の行」= p2 passがまだ verdictを出していない
  時点の比較であり、**矛盾する2つのverdictが存在したわけではない**
  (truncated passはevidenceでないという pre-registered runner設計と同じ原理)。
- runbatch.sh の全guard (truncated retry・replay_done guard) は設計どおりに
  動作した。race window (guard時点で p2 fileが不存在 → 比較時点で存在) は
  インフラ障害が作った一時的な多重実行のみが生む条件であり、単一実行では
  生じない。

## 3. 運用修正 (drive2b_local_step.sh・publish-then-execute)

- `scripts/drive2b_local_step.sh` (sha256
  `4fcb5775b5b89b7b9411ebd3d39a8328335913f1bf4ebc558f8ac659a9857f77`):
  published `drive2_local_step.sh` (`8baf929b…`) からの最小delta。
  **pinned runner runbatch.sh は byte不変**。変更は2つの orchestration gateの
  MISMATCH検出を「genuine mismatch (p1・p2 両fieldに値あり)」に限定する
  ERE (`MISMATCH p1=[0-9,]+ p2=[0-9]`) のみ (start gate 1箇所 + end gate
  1箇所・計2行)。**runner自身は genuine mismatch 検出時に相変わらず即時
  per-key hard-stop (rc=42)** するため、fail-closed性は保全される。
  artifact行 (p2 field空) は status.log に append-only で残存し、本note・
  README・completion logで永続開示する。
- ad033/ad034の honest label は両キーとも **LOSS(2)** (3-pass一致・
  nodes 5,883,887 / 4,885,748)。MISMATCH行は artifact記録として扱い、
  verdict不消費の原則は不変。

## 4. UNKNOWN担保 (最優先・維持)

**標準11×11空盤・19 central-reply roots・二石root・S2・class 5804 (55キー
すべて) は本incidentの実行・出版のどの時点でもUNKNOWNのまま。** nodes数・
wall秒数を勝敗として読まない。
