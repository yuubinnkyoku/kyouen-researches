# 研究log: fold17 WIN8-D10 receipt fold root 22081000（2026-11-20）

単一オーナー宣言（commit `7f824364`・先行出版）に基づく実行記録。
前段: 同一レーン実行で fold16（K1116・root 8890020・残余 55 → 51）の出版までを実施。並走レーンは fold16 完了の 3 分後（04:26Z・commit bf5fcbee）に K1117（root `00000000000000801202000022081000`・並走宣言 22eb87df からの抽出・三重検証・19 gate）を出版した。本 fold はその K1117 証明書の receipt fold であり、fold16 正本（residual-51 baseline）の続きに接続する。第24 receipt・7番目の WIN8 receipt fold。

## 事前検証

1. **最新 main の確認と着手権**: K1117 出版（bf5fcbee・item/log 6eedf44d・README弾 b66dd5e8）を確認し、fold17 を宣言するレーンがいないことを list_commits で確認した上で、単一オーナー宣言ノートを先行出版（commit 7f824364）。並走の K1117 README 弾・実験 README に「fold時は別工程」と明記されていることを確認し、fold17 の着手権は本レーンに確定した。宣言直後の最新 HEAD（93f56291）で並走が別 root `00000000000000801212000001009000`（K1091系・主張4行）の証明書抽出を宣言したが、これは receipt fold とは経路不競合。
2. **K1117 材料の取得と SHA 照合**: K1117 証明書本体（341,498 bytes・9,460 行・SHA-256 `f62f6704a0d9a1366d333529dd9e742813fe87814f3857a00406d6cfc87f3c8f`）と監査正本（`3d97ac6d90e239638b019c95218f0051b432ccdcc6dd2d25e805dcbab11024d9`）を repo raw から取得し SHA-256 照合（一致・README 出版値とも一致）。K1117 実験 dir の `.input-k1095.json`・`.input-k1097.json`・runner_v17.ts・監査機・検証器・抽出器も取得（fold16 同様 rerun gate 用ではなく参照記録として）。
3. **隔離 W（W17tree）の構築**: 前回実行で構築・検証済みの W15tree（完全 W・fold11〜16 機・fold16 正本・K1113/K1114/K1115 材料・map.txt）を複写し、K1117 材料（k1117/certs・k1117/output）を追加配置。fold16 正本の SHA-256（`edd55258…`）を複写後に再計算で確認。
4. **K1117 監査正本の解析**: 19 gate の全 detail 値（g01 K1095 pin `335eca5e…`・g05 mobility 39・g06 probes andclose1 126,683/andclose0 137,565・g07 主張3行 `00000000000000003800000808001000`・`00000000000000801202000000081000`・`00000000000000801202000020001000`・g13 nodes 731,232/534,121・g16 miss 0/extra 0・g19 footprint 3 行 + k1097 pin）を抽出し、recorded.third_method 集計（root_first_moves 39・terminal 3,282・range [14,18]・visited 23,542・winner 15,228・loser 5,032・loser_reply_edges 22,031）を確認して fold17 機の期待値定数とした。
5. **宣言ノートの事前計算とその範囲**: 余剰行の予測は宣言段階で機械判定に委ねると明記（fold16 の実例では主張 4 行+余剰 1 行。fold15 では宣言ノートの「主張 3 行のみ」予測が余剰 3 行を見落としていた過去があり、target 外 open 行の混入は fold11 以降全 receipt で発生しうる）。実際に target 外余剰 4 行が閉鎖・分離記録された。

## 本体実装

`fold_win8_root22081000.py`（fold16 機械の移行型・943 行・約 95 秒）:

