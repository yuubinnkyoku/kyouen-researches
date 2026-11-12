# 2026-11-12 n11 S2 {59,60} orbit-level milestone-5 manifest（K0773）

## 背景

K0762のレジューム（blocker 73閉鎖判定の方向規約未確認）から開始。

## 実行内容

1. **方向規約の解決**: K0675 s5_verdicts.pyの生成規則（verbatim取得）とrecords 94件の
   クロス集計で、FIRST_WIN ⟺ win_children===children（S5手番側=第二手・FIRST_WINは
   loss-for-mover）を確認。W4(S4)=∃FIRST_WIN S5子もK0766のchain機関確認と一致。
   K0762の「パリティ矛盾」は誤読と確定。
2. **orbit-level自動閉鎖**: 78 FW記録の8 D4像からfcOrbitを再計算し、110合法S4子中
   102が即閉鎖・残blocker 8個（3類）を得た。作業中に並走セッションのK0766が
   同一結論（102/110・8 blocker・7,880/616,491）をpush済みであることを検出し、
   独立計算による完全一致を相互検証として記録した。
3. **オラクルhex配列破損の機関特定**（K0773主成果）: milestone4_worklist.ts 5件・
   cert73_regen_audit.ts 6件の配列エントリがK0675 recordsと不一致（fw[16]/[17]は
   plausible-but-wrong位置・fw[75..77]とsw[12]は32文字桁消失、×16³回復で
   {49,50,51,59,60,61,69}系に一致）。94記録鍵を過不足なく説明。
   published 61 blocker過大計上の原因（D4像非照合+破損5記録のextras喪失）を確定。
   cert73監査passは非感受性で無傷。
4. **未知S5 196の会計**: raw義務17,524・judged子479インスタンス（13 LOSS）。
   10 S5 orbitは∃judged LOSS子で即SECOND_WIN確定（worklistから除去）。
5. **milestone-5 manifest生成**: 7,867 S6 orbit / 615,497 S7合法辺cost・cost昇順・
   類bit付きCSV（外部solver直接入力）。first-strike最安候補は各類 5,128/4,368/5,178辺。

## 実装教訓

- per-blockerループで mask=S3m|(1n<<t) の書き漏れが一度発生（検出・修正済み）。
- 義務の二重カウント（35,048=2×17,524）をanchor不整合で検出。
- settled S5の子のreducedセット混入（7,875≠7,867）を検出: LOSS子検出を先に
  完了させてからworklist追加する2パス化で修正。検証script側も同修正。
- 並走セッションとの重複はpush前の最新main確認で検出可能。本回はK0766の
  独立会計との一致が相互検証になった（無駄ではなく強化）。
- open_urlの~32k文字打ち切り・JSON内改行混入は従来通りposition修復で対処。

## repo反映

- experiment: research/experiments/n11-s2-5960-milestone5-20261112/
  （scripts/orbit_ms5_worklist.ts・output/ms5_closure_summary.json・
  ms5_s5_worklist.json・ms5_s6_manifest.csv）
- K0773・本log。generated viewsは別コミットで再生成予定（sandboxでbuild.py不可）。

## レジューム

- 7,867 S6の消化（first-strike 3候補から開始が最安）。S5 verdict merge後、
  3類blocker閉鎖 → S3 {59,60,61} proven-first → S2 {59,60}。
- 11×11空盤・二石root {49,60}・S2 {59,60} は全てUNKNOWN。
