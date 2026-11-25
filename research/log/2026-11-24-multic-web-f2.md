# 実行 log: multi-c web F2 スプレッド法則表・T-RC 子恒等式・mex 不動点証明書（K1287・高速レーン・2026-11-24）

- lane: 高速レーン（短〜中時間・厳密結果・branch/PR なし・main 直接反映）。
- 成果一式: 宣言ノート `40f945b8` → kit `35394ac8`（fetch-back 12 ファイル
  byte 照合）→ 公式 4 走（全て宣言 sha と byte-identical）→ 公式変異電池
  9 走（宣言期待値と全件一致）→ 成果物出版 `16bd8d12` → K item・本 log・
  knowledge README bullet。
- 関連: K item [K1287](../knowledge/items/K1287-multic-web-f2-spread-laws.md)・
  宣言ノート [single-owner note](2026-11-24-multic-web-f2-single-owner-note.md)・
  kit [multic-web-f2-20261124](../experiments/multic-web-f2-20261124/README.md)。

## 0. 着手時の状況と番号確定

- 着手時の観測 HEAD は `5b9c6231`。並走する対抗 fast-lane がこの直後に
  **K1286 を出版**（`f6db3f33` 宣言 → `ccf48d10` kit → `a92dcc12` 公式
  成果物 → `9336611a` K item/run log → `9305b278` README bullet →
  切断事故の修復 `e56c8cce`）。K1286 の内容はペア (m,m+g) の境界スライ
  ス・床負域・pre-diag 分裂の全称定理パッケージであり、その §5 O3 は
  「**F_d/G_d（d∈{1,2,3}・288 点・OBS）を未来課題 F2（spread 理論）
  への入力として登録する**」と明記していた。
- K1287 は空き（items dir のコミット履歴で最新は K1286 = `9336611a`）・
  「K1287」および「multic-web-f2」領域の対抗宣言なしを機械確認。
- 本セッションの成果（multi-c 5 族 × 3 面の法則表・frontier・子恒等式
  I1–I11・mex 不動点証明書）は、**その F2 を継承・拡張する K1287** と
  して出版すると決定。K1286 O1/O2/O4（床負域・pre-diag・z1/z2 床の
  m 分裂）には非接触（O1 blocker 診断での引用のみ）。d≤3 の F/G 列
  （288 点・OBS）は整合行として census で再検証するのみで、全称主張の
  重複なし。
- push 直前の再取得で観測 HEAD は `076e05c1`（Part DH takeover・interim
  note・長期レーン bookkeeping・いずれも非接触）。

## 1. 発見順（宣言まで）

1. **z0/z1/z2 の面別 census**（explore_k1287.py の前身の探索スクリプト）で
   multi-c web の 5 族（W/D/E/A'/A）の値を幅広く採集。まず機体コア箱
   （d≤8・c 2..6・m≤10 前後）で各面の FAMILY_SUMMARY が bad=0 になる
   法則表候補を数回の iterate で収束。
2. **例外行の直接確認**: W(z2,m=1,d=1)=2（全 c）/ W(z0,m=1,d=1) は
   c=2→0・c≥3→2 / D(z{0,2},m=1,d=2)=2（ただし (z2,m=1,c=2)=0）/
   A(m=1) の 3 面の z 依存。いずれも SPOT 行として explore 出力に
   固定値で残す。
3. **E 族旧法則の反例検出（失敗の honest 記録）**: 当初の読みは
   「E 族は偶 d → 1・**奇 d → 2（z0/z2）**・z1 は別」というもの。
   lawcheck の広域走（z0/z2 面）で **bad=96**（すべて奇 d≥5 の 96
   cell: d 5..8 × c 2..7 × m 1..9 の範囲で該当行）として反例検出。
   binham 表を取り直し、**修正表 EL(z,d): 偶 d→1・d=3→(z1→0,
   z0/z2→2)・奇 d≥5→0** が全箱で bad=0 になることを確認してから
   宣言に凍結した。旧 lawcheck 出力（反例行 96 を含む）は探索過程の
   一次資料として保持。機体は tamper=elaw に旧法則（奇 d→2）を
   わざと残し、公式電池で bad 387（D3 315 + D9 72）を検出する設計。
