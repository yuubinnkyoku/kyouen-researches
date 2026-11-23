# generalx-merge-frontier-reduction-20261123

一般Xマージ法則 (GX-M) の有限監査と frontier reduction 補題 (FR-X) の証明・
2トークン境界行閉形式則 (BSL) の大掃引。横断法則一般補題化レーンの第1成果。

- 単一オーナー宣言（実行前に出版）: research/log/2026-11-23-generalx-merge-frontier-reduction-single-owner-note.md（commit efe21bd3・宣言時点観測 HEAD cf3fbe4a・対抗宣言 grep clean・K1254 仮採番）
- 正本監査機: audit_frontier.py（SHA-256 6c275bfe3621eca48b53a43beb41850ec9f3b3b132c501fc779f3dd0ede88c28・31,761 bytes・9成分 CX/XB/M2/M2D/G3/G4/L4/E5/C8・fail-closed tamper 電池 --tamper 1..6 同梱）
- 監査正本: output/audit.json（SHA-256 206ab3ac51e481e5761aba5c65a9cba0fd65a4003c8cd42782e38497bc14a69b・overall_bad 0・総照合点 5,737,883）
- 転写検査: scripts/check_blocks.py（@@TRANSCRIPTION 3ブロックの byte SHA 照合・PASS）
- 定理と証明・各法則の正確な宣言: report.md
- 実行記録: output/published_run.txt

## 内容

1. **Theorem FR-X（proved・条件つき補題）**: トークン簡約で閉じた多重集合クラスで境界行 z=σ の前沿条件 F±X（有限・2σ+1 点）が成立すれば、マージ領域 z ≥ σ+1 全域で H(R;X;z) = ST(σ,R)。アリティ非依存・mex 3値表は全27ケース機械検証（C8）。族全領域検証（~700万点/族）が境界行パリティ検査に削減される。証明は report.md §2。
2. **GX-M（observed）**: 3/4/5トークンでも z ≥ σ+1 でマージ法則成立。G3 5,080点 96族 bad 0。3アリティ以上は初観測。
3. **F±X の 3/4/5トークン盤査（observed）**: G4 65族 1,237点 violation 0（FR-X の仮定が観測的に成立）。
4. **BSL（observed）**: 2トークン境界行の R* = x+2y+1+(x mod 2) 公式。b=s below R*、tail は R*-1 から、最初の乖離は R* ちょうど（(1,1) は例外・乖離窓がそもそも空）、窓 [R*, 2σ] に局限。M2D y=1..30 × x=y..y+12（390族・124,800照合）+ M2 生三点照合12族（y ∈ {20..30}）+ E5 証明済み閉形式 cand17/cand18 での 9,266 セル一致。
5. **マージ法則大掃引**: M2D 63,180点。y ≤ 20 は出版全称系の再導出（y=20 は出版 K1249 全称と独立な DP 再照合）、y=21..30 の130族が新規証拠。
6. **low-R 一般X縮約（observed）**: L4 5,984点。R ≤ z+1 で全アリティ単一トークン縮約。
7. **DP 列エンジン**: CX 6族全セル 5,567,472 点、出版生エンジンと不一致 0。

## 転写プロバイナンス（check_blocks で機械照合・PASS）

- 出版 y=18 全称検証器 verify_y18_universal.py（part2・全 file SHA-256 8ddd0c2f…・K1242 proved / K1245 実験dir）から:
  - engine ブロック（H_ordered/H_canonical/mex/single_token）2,022 bytes SHA-256 e5abe053…
  - cand17 ブロック（K1240 proved・single_token_val を含む）3,529 bytes SHA-256 44f1ce4e…
  - cand18 ブロック（K1242 proved）3,275 bytes SHA-256 caf13e80…

## 再実行

```
python3 audit_frontier.py --out output/audit.json          # ~3-4 min, rc=0
python3 audit_frontier.py --components C8                  # quick smoke
python3 audit_frontier.py --tamper 1 --components M2D,G3  # TAMPER-DETECTED rc=1
python3 scripts/check_blocks.py                           # PASS
```

決定性: audit.json は2実行（同一cwd + 隔離tree+PYTHONHASHSEED=random）+ サンドボックスフルリセット後の全再構築再実行の3実行で byte-identical（published_run.txt）。

## スコープ外

標準11×11空盤・二石root・S2・class 1/2/4 はすべて UNKNOWN のまま。固定幅・q点版安定化長、y族閉形式の fit/全称（y=20 全称は K1249 出版済み・最新main再取得で確認、y=21 以降は fit レーン群）は本dirの外。
