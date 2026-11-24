# raxis-band-z01-20261124 — 低z (z∈{0,1}) R-axis 帯全域+対角崩壊と前線分類（K1281 仮採番）

単一オーナー宣言 `research/log/2026-11-24-raxis-band-z01-single-owner-note.md`
（publish-then-execute）に対応する実験キット。主張の区分は宣言ノート §1
のとおり:

- **仮説 H1/H2（observed・open）**: z0-δ2 arm-1 法則・z1-δ2 mixed 則。
- **定理 T-B0/T-B1（proved【H1/H2 の含意】）**: z0/z1 両面の
  帯+対角崩壊（z0: R∈[m+1,2m]・z1: R∈[m+2,2m]）と前線分類
  （R=2m+1）。証明全文は宣言ノート §2。
- 観測記録（主張しない）: LAW-C 全文・δ3/δ4 現象・z=2 帯プローブ・
  m=2 z0 前線（K1278 D9 と整合）。

## ファイル

- `verify_raxis_band_z01.py` — 公式検証機。engine block は published pin
  `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
  を byte 埋め込み・sha ゲート内蔵。電池 D1-D8（宣言点数
  91,020・内訳は宣言ノート §4）。stdout の audit JSON は決定的（時刻等
  の volatile 情報は stderr のみ）。
- `engine_block.py` —検証機に埋め込まれた engine block の単体ファイル
  （byte 一致・sha256 = pin）。
- `exploration/` — 宣言前探査一式（explore1: z0 帯生値・explore2:
  z0 前線分類・explore3: δ 行観測・explore4: δ2 則原型・explore5:
  表構築・explore6: 広域 census（H2・帯崩壊・LAW-C 分類表）・
  explore7: LAW-C 検証。explore*.py は pin sha-gate assert つき）。
- `output/dryrun*.json|info` — dry run 3 本（dryrun1: D8 bad=2 修正前・
  dryrun2: 全 green 旧形式・dryrun3: 全 green・決定性形式の確定盤）。
- `output/audit*.json` — 公式 4 走（同一 cwd×2 + 隔離 tree/env×2。
  受入条件: 4 走とも stdout byte-identical・sha256
  `c64639c24f2f226164466bbe430d7f5a640c09cbdc06d427c273f3a63489ad40`）。
- `output/tamper*.txt|json` — 変異電池 3 本（--tamper-engine → rc2・
  --tamper=lawc → rc1 D2 bad=5,873・--tamper=lawc-allm → rc1 D2
  bad=56）。
- `MANIFEST-sha256` — 最終状態の全ファイル digest。

## 実行方法

```
python3 verify_raxis_band_z01.py            # 公式走 (rc=0, stdout=audit)
python3 verify_raxis_band_z01.py --tamper-engine   # rc=2 想定
python3 verify_raxis_band_z01.py --tamper=lawc     # rc=1 想定 (D2 bad>=1)
python3 verify_raxis_band_z01.py --tamper=lawc-allm # rc=1 想定
```

## 規約

- 11×11 空盤等の標準課題は **UNKNOWN 維持**（検証点数を勝敗として
  読まない）。z10/z11 ストリップレーン（K1279/K1280）は非接触。
- H1/H2 は有限 census 観測。定理は含意としてのみ主張。有限 grid を
  全称として読まない。
