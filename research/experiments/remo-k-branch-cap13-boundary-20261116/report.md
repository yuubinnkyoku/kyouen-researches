# 3枝REMO決定性のサイズ境界cap≤13拡張（r=3・非坍縮キーは定理Hの22個のまま）

実験: `research/experiments/remo-k-branch-cap13-boundary-20261116/`
日付: 2026-11-16
位置づけ: K0875（定理H12・cap≤12・r=3）のサイズ境界を 12→13 へ伸ばす有限完全列挙。r=3 固定。

## 主張（定理H13・cap≤13・r=3・有限完全）

3枝点族で全枝サイズ C_i≤13・任意γ のとき、生存者決定性が
(sorted sizes, γ) に坍縮しないキーは**定理H（cap≤10）の22個と同一の集合**である。
サイズ境界を 10→12→13 へ広げても非坍縮キーは0個増える。

付随する確定事実:

- 軌道数（正準形プロファイル）は cap 13 で 77,828（Burnside fix(id),fix(trans),fix(cyc)=(432,906, 11,186, 252)、直接正準化列挙と一致）。キー数 1,820（一様決定313・一様非決定1,485・mixed 22）。
- **サイズ13枝を含む455キーはすべて坍縮**。サイズ11枝451キー・サイズ12枝454キーもすべて坍縮（K0875の観察の再確認を含む）。
- 22キーの構造はcap≤10/12と完全不変: 決定側生存者一様 P_1、非決定側可能生存者集合 ⊆ {{1,2},{0,1,2}}、per-key det/ndet/profile 分割は K0876 監査の `sweeps.r3.failing_partitions` と完全一致、K0862 出版witness 44組は本設定でも有効。
- 補題FL（可能第1敗者 == {C_i mod 3}）は **cap≤13 全77,828プロファイルで違反0**（cap≤12観察の拡張）。
- 剰余レンズ（K0872）: 22 mixed キーはすべて剰余対 {0,2}。1剰余キー330個・3剰余キー300個はすべて坍縮。2剰余キーは1,190個で、非坍縮は同じ22個のみ。「非坍縮 ⇒ |L_3|=2」の必要条件観察はサイズ13までアウトオブサンプルで無反例。

## 検証構成

- 列挙・Burnside・verbatim領域ゲーム・Python mask twin は出版済みK0876検証器（packed読み取り修復版・commit c50f31f1）からverbatim抽出。
- スイープレコードは決定的JavaScript maskエンジン（mask_engine_fast.js・K0876系譜）で r=3・正準cap≤13列挙77,828プロファイルを一括生成し、**packed出版形式** `[i, sv_mask, fl_mask, states]`（K0876修復と同一形式・atomsは検証器内の正準列挙で無損失再構成）でコミット。sha256 `47a5eb34f738dc60a74d4ef0c66e54032d7c79f2e3413b47c40dbc56c07df5fd`。最大状態数 48,256（状態総数 294,553,171）。
- 検証器 `verify_remo_k_branch_cap13_boundary.py`（stdlibのみ・決定的・assemble二重実行byte同一）は19機械チェック+3 liveチェックを実施:
  - **交差アーティファクト照合**: 正準列挙の順序保存部分列性（D_12 ⊂ D_13）を用い、D_12 に対応する位置で **K0876出版 r=3 packed レコード47,595件をすべて再現**（sha256ピン付き・0不一致）。さらに K0876 監査JSON（sha256ピン付き）の r=3 22キー分割表と突合。
  - live: cap≤7 全域 2,048 verdicts で verbatim == mask twin == committed records、stride 32 の層化サンプル 2,433 verdicts で mask twin == committed records、K0862出版44 witness をverbatimエンジンで再実行+committed records 突合。

## 再現

```sh
cd research/experiments/remo-k-branch-cap13-boundary-20261116
python3 verify_remo_k_branch_cap13_boundary.py
# -> AUDIT PASSED (18 checks) + LIVE OK x3、audit byte-identical
```

スイープレコードの再生成は `node mask_engine_fast.js profs.json 3 out.jsonl`
（profs.json = 正準cap≤13列挙; 列挙は検証器内蔵の direct_constrained(13) と
byte単位で同一の profile 列を生成する）。

## 限界・interpretation guard

- r=3のみ。**r≥4で枝サイズ11,12,13を含むキーは本項では未走査**（K0876はr=4,5,6・cap≤12; r=7,8は別作業が進行中）。
- **枝サイズ≥14は未走査**で「サイズ8が失敗に必要」はサイズ≤13でのみ確定。非坍縮22キーの構造的特徴づけ（なぜサイズ8か）は未解決のまま。
- 「非坍縮 ⇒ 2剰余」は必要条件の有限観察であり、一般の証明ではない（K0872と同様の位置づけ）。有限観察を全称定理へ昇格させない。
- 11×11空盤はUNKNOWNのまま。順位決定性は本項で扱わない。
