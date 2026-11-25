# K1283 実行 log: z1 面の確定 — H2 全称証明・T-B1 無条件昇格・δ2 行完全分類・δ3 非零/クラスE 下界（2026-11-24・Vibe 高速レーン）

## 0. 事前確認（毎回の規約どおり）

- 最新 main・AGENTS.md・knowledge README・未解決事項を確認。
  宣言直前の観測 HEAD: 5855e3f8（2026-11-24T06:21:47Z・Part CY
  drive-2 takeover 宣言）。K item の最大番号は K1282（K1283 空き）。
  直近コミットは batch-28/29/31 第三実装交叉検証レーン（Part
  DH/DA/CY）と K1282 出版群で、z1/H2 系の対抗宣言なし。
- 前回セッション（K1281/K1282 の流れを引き継いだ同一実行内）で
  z1 側の解析・機体製作・dry run まで完了していたのを引き継ぎ、
  本 log は出版フェーズ（宣言→公式実行→出版）を中心に記録する。

## 1. 数学的内容（宣言ノート = 証明の正本）

- **T-H2**: ∀m≥1・mixed: H(2m+2;X;1)=min(Σ,2m+2)%2（H=1 ⟺
  X=(m,m+1)）。K1281 仮説 H2 の全称証明。
  - 鍵 (1): min 落下子は常に arm-1 mixed であり C手子
    1 XOR T-H1(j) = 0 から **L-Z1F** が無条件非零を供給。
  - 鍵 (2): 特別形の落下子 (m−1,m+1) は (j,j+2) 形で **L-S** が
    ≥2 を供給（stair 子 = T-H2(j) special = 1 ∈ opts）。
  - 鍵 (3): 行1基底 H2(1) が床分類（F4/F3 + 新規 **G3z2**・
    **B2z3**・v 系）の直接場合分けで閉じる（F14b 非依存）。
- **T-E1**: ∀m≥1・a≥2: H(2m+2;(m^a);1)=0。落下子は z1-δ3(m−1)
  （budgey 2m+1 = 2(m−1)+3）で arm-1 mixed → L-Z1F ≥1・C手子
  1 XOR T-Q-allm = 1 → 0 ∉ opts。**K1281 走査メモの「落下子 =
  z1 前線(m−1)」は予算計算誤りであり訂正記録**（値への影響なし）。
- **系 T-B1′**: K1281 II-1′/II-2′/II-3′ を H2 → T-H2・
  T-B0(i) → T-B0′（K1282）でそのまま再利用。行内順序
  P1-band → P1-diag → Q1 → T-H2 → T-E1。循環なし。z1 帯+対角
  崩壊・前線分類が ∀m≥2 で無条件。
- **T-N0z1**（K1281 観測 (c) の全称化）: z1-δ3 mixed ≠0。
  arm-1/arm-2 は C 経由（T-H1/T-LC）、クラスE は stair/compress
  子が T-H2/T-E1(m) で 0、行1 mult(1)≥2 は A 子経由。
- **T-IIz1**: z1-δ3 クラスE ≥2（C=1 XOR T-E = 1 ∈ opts +
  0-witness）。値 =2 は **C-IIz1-2 として open**（census 790 点
  全て 2）。

## 2. 機体・publish-then-execute の遂行

