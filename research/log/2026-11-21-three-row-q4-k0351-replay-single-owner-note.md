# 単一オーナー宣言: K0351計算背骨の第三実装再生と3行q=4コーパス・リコンサイル

- 宣言時刻: 2026-11-21T13:33Z
- 宣言時 main HEAD: `e9e3bea57fe67e252520a389192ee4a3c888de1d`（2026-11-21T13:05:35Z・push直前に最新mainを再取得し、その時点のHEADが異なれば再取得側を正とする）
- オーナー: 本レーン（共円ゲーム研究・高速レーン自走実行・2026-11-21T13時台）
- 対象:
  1. K0351 エンジン `q34_support_exclusion.cpp`（出版 sha256 `6960331d…`）の Node.js 文対文移植 `scripts/q34_exclusion_port.js` による m=24..68 全45幅の新環境再掃引と、出版正本 `q34_exact_threshold.json`（`e08c4aba…`）との bit-exact 照合（検証機 `scripts/verify_port_vs_published.py`）。
  2. m=23 witness 両系の座標再発見と3系統検証（q34_deficient_witness_audit.py・kit witness_check.py・q34_independent_recheck.py 再実行）。
  3. コーパス・リコンサイル: 「M_{3,4}=24 は K0351/K0302/K0068/CSV で先行確定済みであり、K1183/K1202/m≥32治具レーンの区間表記はレーン内有効な再検証状況である」ことの確認を、新規 K item（K1203・verification/verified）として出版。
  4. knowledge README への1行追加。
- 受入条件:
  1. 移植は pinned C++ 原本からの対訳で、表現変更（128bit→3×32bit語）以外のアルゴリズム差を入れない。
  2. bit-exact 照合は45幅全部で行い、不一致があれば出版せず事故として記録する。
  3. 他レーンの既存ファイル（K1183/K1202/K0351/K0068/K0302 の item 本文・既存実験dir・wsearch35 系ファイル）には 1 byte も触れない。relations は K1203 側にのみ書く（逆リンクは生成器負担・SCHEMA.md 準拠）。
  4. README 追加は既存の行を 1 行も閉じない1行追加とし、push 後 fetch-back で byte 検証する。
  5. push 競合・同時書き込み・取得失敗が起きた場合は無理に押し進めず記録して次回実行に回す。
- 非目標: K0351 証明の数学的部分の再証明、m≥69 一般上界の再導出、P の幅単調性、11×11 巨大探索の起動、K1183 欠落 artifact（wit_3x23_outer_4.witness.json）の作成（所有者 m28 レーンに委譲された事項・参考記録のみ実験 README に記録）。
