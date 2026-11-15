# five-row-q7-band-closure-35-157-20261115

IN FLIGHT (claim) — 高速レーン。(5,7) の現在の境界は **19 ≤ M_{5,7} ≤ 158**
（下界 19: K0332 の 5×18・29石・occupancy (5,6,6,6,6) 欠損極大証人・最小不在幅 19 は
K0738–K0759 の 5×19 全 occupancy クラス完全列挙で確定。上界 158: K0332 の同和弦
energy + Melchior による全称証明・SAT に依らない）。witness-free 幅集合は
{19,...,34}（K0738–K0759・K0816・K0821・K0834–K0847 の class-split / 完全列挙）に
**5x35 = K0849（five-row-q7-m35-class-split-20261115・63 deciding instances 全 UNSAT）**
を加えた {19,...,35}（鋭い形は M = 19 または ≥ 37）。本実験は残る帯
**m=35..157（123幅）** を掃引し、**M_{5,7} の完全決着**を狙う
（全幅 UNSAT なら **M_{5,7} = 19 exact・w=5 で初の真の安定化長の完全確定**。
帯内 SAT なら witness 発見として dual-verify して下界を更新し前線を進める）。

## 手法

- CNF 生成: **genfast3.js**（弦対抽象円 census・q≥w+2 限定・
  `six-row-q8-band-closure-22-370-20261114` と同一 blob sha a2fc1cb5・
  `seven-row-q9-band-extension-201-612-20261114` 由来）。(5,7) は q=7=w+2 で
  適用条件を満たす。完全性論は同 script のヘッダコメント（q≥w+2 なら全 q点円が
  ≥2つの double row を持ち、(ya,yb,ℓ,ℓ') の弦対抽象で決まる・4点は自動的に共円）。
  O(C(w,2)·m²·w) で m=157 は秒級。sat2.js 全三つ組 census の OOM 壁を回避。
- 較正（`output/controls/` に記録）:
  - **CNF byte-identity vs sat2.js 全三つ組 census**: 5x18 def / 5x18 def+lex=H,V,HV /
    5x19 def / 5x19 def+lex=H,V,HV / 5x24 def+lex=H,V,HV / 5x34 def の6サンプル全て cmp 0 diff。
  - **陽性対照 instance-identity**: 5x18 def-mode kissat SAT（conflicts 2,412,032・75.6s）、
    decode 29石 witness rows [6,6,6,6,5]（K0332 の occupancy (5,6,6,6,6) と V-鏡像で一致）、
    js census-free verifyConfig + Python Fraction verify_witness.py の二重検証 PASS。
  - **honest negative**: 5x19 def-mode は 230s cap で INDET（6,046,287 conflicts）。
    m=19 の不在は K0738–K0759 の完全列挙が担保（def-OR は小 m で難しい・既知パターン）。
- **第三系 census 検証**: 水平弦+第3点列挙による方法非依存の独立 census
  （`scripts/ts_verify_census5q7.js`・sat2 全三つ組・genfast3 弦対のどちらとも
  方法が異なる・完全性論は「≥7点円は水平弦を持ち4行以上に触れる」）。
  掃引済み13幅で genfast3 の curves 数と **13/13 一致**
  （`output/ts-census-check.json`）。さらに**全帯 m=35..157 の予測曲線数表**を
  第3系で計算済み（`output/ts-census-fullband.json`・123幅網羅・欠落なし）—
  掃引進行に合わせて各幅の meta curves と照合する。
- **K0726 アンカー検証**（`scripts/ts_census_k0726_anchor.js`・
  `output/ts-census-k0726-anchor.json`）: 新規に書き直した2系統
  （A: 水平弦対+第3点、B: 全三点組 Cramer 整数解・被覆論非依存）が
  **K0726 の 5×19 census（95円 = 7点8本+8点87本・5行直線・64,980 行対構成・
  132,180 非共線三点組・83,471 distinct 円）と全数値完全一致**、
  5×18（84円 = 7点4本+8点80本）も完全一致、両系統互いに一致・self-check 0失敗。
  帯頭 m=35 も 239円+5直線=244 曲線で records.jsonl と一致。
  これで K0726 ↔ 本レーン検証スタック ↔ genfast3 掃引記録（13/13）↔ sat2
  byte-identity の鎖が帯頭で接続し、全帯予測表は repo 確立済み census に錨止めされた。
- 帯掃引: 各幅 genfast3 def-mode CNF → kissat 4.0.4（230s cap）→ 記録は
  `output/records.jsonl` に resume-safe に追記。**def-mode UNSAT はその幅の
  欠損極大非存在の完全証明（1インスタンスで完結）**。INDET 幅が出た場合は
  rowY=0/1/2 行固定分割（V-鏡像 y↔4-y で 3クラスが全5行を被覆・K0829 と同一の
  被覆論の w=5 版）で継続。交差確認は代表幅で def+lex=H,V,HV、決定性は代表幅の
  再生成・再解 bit-exact。
- ソルバ: kissat 4.0.4 official linux-amd64（md5 3a5eba830aa6008a604fcc9bbe99a325）。

## 進捗

- 2026-11-15: IN FLIGHT claim。較正完了（byte-identity 6/6・陽性対照二重検証 PASS・
  honest negative 5x19・第三系 census 13/13・全帯予測表 123幅・K0726 アンカー一致）。
- 帯掃引（def-mode・230s cap・INDET 0）: **m=35, 36, 37, 40..49 の13幅 UNSAT**
  （conflicts 2,809,004 (m=35) → 漸減 → 1.36M..1.79M の平台帯・m=49 で 1,483,146。
  records.jsonl は main に checkpoint push 済み・各幅の curves は第三系表と一致）。
  **未実行: m=38, 39（次の実行で最優先）、残り帯 m=50..157。**
- 2026-11-15 (追記): 実行環境の長時間障害（アップグレード環境が一時利用不能）により
  m=50 の実行が中断。m=50 以降と m=38, 39 は環境復旧後に再開する。
  生 kissat ログは環境復旧後に batch push する。

## 並走協調ノート

- **5x35 は二重決着**: class-split レーン（five-row-q7-m35-class-split-20261115・
  K0849・63 deciding instances 全 UNSAT・66 records）と本レーンの def-mode
  UNSAT（2,809,004 conflicts・1インスタンス）が**独立な符号化で一致**した。
  以降の幅でも、class-split レーンが先行して決着した幅は本レーンの def-mode
  掃引と交叉確認として機能する（両者とも各幅で完全な非存在証明）。
- 本レーンの def-mode 掃引が m=36 以降の幅を先に決着した場合、class-split レーンの
  同幅エントリは省略可能（省略しない場合は交叉確認として価値がある）。
- 本レーンは実行環境障害中。復旧後は records.jsonl への追記で resume する
  （m=38, 39 → 50..157 の順）。

## スコープ

有限機械検証（genfast3 弦対 census の完全性論 q≥w+2・CNF byte-identity・
陽性対照の witness 再発見、kissat 4.0.4 の正確性まで）。m=35..157 の各幅
def-mode UNSAT はその幅の欠損極大非存在の完全証明。全幅 UNSAT の場合、
witness 幅 {7..18}（K0808..K0815 系）・witness-free {19..35}（class-split 系・
K0849 含む）・m≥158 witness-free（K0332 全称上界・証明済み）と合わせて
**M_{5,7} = 19 が exact に決着**する（w=5 初・q=w+2 帯では (6,8) に次ぐ例）。
SAT 幅が出た場合はそこで停止し、witness を dual-verify して下界更新として記録する。
