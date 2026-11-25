# boundary-band-20261125 — 境界帯全多重度パッケージ機体（K1311）

publish-then-execute: 単一オーナー宣言ノート
`research/log/2026-11-25-boundary-band-single-owner-note.md` が先に出版
されており（`7653a639`）、本キットはその §4 機体宣言の実体。定理・証明・非主張の区別はすべて
宣言ノート参照（この README は重複正本としない）。

## 主張の要約（詳細は宣言ノート §1/§4.5）

- **T-DB（全称・全多重度）**: ∀ n≥2, z≥0, 降順 multiset X=(x1≥…≥xn≥1)
  境界行 k:=z+n−2, 過剰座標 E:=x1−Σ_{i≥2}x_i として
  **H(S+k; X; z) = D(E, k)**（D は公刊 K1308 Z-DIAG 3 分岐則・値 2 は E=k+1 直線上ちょうど）。
  値は x2..xn の個別値に非依存（単一座標 E）。n=2 インスタンス = 公刊 Z-DIAG/T-DU′（被包）。
- **L-SDB（導出・K0832 閉形式の 3 枝スライス）**: ∀ x≥1, z≥1: v(x,z,x+z−1)=D(x,z−1)
  （単一トークン境界行・T-DB の帰納 base）。
- **C1**: K0832 3 トークン過渡帯の頂行 k=z+1 を全確定し、**予想 B（κ=0 スライス R=2x−1・j=2 族
  の値 2）を E=z+2 部分族として全称証明**（予想 A/C は下帯で open のまま・O-BBL 登録）。
- **C2**: n 山面の k 軸 3 層フレーム（tail k≥z+n−1〔公刊 K0832 Lemma P 系・接続記録のみ〕/
  境界行 k=z+n−2〔本項〕/ 下帯 k≤z+n−3〔n=2 は公刊で確定済み・n≥3 は open〕）。
- 規約上: verdict 不消費・11×11 巨大探索への影響は literary（構造補題の接続は giant レーン
  オーナーの判断）。

## ファイル（sha256）

| file | sha256 |
|---|---|
| verify_k1311.py | `4b5b81de90a8c45da69d36d1903ed543f40212c1394afb999c16d22ff1f20b9b` |
| engine_block.py | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`（K1282..K1310 chain と同一 bytes） |
| explore_db.py | `5747cb9a4606ce2586af046fba2d1fdecef85c91a23f7b0b178ca59986a02331` |
| explore_db.out | `6b48b840089be97a837d03d9bfbc3623e4f83b61dd6db4b308806a6237bc37a5`（宣言前探索 X1–X5 の正本） |
| predry/dryrun1-4.out | 4 走とも `811d7ae3390ef43c94cc24f3ae5d77c32de179bc9336d468be49201997d44bdb`（byte-identical） |

埋込み engine block の起動 sha gate: pin
`bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
（verify_k1311.py 内蔵・不一致なら即時 abort）。

## 電池（宣言ノート §4・総計 12,409 点・期待 overall_bad = 0）

D1 L-SDB census（x≤20・z=1..12）240 / D2 n=2 境界アンカー（pairs+beds・z=0..10・a≤8・g≤20・
S≤28）1,628 / D3 triples 境界 census（z=0..10・S≤16 全掃引）1,353 / D4 n=4..7 census
（z≤6・heaps≤8）2,303 / D5 typed self-check（n=2..5・z≤6・heaps≤6・S≤15・申立+L-SDB 表のみで
子構成・mex==申立==engine 三点一致）1,659 / D6 cross-engine+申立（canonical vs ordered vs D・
n=2..4・z≤6）861 / D7 tail 行 k=z+n−1, z+n（公刊系転写・n=2..4・z≤4）1,390 / D8 far stress
（seed 1311/1312/1313・triples z7..14・quads z7..12・n=5..7 z7..9）1,200 / D9 K0832 予想B
interface（値 2 ⇔ E=z+2 の両含意・triples z0..8・S≤14）747 / D10 all-ones n=2..14×z0..10・
near-all-ones n=3..8・x2..8・z0..8 521 / D11 OBS-BBL 凍結表再現（triples k=z 行・z=1..7・
7 行照合）7 / D12 random multiset sweep（seed 1314・n=2..6・z=0..7）500。

## 変異電池（fail-closed・事前宣言）

- `--tamper-engine` → rc=2（変異 sha `0ea47a80…` ≠ pin）
- `--tamper=np1` → rc=1, bad 228 / `np2` → 1,540 / `np3` → 1,297 / `np4` → 2,295 /
  `ty` → 1,659 / `ce` → 838 / `tl` → 1,390 / `fs` → 1,199 / `kb` → 747 /
  `ao` → 512 / `ob` → 7 / `rs` → 490

## 公式監査（本キット出版後に fetch-back bytes から実行・成果物は output/ に追記出版）

1. fetch-back: 全ファイル size+sha256 byte 照合（API 側・全ファイル）
2. 公式 4 走: 同一 cwd ×2（PYTHONHASHSEED=random/1）+ 隔離 tree/env -i ×2
   （PYTHONHASHSEED=99/7）→ 全走 rc=0・stdout byte-identical
   （predry と同一 sha `811d7ae3…` を確認）・総計 12,409・overall_bad=0
3. 変異電池 13 種 → 上表 bad count・rc で全 fail-closed 確認
4. output/audit_run1-4.out/.info・tamper レコード・detcheck.json・MANIFEST-sha256 出版

## 規約

verdict 不消費・11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は全時点
UNKNOWN。engine は K1138 転写（sha pin 実装）・census は照合であって証明の代替ではない。
証明は宣言ノート §2（手証明全文）。
