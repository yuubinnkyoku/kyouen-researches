# 2026-11-18 合成NのV/U値完全決定（K0941）

K0939の直接続き（K0939ログの「次の候補」第1項を実行）。高速レーン。
branchなし・main直接出版。K0941として出版。

## 発見順

1. **着手判断**: K0939は素数側（V=0・U=m−1）を閉じ、合成Nの値そのものを
   残課題として明示していた。これが情報価値最上位。
2. **LADDER-ONLY（定理A）**: 合成Nがt=0エンドゲームに入れないことを
   「stretch 2..w−1生存→N≥spf(N)²≥(w+1)²」と「family入口では
   N≤w²+2w<(w+1)²」の矛盾で全称証明。ENTRY-LOCのfamily h範囲の
   「隙間」（V: h≤w・U: h≤w−1）が本質的に効く。K0939 END-SIEVE-IFFの
   合成側引数（family状態では必ず死亡）と対をなしすっきた二分法になる:
   エンドゲームに入れるのは素数Nだけ。
3. **死の二分法（定理B）**: 死亡合同式 a=r+1 から V死=breaking死（r=h−1）・
   U死=block死（r=h）。Vのbreaking dealは [n−h−w, n−h−2] でtailに
   触れない（r=h−1が本質）→死後は一様 Z(w+1, n−t)。
   Uはblock死（cold・pot w）後もstretchが続いてbreaking位相が走り
   E(w+1; n−t−1−w, w)、崩壊 (1,0,0) はZ(w+2, w−1)。
   これらはLAD-GEN（K0934）のdeal範囲・保持値の読み替えで機械アンカー前に確定。
4. **E-game閉包（定理C）**: K0939 END-INVの遷移公式が状態局所の計算で
   あることを一般化（任意E状態でE形式自己保存）。一様Z→1フェーズ→E。
   生存位置は逆合成 σ_旧=(r+1+σ_新) mod k（Josephus型）。
   σ_Z(3,K)=1のK分布（4,8,12,28,40,52,72,…・K≤4,000）を調べたが
   閉形式は発見できず、「再帰そのものが決定結果」と明記して公開。
5. **ラベル合成（定理D）**: 死亡stretchのフレーム→ラベル写像は
   生存stretchのLAD-GEN除去・再起点（bl+1）の反復。Vのbaseはphase-1後
   LS[i]=(i+2) mod m、Uはidentity。ここで値=frame[σ]が純算術確定。
6. **検証器の構成**: composite_core.py（σ_E/σ_Z・death_frame・predict）+
   composite_verify.py（7チェック）+ audit_build.py。
   - FULLREPRO: コミット16,000値（K0929 JS engine産出）を純算術から
     完全再構成・0不一致（17秒）。
   - STRUCT: 合成m≤1,500両側2,141ゲームをリテラル位置エンジンで
     完全プレイし、死後境界のフレームラベル・holdings/pot・最終生存者を
     予測器と照合・0失敗（30秒）。
   - EGAME: family・死後状態の外の一般E状態8,000強+一様300の
     σ照合・0失敗（定理Cの独立アンカー）。
   - ENGINE: m≤600両側1,200ゲームを生存者ラベル値レベルで照合。
   - P2OBS: U崩壊死⟺N=spf²（29↔29全単射）・V N=p²死状態(p,1,0,1)。
   - DEATH: 合成12,277ゲームの死亡stretch幅・r/h・保持の全範囲照合。
7. **監査**: audit_build.py は in-process 1回 + composite_verify.py
   （内部2回実行）のcold 2回でbyte同一・output/composite_values_audit.json
   （sha256 97e854f7…）。

## 検証

- composite_verify.py: 7チェック全合格
  （PIN/DEATH/FULLREPRO/STRUCT/EGAME/ENGINE/P2OBS）。
- audit_build.py: cold 2実行byte同一・各cold実行内でin-process 2回一致。
- 独立性: リテラル位置エンジン（K0928補題Pの独立実装・2種）と
  純算術予測器（出版定理の合成）の相互照合、コミット表（JS engine産出）
  とのFULLREPRO照合。

## 出版

- K0941（proved）: 定理A（LADDER-ONLY）・B（死の二分法・死後状態）・
  C（E-game閉包・σ再帰）・D（ラベル合成）・系COMPOSITE-VALUES
  （全m≥1のV/U値・全C≥2のP(C)が純算術決定）。実験ディレクトリ
  research/experiments/remo-composite-values-20261118/
  （report.md・sievegen_core.py・composite_core.py・composite_verify.py・
  audit_build.py・output/composite_values_audit.json）。
- READMEにK0939 bullet直後にK0941 bulletを挿入。

## 次の候補

- **P2OBSの全称証明**: N=p²軌道のh-walk記述（V死状態(p,1,0,1)・
  U崩壊(1,0,0)の証明）。p²のstretch列は特別な構造を持つ可能性。
- **σ_E/σ_Z閉形式の探索**: Josephus型。用途は限定的かも（再帰が既に算術）。
- **r人対戦・d次元版への転写**: 「ladder篩→死の二分法→E閉包→ラベル合成」
  の構成がK0906定理J周辺の一般化レジームで機能するか。

## 備考

- K0939実験dirの audit_build.py が main 上で中身が監査JSON本文と同一に
  なっている（出版時の混入と思われる・output/sieveprime_audit.json が本体・
  1033 bytesで一致）。本項では触っていない。次回K0939に触れるレーンで
  修正候補。
- push前に最新main HEADを再取得し、items/でK0941空き・READMEのK0939 bullet
  位置を確認してから出版。
- AGENTS.mdの統合前確認（uv run tools/knowledge/{check,build}.py・unittest）は
  本実行環境にrepoのcloneとuvがないため未実施。generated/とroot READMEは
  編集していない（次の統合時に再生成）。
