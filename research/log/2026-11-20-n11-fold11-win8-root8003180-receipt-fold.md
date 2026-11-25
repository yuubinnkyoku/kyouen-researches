# 研究log: fold11 WIN8-D10 receipt fold root 8003180（2026-11-20）

単一オーナー宣言（commit `d36e15b6`・先行出版）に基づく実行記録。

## 事前検証

1. **チェーン入力の所在特定・blob照合**: fold10 機械 `fold_seventeenth.py` が必要とする全入力
   （worklist・ledger・globalFold・previousCostFold・firstFoldTarball・census・audit・secondThirdFold・fold4・fold56・fold912・fold_fourth_fifth_sixth・fold7/fold8/resolve6/fs13/sv17正本/sv17証明書）が
   repo 出版物として存在し、blob SHA-1 / SHA-256 が機械の pin と一致することを確認した。
2. **fold10 再実行のbyte-identical確認**: 同機械を本実行環境で新規に走らせ、出力 SHA-256 `bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a` が公布値と完全一致（1.4 秒）。
   チェーン上流が手元とrepoで同一bytesで再現できることを vertex として確定。
3. **K1096/K1097 正本のフィールド照合**: g07 主張 4 行・第三法集計・win16 footprint（root 8003180: intrinsic == claimed）・residual23 不交差を正本と突合してから機械に組み込んだ。
   初稿に `x == 53 == y['passed']` 型の連鎖比較バグ（`53 == True` が偽になる）があったので lint 修正した。

## 本体実装

`fold_win8_root8003180.py`（fold10 機械の完全移行 + 追加 gate 群）:

- チェーン全段の frontier 再計算 6,259/495,507 → cost78c/79c 6,240/493,965 → first 6,236/493,703 → second/third 6,229/493,184 → fourth 6,226/492,970 → fifth/sixth 6,224/492,830 → seventh 6,223/492,762 → eighth 6,222/492,688 → ninth-twelfth 6,213/492,021（incidence 11,826・solved 1,635）→ thirteenth-sixteenth 6,209/491,722（11,818・1,639）→ seventeenth 6,206/491,497（11,810・1,642・residual72）。全段で正本と一致。
- fold10 レコードの被覆行の open 性・記録 cost と worklist の照合・residual72 == residual74 − fold10 target 2 行の差分照合。
- K1096: 18 gate 全再検証・証明書 byte 検証（1,251,923 bytes・34,529 行・sorted unique・header 行）・root 幾何（8石・共円 quadruples 0・D4 正準・合法手 53 を venue の法手導出コードを exec で呼んで独立再導出）。
- K1097: 27 gate・footprint partition（49 行 exactly-once）・residual23 と不交差。
- **被覆幾何 2 方法**: (A) 8 D4像 × C(8,2) 2石除去 = 224 操作 (B) C(8,6)=28 部分集合直列挙。canonical 行集合が完全一致した（28 行）。
- 分類: root の 6 石部分幾何 28 canonical 行を open-frontier / closed-before-this-receipt / not-in-worklist に分類。

## 結果

- receipt は **open 5 行**を閉じた: K1097 主張 4 行（5親 target 内・c2 行）+ **target 外 open 行 `0000000000000000380000000800000c`**（cost 83・同じ C(8,6) 28 部分集合幾何に内在・宣言ノートの予想「追加行は余剰として記録」どおり）。
- closed edge cost 387・frontier 6,206/491,497 → **6,201/491,110**・solved S6 1,642 → 1,647・incidence 11,810 → 11,803（影響 3 parent・完全閉鎖 0）・5親 target 40 → 44/112・残余 72 → 68。
- 出力 SHA-256 `d7bf2cd53d99d836418678abd172f4d5890d70bf8a90633b1e434b784bf7e50e`。同一 cwd 2 回 + 別 cwd・別プロセス・独立 W 複写（FOLD11_W env）1 回の 3 実行で byte-identical。

## 採番

着手時の引き継ぎ資料では次の空き K 番号を K1104 としていたが、出版直前の再取得で並走レーンが y=3 パラメトリック全称証明（K1104・commits `e202d516`〜`9aa9f8e8`・先行宣言 `b7a9f7c6`）を取得していたため、
AGENTS.md 規約（衝突側が再採番）に従い items ディレクトリの tree 走査・README grep・list_commits の 3 点で K1105 空きを確認し **K1105** として出版した。

## 未着手・次の一手（宣言不要の未着手領域）

- 残り 15 WIN8 候補（win16 footprint の他根）の証明書抽出と fold。着手時に単一オーナー宣言を要する。
- 残余 68 行の refsolve（第5ラウンド再解決）。
- K1103 の 149 根二手応答被覆計画の item 化（並走宣言済み対象のため着手しない）。

## 解釈規約

REFUTED-D10 は LOSS 証明ではない。WIN8-D10 は root のゲーム木のみを証明する。fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。
pn/dn・nodes 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