- フォールド連鎖: fold11 chaining（fold11 機 rerun gate 継続）→ fold12 chaining（隔離 W 複写 rerun gate）→ fold13 chaining（同左）→ fold14 chaining（同左）→ fold15 chaining（同左・6,173/488,954・residual 55）→ **fold16 chaining: 被覆 5 行 open 性・cost 照合・frontier_after 出版値（6,168/488,575・solved 1,680・incidence 11,743・s6_needed 4,476・cost_needed 355,023）・residual51 == residual55 − fold16 主張 4 行・closed target 61 を全 gate 一致**。
- **fold16 機 byte-identical rerun gate**: W 隔離複写（shutil.copytree）+ FOLD16_W env で fold16 出版機械を再実行し、出力 SHA-256 が出版正本 `edd55258…` と一致。fold16 機内の fold15 rerun gate が再帰的に走り（fold15 → fold14 → fold13 → fold12 → fold11）通算 7 機連鎖 rerun・fold16 機は約 47 秒で再現。
- 生成方法: mkfold17.py（変換スクリプト・全置換が出現回数 assert 1 で機械検証・構文 AST 検証済み）で fold16 機から生成。差し替え: ROOT_HEX・OUT・CERT_RELPATH・PIN256 追加 3 件（fold16 正本・K1117 監査正本・K1117 証明書）・fold16 chaining + rerun gate 追加・K1113 gate ブロックを K1117 gate ブロックに全面差し替え（g01 K1095 pin・g07 3行版 gate 名〔`g07_k1095_root_claimed_coverage_3rows`・`== 3` 定数〕・g05 mobility_39・g06 probes 126,683/137,565・g13 731,232/534,121・証明書 341,498 bytes/9,460 行・third_method 集計）・root 幾何（合法手 39 の独立再導出）・K1097 crosscheck の residual51 参照・open51/residualSet51 適用・solved 基準 1,680・closedAllNew 基準 61・controls 追加。
- K1097: 27 gate・footprint partition（49 行 exactly-once・root 22081000 は intrinsic == claimed == 3 行〔K1095 掃引系候補〕）・主張 3 行が residual51 内・residual23 と不交差。
- **被覆幾何 2 方法**: (A) 8 D4像 × C(8,2) 2石除去 = 224 操作 (B) C(8,6)=28 部分集合直列挙。canonical 行集合 28 行が完全一致。
- 分類: open-frontier 7（本 receipt で閉鎖）・not-in-worklist 21・closed-before-this-receipt 0。

## 結果

- receipt は **open 7 行**を閉じた:
  K1117/K1095/K1097 主張 3 行（target 内）`00000000000000003800000808001000`（cost 73・unswept・c2×2）・`00000000000000801202000000081000`（cost 66・unswept・c2×2+c4×2）・`00000000000000801202000020001000`（cost 74・unswept・c2×2）+
  **target 外 open 4 行** `00000000000000801002000002081000`（cost 64・c4×1）・`00000000000000801002000002102000`（cost 64・c4×2）・`00000000000000801002000022002000`（cost 70・c4×1）・`00000000000000801202000020080000`（cost 70・c2×2+c4×2）（同じ root の C(8,6) 部分集合幾何に内在・余剰 4 行は WIN8 receipt 史上最多）。
- closed edge cost 481・frontier 6,168/488,575 → **6,161/488,094**・solved S6 1,680 → 1,687・incidence 11,743 → 11,729（影響 6 parent: c2 18→15〔3行〕・c4 79→76〔3行〕・c2 49→48〔1行〕・c4 67→64〔3行〕・c2+c4 50→48〔2行〕・c2 37→35〔2行〕・完全閉鎖 0）・5親 target 61 → 64/112・残余 51 → 48。s6_needed 4,476 → 4,469・cost_needed 355,023 → 354,542。
- win16 候補は 10 → 9 根（主張 28 → 25 行）。残余23行掃引計画は不変。
- 出力 SHA-256 `1175244d1da269b1851d5298a824b12a6ed445edc99307acc9c0fefd803bd674`（22,925 bytes）。
  同一 cwd 2 回 + 別 W 複写・別プロセス・別 HOME 1 回の 3 実行で byte-identical（`cmp` で検証・GATE FAILED 0）。
- 計測: 1 実行（7 機連鎖 rerun・fold16→fold15→…→fold11 の再帰 rerun を含む全 gate）94.4 秒（user 84.9 秒）。

## K1118 採番の 3 点確認（実施時刻・直近 HEAD 93f56291）

repo README・knowledge README とも grep 0 件・list_commits 40 件に K1118 なし・items dir に K1118 接頭辞なし。並走の最新宣言（93f56291・commit 04:33:41Z）は別 root `00000000000000801212000001009000` の抽出で fold17 と経路不競合。

## 解釈規約（不変）

fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 はこの8石rootのゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
