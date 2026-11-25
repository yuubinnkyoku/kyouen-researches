# {1}^t 行の窓端分離の全称法則 実行記録（2026-11-23・高速レーン）

## 選定と着手の経緯

- 当実行の最有力候補「T2 (z=1,R=3) の独立 K 昇格」は着手直前に並走が宣言
  9ceb96d0 を出版（K1269: T2 昇格の宣言・K1270: min>=2 の z∈{0,1} banded
  window 拡張の宣言）したため回避（単一オーナー規約）。生成済みだった T2 用
  機体（実験dir ones-multiset-z1r3-separation-20261123）は出版せず廃棄扱い。
- 代替: K1268 未解決課題 E5（{1}^t 行の疎パターンの一般則）の全称解決を選定。
  行 census（t<=30・z<=30）で分離集合 S(t) の完全法則を発見 → A_j(k,z) 族の
  閉形式 RC → 紙面の強帰納証明成立 → 宣言前探査として大規模機械照合
  （A-family 26,190点・分離法則掃引 4,720点・いずれも bad 0）まで先行して
  完了。これら探査は宣言ノートに全開示（publish-then-execute 誠実記録）。

## 宣言（publish-then-execute・単一オーナー）

- 宣言ノート: research/log/2026-11-23-ones-row-frontier-single-owner-note.md
  commit 55e6b109（push 時点の observed HEAD: 9ceb96d0・push 後 commit-pinned
  raw fetch-back で byte 一致・sha256 64575c7e…）。
- スコープ: M-RC（A_j 族全称閉形式・証明全文開示）・M-DIAG・M-SEP と専用機体
  protocol D1-D4（26,190+2,244+2,420+225 点・総 93,210 照合・分離546・bad 0・
  電池10種・決定性4実行）の事前登録。min>=2 側・アリティ>=3 一般X・11×11 巨大
  探索は保持しない（宣言ノート記載どおり）。

## 機体構築（手転写ゼロ）

- build_engine_from_published.py（SHA-256 d99361a3…）が出版 K1264 検証器
  verify_min_token_staircase.py（108fdd65…）と出版 K1268 機
  verify_unified_window_sharpness.py（0ab66665…）の両方から engine block
  （2,508B・bd5f22e4…）を SHA ゲート付きで抽出・三方 byte 照合
  PROVENANCE PASS。
- 最終機体 verify_ones_row_frontier.py（SHA-256 1ce7df23…）。初期組版
  （85e5c7e7…・z1r3 用）は出版せず、宣言文言の M1 ラベル（+1）を電池実装
  （閾値−1）に一致させて再組立てした（下記誠実記録1）。

## 実行結果（AUDIT PASS・宣言予想と完全一致）

- D1 A-family: 26,190 pts / 78,570 comps bad 0（j=0..7・k=0..44・z 有効全域）。
- D2 対角+z=0列: 2,244 / 4,488 bad 0。
- D3 分離 sweep: 2,420 / 9,680 bad 0・分離点 546 = 宣言算術値
  （偶t |S|=t/2 の 252 と 奇t |S|=(t+5)/2 の 294 の和）。
- D4 出版アンカー: 225 / 472 bad 0（K1268 (a)/(b)/(d)・T1 t=3..12・
  T2 t=2..16・K1265 行 z<=12・R<=8・E5 sparse 3件の文字列一致）。
- 総計 31,079 pts / 93,210 comps / bad 0: 宣言予想（31,079・93,210・546・0）
  と完全一致・ドリフトなし。
- 決定性: audit 4実行（同一cwd×3 + 隔離tree・env -i・PYTHONHASHSEED=random・
  別HOME）で output/audit.json byte-identical（SHA-256 fb35211a…）。
- fail-closed 変異電池 10種すべて捕捉（bad 内訳 119/2,519/2/119/17/106/43/
  163/570/21）。

## 誠実記録

1. **M1 宣言文言「CFG 2帯閾値+1（奇k）」は no-op だった**: 奇 k では
   k+2j−1 が偶数のため 2帯（z 奇数）の実効集合が不変。初回電池が
   TAMPER-MISSED（rc=1）でこれを機械検出した。宣言種（CFG 奇k 2帯閾値変異）を
   保持した有効変異「閾値−1」に差替え（bad=119 捕捉）。K1268 実行の変異⑦
   差替え先例と同型。no-op であること自体が CFG の偶奇保護構造（奇k の 2帯
   上限 k+2j−2 と 1帯下限 k+2j−1 の偶奇分離）の傍証。
2. 宣言点数・照合数・分離 546 は宣言時に protocol 定義から算術計算した独立値
   （探索実行の結果は参照していない）。
3. 宣言前探査（行census・d グリッド・A-family 26,190点・分離掃引 4,720点）は
   宣言ノートに全開示済み。宣言 protocol 実行は宣言出版（55e6b109）後。
4. M1 ラベル修正による機体の再組立て 1回（最終版 1ce7df23… のみ出版）。

## 出版

- 宣言ノート: commit 55e6b109（fetch-back byte 一致・sha256 64575c7e…）。
- 実験dir 4ファイル（report.md・verify_ones_row_frontier.py・
  build_engine_from_published.py・output/audit.json）: commit 71a8c3f2
  （commit-pinned raw fetch-back・全4ファイル sha256 完全一致）。
- 並走（毎時実行）は本レーンの実験dir出版と同時期に K1269/K1270 を出版
  （実験dir 6f24d49f・item+run log 5fa9ce83）。K1271 の relations に
  K1269/K1270 の related を追記（z=1 切片の包含関係と min>=2 banded との
  相補性・機体は非接触）。
- 本 run log と K1271 item: 本 commit（出版後に追記しない）。
- README bullet: 上記に続く commit。

## 次課題（resume 候補）

1. M1 no-op が傍証した CFG 偶奇保護（奇k の 2/1 帯閾値の偶奇分離）と
   2トークン (y,z) 列の対応構造の関係。
2. A_j 族の d=R−z 奇数状態（窓端から到達不能）の値の閉形式と到達可能性の
   一般論（本項では範囲外・open）。
3. min>=2 banded（並走 K1270 claim）と min=1 行 S(t) を併合した
   「min(X) とアリティごとの窓端分類表」への統合。
4. S(t) 型法則のアリティ>=3・一般X（例: {2}^t・{m}^t 行）への一般化。
5. 並走 K1269/K1270 の item は出版済み（5fa9ce83）のため相互 relation は
   K1271 item 側に記載済み。K1270 側から K1271 への back-reference は
   並走所有のため本レーンでは追記しない（相手の次回実行に委ねる）。
