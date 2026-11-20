# 研究log: fold16 WIN8-D10 receipt fold root 8890020（2026-11-20）

単一オーナー宣言（commit `d6a65fff`・先行出版）に基づく実行記録。
前段: 直前の同一レーン実行で fold14 出版正本（`fold_win8_root9090022.py`）の隔離 W からの完全再構築・byte-identical 再現（RC=0）と K1113（root 8890020 証明書抽出・21,446 行・三重検証）の出版までを実施。並走実行は fold15（K1115・root 120000038・residual 58 → 55）を 04:14Z に出版したため、本 fold は当初の「fold15」呼称から **fold16（第23 receipt・6番目の WIN8 receipt fold）** に再採番した。fold16 は K1113 証明書の receipt fold であり、fold15 正本（residual-55 baseline）の続きに接続する。

## 事前検証

1. **最新 main の確認と着手権**: fold15 出版（commit 1832fe7a02・宣言 3f149dc3）と K1113 抽出出版（267f19668f・K1113 README 弾丸 d021a60eb3 の一段前）を確認。並走の「independently audit K1113 fold16 geometry preflight」（4f4d9702・K1113/K1114 の fold 幾何事前監査）は宣言と矛盾しない監査記録であることを確認の上、root 8890020 fold16 の単一オーナー宣言ノートを先行出版（commit d6a65fff2c）。同ノートは fold15 出版後の baseline（残余 55 → 51・5親 target 57/112 → 61/112・frontier 6,173/488,954）に更新してある。
2. **fold15 材料の取得と SHA 照合**: fold15 正本（20,759 bytes）を repo raw から取得し git blob SHA-1（`c02f87810c7be4141e3e7c89553203f5ce114441`）と SHA-256（`bae2b3c182da6b0b06be530604f43d1bfa3bf008190860dad6d27f2b9c285aef`）を K1115 README 62 行目の記載値と照合（一致）。fold15 機（SHA-256 `03000c14…`）・K1114 監査正本（`ab8cd535…`）・K1114 証明書（`5a135903…`・1,171,958 bytes）も raw 取得し SHA-256 合致を確認の上、隔離 W（W15tree）の既構築チェーン材料に追加配置。
3. **K1113 材料の再照合**: K1113 監査正本（`b8c264e6…`）と証明書本体（`105e1e2a…`・775,317 bytes・21,446 行）は前実行で raw から SHA 照合済みの W15tree 在庫（map.txt 24 行対応表）を再計算で確認。
4. **宣言ノートの事前計算とその範囲**: root の C(8,6)=28 canonical join と fold15 正本の残余 55 行（5親 target）の交差は主張 4 行ちょうど（K1113 g07・K1097 footprint と一致）。target 外 open 行との交差は（fold11〜15 と同様に発生しうるため）宣言段階では機械判定に委ねると明記済みで、実際に target 外余剰 1 行が閉鎖・分離記録された。

## 本体実装

`fold_win8_root8890020.py`（fold15 機械の移行型・883 行・約 47 秒）:

