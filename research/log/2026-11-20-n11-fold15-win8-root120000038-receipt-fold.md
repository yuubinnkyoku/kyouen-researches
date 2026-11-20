# 研究log: fold15 WIN8-D10 receipt fold root 120000038（2026-11-20）

単一オーナー宣言（commit `3f149dc3`・先行出版）に基づく実行記録。
前段: 同一実行で K1114（root 120000038 証明書抽出・三重検証・32,470行）を出版済み。
fold15 は K1114 証明書の receipt fold（第22 receipt・5番目の WIN8 receipt fold）。

## 事前検証

1. **K1114 の着地確認**: 出版済み実験 dir（`n11-residual58-win8-cert-extract-root120000038-20261120`・監査正本 5,374 bytes・証明書 1,171,958 bytes）を repo raw から取得し SHA-256 pin（`ab8cd535…`/`5a135903…`）と照合。
2. **着手権の確定**: 最新 main（`8ad76a9ee8`・K1114 README 弾丸）を再取得し、fold15 および代替foldの並走宣言がないことを確認の上、宣言ノートを先行出版（commit `3f149dc3`）。
3. **W15 構成**: チェーン入力 34 pin（fold14 機の PINS/PIN256 表と同一の 12 blob SHA-1 + 22 SHA-256）を全て repo から取得し事前検証（ALL PASS）。追加分: fold14 正本（`ed3159fd…`）・K1114 監査正本（`ab8cd535…`）・K1114 証明書（`5a135903…`）の 3 SHA-256 pin と fold14 機械（rerun gate 用）。fold11〜14 機械 4 本を W 直下に格納。計 37 input pins。
4. **宣言ノートの事前幾何計算（とその限界）**: root の C(8,6)=28 部分集合 canonical join を fold14 正本の残余 58 行（5親 target）と照合し、主張 3 行ちょうどが hit（extras なし・fold14 既閉鎖 5 行と不重複）を確認。root 幾何（8石・quadruple-free・D4 正準・合法手 53）も機械規約そのままで事前確認。**この事前計算は target 交差のみを確認しており、open frontier 全体との交差（target 外 open 3 行）は見ていなかった。**
5. **並走の独立 preflight との照合**: push 直前に並走が出版した `n11-residual58-fold16-k1113-geometry-preflight-20261120`（commit `4f4d9702`・K1113 と K1114 の fold 幾何事前監査）の K1114 エントリは、独立実装で target 交差 3 行 == 主張 3 行・extra_hits 0・claims_all_open を再現しており、fold15 の target 予測と独立に一致。同 preflight は K1113 root との幾何交差 0・主張交差 0 も確認しており、本 fold の 6 行閉鎖（target 外 3 行を含む）は fold16 の K1113 主張 4 行の open 性に影響しない（preflight 側の interpretation guard も「fold16 は fold15 完了後に実 frontier を再照会」と明記）。

## 本体実装

`fold_win8_root120000038.py`（fold14 機械の移行型・825 行・約 23 秒）:

- フォールド連鎖: fold11 chaining（fold11 機 rerun gate 継続）→ fold12 chaining（隔離 W 複写 rerun gate）→ fold13 chaining（同左）→ **fold14 chaining: 5 行 open 性・cost 照合・frontier_after 出版値（6,179/489,440・solved 1,669・incidence 11,765・s6_needed 4,487・cost_needed 355,888）・residual58 == residual62 − fold14 主張 4 行・closed target 54 を全 gate 一致**。
- **fold14 機械 byte-identical rerun gate**: W 隔離複写（shutil.copytree）+ FOLD14_W env で fold14 出版機械を再実行し、出力 SHA-256 が出版正本 `ed3159fd…` と一致。fold14 機内の fold13 rerun gate が再帰的に走り（fold13 → fold12 → fold11）通算 5 機連鎖 rerun・11 機実行でも 23 秒に収まった。
- K1114: 19 gate 全再検証。**g07 は gate 名ごと 3 行版に差し替え**（`g07_k1086_root_claimed_coverage_3rows`・`== 3` 定数・`recorded.k1086_claimed_coverage_rows` 二重照合）し、**g01 K1086 master SHA pin（`3045e152…`）・g06 terminal 石数範囲 [14,18]・g16 第三方法 miss 0/extra 0/failure null を新規に gate へ固定**（機械側からの主張源の紐付け強化）。g05 mobility 53・g06 uncapped probes 825,127/657,152・g13 nodes 2,723,200/2,141,807・g19 footprint（claimed 3 行・k1097 SHA pin）・証明書 byte 検証（1,171,958 bytes・32,470 行・sorted unique・header・root 行）・root 幾何（8石・quadruples 0・D4 正準・合法手 53 の独立再導出）。
- K1097: 27 gate・footprint partition（49 行 exactly-once・root 120000038 は intrinsic == claimed == 3 行）・主張 3 行が residual58 内・residual23 と不交差。
- **被覆幾何 2 方法**: (A) 8 D4像 × C(8,2) 2石除去 = 224 操作 (B) C(8,6)=28 部分集合直列挙。canonical 行集合 28 行が完全一致。
- 分類: open-frontier 6（本 receipt で閉鎖）・not-in-worklist 22（closed-before-this-receipt 0）。

