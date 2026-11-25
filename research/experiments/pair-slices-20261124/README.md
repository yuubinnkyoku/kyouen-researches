# pair-slices-20261124 実験キット（K1285・publish-then-execute）

単一オーナー宣言ノート:
`research/log/2026-11-24-pair-slices-pure-c1-ladders-single-owner-note.md`
（定理・証明全文・open 登録・honest 記録の正本）。

## 内容

- `verify_k1285.py`: 公式機体。D1–D10 バッテリ（9,794 点）。engine block は
  K1138/K1282/K1283/K1284 連鎖の公開 block を verbatim 同梱、起動時に
  sha256 ゲート（pin = K1283/K1284 と同一）。stdout は決定的（byte-identical
  保証・揮発性情報は stderr のみ）。TAMPER: `--tamper-engine` (rc 2)・
  `--tamper=zz0|zz1|zz2|lad|alm|fl|pb` (rc 1)。
- `engine_block.py`: 上記 block の単体ファイル（バイト同一・参照用）。
- `explore_k1285.py` / `explore_k1285.out`: 宣言前探索（E1–E6）の再現
  スクリプトと出力。k スライス族の発見表・J-family・pre-band 単層則・
  境界三角形・multi-c web 試行と z2-band blocker・広域確認。
- `output/dryrun*.out/.info`: 宣言前 alive-run（json・sha 記録用）。
- 公式監査成果物（公式 4 走後に追加出版）: `output/audit_run1-4.json`、
  `detcheck.json`、`MANIFEST-sha256`。

## main claim（機体は照合のみ・証明はノート）

- **T-PS0/1/2**: ペア対角スライス族。k := R − 2m − g に対し
  z0 k∈{1,2,3}・z1 k∈{2,3}・z2 k∈{3,4} で
  H(2m+g+k; (m, m+g); z) = [g odd]（全 m>=1, g>=1）。
- **T-L1/L2/L3**: pure-c1 ラダー。H(2m+d+2; (m,m+d); 0) =
  H(2m+d+3; …; 1) = H(2m+d+4; …; 2) = [d odd]（全 d, m）。d=1 の z1 行は
  K1284 open 登録 C-PC1z1-d4 の c=1 半分の全称解決。
- **T-ALM**: allm-2 族の 6 床 = 0。
- **C-PB2 / C-PC**: pre-band 単層族（既刊 T-B1′/T-B0′ 帯崩壊の直接实例）。
