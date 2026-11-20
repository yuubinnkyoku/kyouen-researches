# 研究log: fold19 WIN8-D10 receipt fold root 1009000（2026-11-20）

単一オーナー宣言（commit `3a23ccf30bfe1634dcbb4fc53d08b0f8c8b297c1`・先行出版）に基づく実行記録。
前段: 同一レーン実行で fold18（K1122・root `00901010`・残余 48 → 45）を出版（commits `ff10d824f9` + index `dc99280809`）。本 fold は並走レーン出版の K1119 証明書（root `00000000000000801212000001009000`・16,262 行 587,989 bytes・SHA-256 `b4dd1e06…`・19 gate 監査正本 `4696ce14…`・実験 `n11-residual51-win8-cert-extract-root1009000-20261120`）の receipt fold であり、fold18 正本（残余45 baseline）の続きに接続する。第26 receipt・9番目の WIN8 receipt fold。

## 事前検証と設計決定

1. **300秒timeout問題と rerun-gate 再設計**: fold18 機（8 機連鎖再帰 rerun・約186秒/実行）を 300 秒 bash 上限の環境で安全に再実行する術が本レーンの課題だった。fold19 着手前に設計ノート `d3dbc614`（fold19 共有案: rerun gate を「直前機のみ1回再実行」に狭め、上流は SHA pin + チェーン全段 frontier 再計算で検証する FOLD_PREVERIFIED_CHAIN）を検討し、**本レーン実行で正式採用**（採用ノート出版 commit `fbea3ecc`）。fold11〜fold17 機の再帰 rerun 連鎖を fold19 機から削除しても fail-closed 検証内容は減らない: 上流の全正本・証明書・監査は SHA-256 pin で固定され、チェーン各段の frontier・残余は fold19 機内で毎回全再計算・出版値照合される。
2. **preverified 写しの生成と検証**: fold18 出版機（SHA-256 `dcdfbf92…`）は逐語保存し、通すのは marker-reversible な preverified 写し（`make_preverified_patch.py` が自動生成・SHA-256 `d342f1f8…`）。reverse patch が出版機 SHA-256 と厳密一致すること、`FOLD_PREVERIFIED_CHAIN=1` のときのみ rerun gate 群をスキップすること（guard マーカー `FOLD_PREVERIFIED_CHAIN_GUARD` BEGIN/END で範囲固定・デフォルト挙動は完全連鎖機と同一）を機械検証した。実測で preverified fold18 機は**1.56 秒/実行**で fold18 出版正本（`18b543c4…`）を byte-identical 再現した。旧環境の 186 秒のうちチェーン rerun 部分がほぼ全ての所要時間だったことがここで確定した。
3. **隔離 W（W19）の構築**: fold18 系譜の W を複写し、fold18 正本・K1119 監査正本・K1119 証明書本体の 3 ファイルと fold18 出版機（pristine）・preverified 写しの 2 機械を配置。46 input pin（12 blob SHA-1 + 34 SHA-256）を機械実行時に全照合（bad=0）。
4. **fold19 機の生成**: `build_fold19.py`（全置換が出現回数 assert で機械検証・stale 定数 grep・py_compile・ast 解析）で fold18 出版機から変換生成（1,028 行・約3.0秒/実行）。fold11〜17 再帰 rerun gate ブロック削除・fold18 chaining + preverified rerun gate 1 件挿入・K1120 gate ブロックを K1119 ブロックに全面差し替え（全定数は K1119 監査正本から機械取得: g01 master pin `edd7ac84…`・g05 mobility 44・g06 uncapped probes andclose1 192,365 / andclose0 229,502〔loss=true・終端石数 [14,18]〕・g07 主張4行・g13 nodes A1 865,602 / B 712,106・g16 miss 0/extra 0・g19 K1097 pin `2896deb0…`・third_method〔terminal 5,783・visited 37,696・winner 24,352・loser 7,561・応手辺 34,261〕）・root 幾何（合法手44独立再導出）・open45/residualSet45 適用・solved 基準 1,691・closedAllNew 基準 67・win16 8→7 根/22→18 行会計。
5. **出版前レビューで転写ミス 1 件を捕捉**: 証明書来源の説明文字列（K1097 claims_record）に fold18 由来の「intrinsic == claimed == 3 rows」が残っていた。root 1009000 の正しい値は 4 行で、gate は最初から 4 行を検証していたため数値への影響はないが、変換スクリプトに当該置換を追加して機械を再生成し、3 実行 byte-identical をやり直した（出版正本は修正後のみ）。fold18 の2件（SHA リテラル打ち間違い・frontier_after 参照漏れ）に続く通算3例目の転写系捕捉で、今回は gate 以前の文字列レビューでの発見。

## 結果

- receipt は **open 5 行**を閉じた:
  K1091/K1119/K1097 主張 4 行（target 内）`00000000000000003800200008001000`（cost 72・unswept・c2×2）・`00000000000000003800200009000000`（cost 78・unswept・c2×2）・`00000000000801212000000001000`（cost 78・unswept・c2×2）・`00000000000801212000001000000`（cost 74・unswept・c2×2）+
  **target 外 open 1 行** `00000000000801212000000008000`（cost 80・unswept・c2×2・同じrootのC(8,6)部分集合幾何に内在）。
- closed edge cost 382・5親 target 67 → **71/112**・残余 45 → **41** 行・frontier 6,157/487,800 → **6,152/487,418**・solved S6 1,691 → 1,696・incidence 11,721 → 11,711（影響4 parent・いずれもclass 2・完全閉鎖0）・s6_needed 4,465 → 4,460・cost_needed 354,248 → 353,866。
- 6石部分幾何28行: open-frontier 5（本receiptで閉鎖）・not-in-worklist 23・closed-before-this-receipt 0。
- win16 候補 8 → **7 根**（主張 22 → 18 行）。残余23行掃引計画は不変（全win16主張と不交差を機械再確認）。
- 出力 SHA-256 `c02d9a549fb685a1310813e47726598417907fe1e007495b06799ec0b57052ae`（22,898 bytes）。
  同一 cwd 2回 + 別 W 複写・別プロセス 1回の 3 実行で byte-identical（`cmp` で検証・GATE FAILED 0）。
- 計測: 1 実行（46 pin 照合・チェーン全段 frontier 再計算・preverified fold18 rerun 含む全 gate）**約3.0 秒**（旧 fold18 機の約62分の1）。採用ノートの事前試算 150〜180 秒は保守的すぎた。fold20 以降の receipt fold 実行は全てこの系譜で数秒になる。

## K1128 採番の 3 点確認

最新 main で K1127 までの出版（高速レーン・y=6 族パラメトリック全称証明・index commit `73d8e825e5`）を knowledge README・recent commits・items dir（git tree API で items K1128 接頭辞なし）で確認し、K1128 を fold19 item に採番した。fold19 と経路を競合する並走声明はなし。

## 解釈規約（不変）

fold は行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 はこの8石rootのゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
