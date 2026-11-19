# 2026-11-20 n11: 残余72行のfull cache join候補供給再構築（K1075）

単一オーナー宣言ノート（`2026-11-20-n11-residual72-candidate-supply-single-owner-note.md`）
を先行出版した上で、K1072（resolve7）が「retire済み39-root計画の供給ゼロ」と
確定した直後の残余72行について、**resolve6のcorpus/join/universeをverbatim
再構築して、まだ使える候補供給を実計算**した。1行も閉じず、いかなるrootの
新規掃引判定も行っていない。

## 入力（SHA-256 pin・fail-closed・8正本）

- resolve5 正本 `5a2f4815…`（残余78行base）
- published resolve6 出力正本 `e85d4bfb…`（stage-1再現の直接比較対象）
- 39 dead root 掃引正本 `f8608d0a…`
- fold9（windfall4）正本 `24db2352…`（閉鎖4行・残余74行）
- fold10（seventeenth）正本 `bed7d331…`（閉鎖2 target行・残余72行）
- sv17 38 gate 正本 `c1073bae…`（root・証明書SHA・coverage claim 2行）
- 39 live 掃引正本 `22953ae1…`（WIN 1/REFUTED 38・両順序）
- resolve7 正本 `207f4094…`（post-retire割当表の幾何独立再検査用）

## 結果（25 gate 全 PASS・正本 SHA-256 `49b6f85f…`）

1. **stage-1再現**: corpus 1,279 manifest中1,272 sha一致（7除外ファイルは
   published resolve6と同一の信頼境界）・join stats judged 7,493/REFUTED
   6,707/WIN 786・衝突0・universe 7,969・fresh-safe 4,417・win cover hits 4根
   がpublished resolve6と**全数値完全一致**（不一致ならfail-closed）。
2. **phase-2 join**: windfall4 receipt 4根・十七 receipt 1根・39 live掃引分類を
   結合。新規判定は**ちょうど39根**（十七rootがreceipt＋live掃引の二重出典WIN、
   他38根REFUTED）。canonical合計 7,532（REFUTED 6,745・WIN 787）・衝突0。
3. **残余72行**: 78−4−2=72がfold10正本残余リストと完全一致・閉鎖6行はroot
   幾何被覆再導出で確認・fold10の3行目は78行計画外extra行。
4. **universe72 = 7,448**（unsafe-equal部分宇宙・coverage部分性 PASS）。
   判定済みはREFUTED 468のみで**WIN 0**（既知WIN証明書は72行のどの行も
   もう被覆しない）。
5. **候補供給**: fresh 6,980（fresh-safe **4,109**・fresh-unsafe 2,871）・
   pair辺 536・**72行すべてにsingleton候補**・**最大matching 36が残余72行を
   完全1回被覆（stranded 0）**・greedy 40本も可・1行あたりfresh-safe候補
   52〜76本。retire後38 live根は38/38本がopen行被覆のままREFUTED-D10
   （resolve7「供給ゼロ」の行単位裏付け・34×2+4×1割当の幾何独立再検査PASS）。
6. **無償閉鎖供給の枯渇を確定**: windfall型第18証明書候補 **0根**、既receiptの
   open行追加被覆 **0行**。次の一手は (a) fresh-safe 36本計画のdepth-10両順序
   掃引（着手時に別途単一オーナー宣言）、(b) fresh-unsafe 2,871本の構造分類、
   (c) add-two-stones拡張、(d) depth>10。

## 決定論性

stdlibのみ。repo実験ルートから約47秒。2回実行・別プロセス別cwdで
byte-identical（出力 SHA-256
`49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa`）。

## 解釈規約

REFUTED-D10はLOSS証明ではない。fold・matching・被覆は行の簿記であり、
witness計画・windfall候補は条件付き計画で証明書ではない。本項は1行も
閉じず1根も新規判定しない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
すべてUNKNOWNのまま。**
