# border-slices-20261124 実験キット（K1286・publish-then-execute）

単一オーナー宣言ノート:
`research/log/2026-11-24-border-slices-prediag-single-owner-note.md`
（定理・証明全文・open 登録・honest 記録の正本）。

## 内容

- `verify_k1286.py`: 公式機体。D1–D10 バッテリ（18,118 点）。engine block は
  K1138/K1282/K1283/K1284/K1285 連鎖の公開 block を verbatim 同梱、起動時に
  sha256 ゲート（pin = K1283/K1284/K1285 と同一）。stdout は決定的
  （byte-identical 保証・揮発性情報は stderr のみ）。TAMPER:
  `--tamper-engine` (rc 2)・`--tamper=f0|z1|z2|bed1|bed2` (rc 1)。
- `engine_block.py`: 上記 block の単体ファイル（バイト同一・参照用）。
- `explore_border.py` / `explore_border.out`: 宣言前探索（E1–E6）の再現
  スクリプトと出力。境界スライス census（有効 cell のみ・R<0 除外）・
  δ 崩壊候補の直接検証（5,585 cell mismatch 0）・床 census・
  Z1/Z2 法則表照合・F2 web census・z1/z2 pre-diag 核生成 census。
- `output/dryrun1-4.out/.info`: 宣言前 alive-run 4 走
  （PYTHONHASHSEED=random/1 同一 cwd ×2 + 隔離 tree env -i 99/7 ×2）。
  4 走とも stdout byte-identical
  （sha256 `ac7d104d8a70b69c37ae354d98048fcc07c69ca836cb482166c22ba1864967e9`）。
- 公式監査成果物（公式 4 走後に追加出版）: `output/audit_run1-4.out/.info`、
  tamper 記録、`detcheck.json`、`MANIFEST-sha256`。

## main claim（機体は照合のみ・証明はノート）

- **T-PD0**: z0 対角下バンド一次元崩壊則。δ := R − 2m に対し
  H(R; (m, m+g); 0) = f0(R−2m)（全 m>=1, g>=1, 0 <= R <= 2m+g）。
  f0(δ) = 2 (δ=1); [δ odd] (δ<=0); [δ even] (δ>=2)。値は **δ のみ**に
  依存し m・g を経由しない。
- **T-B0**: z0 床 b0(j) = f0(j)（j <= 0・m 非依存）。
- **T-Z1/T-Z2**: z1 境界スライス k∈{−1,0,1}・z2 境界スライス k∈{0,1,2}
  の全称確定（z2-k1 = [g odd] clean を含む）。
- **T-B1/T-B2**: z1 床（j∈{−1,0,1}）・z2 床（j∈{0,1,2}）の確定
  （b1(1)=0 は公刊前線の再掲・照合用）。
- **系**: K1285 OBS-D9 境界三角形 4 脚（z0-k0/z1-k1/z2-k2/z2-k1）の
  全称昇格 = **K1285 lane の未来課題 F1 を完了**。z1-k0/k(−1)・z2-k0 は
  新規確定領域。
- **D10 OBS**（全称主張なし）: F2 spread web F_d/G_d（d∈{1,2,3}）・
  z1-k(−2) 核生成行・z2-k(−1) m 非依存候補・z2-k(−2) パターン行。
