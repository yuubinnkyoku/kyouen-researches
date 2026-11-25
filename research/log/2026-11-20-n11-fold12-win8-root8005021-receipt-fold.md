# 研究log: fold12 WIN8-D10 receipt fold root 8005021（2026-11-20）

単一オーナー宣言（commit `7bb492cd222a5f94d717760f8fc398941a462f11`・先行出版）に基づく実行記録。
前段: 同一実行で fold11（K1105）・K1106（root 8005021 証明書抽出・19 gate）を出版済み。

## 事前検証

1. **K1106 README弾丸の着地確認**: 前回実行末尾で実行した README 弾丸 push（commit `5697696c`）の着地を
   commit-SHA pin raw fetch + grep で確認（行278・K1105弾丸直後挿入・byte差 3,014）。
2. **fold11 正本・fold11 機械・K1106 正本の取得**: commit `f49bcc16`（fold11 実験dir）・`db169cf5`（K1106 実験dir）から
   fold11 正本（SHA-256 `d7bf2cd5…` 確認）・fold11 機械 578 行・K1106 監査正本（`0bd2dd10…`）・証明書本体（945,298 bytes・`69f32661…`）を取得。
3. **fold11 機械の byte-identical 再実行**: W に fold11 の全チェーン入力を複写し、fold11 機械を再実行して
   出力が出版正本と完全一致（約 1.4 秒）。この gate を fold12 機械の内部にも組み込んだ（subprocess・FOLD11_W env）。

## 本体実装

`fold_win8_root8005021.py`（fold11 機械の移行・変換スクリプト make_fold12.py で verbatim 保持変換後に手直し）:

- チェーン全段 frontier 再計算 6,259/495,507 → … → 6,222/492,688 → ninth-twelfth 6,213 → fs13 6,209 → fold10 6,206/491,497（incidence 11,810・solved 1,642・residual72）→
  **fold11 chaining: 5 行 open 性・cost 照合・frontier_after 出版値（6,201/491,110・solved 1,647・incidence 11,803・s6_needed 4,504・cost_needed 357,196）・residual68 == residual72 − fold11 主張 4 行・closed target 44 を全 gate 一致**。
- **fold11 機械 byte-identical rerun gate**: fold12 機械の実行中に fold11 出版機械を subprocess で再実行し、
  出力 SHA-256 が出版正本 `d7bf2cd5…` と一致しなければ fail-close。fold10 再実行 gate（fold11 機内）との二重の上流検証。
- K1106: 19 gate 全再検証（g05 mobility 41・g06 uncapped probes 619,138/751,581・g07 主張 3 行・g08 pilot_d6 4・g13 nodes 3,272,039/2,876,091・g19 footprint 照合）・
  証明書 byte 検証（945,298 bytes・26,083 行・sorted unique・header）・root 幾何（8石・quadruples 0・D4 正準・合法手 41 を独立再導出）。
- K1097: 27 gate・footprint partition（49 行 exactly-once・root 8005021 は intrinsic == claimed == 3 行）・residual23 と不交差。
- **被覆幾何 2 方法**: (A) 8 D4像 × C(8,2) 2石除去 = 224 操作 (B) C(8,6)=28 部分集合直列挙。canonical 行集合 28 行が完全一致。
- 分類: open-frontier 8（本 receipt で閉鎖）・not-in-worklist 20。closed-before-this-receipt 0（worklist-but-not-open gate で chain 不整合 0）。

## 結果

- receipt は **open 8 行**を閉じた: K1106/K1097 主張 3 行（`…8001001` cost 74・`…8001020` cost 65・`…8005000` cost 71・5親 target 内）+
  **target 外 open 行 5 行**（`…0004021` cost 79・`…0005020` cost 80・`…08000021` cost 69・`…08004001` cost 77・`…08004020` cost 69）。
  余剰行が主張行を数で上回った初の receipt。余剰は c1 需要行が多く、class-1 側の簿記上前進。
- closed edge cost 584・frontier 6,201/491,110 → **6,193/490,526**・solved S6 1,647 → 1,655・incidence 11,803 → 11,790
  （影響 5 parent: c1 3・c2 2・完全閉鎖 0）・5親 target 44 → 47/112・残余 68 → 65。
- win16 候補は 16 → 14 根（主張 42 行）。残余23行掃引計画（並走宣言済み）は不変。
- 出力 SHA-256 `0f73795ce71aec83ba4a9f1b97a530891f3e6d1c807bfa47c9fbb88a1b33f5bd`。
  同一 cwd 2 回 + 別 cwd・別プロセス・独立 W 複写（FOLD12_W env）1 回の 3 実行で byte-identical。

## 実装上の注記

- 初稿の変換スクリプトに「古い行リストからソースを再構築して中間置換が失われる」バグがあり、
  最初の実行で W/ルート定数が未置換のまま全チェーン gate だけ通る状態になった（fail-close で最終出力までは進まず）。
  置換後の再生成・全 gate 再実行で解消した。生成機械上の `unique_remaining_s6` のみ旧変数（len(open72)）を参照しており
  6,206 という異常値を出したが、gate 群は他の値（sum・incidence・solved）で閉じており差分箇所は 1 行のみ。
  修正後 3 実行 byte-identical。この種の移行では「出力の全数値を独立に読み戻しての検算」を gate に加えるべきである。

## 採番

K1106 は同一実行で当レーンが使用済み。items tree 走査・README grep・list_commits の 3 点で K1107 の空きを
push 直前に確認して K1107 として出版した（並走の y=4 族全称証明・K1058 extremal レーンの採番と衝突した場合は再採番規約に従う）。

## 未着手・次の一手

- 残り 14 WIN8 候補（主張 42 行）の証明書抽出と fold。着手時に単一オーナー宣言を要する。
  K1086 per_root probe 上の次の最安価候補: `00000000000000003800000009840004`（nodes 1,143,198/1,528,656・claims 3）→
  `00000000000000909002200080100000`（nodes 512,590/614,246・claims 4）。並走宣言済みの `…8180000`（4496c888）・`…0810000a` は着手禁止。
- 残余 65 行の refsolve（第6ラウンド）。fold12 後の pool は残り WIN 候補 14 根を含めて再計算が必要。

## 解釈規約

REFUTED-D10 は LOSS 証明ではない。WIN8-D10 は root のゲーム木のみを証明する。fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。
pn/dn・nodes 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