| フェーズ | commit | 内容 |
|---|---|---|
| 宣言ノート | c075b512 | 単一オーナー宣言（観測 HEAD 5855e3f8・対抗なし・定理全文 §2・protocol D1–D10・宣言値事前登録）。fetch-back byte 一致（sha256 feaecdf6…） |
| 機体出版 | 536921ff | verify_k1283.py (16,317B・sha256 ca515dfe…) + engine_block.py (pin bd5f22e4…) + exploration（E1–E10・E9 G3z2 (1,1)→2 例外捕捉）+ dryrun 4 本 + MANIFEST-sha256。fetch-back 12 ファイル照合・verify と engine はローカルと byte-identical |
| MANIFEST 訂正 | 52939752 | MANIFEST 内のパス接頭辞（ローカル構成 explore/out → repo 出版構成 exploration/output）を repo 相対表記に修正。sha 値は不変・中身 hash 変更なし |
| 公式実行 | （local-only） | fetch-back 機体から 4 走: 同一 cwd×2（PYTHONHASHSEED=1・random）+ 隔離 tree /tmp ×2（env -i・PYTHONHASHSEED=99・7）。rc=0×4・stdout 4 本とも byte-identical・sha256 cf182f24…=宣言想定と完全一致 |
| 変異電池 | （local-only） | 10/10 検出・宣言どおり: engine rc2（mutated sha 0ea47a80…≠pin bd5f22e4…）・h2 6,947・e1 56・q1 2,940・band 3,388・lzf 4,278・ls 14・n0 650・ii 790・g3 4,355 |
| 成果出版 | 44215dad | audit_run1-4.json・run1-4.info・tamper 記録 10 ファイル・detcheck.json・MANIFEST-sha256（30 files・repo 相対）。fetch-back 抽査照合（audit_run1.json/detcheck.json sha 一致） |
| 出版 (D) | 本 commit | K item + 本 run log + knowledge README 末尾 bullet（純 append・sha/wc 照合） |

- 実測: counts [6,947; 64; 2,976; 3,388; 4,278; 21; 650; 790;
  8,757; 5,820]・総計 33,691・bad 0・h2_ones 7〔(m,m+1) コーナー〕
  ・n0_hist {1:454, 2:196}・ii_hist {2:790}。宣言値と完全一致。
- 付帯観察: tamper_n0.out は dryrun1.json と byte 一致（ともに
  D7 の (h==0) 述語という同一の誤検知構造。dryrun1 が捕捉した
  初版バグと tamper n0 の宣言された変異が同一述語にあたると
  いう整合の副産物）。

## 3. honest 記録

1. dryrun1: D7 の比較演算子が初版では `(h == 0) != flip` と
   すべき所を誤実装しており、宣言値との突合で bad=650 として
   検出（fail-closed モデルが意図どおり作動した実例）。修正し
   dry2 以降 green。
2. 宣言前探査 E9: 初版 G3z2 草稿（multi → 常に 1）に対して
   (1,1)@3z2 = 2 の例外を捕捉（bad=1・FAIL 行を explore1.out に
   残置）。床分類を「(1,1)→2・(2,) single→2〔=v(2,2,3)〕・他→1」
   に修正して機体に反映。行1基底の (1,2) special の B 子
   (2,)@3z2 = 2 として理論と整合。
3. T-E1 の落下子の座標は予算計算の訂正版（z1-δ3(m−1)・L-Z1F
   経由）を宣言ノート §2.3 に明記。K1281 時点の走査メモの誤記は
   値・機械監査に無影響。
4. dryrun3.info は当時の stderr 取得漏れで不在（時刻情報のみの
   欠落・audit JSON 本体は 3/4 本とも byte 一致で保存）。
5. MANIFEST にローカル構成のパス接頭辞が残っていたのを fetch-back
   照合で検出し repo 相対表記に訂正出版（52939752）。sha 値不変。

## 4. 受入判定

- すべての宣言値（counts・hist・stdout sha・変異挙動）が公式
  実行で完全再現。fetch-back 機体からの実行（最強プロトコル）。
- **受理**: T-H2・T-E1・T-B1′・T-N0z1・T-IIz1・L-Z1F・L-S・
  G3z2・B2z3・v 系・行1基底を定理として昇格。
  C-IIz1-2・C-LS2・(α) generic 値・z1-δ3 allm・z1-δ4+・z≥2 面
  ・純カウントラダー・F14b は open 登録（過大主張なし）。
- verdict 不消費・11×11 UNKNOWN 維持・z10/z11 ストリップレーン
  とは非接触。

## 5. 次課題

1. **z1-δ4(m−1) の開拓**（C-IIz1-2 / C-LS2 の fall 子 ≠2 確認）
   — クラスE 値 = 2・L-S 値 = 2 の精密化が着地する。
2. **(α) クラスの値の構造化**（z1-δ3 arm-1 一般形・census
   {1:454, 2:196} の分岐則）。
3. **z1-δ3 allm** の分類。
4. z≥2 面（z=2 帯端シフト）・純カウントラダー・F14b。
5. 11×11 giant レーンへの構造補題接続（採用判断は giant レーン
   オーナー・本レーンは記録のみ）。
