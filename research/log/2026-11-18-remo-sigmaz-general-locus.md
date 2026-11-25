# 2026-11-18 σ_Z(M,·) 値1軌跡の一般構造・ONE-CHAR全M一般化・素数M法則（K0946）

K0945（remo-sigmaz3-fold）の直接続き（同ログの次候補2「σ_Z(M,K)の
一般MへのRUN-M/FOLD拡張」を実行）。高速レーン。branchなし・main直接出版。
K0946として出版。

## 発見順

1. **着手判断**: K0945の次候補のうち「一般MのRUN拡張」が情報価値最上位
   （K0945はM=3に固定で、ONE-CHARのM=3固有の証明が一般Mで成り立つかが
   最初の問い）。並走はK0944/K0945を取得済みのためK0946で出版。
2. **RUN-UNIV**: M=3のRUN-3（runはs=u−1フェーズ・打ち切り不能）の一般M版。
   run中のkの最小値がk_t+1=K−s ≥ M+2 > Mとなること（s ≤ α₀−1）で
   割り算レジームに入らずrunが常にsフェーズ完走するのが一般Mの本質。
   tailはE(M; κ, M(s+1))・κ=K mod (M+1)。K0945では「k>3は常に成立」
   だった部分をM任意で証明した点が新規。
3. **ONE-CHAR-GENERAL**: K0945のM=3証明（積分性4ℓ_m=3K−1+v_mの場合分け）
   はM=3固有だったため、一般Mには後方チェーン引数を新規構築。
   wrapが1つでも残るとσ_{k_t} ≥ κ+1+k_t+1 > k_t−1で矛盾すること
   （NO-WRAP-RECOVERY）は値1⟺全面silentをM一斉に確定する。
   K0945 ONE-CHARはM=3の場合として回収。
4. **EXCL-2**: κ=M−1（K≡M−1 mod M+1）のtail第1フェーズはbumpで
   σ_tail=MがI ≡ −1 (mod k_t)を要求するがI ≤ k_t−2で不可能。
   K0945 A2-NEVER（M=3, K≡2 mod 4）の全称一般化。
5. **EXCL-1**: κ=Mのtailはbump後 E(M+1; M(s+2)−1, 0)（均一game）に
   帰着し、σ_tail=M+1 ⟺ I=0。U0-NEVER（σ_E(M+1;Mt−1,0)≠0）への
   帰着を確定。U0-NEVERは未証明・機械検証（JS 1,769・pinned 315状態）。
6. **M1-EMPTY・DEG**: M=1は値1不可能（σ_{K−1}∈[0,K−2]）。退化K≤Mの
   閉形式（σ_Z(M,2)=1 ⟺ M偶数・σ_Z(M,3)=1 ⟺ M≡2 mod 3・
   σ_Z(M,M−1)≠1）を紙上証明。
7. **PRIME-M・PARITY・スペクトラム（機械）**: M≤40・K≤10⁵の完全掃引
   （fast engine・pinned照合はK≤1200全M）で、非退化軌跡非空が素数Mと
   完全一致（合成数とM=1は全て空）。深部: M∈{2,3,5,7} K≤10⁶・
   M=8,9 K≤4×10⁵・M=15,25 K≤3×10⁵。素数M≥3のヒットは全て偶数。
   (M+1)|K divisibility lawはM∈{2,3,5}のみ（素数M≥7の最初の非整除
   ヒットを列挙）。旧「M+1素数⟹空」観察は死んだ（分類変数はM自身）。
   深部M=11 [10⁵,2×10⁵] は1,305ヒット全偶数。
8. **classify**: ONE-CHAR-GENERALの予言するsilent性（σ_tail=κ+1・
   cascade 0）を全素数M∈{2,...,23}・K≤20000の全ヒットで確認（0例外）。
9. **検証器**: sigma_locus_core.js（naiveポート+literal engine+fastの
   3実装・audit/div3/locusモード・決定的）+ audit_build.py（COREPIN+
   node audit+pinned相互検証→output/sigma_locus_audit.json・
   2回cold実行byte同一・監査sha256
   edfe71c3574b06af3424ebf6327bac6283d715b14f6ff4ce002ba0d01aefa5e9・
   26秒/実行・all_ok=true）。
10. **出版**: 単一コミットで実験dir 6ファイル・item・README bullet
    （K0945 bullet直後）・本ログ。push前に最新main（995a1c76）を再取得し
    K0946が空きであることを確認。K0945と同一のFAST算法は再主張しない
    （report.mdに分工記載）。

## 次の候補

1. U0-NEVERの全称証明（σ_E(P;n,0)の生存位置の閉形式分類から始まる。
   参考データ: σ_E(P;n,0)=0の解はP≤24・n≤300に100個あるが
   n ≡ −1 (mod P−1) のものは0件）→ EXCL-1昇格。
2. PRIME-Mの機構: ONE-CHAR-GENERALによりPRIME-Mは「M合成 ⟹ 全
   (κ,s)でσ_E(M;κ,M(s+1))≠κ+1」と書き直せる。tail→bump→
   E(M+1;·,·)再帰の合同条件を書き下ろしM合成の障害物を同定する。
3. PARITY法則の証明（奇素数Mで奇数κが全滅する2進機構）。
4. 一般MのU_M冪減衰の比較（M∈{2,3,5,7}のK≤10⁶データで減衰指数を推定）。
