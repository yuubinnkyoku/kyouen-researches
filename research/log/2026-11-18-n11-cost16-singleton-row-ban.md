# 2026-11-18 N11 31行cost-16 parent singleton行ban拡張・混合生存点（top-10 pair ban + 上位singleton行ban）

## 成果

31行cost-16 parent `00000000000000003800000008001000` の生存曲線を **singleton行banへ拡張**した。イベント F_s = 「A型計画のsingletonが行sを被覆」（= 行s上の全 w1[s] 個のsingleton rootをban）。**top-10 pair root ban（kill 39.659%）に上位3行（4・0・24）のsingleton行banを加えた混合生存点を厳密決定**した。

- script: `cost16_singleton_row_ban_20261118.py`（run row_rank / finalize の2 mode・checkpoint resume付き）
- output: `output/cost16-singleton-row-ban-20261118.jsonl`（3 row record）・`output/cost16-singleton-row-ban-20261118.json`（20 checks all PASS・二重実行byte-identical sha256 `5a7c2ab6…`）
- 混合kill: **39.659% → 41.479%（+行4）→ 43.159%（+行0）→ 44.822%（+行24）**。

## 構造（I-E の項がどこで止まるか）

1. **singletonを含む計画はA型のみ**（B型coverは16 pair rootでsingletonなし）→ 重なり項はすべてA型。
2. **F_s と F_s' は互いに排他**（A型計画のsingletonはちょうど1つ）→ 行marginalはpair ban群の上に加算的。
3. |F_s| = w1[s]·pm(V∖{s})（phase A per-row pm・pin `fe4b4b55…`）。F_s∩E_e = w1[s]·pm(V∖{s}∖e)。F_s∩E_e∩E_e' は互いに素な e,e' のみ非ゼロ（行共有はA型で2重被覆になる）= w1[s]·pm(V∖{s}∖e∖e')。**3本の互いに素なtop-10 pairは存在しない（ハブ行18/19）ので I-E はpair項で打ち切り厳密**。
4. 全数値は w1[s] について線形なので、root単位のmarginal（行s上の1個のsingleton rootをban）は同じ数値を w1[s] で割るだけ。

計算量: 各行で 10本のpm(V∖{s}∖e)（28行）+ 23本のpm(V∖{s}∖e∖e')（26行）を1個の共有memo（330万-420万状態）で計17-19秒・3行で約52秒。

## 主要数値

| ban対象 | marginal | 累計kill share |
|---|---|---|
| top-10 pair（既存・k10曲線） | — | 39.6593% |
| +行4 singleton（w1=50・\|F_s\|=2.768%） | +53,978,570,768,229,600（+1.8202%） | 41.4789% |
| +行0 singleton（w1=48・\|F_s\|=2.675%） | +49,840,637,651,254,656（+1.6807%） | 43.1596% |
| +行24 singleton（w1=48・\|F_s\|=2.661%） | +49,316,811,498,945,360（+1.6625%） | 44.8215% |

- **行marginalは |F_s| の約65-66%を保持**（例: 行4は |F_s|=82.1e15 中 54.0e15）。重なり減衰（行4: j2和=616,467,997,185,555・j3和=53,847,792,189,450）を差し引いても、pair ban10本とsingleton行banはほぼ独立に効く。
- **root単位のmarginalは pm(V∖{s}) の約63-66%**（行4: 1,079,571,415,364,592 / 1,642,191,620,360,697）。ただしroot単位の寄与は全最小coverの0.036%程度で、**pair ban（top-1で4.60%）より2桁弱い**。coordinatorの証明書候補順位としては、個々のsingleton root より「行まとめban」（1行で+1.7-1.8%）が実用的。
- 上位singleton行は |F_s| 順で 4 > 0 > 24 > 5 > 19（いずれも w1[s]≈40-50 の行）。root単位membership順は 18 > 19 > 15 > 5 > 0（pm(V∖{s}) 順）で順位が異なることに注意。

## 検証（finalize 20 checks all PASS）

- 入力pin: phase A `fe4b4b55…`（per-row pm）・groups aggregate `31bdefdb…`・出版45-combo joint `95194096…`・**k10曲線JSON `6be591d4…`（当日出版・git blob pin）**。disjoint pair 23本のkeysが出版shared_row表と一致。
- per-row pm anchor 3/3（fresh再計算==出版per_row）・j2 ≤ pm_full（30本）・j3 keys == disjoint 23本・j3 ≤ min(j2)（23本）・marginal ∈ [0, pm_full]・rank順（|F_s| 降順）確認・混合kill単調・≤ total。
- k10のkill(10)=1,176,471,942,925,388,348 をpinから読んで基底として使用。
- 二重実行byte-identical。環境リセット（workdir消失）を1回挟んだが、scratch snapshot + raw CDN再取得（pin一致）で損失なく再開・row 4のrecordは再計算不要だった。

## 運用メモ

- 実行中にsandboxの接続断（503）でworkdirが消えた。**scratch `_scratch/cost16phaseb/` へのsnapshot + 出版済み入力のraw CDN再取得（git blob pin照合）**で5分以内に復帰。checkpoint resume機構が効いた。
- 本成果で cover計画空間の削れ方は「pair上位10本ban: 39.66%」+「singleton上位3行ban: +5.16%」まで厳密に判明。残り55.2%はこれらのbanでは削れない計画で構成。

## 解釈上の注意

marginalは最小cover計画の数であって探索コストでもverdictでもない。REFUTED-D10・STERILE は LOSS 証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。
