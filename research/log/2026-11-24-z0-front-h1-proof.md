# K1282 実行 log: z0 面の確定 — H1 全称証明による T-B0 無条件昇格・LAW-C/δ3/δ4/II/E 定理パッケージ — 宣言→機体→公式監査→出版

- 実行: 2026-11-24（Vibe 高速レーン・定時自律実行）
- 宣言ノート: `research/log/2026-11-24-z0-front-h1-proof-single-owner-note.md`
  （出版 89a8b438・観測 HEAD 4db1ffcb・K1282 空き・対抗宣言なし）
- 機体出版: `research/experiments/z0-front-h1-proof-20261124/`
  （2ca77ca6・11 ファイル・公式実行より前に凍結）
- 監査成果物出版: 同一実験 dir に audit_run1-4.json・run1-4.info・
  detcheck.txt・tamper 記録 16 ファイル・MANIFEST-sha256
  （commit 79163e48）。

## 主結果（K1281 残課題1前半の完了）

**T-H1（無条件全称定理）**: ∀m≥1・z0-δ2 arm-1 mixed
（min(X)=m・mult(m)=1・max>m）⟹ H(2m+2;X;0)=1。

鍵の発見: 行帰納の段消費が**行1の基底事実のみ**で閉じる。
行 m の δ2 arm-1 の落下子 (m−1,U) は行 m−1 で必ず high-gap
（(m)=（m−1)+1 トークンが不在・ j 個のアームは値 ≥m+2）になり、
その値 0 を T-L3(m−1) が 0-witness として供給する。圧縮子は
行 m−1 前線 mixed→2（T-Q）・階段子は行 m−1 クラスII→≥2（T-II）。
mex{0,2,…}=1。T-L3/T-Q/T-II/T-E/T-LC は互いに行 m−1 インスタンス
と行1基底 J1–J5（H1(1)/L3(1)/B46/F14/II(1)）・床分類 F0–F6
（予算≤4）から帰納で確定し、サイクルが閉じる。

**系 T-B0′**: K1281 T-B0 の結論（z0 帯 R∈[m+1,2m]+対角崩壊
H(R;X;0)=v(Σ,0,R)・前線 R=2m+1 分類）が**無条件定理**に昇格
（K1281 II-1/II-2/II-3 を再利用し H1 を T-H1 で置換・前線 m=2 は
T-Q が拡張）。z0 面は予算全域で確定。

同時確定した定理（宣言ノート §2 に証明全文）:

- **T-Q**: ∀m≥2・z0 前線 R=2m+1: mixed→2・allm a≥2→0
  （K1281 T-B0(ii) の m≥3 からの m≥2 拡張・H1 不要化）。
- **T-LC**: ∀m≥2・z0-δ2 mixed: arm-1→1・arm-2→1・mult≥2 それ
  以外→0（旧 LAW-C の定理化）。
- **T-L3**: ∀m≥1・z0-δ3 R=2m+3 high-gap arm-1 → 0。
- **T-C4**: δ4 R=2m+4・arm-1 で ≥(m+3) トークンあり → ≠0
  （gap=2 でも ≥(m+3) ありなら ≠0 を含む）。
- **T-II**: クラスII（δ3 arm-1 で (m+1) トークンと ≥(m+2) トークン
  あり）→ **≥2**（=2 までは open 予想 C-II2）。
- **T-E**: z0-δ2・mult(m)≥2 mixed 非 arm-2 → 0。

## 主張の区分（明確化・過大主張なし）

- 全称証明: T-H1・T-Q・T-LC・T-L3・T-C4（≠0 まで）・T-II（≥2 まで
  精確）・T-E・T-B0′・J1–J5・F0–F6。
- open（宣言ノートに登録済み）: **C-II2**（クラスII 値=2 予想・
  census 916 点全て 2）、allm-δk（k≥2）一般則、純カウント・ラダー
  （(2,3)@k3=1・(2,3,3)@k3=0・(2,4)@k4=0・(2,4,4)@k4=1 が根拠
  観測・explore_ladder.out 1,236 行）、H2/z1 側全般、F14b。
- census（42,725 点・bad 0）は定理の実機照合であり証明の代替ではない。

## 公式監査（宣言 protocol D1–D10・fetch-back 機体から走行）

