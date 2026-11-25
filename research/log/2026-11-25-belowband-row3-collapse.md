# 実行 log: K1315 下帯第3行観測パケット (OBS-BBL3 + L-BR3 + CONJ-BBL3) — 高速レーン 2026-11-25

前回 (K1315 セッション前半): compaction を挟みながら、(E,z) 生層の非崩壊確認、
クラス (n,j) 層化の発見、n=7 の 2-族分離 (m2) の特定、n=8 j=0 の 4 相ラダー、壁族の
V_LAW 固定までの発見作業と、単一オーナー宣言ノートの出版 (da3f6538)、kit の出版
(919b51bf / 12c402a2)、および kit 転写破損の修正 (3b833e3f / 9ae7d106・API
contents 経由の sha 照合で 4 ファイル完全一致を確認) が完了していた。本 log は
 Publication chain の後半 (凍結 .out の出版・公式実行・detcheck・item/log/README)
を記録する。

## チェーン (publish-then-execute)

1. **採番確認**:着手時観測 HEAD 5085d19f。K1315 commit 検索 total 0 (宣言ノート
   §0 どおり)。
2. **宣言ノート da3f6538**:
   `research/log/2026-11-25-belowband-row3-single-owner-note.md`
   (§1 主張 L-BR3 / OBS-BBL3 (a)–(e) / CONJ-BBL3・§2 規約・§3 凍結探索・§4 機体
   宣言 5 電池 1,307 点 + 変異 6 種 + predry stdout sha 5990db75…・§4.5 主張の
   区別・§5 open 登録・§6 honest 経緯)。単一 commit。sha256
   6c6b056fc87d6fc5f9136794138ec616d85f3fb1810fd3b2e794d4496bb44f3c
   (出版後 fetch-back で byte 一致を確認)。
3. **kit part A 919b51bf**: verify_k1315.py (最終 sha256 de580d46…・engine pin
   bd5f22e4… startup ゲート内蔵) + engine_block.py (582c93c1…・K1282..K1314
   chain と同一 bytes)。
4. **kit part B1 12c402a2**: kit README.md (d1c2f5a5…) + 凍結探索
   explore_k1315.py (29f7080a…)。この時点で .out は未出版 (後の Actions で
   出版)。
5. **内容修正 3b833e3f + 9ae7d106**: verify の V_LAW 転写破損 ((2,2,2,2,1,1) 行
   の vals 7 zero 復元) と explore の docstring quote修正。API contents の
   base64 を decode する照合で 4 ファイルが目標 sha (de580d46 / 29f7080a /
   582c93c1 / d1c2f5a5) に完全一致したことを確認して確定。
6. **凍結 .out の出版 (Actions 切替)**: explore_k1315.out (82,348 bytes・sha256
   558ed202…) の直接インライン push を試みたが、大ファイル (110 KB base64) の
   実行環境経由転写で破損リスクが高く (3 回の試行でそれぞれ破損・_Length 不一致
   を検出・いずれも sha 検証前なので実害なし)、確実性のため GitHub Actions workflow
   に切替:
   - workflow v1 push `8bef5e61` (.github/workflows/k1315-publish-out.yml):
     runner が kit から PYTHONHASHSEED=1 (python 3.12) で再生成し、frozen sha
     とのゲートを通過した場合のみ commit する設計。
   - run 45553561132: **sha ゲート PASS** (runner 再生出力が 558ed202 と byte
     一致) したが、最終 git push が同時刻の並走 lane commit (Part ED a094f29f)
     と競合し失敗。
   - workflow v2 (race-safe) push `67b87d26`: fetch + rebase origin/main を
     push 前に実行。run 45554259140 成功 → **Actions bot commit `7954ae84`**
     で .out 出版。fetch-back で 82,348 bytes / sha256 558ed202… 一致
     (IDENTICAL)。
   - この方式は sha ゲートが破損出版を構造的に排除し、runner 再生が byte 一致
     したこと自体が sandbox とは独立な第三環境での再現性実証にもなった。
