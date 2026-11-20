# 単一オーナー宣言ノート: 残余29行レーン WIN8-D10 root `0000000800000000380000000810000a` 証明書抽出（g19プロトコル拡張宣言つき）

本ノートは、検証可能な小証明を積み上げる11x11長期レーン（残余29行）の衝突防止のため、下記作業の単一オーナーを宣言する先行出版物である（AGENTS.md の first-published-priority 規則に従う）。

- 宣言日時 (UTC): 2026-11-20T09:14:25Z
- 宣言時点の main HEAD: `3bd83c63118ef697cc62556c02a3ab589e7ed437`
- 対象作業: K1095（残余72行 代替12根 depth-10掃引正本・schema `n11-residual72-replace12-d10-sweep-20261120-v1`・SHA-256 `335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707`）が両AND順序 uncapped でWIN8-D10候補として確定した根 **`0000000800000000380000000810000a`**（8石 [1,3,20,27,59,60,61,99]・quadruple-free・D4正準・probe nodes andclose1 1,226,804 / andclose0 1,416,679・既に事前計算でroot loser mobility 58 を確認）の完全勝利戦略証明書（n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS）の盲抽出・三重検証・出版。残余29行レーンの3候補（候補A root `00000000000000043800000008180010` = K1136 出版済み・候補B/C root `00000000000200003800200008180000` = K1137 出版済み）のうち残る1根であり、本抽出の出版で残余29レーンの全候補の証明書が出版済みとなる。
- 旧宣言の更新（supersede）: 残余72行時代の旧宣言 `research/log/2026-11-20-n11-residual72-win8-cert-extract-root0810000a-single-owner-note.md` は未完のまま残っていたため、本ノートがこれを更新（supersede）する。旧宣言にあった応答被覆計画（149-root計画の第2固定根）の文脈は、fold11 が root `00000000000000003800000008003180` の receipt で親行 `00000000000000003800000008001080` を簿計閉鎖した時点で本抽出とは独立の扱いとなっており、本抽出は証明書本体の出版のみを担当する。

## g19プロトコル拡張宣言（本root固有・本宣言の核心）

本rootは、出版probe pinを持つWIN8-D10候補のうち唯一、K1097 refsolve（正本 SHA-256 `2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40`）の win16 intrinsic footprint が `intrinsic_equals_claimed == false` である: claimed 1行 `00000008000000003800000008100000`（== K1095 per_root covered_rows）に対し intrinsic 2行（claimed + `00000000000000003800000008001080`）。余剰intrinsic行 `00000000000000003800000008001080` はK1097 win16計画上はroot `00000000000000003800000008003180` の主張行であって、fold11（18番目receipt・正本 SHA-256 `d7bf2cd53d99d836418678abd172f4d5890d70bf8a90633b1e434b784bf7e50e`）の receipt `covered_five_parent_target_rows` で既に簿計閉鎖済みであり、fold23出版正本（SHA-256 `04f334ff0f6aa995375283e94afc0e83ced6bebfeefea47359a5090a338fad59`）の残余29行内には存在しない（着手前に出版3正本から機械確認済み）。

よって本rootの監査機械の g19 gate は、歴代（K1117/K1120/K1124/K1136/K1137）の「intrinsic == claimed 三点一致」検査の代わりに、次のfail-closed拡張を本宣言に基づいて採用する:

1. claimed == covered == 1行（K1095 per_root `covered_rows` と監査機械自身の root 6石部分幾何計算の一致）。
2. claimed 行 `00000008000000003800000008100000` はfold23出版正本の残余29行 `residual_row_hex_after` 内で open（`residual_target_rows == len == 29` 照合込み）。
3. intrinsic == claimed ∪ {`00000000000000003800000008001080`}（K1097正本 pin と一致・`intrinsic_equals_claimed == False` の記録どおり・claimed ⊂ intrinsic）。
4. 余剰intrinsic行が (a) K1097 でroot `00000000000000003800000008003180` の claimed に含まれ、(b) fold11正本（`.input-fold11.json` としてSHA pin）の receipt covered rows に含まれ、(c) fold23残余29行外であること（3点すべて機械検証）。

本拡張は行の閉鎖主張を一切変更しない。本抽出は行を1つも閉じない。将来の本rootのreceipt foldは別の単一オーナー宣言を要し、fold23残余29内にopenな行はclaimed 1行のみであるため、その簿計対象もclaimed 1行のみとなる。

## 実行プロトコル（K1114/K1120/K1124/K1136/K1137と同一構成）

- verdict基盤の再現: runner v17 repo原本固定コピー（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`・pilot_d6制御 nodes 3,402）で child=`00000008000000003800000008100008`（root − 最小セットビット bit 1）+ bit 1 の両AND順序 depth-10 probe を計4回実行。K1095出版値（andclose1 1,226,804・andclose0 1,416,679・両順序 uncapped loss=true・終局石数 [14,18]）と node-exact 一致を要求する。
- root初手の独立再導出: 純Python整数 3×3余因子幾何でroot loser初手58手を再導出・監査機械 g09 で照合。
- 抽出: K1124系譜の extractor（K1137出版 `cert_extractor_win8_root00000000000200003800200008180000.ts` と探索核同一bytes）をroot引数・filename guardのみ差し替え。Run A1 = 初手ごと新規プロセス58本（xargs -P 4・1実行1ファイル厳守）・Run A2 = A1の完全再実行・Run B = 全58初手を単一プロセスで一括、の3実行で証明書行集合 byte-identical を要求する（fbt_drops==0・fatal/conflict 0）。
- 独立検証3方法: TS BigInt 3×3余因子展開・TS Bareiss 4×4整数行列式・Python第三実装（標準ライブラリのみ・全木再走査）の全集計値一致・consumed union == 証明書行（過不足0）・終端はloser-stuckのみ・終局石数範囲の一致。
- 監査機械: K1137出版機（`assemble_win8_audit_root00000000000200003800200008180000.py`）のroot定数差し替え版（出現回数assertつき変換・K1086→K1095基盤化〔g01 SHA pin・g06 probes・g07 claimed 1行・g08 bit 1〕・mobility 42→58・g19は上記拡張・fold11正本を追加pin）。
- 成果の出版: experiment dir `research/experiments/n11-residual29-win8-cert-extract-root0810000a-20261120/`（README・scripts・outputs・証明書 `certs/win8-root-0000000800000000380000000810000a-20261120.n11`）・知識item（採番はpush直前に3点確認）・研究log・index README bulletの順。機械は同一cwd 2回＋別EXPERIMENT_ROOT別cwd別プロセス1回の3実行で監査JSON byte-identical を要求する。

## 競合処理・進行

他レーンが同一rootの抽出を本ノートより先行出版していた場合、本宣言は無効。fold24（候補Aのreceipt fold・並走宣言済み commit `0c9e174e9c`）・候補Bのreceipt fold（未宣言）はいずれも本宣言の対象外であり、それぞれ別の単一オーナー宣言を要する。失敗・環境消失が起きた場合は本ノートを更新して状況を簡潔に記録し、無理に押し進めない。重要証拠は再現不能なローカル状態に残さない。

foldは行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。
