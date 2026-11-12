# n11-s2-5960-milestone5 — S2 {59,60} 残りworklist（orbit-level再構成・K0773）

S2 {59,60}（11×11二石root）→ S3 {59,60,61} のblocker証明に必要な残計算を、
milestone-1..4のconcrete-level fc/UNI会計（61 blocker・43,375 S6 orbit）から
**K0675 94位置オラクルのorbit-level（全8 D4像）会計に置き換えて**再構成した実験。

## 確定した会計（全て機械検証・assertPass: true）

- S3 {59,60,61} の合法S4子は110個、orbit-level FIRST_WIN像照合で102個が即W4閉鎖、
  残blockerは8個 {5,23,27,31,89,93,97,115} = 3同値類
  （{5,115} / {27,93} / {23,31,89,97}）。K0766と独立に一致。
- 未知S5 orbit（blocker子のうちオラクル94位置に含まれないもの）: **196**。
  raw義務 17,524 のうち 479子インスタンスはK0675スイープ（3,868 S6）で判定済み
  （うち13インスタンスがLOSS-for-mover）。
- **10個の未知S5は判定済みLOSS子を持ち即SECOND_WIN確定**（verdict規約:
  FIRST_WIN ⟺ 全子WIN-for-mover）。これらの残り子はworklistから除去。
- 残りS6 worklist: **7,867 orbit / 615,497 S7合法辺cost**
  （K0766の削減前会計 7,880/616,491 と独立再計算で完全一致した上での、
  settled-10除去後の削減版）。
- first-strike（各類で最も安いS5候補1個の全子WIN検証コスト）:
  類1 {5,115}: 5,128 / 類2 {27,93}: 4,368 / 類4 {23,31,89,97}: 5,178 S7辺。

## ファイル

- `scripts/orbit_ms5_worklist.ts` — 94オラクル鍵+14 LOSS S6鍵を埋込み
  （s5_verdicts.json由来・自己assert）し、blocker特定・S5/S6会計・manifest生成を
  再実行する自己完結TS検証script。anchor不一致時はthrow。
- `output/ms5_closure_summary.json` — 全anchor・類別統計・first-strike表。
- `output/ms5_s5_worklist.json` — 196未知S5（類bit・義務・judged LOSS子有無・cost）。
- `output/ms5_s6_manifest.csv` — 7,867 S6 orbit（cost昇順。classes列はblocker類bit
  のOR: 1={5,115}, 2={27,93}, 4={23,31,89,97}）。外部solverの直接入力。

## 消化プロトコル（レジューム）

1. manifestをcost昇順（またはfirst-strike候補から）消化し、S6 verdict
  （WIN/LOSS-for-mover・S7オラクル照合）をmerge。
2. S5 verdict: FIRST_WIN=全子WIN-for-mover・SECOND_WIN=∃LOSS-for-mover子。
   settled-10は既にSECOND_WIN確定済み。
3. blocker閉鎖: ∃FIRST_WIN S5子 ⟹ W4（S4-t = N-for-mover）。
   3類とも閉鎖でS3 {59,60,61} proven-first → S2 {59,60}判定へ。
4. cache merge時はWIN/LOSS conflictを即検出（既存規約）。

## スコープと注意

- 53+8=110 S4子のうち102閉鎖・10 S5即SECOND_WINは、すべて**K0675の監査済み
  verdict（3,854 WIN / 14 LOSS・感受性証明書4,288件fails 0）に条件付き**。
- milestone-1..4のpublished 61 blocker / 43,375 orbit censusは、concrete-level
  FC/UNI + オラクルhex配列の転写破損（K0773で機関特定）に基づく歴史的会計として
  置き換えられる（数値自体の算術は間違いではない）。
- **11×11空盤・二石root {49,60}・S2 {59,60} は全て UNKNOWN のままである。**
  本実験はいかなる勝敗も判定しない。
