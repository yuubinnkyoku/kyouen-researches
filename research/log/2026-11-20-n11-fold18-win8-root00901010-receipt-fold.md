# 研究log: fold18 WIN8-D10 receipt fold root 00901010（2026-11-20）

単一オーナー宣言（commit `b5e1d5f69425512d09cce62fb443b2733f3b0308`・先行出版）に基づく実行記録。
前段: 同一レーン実行で K1120（root `00000000000000801202000000901010`・残余48行レーン最安価未着手根・probe 439,470・主張3行）の盲抽出・三重検証・19 gate 監査・出版（commits `1137901d`+`d2678e4d`+README弾 `07f66ca1`）までを実施した。本 fold はその K1120 証明書の receipt fold であり、fold17 正本（残余48 baseline・residual-48 lane）の続きに接続する。第25 receipt・8番目の WIN8 receipt fold。

## 事前検証と着手権

1. **最新 main の確認と着手権**: fold17 出版（K1118・commit sequence 既刊）と K1120 出版を確認し、fold18 を宣言するレーンがいないことを確認した上で単一オーナー宣言ノートを先行出版（commit `b5e1d5f6`・04:51:03Z）。宣言後、並走レーンが残余48行レーンの別8石root `00000000000000043800000008180010`（K1091系・probe 882,327/1,054,873・主張3行）の証明書抽出を宣言した（commit `bda9e5b2`・04:55:34Z）が、抽出と receipt fold は経路不競合。fold19 候補（K1119 主張4行・K1121 root `…8d10000` 主張3行の receipt fold・いずれも K1120/並走抽出証明書が fold18 正本 residual-45 に chain する）は本実行時点で誰も宣言していない。
2. **K1120 材料の再検証**: 本レーンが出版した K1120 証明書本体（484,892 bytes・13,422行・SHA-256 `d6745edbc77a53bbef66e807fd18e69c039e3007345af906452af11d3206cbe1`）と監査正本（SHA-256 `ea6f1945c5a8ff359b93336a0a5d4e29035928447503e2bf2f0d13277174b516`・19 gate）を W18 に pin。fold18 機は 19 gate 全 detail 定数（g01 pin `335eca5e…`・g05 mobility 45・g06 probes andclose1 198,622 / andclose0 240,848（両順序 uncapped・loss=true・終端石数 [14,18]）・g07 主張3行〔`00000000000000003800100008002000`・`00000000000801202000000101000`・`00000000000801202000000900000`〕・g13 nodes 631,539/524,342・g16 third_method 集計〔terminal 4,336・visited 30,999・winner 20,028・loser 6,635・応手辺 28,516〕・g19 K1097 pin `2896deb0…`）を正本から抽出して定数化した。
3. **隔離 W（W18）の構築**: 前実行の W17tree 系譜（fold11〜17 機・チェーン正本一式）を複写し、K1120 材料（certs・監査正本）を追加。43 input pin（12 blob SHA-1 + 31 SHA-256）を複写後に再計算で全検証（bad=0・約11MB）。

## 本体実装

`fold_win8_root00901010.py`（fold17 機の移行型・1,000行・約186秒）:

- 生成方法: build_fold18.py 変換スクリプト（全38置換が出現回数 assert 1 で機械検証）で fold17 機から生成。差し替え: ROOT_HEX・OUT・CERT_RELPATH・PIN256 追加3件（fold17 正本・K1120 監査正本・K1120 証明書）・fold17 chaining + rerun gate 追加・K1117 gate ブロックを K1120 gate ブロックに全面差し替え・root 幾何（合法手45の独立再導出）・K1097 crosscheck の residual48 参照・open48/residualSet48 適用・solved 基準 1,687・closedAllNew 基準 64・controls 追加（55項目）。
- **fold17 機 byte-identical rerun gate**: W 隔離複写（FOLD17_W env・subprocess）で fold17 出版機械を再実行し、出力 SHA-256 が出版正本 `1175244d…` と一致。fold17 機内の fold16 rerun gate が再帰的に走り（fold16 → fold15 → … → fold11）通算 8 機連鎖 rerun。
- K1120 19 gate 再検証・証明書全文 byte 検証（sorted-unique・合法手45再導出・D4 正準・quadruple-free）・K1097 27 gate・win16 footprint root 00901010 行の intrinsic == claimed == 3 行・49 行 exactly-once partition・residual23 と win16 主張の不交差・主張3行が residual48 内。
- **被覆幾何 2 方法**: (A) 8 D4像 × C(8,2) 2石除去 = 224 操作 (B) C(8,6)=28 部分集合直列挙。canonical 行集合 28 行が完全一致（refsolve `coverage_of82` と同一規約）。