4. **frontier の法則化**: m=1 の B-exit が落ちる単一層族 SLB2/SLB3
   （(x^c)@(x+3) z2 / (x^c)@(x+4) z3）・L 族（{d,(d+1)^s}@(d+2+zp)
   plane zp+1）・Am 族（{m^2,(m+h)^s}・h≥2）を frontier として
   census。Am の z2 面で (m=1,h=2,s=1) のみ 1 という**単点異常**を
   観測（O4 として open 登録・構造説明なし）。
5. **T-RC 子恒等式 I1–I11 の発見**: 5 族の全ての手が「同 web の既知
   族点・または SLB/L frontier 点」に予算 R−1 で落ちることを multiset
   等式で確認。特に I2（A-min of W = W(d+1,c,m−1)・**d が +1 しな
   がら行が下がる** Episcopal 構造）と I10/I11（m=1 の B-exit が
   L 点・単一層 frontier 点に正確に飛ぶ）が全称証明の見通し
   （typed 子 mex 解析の R 強帰納）を与える。恒等式は自明の代数
   として手証明、機体 D8 で 3,132 点を engine-free 照合。
6. **mex 不動点ゲート（D9）の設計**: 法則値が単なる表の一致ではなく
   mex(engine 子値) の不動点であることを各箱点で直接検証。tamper=mex
   （子を最初の 1 子に制限）で bad 175 が宣言どおり出ることで、
   証明書が子集合の完全性に依存していることも検証可能。
7. **宣言前 dryrun（決定論）**: PYTHONHASHSEED random/1/99 の 3 走で
   stdout byte-identical（sha256
   `9e3a61f524af7bdcf7f32a31ceb465b3a63e69e0d86ae25ccee4243f0f8d7594`）
   ・変異 9 走の rc/bad を確定し、**全てを宣言ノートに事前記載**して
   から出版。

## 2. publish-then-execute の実行記録

1. **宣言ノート出版 `40f945b8`**（single-owner note）。
2. **kit 出版 `35394ac8`**: verify_k1287.py（sha256
   `52e7eea7…`・engine pin `bd5f22e4…` の startup ゲート内蔵）・
   engine_block.py（`582c93c1…`・K1282–K1286 kit と同一 bytes）・
   explore_k1287.py（stage z0|z1|z2|frontier・stdout 決定的）・
   output/（explore 出版走 4 組）・predry/（宣言前 3 走 + 変異 9 走）。
3. **fetch-back byte 照合**: 出版済み 12 ファイルを get_file_contents
   で取得しローカルと照合（remote == local・12/12・初回の内容抽出
   誤読み〔content フィールド誤認で remote_len=0〕は resource text
   抽出に修正して解決・この失敗も工程の honest 記録）。fetch した
   bytes から隔離 tree `/home/user/kr/k1287_iso`・`k1287_iso2` に機体
   を書き出し、両 tree で機体 sha が宣言値と一致することを確認。
4. **公式 4 走**（fetch-back 機体から）:
   - run1: iso tree・PYTHONHASHSEED 未設定 → rc 0・sha
     `9e3a61f5…`（elapsed 28.2s）
   - run2: 同 cwd・PYTHONHASHSEED=1 → rc 0・同一 sha
   - run3: iso2・`env -i PATH=… PYTHONHASHSEED=99` → rc 0・同一 sha
   - run4: iso2・PYTHONHASHSEED=7 → rc 0・同一 sha
   - 4 走とも counts
     `[1200,1050,810,945,252,832,702,3132,1458,18,1344]`・総計
     11,743・bad 全電池 0・engine_gate PASS。
   - 注: `/usr/bin/time` が環境に存在しなかったため、elapsed/finished
     は機体自身の stderr（揮発）を .info に記録。