- フォールド連鎖: fold11 chaining（fold11 機 rerun gate 継続）→ fold12 chaining（隔離 W 複写 rerun gate）→ fold13 chaining（同左）→ fold14 chaining（同左・6,179/489,440・residual 58）→ **fold15 chaining: 被覆 6 行 open 性・cost 照合・frontier_after 出版値（6,173/488,954・solved 1,675・incidence 11,753・s6_needed 4,481・cost_needed 355,402）・residual55 == residual58 − fold15 主張 3 行・closed target 57 を全 gate 一致**。
- **fold15 機械 byte-identical rerun gate**: W 隔離複写（shutil.copytree）+ FOLD15_W env で fold15 出版機械を再実行し、出力 SHA-256 が出版正本 `bae2b3c1…` と一致。fold15 機内の fold14 rerun gate が再帰的に走り（fold14 → fold13 → fold12 → fold11）通算 6 機連鎖 rerun・12 機実行でも 47 秒に収まった。
- K1113: 19 gate 全再検証。**g07 は 4 行版 gate 名に差し戻し**（`g07_k1086_root_claimed_coverage_4rows`・`== 4` 定数・`recorded.k1086_claimed_coverage_rows` 二重照合）し、g01 K1086 master SHA pin（`3045e152…`）・g05 mobility 50・g06 uncapped probes 575,570/409,407 と terminal 石数範囲 [14,18]・g13 nodes 4,424,758/4,424,758・g16 第三方法 miss 0/extra 0/failure null・g19 footprint（claimed 4 行・k1097 SHA pin）・証明書 byte 検証（775,317 bytes・21,446 行・sorted unique・header・root 行）・root 幾何（8石・quadruples 0・D4 正準・合法手 50 の独立再導出）。
- K1097: 27 gate・footprint partition（49 行 exactly-once・root 8890020 は intrinsic == claimed == 4 行〔K1097 win16 未着手 8 根の nodes 資料と一致〕）・主張 4 行が residual55 内・residual23 と不交差。
- **被覆幾何 2 方法**: (A) 8 D4像 × C(8,2) 2石除去 = 224 操作 (B) C(8,6)=28 部分集合直列挙。canonical 行集合 28 行が完全一致。
- 分類: open-frontier 5（本 receipt で閉鎖）・not-in-worklist 22・closed-before-this-receipt 1（`00000000000000003800000008003000`）。

## 結果

- receipt は **open 5 行**を閉じた:
  K1113/K1086/K1097 主張 4 行（target 内）`00000000000000889002000000100000`（cost 74）・`00000000000000889002000080000000`（cost 67）・`00000000010000809002000000100000`（cost 81）・`00000000010000809002000080000000`（cost 75）+
  **target 外 open 1 行** `00000000000000801222000100000000`（cost 82）（unswept・c2×2 需要行・同じ root の C(8,6) 部分集合幾何に内在）。
- closed edge cost 379・frontier 6,173/488,954 → **6,168/488,575**・solved S6 1,675 → 1,680・incidence 11,753 → 11,743（影響 4 parent: 全 c2〔20→18・21→19・42→39・60→57〕・完全閉鎖 0）・5親 target 57 → 61/112・残余 55 → 51。s6_needed 4,481 → 4,476・cost_needed 355,402 → 355,023。
- win16 候補は 11 → 10 根（主張 32 → 28 行）。残余23行掃引計画は不変。
- 出力 SHA-256 `edd552588e265ada1cf015b4359584288cca3f18686c0fc8ca1536b6458b969b`（20,963 bytes）。
  同一 cwd 2 回 + 別 W 複写・別プロセス・別 HOME 1 回の 3 実行で byte-identical（`cmp` で検証・GATE FAILED 0）。
- 計測: 1 実行（6 機連鎖 rerun・fold15→fold14→fold13→fold12→fold11 の再帰 rerun を含む全 gate）46.9 秒（user 42.1 秒）。

## 実装上の注記

- fold15 → fold16 の移行定数: g07 gate 名差し戻し（`3rows` → `4rows`）・`len(CLAIM) == 4`・g19 `len(claimed) == 4`・g05 `mobility_50`・g06 probe nodes 575,570/409,407・g13 nodes 4,424,758/4,424,758・証明書 21,446 行 775,317 bytes・third_method 集計（root_first_moves 50・terminal 7,653・visited 48,855・winner 31,320・loser 9,882・loser_reply_edges 43,837）・base 定数（fa15・closedAllNew 57・残余基数 55・solved 1,675 基準）。
- **転写ミス 1 件を gate が捕捉**: PIN256 の fold15 正本 SHA-256 を一時 `bae2b3c1…da0b…` と転写（正は `…da6b0b…`）したとき、初回実行が `input sha256 mismatch` で即座に fail-close した。repo raw 再取得・README 記載値との照合で修正後に 3 実行とも完走。fail-closed 設計の実効性を実証した失敗記録としてここに残す。
- K1116 採番の 3 点確認（実施時刻・直近 HEAD）: repo README / knowledge README とも grep 0 件・items dir に K1116 接頭辞 0 件・list_commits に K1116 なし。