7. **公式実行 (fetch-back bytes から)**: kit 4 ファイルを API contents で再取得
   (全 sha 一致)。
   - **O1**: explore cwd PYTHONHASHSEED=1 → rc 0・144.9 秒・出版 .out と byte
     一致 (cmp IDENTICAL)。
   - **O2**: explore 隔離 env (`env -i` PATH 指定・PYTHONHASHSEED=1337・LC_ALL=C)
     → rc 0・146.5 秒・byte 一致。ハッシュ順序非依存の実証。
   - **O3**: verify (.out 同梱構成) → rc 0・overall_bad 0・engine_gate PASS・
     counts [924, 289, 10, 10, 74] 総 1,307 = 宣言総点数・stdout sha256
     5990db75696b0b7ec29fd81664fee82907167af234ee6bc1c689c50100ea1f13 =
     **宣言 §4 predry sha と byte 一致**。
   - **predry 2 走** (cwd / PYTHONHASHSEED=12345・.out 同梱構成): byte-identical。
     stdout sha は全 seed (0/1/7/12345/1337) で同一 (決定論的)。
8. **honest 記録 (O3 の D5 skip 構成)**: 最初の O3 を .out 未配置で実行した場合、
   D5 (凍結成果物照合電池) は設計上 skip され、counts [924,289,10,10,0]・stdout
   sha 3f605280… という別の値を返す (rc 0・overall_bad 0 のままだが点数不足)。
   宣言構成 (.out 同梱) が本命であり、detcheck.json の honest_notes に両構成の
   説明を記録した。
9. **tamper 6 種** (.out 同梱構成): --tamper-engine rc 2 (engine_gate FAIL) /
   --tamper=law rc 1 (D2 bad 1) / --tamper=cells rc 1 (D3 bad・w1 値と uniform 的中) /
   --tamper=xen rc 1 (D4 bad 1) / --tamper=anchors rc 1 (D5 bad 1) /
   --tamper=census rc 1 (D5 bad 1)。宣言表どおり全 fail-closed。
10. **detcheck.json 出版 b522c00e**:
    `research/experiments/belowband-row3-20261125/output/detcheck.json`
    (OFFICIAL-PASS・predry/O1/O2/O3/tamper/kit-fetch-back/out-publication の
    全実測・honest_notes 3 条・fetch-back sha256
    ceda40d7dd3955f70d510aa7ec18e6cdaca8b0826d3809bb295fe4a7d5ca4f12・valid
    JSON 確認済み)。
11. **K item / 本 log (単一 commit)**: item
    `research/knowledge/items/K1315-belowband-row3-collapse.md` + 本 log。

## 成果の要約

- **OBS-BBL3**: 第3行 k=z+n−5 は生 (E,z) 層では崩壊せず (a)、クラス (n,j) 層化で
  ほぼ崩壊 (b)し、族ごとの 3 ピース則 (c) とアンカー表・ラダー (d)・抑制・壁族 (e)
  が観測として確定 (n=4..8 の 5,779 単一 2 行で法則実違反 0)。
- **L-BR3**: 公刊閉形式の転写が格子上 924/924 で照合。
- **CONJ-BBL3**: 全称構造予想を免責付きで登録 (O-BBL3 は open のまま)。
- **機体**: 1,307 点公式監査 bad 0・stdout sha が宣言と完全一致・tamper 6/6
  fail-closed・.out が sandbox 2 走 + Actions runner 1 走の 3 環境で byte 一致。

## 次課題

1. **CONJ-BBL3 の証明** (本命): typed-children ボトムアップ (第2行既知 → 第3行
   帰納)。K1314 §5 の B 承継 typing (n−1=1→L-BR2, 2→L-2, ≥3→T-BB2) が帰納の
   足場。flat spot j=n−3、(7,0) 2-族、n=8 4-族ラダーの誘導が鍵。
2. **ラダー幾何の一般化**: η(n) の −5 刻み、n=7 の分岐、n=8 の 4 相の構成的説明。
3. **統一予想 U との接続** (K0832 k≥1 スライス)。
4. **plane 摺り合わせ観測** (PB2/L-2 型界面の深層再出現)。