5. **公式変異電池 9 走**（iso tree）: 全て宣言期待値と完全一致:
   - `--tamper-engine`: rc 2・mutated sha `0ea47a80…` ≠ pin。
   - wlaw: rc 1・bad D1 400 + D9 144 = 544。
   - dlaw: rc 1・D2 600 + D9 192 = 792。
   - elaw: rc 1・D3 315 + D9 72 = 387（旧「奇 d→2」法則の復元）。
   - aplaw: rc 1・D4 945 + D9 270 = 1215。
   - alaw: rc 1・D5 84 + D9 60 = 144。
   - amlaw: rc 1・D6 160・他 0。
   - identity: rc 1・D8 336・他 0（I1 の宣言ターゲットを E 族にすり
     替え・d≥3 行 336 点全 bad）。
   - mex: rc 1・D9 175・他 0（子集合を最初の 1 子に制限）。
6. **成果物出版 `16bd8d12`**: output/audit_run1-4.out+.info・
   output/tamper_{engine,8 法則}.out+.info（18 ファイル・うち
   tamper .out は predry と byte 同一〔決定論の追加担保〕）・
   output/detcheck.json（verdict **OFFICIAL-PASS**・4 走 sha 一致・
   変異電池期待値一致を機械記録）・MANIFEST-sha256（54 entries・
   kit 内全ファイルの sha 列挙）。
   - push 直前の最新 main 再取得: HEAD `35394ac8`（自らの kit 出版
     のまま・競合なし）。並走 Part DH 系の新コミットもなし。
   - MANIFEST 生成後にローカル複製（declaration_note.md・repo には
     log 配下に別 path で存在）を除外して 54 entries に確定した
     （kit 内 path と repo path の 1:1 対応を担保するための修正・
     honest 記録）。

## 3. 受入判定

- 宣言した公式期待値（4 走 sha・counts・bad 0・変異電池 9 走の rc と
  gate 別 bad 個数）と実測が**全件一致**。detcheck.json は
  OFFICIAL-PASS。
- **ただし過大主張の防止**: 値法則 C-SPW/D/E/A'/A・OBS-F1..F4 は
  有限 census 箱内の conjecture であり全称定理ではない。全称定理は
  T-RC 恒等式 I1–I11（自明の代数）のみ。D9 mex 不動点も箱内有限の
  機械証明書である。

## 4. open（次回・単一オーナー候補）

- **K1288 目標（O1）**: SLB2/SLB3/L（必要なら Am）の typed 全称証明。
  C 子は SLB 自身に落ち、A 子は L/Am 族で web 閉包するかを判定する。
  床負域（K1286 O1/O2/O4・z1/z2 床の m 分裂）と合流すれば
  C-SP* 5 族の全称化が R 強帰納で閉じる見通し（§2 I1–I11 の含意）。
- **K1289 候補（O4）**: Am z2 面 (m=1,h=2,s=1)=1 の単点異常の構造説明。
- **O2**: C-PC1z1-d4 の c≥2 半分（C-SPW z1 d=1 行 = 0）は census 上の
  解決として登録済み。全称化は O1 待ち。
- **O3**: c 方向不変性（census c≤7 で法則変化なし）の spread 理論として
  の定式化。

## 5. 規約・11×11・並走との関係

- 11×11 巨大探索の verdict 不消費・UNKNOWN 不変。法則表は census 箱内
  で multi-c 低 z 面の枝刈り格子の評価表（O(1) 即値）として使えるが、
  採用判断は巨大レーンオーナーに委ね、接続は記録のみ。
- 対抗 K1286 レーンとは領域が直交（同レーンの §5 O3 入力を継承拡張・
  全称主張の重複なし）。Part DF/DG/DL/DH（b28/b31 solver 系
  bookkeeping）とも対象直交・非接触。
- knowledge README への bullet 追加は全文取得（1,028,444 bytes・切断
  事故 `9305b278`/修復 `e56c8cce` の再発防止）の上、純末尾追記で
  行った（全文字数照合つき）。
