# 2026-11-18 SIEVE構造の全称完結: 不変量INV-TRACKと合成数側死亡定理SIEVE-COMPOSITE-GEN（K0937）

K0936の直接続き（K0936ログの「次の候補」第1項を実行）。高速レーン。
branchなし・main直接出版。K0937として出版。

## 発見順

1. **着手判断**: K0936はspf=7まで類別計算で閉じ、ログ自体が「一般pへの
   帰納構造（分岐パラメータのクラス定数性の不変量論証）を先に定式化する
   方が情報価値が高い可能性」と示唆。m mod 30類を消去する不変量を探した。
2. **不変量INVの発見**: トラッカー座標系（K0936と同一の基礎状態
   V: F(2,1;m−1)・U: F(2,0;m)・いずれもa=1）で全ストレッチ開始状態が
   **a = h（V）/ a = h+1（U）** を満たすことに気づいた。WATCH-MAPの
   4事例（side × r<h/r≥h）を純代数で計算すると、INV条件下ではfront逆
   ケース（a≤r<h）とback逆ケース（a>r≥h）がどちらも発生せず、各事例で
   a2 = h2（V）/ a2 = h2+1（U）が閉じる。帰納完成。
3. **死亡合同式**: T = wn+h+wの保存（基礎値 V: T=N・U: T=N−1）と
   T ≡ h−a (mod w+1)（w≡−1）から、死亡 ⟺ a=r+1 ⟺ **(w+1)|N**。
   spfに一切依存しない。合成Nの死亡stretchはspf(N)−1に決定。
   REGIME補題（合成Nではstretch 2..p−1でt≥1がT下界で強制）で
   「死亡前にendgameへ落ちない」も閉じ、SIEVE-COMPOSITE-GEN全称証明完成。
   spf≥11に依存していた双子法則の残りmod 210類を含む合成数側がすべて
   定理化（TWIN-COMP-GEN）。
4. **t=1ギャップの解消**: K0935 watchmapはt≥2限定が唯一の残ギャップ。
   位置計算でt=1でもcensus・INV関連a2公式が同一であることを証明し、
   全t=1グリッド（w≤11）をミニエンジン（stretch_sim）で照合。
   重要な副産物: (i) t=1では(e)判定（死亡⟺a=r+1）は一般に偽
   （反例 (5,0,8,5): breaking敗者w−rのhot死）→死亡判定を排出集合判定
   death_fastで再実装しengine全域照合。(ii) 非INV窓ケースのa2はt=1で
   崩れる（270偏差・back式はn2超過）→INV関連距離のみ主張と明示。
   (iii) K0936 death_infoのcollapse stretch block-1死亡held=w+2は
   engine真理（held=w）と不一致になる実装特性を特定
   （K0936はtrack()がw≥6で打ち切るため未到達・published結果は無影響）。
5. **素数側の残渣の正確化**: 素数Nではladder部分の生存が上の合同式から
   即座に全称証明され、未解決は**t=0エンドゲーム生存のみ**と特定
   （SIEVE-PRIME予想として分離・m≤2,600 engineで全確認）。
6. **検証器の構成**: sievegen_core.py（出版core verbatim + 新規4道具:
   stretch_sim・watchmap_ext・death_fast・track_gen）+
   sievegen_verify.py（12チェック）。トラッカーがO(1)遷移になったため
   **INVGEN: m≤200,000両側・3,680万stretch entry**（K0936のm≤700から
   285倍）まで0失敗で走査。最大死亡stretch 630（spf=631・631²=398,161）
   を観測。engineアンカーはm≤2,600（死亡stretch≤70・86,615 entry・
   t=1 stretchを含む）。

## 検証

- sievegen_verify.py: 12チェック全合格（PIN/REDRECON/T1MAP/T2REG/
  DEATHFAST/INVGEN/FRESHPIN/CANON/TRK/SIEVEOBSGEN/SV7REG/TWINCOMP）。
  TWINCOMP: C≤8000の合成2,993+2,993で0違反（K0936 TWIN210の全類版）。
  SV7REG: K0936のstretch-5/6法則をengineで回帰。
- audit_build.py: 2回in-process実行一致・2回cold実行でbyte同一
  （file sha256
  5281e92e221ffd589b56dc712e2ad76308d12c51c792496d2216ee3657c761d2）。
- 独立性: トラッカーはLAD-GEN/WATCH-MAP（出版定理）の算術合成、
  engine（play_full/stretch_sim）はK0928 Lemma Pの独立実装。両者の
  全stretch照合（CANON/TRK）がt=1含むで一致。

## 出版

- K0937（proved・素数側は予想として分離）: 定理INV-TRACK・死亡合同式・
  SIEVE-COMPOSITE-GEN・TWIN-COMP-GEN・素数側ladder生存定理・予想
  SIEVE-PRIME。実験ディレクトリ
  research/experiments/remo-sievegen-composite-20261118/
  （report.md・sievegen_core.py・sievegen_verify.py・audit_build.py・
  output/sievegen_audit.json）。
- READMEにK0936 bullet直後にK0937 bulletを挿入。

## 次の候補

- **SIEVE-PRIME予想の攻撃**: t=0エンドゲーム（n≤w・pot≥n+1の非ラダー
  regime）の構造解析。t=1/t=2境界の状態の形状（F族からの連続性）から
  endgame開始状態を分類し、監視位置の不変量を探す。素数側が閉じれば
  双子法則の逆方向（C素数⟹P(C)=1）も全称化されP(C)の閉形式に到達。
- **collapse stretch W_{w+2}(w−1)の一様状態**: N=(w+1)²のU側死亡が
  collapseとして分類された。N=平方数のV側・U側の死亡形の対照表。
- **一般化R/D人対戦・d次元版**: INVが「石数保存+監視位置合同」の
  構造であるため、r人版・高次元版でも同型の不変量が存在するか。

## 備考

- K0936と同一セッション系統の継続出版。push前に最新main HEAD
  （9d884650・n11レーンのcost82d raw batch 2）を再取得し、items/で
  K0937空き（max=K0936・K0936は二重出版状態: 本レーンの
  K0936-remo-sieve7-uv-mod210 とtwo-tokenレーンの
  K0936-two-token-z6-y25-boundary。統合時の再採番は相手レーンが
  活発なため本項では触れず記録のみ）とREADMEのK0936 bullet位置を
  確認してから出版。
- AGENTS.mdの統合前確認（uv run tools/knowledge/{check,build}.py・
  unittest）は本実行環境にrepoのcloneとuvがないため未実施。
  generated/とroot READMEは編集していない（次の統合時に再生成）。