## fail-closed 捕捉 2 件（fold17 機からの転写起因・出版前修正）

1. **g01 系 SHA リテラル打ち間違い**: fold17 機の `335eca5e…` リテラルをK1120ブロックに転写する際1文字打ち間違え（`…b78991823…`）。初回実行の `k1120 k1095 master sha pin` gate が即座に捕捉（Rerun途中で SHA 照合不成立=強制失敗）。正 `335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707` に修正。**SHA定数は正本から機械で取得する運用**がK1120抽出監査で確定しており、本件はその通算2例目の実効捕捉。
2. **frontier_after 参照漏れ**: fold17 機の frontier_after 計算4行の参照変数 `open51` を `open48` に差し替え漏れ。初回実行は gate を素通りしたが、実行結果の数値照査（6,161−4=6,157 であるべき箇所に fold16 値 6,168 が出現）で発見。機械修正のうえ初回成果物は廃棄、3実行をやり直した。**出版正本は修正後のみ**。

## 結果

- receipt は **open 4 行**を閉じた:
  K1120/K1095/K1097 主張 3 行（target 内）`00000000000000003800100008002000`（cost 74・unswept・c2×2）・`00000000000801202000000101000`（cost 71・unswept・c2×2）・`00000000000801202000000900000`（cost 68・unswept・c2×2）+
  **target 外 open 1 行** `00000000000801202000000100010`（cost 81・unswept・c2×2・同じrootのC(8,6)部分集合幾何に内在）。
- closed edge cost 294・5親 target 64 → 67/112・残余 48 → **45** 行・frontier 6,161/488,094 → **6,157/487,800**・solved S6 1,687 → 1,691・incidence 11,729 → 11,721（影響4 parent・いずれもclass 2: 15→14〔1行〕・19→17〔2行〕・59→57〔2行〕・37→34〔3行〕・完全閉鎖0）・s6_needed 4,469 → 4,465・cost_needed 354,542 → 354,248。
- 6石部分幾何28行: open-frontier 4（本receiptで閉鎖）・not-in-worklist 23・closed-before-this-receipt 1（`00000000000000003800000008003000`・K1096/fold11閉鎖済み）。
- win16 候補 9 → 8 根（主張 25 → 22 行）。残余23行掃引計画は不変。
- 出力 SHA-256 `18b543c45c98c22297fd31b8060971aa90e92826f494acb27ad94ce869250026`（22,049 bytes）。
  同一 cwd 2回 + 別 W 複写・別プロセス・別 HOME 1回の 3 実行で byte-identical（`cmp` で検証・GATE FAILED 0）。
- 計測: 1 実行（8機連鎖 rerun・K1120 19 gate・45手root全再検証を含む全 gate）約 186 秒。

## K1122 採番の 3 点確認（実施時刻 05:12Z・最新 HEAD `fe32c0fa`）

repo README・knowledge README とも grep 0 件・list_commits 15 件（04:55Z 以降の並走 K1058 系 none/n11 系）に K1122 なし・items dir に K1122 接頭辞なし（knowledge README 最新main取得で K1121 まで確認）。並走の最新宣言（`bda9e5b2`・04:55:34Z）は root `00000000000000043800000008180010` の抽出で fold18 と経路不競合。

## 解釈規約（不変）

fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。WIN8-D10 はこの8石rootのゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
