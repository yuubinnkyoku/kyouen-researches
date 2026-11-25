# K1284 実行 log — z1ラダーδ4/δ5確定（T-L4z1・L-Z5F・T-LS2〔C-LS2解決〕・T-IIz1-2〔C-IIz1-2解決〕・T-ALPHA・床G4z2/W411/BC5）

- 日付: 2026-11-24（Vibe 高速レーン・定時自律実行）
- 対応宣言ノート: `research/log/2026-11-24-z1-delta45-ladder-single-owner-note.md`
  （出版 66f06ad2・訂正 c5709b87）
- 対応機体: `research/experiments/z1-delta45-ladder-20261124/`
  （出版 35706ae6・公式成果物 9c21ec47）
- K item: `research/knowledge/items/K1284-z1-delta45-ladder.md`

## 内容（成果サマリ）

1. **T-L4z1**: ∀j>=1・arm-1 mixed Y・max(Y)>=j+2 ⟹ H(2j+4;Y;1)=0。
   z1-δ4 の arm-1 高域が値 0 で全称確定。K1283 explore2 の open
   候補 C-L4z1（high-gap arm-1 → 0）の直接解決かつ強化
   （(j+1)-トークン保持の class-II 型高域まで含む。C手子は
   high-gap で T-L3=0 → 1・class-II で T-II>=2 → 1 XOR (>=2) ∉ {0}）。
2. **L-Z5F**: ∀m>=1・U⊆[m+2,∞)・max(U)>=m+3 ⟹ H(2m+5;(m,U);1)≠0。
   0-witness は w>=m+3 を w−1>=m+2 へ動かす min 保持子で、子が
   **同一行**の z1-δ4 高域（= T-L4z1(m) = 0）を直接踏む「行内
   自己消費」構造。T-L4z1(m)〔L-Z5F(m−1) を使用〕→ L-Z5F(m)
   〔T-L4z1(m) を使用〕の行ラダーで循環なし（宣言ノート §2.6）。
   K1283 L-Z1F の「C手子で直前 z 面を消費」と対比される新機構。
3. **T-LS2（C-LS2 解決）**: ∀j>=1: H(2j+3;(j,j+2);1)=2 ちょうど
   〔opts = {C: 1 XOR T-H1 = 0・stair (j,j+1): T-H2 special = 1・
   fall (j−1,j+2): T-L4z1(j−1) = 0}〕。行1は B手子 v(3,2,4)=0
   （BC5-S）で同型。
4. **T-IIz1-2（C-IIz1-2 解決）**: ∀m>=2 クラスE@z1-δ3 = 2 ちょうど
   〔opts = {C: 1 XOR T-E = 1・stair/compress: T-H2 generic/T-E1 =
   0・fall: T-L4z1(m−1) = 0} で {0,1} 両側出現〕。落下子は
   (m−1, m^{q−1}, E′) で全 E′ トークンが m+1=(m−1)+2 以上ゆえ
   T-L4z1 の拡張形（max>=j+2）が必須（high-gap 版では閉じない）。
5. **T-ALPHA（K1283 open 観測 (a) の完全解決）**: arm-1 mixed Y@
   (2m+3, z1): **H=2 ⟺ Y=(m,m+2)、他はすべて 1**（(m,m+1) は
   compress 子 allm (m^2) → T-E1 = 0 で 1）。行1は W411・G4z2・
   v(x,2,4)=0 の床処理。
6. 新規床: **G4z2**（4z2 multi min>=2 → 0）・**W411**（(1,1)@4z1
   → 0）・**BC5**（v(x,2,5)=1 x>=3・v(x,2,4)=0 x>=2・multi
   min>=2@5z2 は C手子 1 XOR F5 = 0 ∈ opts で ≠0）。
7. open 登録: **C-Z5F1**（δ5 値=1 予想・census 480 点全 1・本項は
   ≠0 のみ主張）・**C-PC1z1-d4**（z1-δ4 pure-c1 族・census 30 点
   c=1→1・c>=2→0・a-ladder〔(j,j)@z1-δ3 allm a=2→0〕と
   z0-δ3-pure-c1 が blockers）・**z0-δ4 arm-1 census**（値 {0,1} の
   み・2 不在・234 点・C-II2 の fall 子資料として主張せず登録）。

## 出版・監査の記録（publish-then-execute）

1. 最新 main 確認: HEAD 観測 a9dba61e →（宣言push時）70d79714。
   直近コミットはすべて Part CY/CP/DH/DA（batch-28/29/31 探査
   レーン）と K1283/K1282 出版群で本トピックと非接触・対抗宣言
   なし。K1284 空き（items に K1284-* 不在・K1283 item 出版済み
   を直接アクセスで確認）。
2. **commit 66f06ad2**: 宣言ノート先行出版。初回 push 試行は
   並走レーンとの fast-forward 競合（"Update is not a fast
   forward"）で失敗。レールに従い無理せず HEAD 再取得のうえ
   再試行して成功。競合の状況はノート訂正に honest記録。
