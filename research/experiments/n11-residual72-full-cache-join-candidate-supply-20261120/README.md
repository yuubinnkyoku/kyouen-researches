# n11-residual72-full-cache-join-candidate-supply-20261120

残余 72 行の full cache join 候補供給再構築（単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-candidate-supply-single-owner-note.md`
を先行出版した同一レーンの実行）。branch/PR は作らず main に直接出版。
resolve7（K1072・出版正本のみの再照合）が確定した「retire 済み 39-root 計画の
供給ゼロ」に対して、**resolve6.py の corpus/join/universe を verbatim 再構築し、
残余 72 行にまだ使える候補供給を実際に計算した**もの。

## 何をしたか

- **入力はSHA-256 pin 8 正本**（fail-closed）: resolve5（`5a2f4815…`）・
  published resolve6 出力（`e85d4bfb…`）・39 dead root 掃引（`f8608d0a…`）・
  windfall4 fold9 正本（`24db2352…`）・seventeenth fold10 正本（`bed7d331…`）・
  sv17 38 gate 正本（`c1073bae…`）・39 live 掃引正本（`22953ae1…`）・
  resolve7 正本（`207f4094…`）。
- Stage 1: resolve6 機械（corpus 1,272 ファイル・engine map・transfers・
  post-K0863 sweeps・sweep6・全 receipt fold・windfall hit 機構）を verbatim で
  再実行し、join stats・universe hits・win cover hits・base rows が
  published resolve6 正本と**全数値完全一致**することを gate。
- Stage 2: post-resolve6 出典を加えた phase-2 join（windfall4 receipts 4・
  seventeenth receipt 1・39 live 掃引分類）を D4 canonical root 単位で結合、
  WIN/REFUTED 衝突 0 を fail-closed で gate。
- Stage 3: 残余 72 行（78 − fold9 4 行 − fold10 2 行）を resolve5→fold9→fold10
  正本と幾何再導出で過不足なく導出し、残余 72 行の add-one-stone universe
  （7,448 root）と fresh-safe pool を再構築、最大 matching・pair/singleton 構造・
  1 行あたり demand を計算。
- Stage 4: windfall 型（corpus judged WIN・未 receipt）の第 18 証明書候補と
  既 receipt の追加被覆（free fold）を列挙。resolve7 の 34×2+4×1 割当表を
  本レーンの幾何で独立再検査（72/72 行の幾何被覆一致 gate）。

## 結果（output/…-20261120.json が正本・全 25 gate PASS）

1. **stage-1 再現**: join stats（judged 7,493・REFUTED 6,707・WIN 786・
   conflicts 0）・universe hits（fresh-safe 4,417 ほか全数値）・
   win cover hits 4 root が published resolve6 正本と完全一致。
2. **phase-2 join**: 新規判定はちょうど 39 root（十七 root の WIN 1〔receipt と
   live 掃引の二重出典〕+ 38 REFUTED）、canonical 合計 7,532（REFUTED 6,745・
   WIN 787）・衝突 0 fail-closed。
3. **残余 72 行の出自**: 78 − 4 − 2 = 72 が fold10 正本の残余リストと完全一致、
   閉鎖 6 行は幾何再導出で確認、fold10 の 3 行目は 78 行計画外 extra 行。
4. **universe72 = 7,448**（78 行時 7,969 の unsafe-equal 部分宇宙・
   coverage 部分性 gate PASS）。判定済みは REFUTED 468 のみで
   **WIN 0**（既知 WIN 証明書はもう 72 行のどの行も被覆しない）。
5. **候補供給**: fresh 6,980（fresh-safe 4,109・fresh-unsafe 2,871）。
   pair 辺 536・**72 行すべてに singleton fresh-safe 候補**・multi-cover 根 0。
   **最大 matching 36 が残余 72 行を 1 回被覆で完全に覆う（stranded 0・
   greedy なら 40 本）**。1 行あたり fresh-safe 候補は最少 52 〜最大 76 本で
   供給は濃密。retire 後 38 live root のうち 38/38 が閉鎖済み 72 行を
   被覆したまま REFUTED-D10 判定済み（resolve7 の供給ゼロの行単位裏付け）。
6. **windfall 第 18 証明書候補: 0 根**。既 receipt の open 行追加被覆も 0 行。
   よって corpus/receipt 系からの無償閉鎖供給は枯渇しており、次の一手は
   fresh-safe 36 root 計画の depth-10 両順序掃引（着手時に別途単一オーナー宣言）
   か unsafe pool 2,871・add-two-stones 拡張・depth>10 のいずれか。

## 決定論性・再現

- stdlib のみ（json/hashlib/os ほか）。repo 実験ルートから約 47 秒。
- 2 回実行・別プロセス別 cwd で byte-identical
  （出力 SHA-256 `49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa`）。
- 7 つの post-scan 変更 corpus ファイルは published resolve6 と同様に除外したまま
  （manifest 一致 1,272・信頼境界は resolve6 と同一）。

## 解釈規約（他の n11 項目と同一）

- REFUTED-D10 は LOSS 証明ではない。fold・被覆・matching は行の簿記であり、
  閉じた行・残った行・witness 候補 root のゲーム理論的値には一切言及しない。
  witness 計画は条件付き掃引計画であり証明書ではない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。**

## 次の一手

1. fresh-safe 36 root 計画の depth-10 両順序掃引（着手時に単一オーナー宣言ノート
   を先行すること。runner v17・pilot_d6 制御・cap は K1069 と同じ均一 30M）。
2. fresh-unsafe 2,871 本の構造分類（unsafe 四つ組の型別）と
   add-two-stones 拡張のコスト見積り。
3. 39-root 計画同様、掃引で WIN が見つかった場合のみ証明書抽出
   （repo-verbatim extractor・BigInt 3x3 / Bareiss 4x4 二重検証）を宣言に従って
   別レーン展開。


## 独立第二検証（44 gate PASS・2026-11-20）

K1075生成器をimportしない別実装で、出版済み正本6件をSHA-256 pinし、残余72行のadd-one-stone universe・D4削除被覆・安全性を再導出した。安全性は4×4 Bareiss determinantで全7,448 rootの4点組を厳密整数検査した。

- universe 7,448 rootを独立再構築。safe 4,577・unsafe 2,871。被覆サイズは1行6,616 root・2行832 rootで、3行以上は0。
- K1075の36 fresh witness rootは全件7石・D4正準形・safe。各rootの被覆2行を独立再導出し、36本が72行を重複なく完全被覆。72頂点のmatching上界36に達するためmatching 36は最適。
- resolve7の38 root assignmentも再検査し、34×2行+4×1行=72行を重複なく被覆。
- fold9/fold10/resolve7/K1075の残余72行リストは完全一致。K1075のfresh-safe 4,109・fresh-unsafe 2,871・judged REFUTED 468・WIN 0と独立safe/unsafe総数の算術も一致。
- 44/44 gate PASS。別プロセス2回でbyte-identical。3回目は37.313秒。検証器SHA-256 `74fd3275baffb576dee2959678b85a655136dd4595fa2d39bf980c7b3a515972`、結果SHA-256 `5511222b5385a2e57845b944e3607d2ac406203e4da827fb4e62b8e362b5a46d`。

**検証境界**: K0863の1,279-file corpusとphase-2 verdict joinは再構築していない。fresh-safe 4,109のroot identity集合とpair edges 536の全辺集合はK1075正本の値をpinしており、本検証で独立列挙したものではない。WIN/REFUTED判定・depth-10探索・証明書・receipt・foldは新規生成していない。

- [独立検証器](verify_candidate_supply_geometry_second_20261120.py)
- [44 gate機械可読結果](output/candidate-supply-second-verification-20261120.json)
- [研究ログ](../../log/2026-11-20-n11-residual72-candidate-supply-independent-second-verification.md)

36-root depth-10 sweepは別のsingle-owner宣言に属するため、本レーンでは実行していない。REFUTED-D10はLOSS証明ではなく、標準11×11空盤・二石root・S2・class 1/2/4はUNKNOWNのまま。