## 結果

- receipt は **open 6 行**を閉じた（初の 53-mobility 候補 fold）:
  K1114/K1086/K1097 主張 3 行（target 内）`00000000000000003800000248000000`（cost 85）・`00000000000000801202000001000100`（cost 76）・`00000000000080003800000048000000`（cost 77）+
  **target 外 open 3 行** `00000000000000801202000020000008`（cost 80）・`00000000010000003800080008000000`（cost 87）・`00000000012000003800000008000000`（cost 81）（unswept・c2×2 需要行・同じ root の C(8,6) 部分集合幾何に内在）。
- **宣言ノートの閉鎖予測（主張 3 行のみ）は過少だった**: 事前計算は残余 58 行（target）との交差しか見ておらず、open frontier 全体（6,179 行）との交差に target 外 open 3 行が含まれていた。機械は fold11（1 余剰）〜fold14（1 余剰）と同様に余剰行を `extra_s6_rows_not_in_target` へ正確に分離記録し、target 簿記（54 → 57・残余 58 → 55）は主張 3 行のみで正確に進んだ。fail-closed 設計では target 判定を宣言や予測に頼らず機械が単独で行うため、予測の過少は出版正文に影響しない（ログに透明に記録する）。
- closed edge cost 486・frontier 6,179/489,440 → **6,173/488,954**・solved S6 1,669 → 1,675・incidence 11,765 → 11,753（影響 4 parent: 全 c2〔13→10・62→59・54→51・40→37〕・完全閉鎖 0）・5親 target 54 → 57/112・残余 58 → 55。s6_needed 4,487 → 4,481・cost_needed 355,888 → 355,402。
- win16 候補は 12 → 11 根（主張 32 行）。残余23行掃引計画は不変。
- 出力 SHA-256 `bae2b3c182da6b0b06be530604f43d1bfa3bf008190860dad6d27f2b9c285aef`（20,759 bytes）。
  同一 cwd 2 回 + 別 cwd・別プロセス・別 HOME 1 回の 3 実行で byte-identical（`cmp` で検証・GATE FAILED 0）。
- 計測: 1 実行（5 機連鎖 rerun・fold14→fold13→fold12→fold11 の再帰 rerun を含む全 gate）23.0 秒（user 20.8 秒）。

## 実装上の注記

- fold14 → fold15 の移行定数: g07 gate 名差し替え（`4rows` → `3rows`）・`len(CLAIM) == 3`・g19 `len(claimed) == 3`・g05 `mobility_53`・g06 probe nodes 825,127/657,152（fold11〜14 の 50/49 手系との差し替え・K1114 監査の fail-closed 教訓〔brc loserMobility 50→53 差し替え漏れ実例〕を引継ぎ二重に固定）。移行ミスは gate が即座に fail する構造。差し替えレスビューで `residualSet62` → `residualSet58` の置換漏れ 1 箇所（`residualAfter` の計算行）を出力前に発見・修正した（この種の見落としは、放置すれば residual accounting gate `len(residualAfter) == 58 - len(targetRows_new)` で必ず fail する）。
- fold14 機の rerun gate の「隔離 W 複写」形式をそのまま継承。fold15 からは fold14 機の隔離 rerun が新たに加わり、再帰 rerun は 5 機連鎖・サブプロセス実行は通算 11 回。

## 解釈規約（不変）

WIN8-D10 はこの 8 石 root のゲーム木のみを証明する。fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。
REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
残り 11 WIN8 候補の抽出・残余 55 行の refsolve・fold16（K1113 root `…889002`）は着手時に単一オーナー宣言を要する未着手領域。