- fetch-back 照合: published verify_k1282.py の sha256
  7b70993a…（byte 一致）・engine_block.py = pin bd5f22e4…
  （PROVENANCE PASS）。公式走行は fetch-back した出版物を隔離
  tree にクローンして実行（最強プロトコル）。
- 公式 4 走（同一 cwd×2〔PYTHONHASHSEED=random/1〕・隔離 tree +
  env -i×2〔random/99〕）すべて rc=0・**stdout byte-identical**
  （sha256 b2600e453a2a78e0a92e47f7591d79379dd074a3f5c19a86538d6afc9a8f85c8
  = 宣言ノート §3 の想定と完全一致）。~8.3-8.5s/走
  （05:26:41Z〜05:27:18Z）。
- counts=[6,348; 2,976; 7,686; 4,256; 1,599; 916; 2,916; 1,134;
  12,293; 2,601]・**総計 42,725 点・bad 0**・ii_hist {2:916}
  （宣言点数と完全一致・4 走同一）。
- 変異電池 8/8 検出・すべて宣言時予告どおり:
  --tamper-engine → rc=2（0ea47a80… ≠ pin・sha ゲート作動）。
  --tamper=h1 → rc=1 bad[0]=6,348。q → bad[1]=2,940。
  lawc → bad[2]=4,746。lawc-arm2 → bad[2]=2,940。l3 → bad[3]=4,256。
  e → bad[6]=2,916。ii → bad[5]=916。

## honest 記録（機体 dryrun・kit README 参照）

1. dry0（記録なし・fail）: ENGINE_SHA pin 定数の転写 typo を sha
   ゲートが AssertionError で捕捉（ゲート実証を兼ねる）。pin 修正。
2. dryrun1: D9 β3z1 期待値誤り（min≥2 multi @3 z1 → 0 は既刊
   K1269 側分類なのにコードが誤期待）。bad 1,087 を検出 → 床分類
   を F4 どおり修正。
3. dryrun2: singles-v-ord 照合タプル構築バグ（(x,x) を検査して
   いた）。bad 601 を検出 → (x,) に修正。
4. dryrun3: 全 green・stdout sha b2600e45…= 宣言想定。

## 飛び先（次の候補・優先度順・open registered）

1. **H2 の全称証明**（または反例）: T-B1 が無条件昇格し z1 面が
   完成する。z1 行1基底の確定が出発点（行帰納が z1 側でも
   行1で閉じるかが本項T-H1構造の直接の対称テスト）。
2. **C-II2**（クラスII 値=2）: ≥2 まで証明済み・残りは 1 排除。
   compress/stair 子の値の精確化で閉じる可能性。
3. allm-δk（k≥2）の一般則（純カウント・ラダーの構造化）。
4. z≥2 面への拡張（z=2 帯端シフトの一般形・K1279/K1280
   ストリップとの接続）。
5. 11×11 giant への接続: T-B0′/T-LC/T-E の O(1) 枝刈りを
   z0 サブツリー評価に実装するかは別レーン（構造補題は記録済み）。

## 規約

- 11×11 空盤・19 central-reply roots・二石 root・S2 {59,60}・
  class 群は **UNKNOWN 維持**（verdict 不消費・検証点数を勝敗と
  して読まない）。
- z10/z11 ストリップレーン・n11 CQ レーン・11×11 giant は非接触。

## honest 記録（出版側インシデント・一連の commit にも記録済み）

6. **knowledge README truncation 事故と修復**: 出版 (D)（commit 705dcd87）で
   K item・run log は byte 一致で無傷だったが、knowledge README
   （1,008,655B = 元 1,003,768B + K1282 bullet 純append）の push が
   読み取り側のバイト上限（~37.5KB/チャンク）で切れた 63,749B の
   前置断片で上書きされていた。直後の curl fetch-back（wc -c）で
   検出し、next_offset チャンク連結（17 chunk・JS 628,446 chars =
   Python 628,444 codepoints + 𝓜 U+1D4DC 2 個のサロゲートペア差
   を機械確認）で全量を復元し、修復 commit 1c2103bb として再出版。
   修復後 fetch-back sha256 5ea4d945… がローカル正本と byte 一致
   （cmp 全 nbytes PASS）。切れっぱなし期間は 705dcd87〜1c2103bb の
   約2分。以後の運用メモ: KB 級超ファイルの push は読み取り
   chunk 連結 + 全文字数照合 + push 後 fetch-back wc/sha の
   3点検を必須とする。
