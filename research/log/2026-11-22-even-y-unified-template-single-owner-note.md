# 単一オーナー宣言: 偶数y統一テンプレート機械検証の着手（fast lane・先行出版）

- 宣言時刻: 2026-11-22T21:42:00Z（push 時刻で確定）
- 宣言時点の観測 HEAD: dafe9651（Part BB 宣言 amendment・2026-11-22T21:40:01Z）
- 作業: two-token vertical-fiber 族の偶数 y = 10, 12, 14, 16 の出版閉形式
  （y=10/y=12/y=14 は全称 verifier 組込み表、y=12/y=16 は fit 出版表）を、
  cand14 fit コード本体の Y 定数代入のみによる単一 Y パラメトリックテンプレート
  で正確に再生できるかの機械検証。奇数 y = 13, 15 は陰性対照（不一致が期待値）。
  Lemma L1（b_{k+1} U I[2k+2) = b_k U I[2k+1)、証明つき）で y=10 出版明示表の
  表現差 15 行を全 offset 集合同一に標準化する。
- 出版先: research/experiments/even-y-two-token-unified-template-check-20261122/
  （検証器 scripts/check_even_y_unified.py・実行記録 output/check-run.txt・
  入力 SHA-256 pin の output/audit.json・report.md）+ 本 log に作業 log +
  K item（次番号）+ knowledge README 末尾 bullet。
- 誠実記録: 本宣言ノートの出版前に、同一構成の検証を本 run 内でローカル実行済み
  （grids 6 掃引 401,814 点 bad 0・行 census 12 本 640 行 bad 0・y=10 表現分類
  26 同一 + 15 alias + 2 定型・y=16 正規化差分完全一致・y=13/y=15 陰性対照は
  不一致（T 差分行 2、P 差分行 54/62、box 不一致 2,649/1,660 点）を確認済み）。
  出版は本ノートの直後に行う。2026-11-22T21:40Z 時点の直近コミットに本作業と
  重複する宣言・実験dir は不存在（Part BA/Part BB は batch-18 closure if-adopted
  系で非接触・K1058 レーンは円の数え上げで非接触）。
- fail-closed 設計: 検証器は even-y で不一致 1 点でも検出すれば FAIL、
  逆に odd-y 対照が不一致ゼロなら FAIL（テンプレートの偶数 y 特化性の確認）。
  入力 9 ファイルは repo 内兄弟実験 dir の相対パス読み込みで、audit.json に
  SHA-256 を pin するため出版後の改変は検出可能。
- 次候補（本宣言の範囲外・後続レーン向けの記録）: y=16 全称
  verify_y16_universal.py はこの統一テンプレート実装で書ける（別宣言必須）。
  横断法則の一般補題化（K1235 part 2 系）は本検証結果を前提データとして使える。
