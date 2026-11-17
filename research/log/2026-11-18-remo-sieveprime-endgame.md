# 2026-11-18 END-SIEVE（エンドゲーム約数篩）とSIEVE-PRIME全称証明・双子法則完全iff全称完結（K0939）

K0937の直接続き（K0937ログの「次の候補」第1項を実行）。高速レーン。
branchなし・main直接出版。K0939として出版。

## 発見順

1. **着手判断**: K0937は残OPENを「t=0エンドゲーム生存のみ」
   （SIEVE-PRIME予想）に特定済み。エンドゲーム（n≤w・ladder regime外）
   の開始状態を分類するのが情報価値最上位と判断した。
2. **END-INVの発見**: エンドゲームの状態はフェーズごとに1人ずつ減る
   のでstretch理論が使えず、かわりに「ptr基準の円が必ず
   E(P;α,β)=[P]^α+[P+1]^β の2ブロック形」であることに気づいた。
   入口census F(w,h;n)（α=n−h・β=h）から遷移を書き下すと
   r<α → E(P+q; α−r−1, β+r)・r≥α → E(P+1+q; β+2α−r−1, r−α)
   でE形が閉じ、監視位置が常に[P+1]block先頭α（V）/pot block末尾
   α−1（U）を保つ。石数恒等式 **N=P(k+1)+β+s**（s=0 V/1 U）が毎
   フェーズ保存される（V: T=N・U: T=N−1のエンドゲーム版）。
3. **END-SIEVE**: 恒等式とP=qk+rから N ≡ r+β+s (mod k)。α+β=kで
   −β ≡ α・−β−1 ≡ α−1 (mod k)なので、監視死亡（r=α（V）/
   r=α−1（U））⟺ **k | N**。エンドゲームは約数篩そのもので、
   円サイズn,n−1,…,2の降下で監視はNの約数（≤n最大）で死ぬ。
4. **ENTRY-LOC**: family状態への到達が問題になった。入口が
   n∈{w−1,w}・h≤min(n,w)（V）/min(n−1,w)（U）であることを
   T下界（直前stretch n′≥wでT≥w²−1）と n≤w−2 の上界
   （T≤w²−2/w²−3）の矛盾で証明。w=2はbase直接ケース。
5. **END-SIEVE-IFF**: family状態では N ≤ w²+2w < (w+1)² なので
   spf(N) ≤ w、n=w−1ではw∤h（V）/w∤(h+1)（U）でspf=wが排除され
   spf ≤ n → 合成Nは必ず死亡。素数N（family最小5）は全円サイズ
   k ≤ n < N でk ∤ N → 生存。**family状態上で監視生存 ⟺ N素数**。
6. **SIEVE-PRIME定理化**: K0937素数側ladder生存定理と組み合わせて
   N素数 ⟹ V(m)=0・U(m)=m−1 が全称証明され、K0937の残OPEN解消。
   K0937 TWIN-COMP-GEN（合成側）+ K0928 RED/系 + ピンP(2)=1 で
   **LAW1/LAW2がmod類制限なしの完全iff全称定理化**
   （P(C)=1⟺C素数・P(C)=C−1⟺C+1素数・C≥2）。
   K0929予想・K0931 SIEVE予想・K0933/K0936類別版をすべて回収。
7. **検証器の構成**: sievegen_core.pyはK0937 committed版のbyte同一
   コピー（tracker・engine・ピン読み込みを再利用）+
   sieveprime_verify.py（7チェック）+ audit_build.py。
   - FAMILY: w≤60全family状態7,198（V 3,553+U 3,645）をリテラル
     位置エンジンで完全プレイし175,086フェーズ・transition 168,922
     照合・死亡合同・iff 全違反0。Eモデル（純算術）と完全一致。
   - ENTRY: 素数m≤200,000両側67,716ゲームでtrackerがエンドゲーム
     到達・入口family形・Eモデル生存・最大入口幅632・違反0。
   - PINREPRO: m≤8,000両側16,000ゲームのコミットU/V表
     （K0929・JS engine産出）を純算術（tracker+ENTRY-LOC+E-model）から
     完全再構成・違反0。
   - ENGINE: 新鮮python engine m≤600両側1,200ゲーム。
   - PINSIEVE: コミット表iff（P表・U/V表・C,m≤8,000）違反0。

## 検証

- sieveprime_verify.py: 7チェック全合格（PIN/REDRECON/FAMILY/ENTRY/
  PINREPRO/ENGINE/PINSIEVE）。
- audit_build.py: 2回in-process実行一致・2回cold実行でbyte同一
  （監査sha256
  07d844c62df54014d8b720a98dbcd51e44dd6e50b52d74c8b05a3e2d03f6a0b3）。
- 独立性: Eモデル（純算術）とリテラル位置エンジン（K0928補題Pの
  独立実装）の相互照合、tracker（出版定理の算術合成）とコミット表
  （K0929 JS engine産出）のPINREPRO照合。

## 出版

- K0939（proved）: 定理END-INV・END-SIEVE・ENTRY-LOC・END-SIEVE-IFF・
  SIEVE-PRIME・LAW1/LAW2完全iff。実験ディレクトリ
  research/experiments/remo-sieveprime-endgame-20261118/
  （report.md・sievegen_core.py・sieveprime_verify.py・audit_build.py・
  output/sieveprime_audit.json）。
- K0937・K0929のstatus更新（SIEVE-PRIME定理化・LAW1/LAW2 proved）。
- READMEにK0937 bullet直後にK0939 bulletを挿入。

## 次の候補

- **合成NのV(m)/U(m)値の決定**: 素数ケース（V=0・U=m−1）は閉じた。
  合成Nでどのラベルが生存するかの closed form（stretch spf(N)−1
  死亡時の以後の展開はendgame E理論で追跡可能なはず）。
- **P(C)閉形式**: P(C)=1⟺C素数・P(C)=C−1⟺C+1素数は完全iffとして
  閉じたが、一般CのP(C)の値の直接式は依然OPEN。
- **r人対戦・d次元版への不変量転写**: END-SIEVEは「石数保存+
  位置合同+約数篩」の構造で、K0906定理J・K0924定理Wと同型の
  ラベル閉包が一般化レジームでも働くか。

## 備考

- K0937と同一セッション系統の継続出版。push前に最新main HEADを再取得し、
  items/でK0939空き・READMEのK0937 bullet位置を確認してから出版。
- AGENTS.mdの統合前確認（uv run tools/knowledge/{check,build}.py・
  unittest）は本実行環境にrepoのcloneとuvがないため未実施。
  generated/とroot READMEは編集していない（次の統合時に再生成）。