3. **commit c5709b87**: 宣言ノート訂正（公式実験前・宣言期待値
   不変）。§3 の探査 E1 記載 hist {0:860} が実出力
   explore_k1284.out の {0:812} と不一致（tall-giant 48 点が探査
   スクリプトの hist 集計対象外。bad 配列空・860 点全て 0。
   機体 D1 の宣言 l4_hist {0:860} は最初から正しい）だったのを
   修正。push 競合の訂正記録も追記。
4. **commit 35706ae6**: 機体出版（README・verify_k1284.py〔sha
   377acf93…・engine pin bd5f22e4… ゲート内蔵〕・engine_block.py
   〔582c93c1…・K1283 kit と同一 bytes〕・exploration 2 ファイル・
   output/dryrun1-4.json+.info）。fetch-back 13 ファイル +
   訂正済み宣言ノート、全て sha256 byte 一致を確認。
5. **公式実行（fetch-back 機体から）**:
   - 4 走すべて rc=0・stdout byte-identical・sha256
     `703199490ea26659ab458d8498d94a9c3de45912d647451fadd6b93f2de0e64c`
     （同一 cwd PYTHONHASHSEED=random/1 ×2 + 隔離 tree
     /tmp/k1284-iso3/-iso4 env -i PYTHONHASHSEED=99/7 ×2・
     /usr/local/bin/python3 3.12.14・HOME=/tmp・~3.8s/走）。
   - counts `[860,480,43,858,2506,683,420,463,4800,2007]`・
     total 13,120・bad 0・l4_hist {0:860}・z5f_hist {1:480}・
     alpha_hist {1:2499,2:7}〔2 側は (m,m+2) 7 点のみ〕・
     ls2_val j=1..11 全 2・engine_gate PASS。宣言値と完全一致。
   - 変異電池 7/7 期待どおり fail-closed: engine rc=2
     （mutated sha `0ea47a80…` ≠ pin）・l4 bad=860・z5f bad=480・
     ls2 bad=11・ii12 bad=810・alpha bad=2506・fl bad=322
     （すべて rc=1・宣言の期待値と一致）。
6. **commit 9c21ec47**: 公式成果物出版（audit_run1-4.json+.info・
   tamper 7 ファイル・detcheck.json〔verdict OFFICIAL-PASS〕・
   MANIFEST-sha256 29 files）。17 ファイル直接 fetch-back sha 照合
   + MANIFEST 収録全ファイルの個別 fetch-back 照合で不一致 0。

## 受入判定

OFFICIAL-PASS。宣言した全期待値（stdout sha・counts・hists・
変異電池の挙動）が fetch-back 機体からの公式実行で再現され、
証明は宣言ノート §2 に全文収録・13,120 点の機械照合が bad 0。
K1283 が open 登録した C-LS2 と C-IIz1-2 がともに肯定的に解決
され、(α) クラスの一般値と explore2 候補 C-L4z1 も閉じた。

## 規約・11×11 への接続

- verdict 不消費・11×11 空盤の UNKNOWN は不変・Part CY/CP/DH/DA
  レーン（batch-28/29/31）と完全非接触。
- z1 サブツリーの O(1) 評価化が δ4/δ5 まで拡大: arm-1 δ4=0・
  (m,U) δ5≠0・δ3 は arm-1（完全分類）とクラスE（=2）。巨大
  レーン（11×11・z>=2 ストリップ）への枝刈り利用は記録のみ
  （採用判断は各レーンオーナー）。

## 次課題

1. **K1285 一次候補: z1-δ4 pure-c1 族 (j,(j+1)^c) の全称証明**
   （C-PC1z1-d4・census c=1→1・c>=2→0）。必要な前工程:
   (j,j)@z1-δ3 allm a=2 → 0（a-ladder）と z0-δ3 pure-c1 ≠1
   （純カウントラダー）。2つとも未解決でどちらが先に壊れても
   本予想は伸びる。
2. C-Z5F1（δ5 高域の値=1）: z0-δ4 分類（C4b 領域）が鍵。
   z0-δ4 arm-1 census（値 {0,1}・2 不在）はその資料。
3. z1-δ3 arm-2 の精確値・allm-δk ラダー（T-E1 の δ3 版）・
   z>=2 面（z=2 帯端シフト・K1279/K1280 ストリップ接続）。

## honest 記録

- 初回宣言 push の fast-forward 競合（並走レーンとの同時書込み）。
  HEAD 再取得後に成功・無理な押し込みはせず、状況を訂正
  コミットに記録した。
- 宣言ノート §3 の E1 探査 hist 記述の不正確（{0:860} vs 実出力
  {0:812}）。公式実行前に transparent な訂正コミット c5709b87 で
  修正。機体側の宣言値は最初から正しく、訂正で変更されたのは
  provenance 記述のみ。
- dryrun1-4 は宣言前のローカル 4 走で byte-identical（sha
  70319949…）を確認済みで、公式 4 走と同一の stdout。
- explore_k1284.py の E1 hist 集計は tall-giant 48 点を除外して
  いる（スクリプト由来の集計範囲の偏り。bad 配列は全 860 点
  を検査しており空＝全点 0）。
