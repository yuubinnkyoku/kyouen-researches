# Part DF takeover 宣言: b28-win46 queue registry P2パッケージ8行 第三実装交叉検証の単一オーナーtakeover

- 2026-11-24T08:3xZ (takeover宣言時刻・commit timestampはGitHub側)・publish-then-execute
- 観測 HEAD-before-push: `2117ea737962d6c5ebdd4a690957e8725cba98ae` (2026-11-24T08:21:58Z・Part DK interim note)
- 原宣言: `59b6540f` (2026-11-24T05:01:52Z・Part DF batch-28 b28-win46 queue registry P2パッケージ8行
  第三実装交叉検証・publish-then-execute)

## takeover事由の機械確認

1. DF実験dir (`research/experiments/n11-centralreply-closure-b28p2win8-thirdimpl-20261124/`)
   へのcommitはscaffold A1 `2245e85e` (05:03:24Z) / A2 `26fc5352` (05:03:54Z) / A3 `50b5b430`
   (05:12:18Z) の3件のみで、outputs (D1-D9) は1件も出版されていない (list_commits path機械確認)。
2. DF scaffold検証log `4db1ffcb` (05:15:35Z) は「solver実行 (D1-D9) 未実施 (file_system持続障害)・
   次回はpublished scaffold 68ファイルからkit復元・sha検証の上、宣言protocol (`59b6540f`) どおり
   実行すること」と原オーナー自身が明記 (引き継ぎ指示)。
3. 最終DF系commit (05:15:35Z) から3時間超・原宣言 (05:01:52Z) から3.5h超の停滞。
   earliest_takeover = 2026-11-24T08:31:52Z を経過 (Part CI/CP/DA/CX takeoverと同一規約)。
4. 対抗takeover宣言なし (観測HEADまでのcommit列でDF/P2 scopeに触れる単一オーナー宣言・
   takeover文言なし・API機械確認時点)。

## kit復元とpin照合 (published evidenceだけが証拠の設計)

- A1/A2/A3 commit-pinned raw fetchで68ファイル (README 1 + scripts 7 + input 13 + sources 39 +
  val-gate 8) を復元し、原宣言ノートの64-hex pin群を**機械抽出** (手転写ゼロ) で照合:
  **44/45 byte一致** (raw 16・input/published-input 12・bf 4・top-level 11・val-gate full pin 1・
  kit scripts 5・rows.json)。
- 唯一の不一致は原宣言ノート内 `run_replica_df.sh` の64-hex pin (`73f09f38b3f53b4e77907a6867…`) が
  A1出版bytesの実測 sha256 `73f09f38b3f53b4ea1b695a557d9f9bc4bd44fb47e8adf97e965b27c469d4ec8`
  と char 17-32 のみ一致しない点。独立2経路 (commit-pinned raw fetch + GitHub contents APIの
  git-blob-sha1 `00384666814358c844c1ffc4d77ddb8d95e21f8d` 完全一致) でA1出版bytesの正本性を
  確認済み。kit README (A1出版) のpinは8-hex `73f09f38…` で実測と一致しており、**原宣言ノート本文の
  手転写誤り**と判定・誠実記録する (constant: sha転写は必ず機械経由・既存規約の再確認)。
  実行はgit-blob機械確認済みのA1出版bytesを正本とする。
- `audit_df.py` sha256 `7693466078f640b063a74879e7fc14ca5356aa5fd1a534cfddfd1c502479d656` =
  kit README pin `76934660…` 一致。`verify_tbl.js` `c8c52528…`・`third_impl.js` `08ea958f…`・
  `jsreplay.js` `84585617…`・`make_inputs_df.py` `a3c6e8e1…` 全て宣言pinとbyte一致。

## 実行

- 原宣言protocol D1-D9 を本sessionで実行する (D1 rules gateは `verify_tbl.js` が参照する
  jsreplay (`/home/user/knowledge/kyouen-research/_class1297036830122704896-lane-kit/inv/jsreplay.js`)
  をkit内 pinned byte-clone (sha256 `84585617…` 機械一致) で同pathに解決して実行)。
- いずれかの gate FAIL/MISMATCH → 停止・誠実記録・出版 (verdict不消費)。

## 非接触

- Part DK (batch-30 ac013 25M再probe・declaration `e411045b`・interim note `2117ea73`・活動中) /
  Part DL (batch-31 51-LOSS canonical adoption・declaration `00e17cda`・本観測時点で活動中) /
  Part DH (b28 P4パッケージ9行・declaration `f63c1654`・env outage `879ae475`・takeover window内)
  はいずれも本takeover scope (P2パッケージ8行・実験dir・queue registry rev4 bookkeeping) と非接触。

## 主張の限定

- verdict不消費: 対象8行 (aa014/aa049/aa051/aa019/aa013/aa020/aa010/aa040) は honest WIN labels
  のまま。adoption は scrutiny owner C++第二実装 gate `9193f5b6…` 通過後・pinned merger
  `90711961…` 経由の別adoption Part 専権。
- 閉鎖・被覆・secured・root勝敗の主張をしない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・
  class 5343 (54キーすべて・P2の8キー含む) は本takeoverの前後を通じてすべてUNKNOWNのまま。**
  nodes数・expansions数・ttHits数を勝敗や距離として読まない。
