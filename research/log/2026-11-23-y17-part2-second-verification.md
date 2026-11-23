# y=17 全称証明 part2（K1240 observed→proved 昇格・K1241 part2 追記）の独立第二検証（2026-11-23 高速レーン・並走実行）

本 log は [K1240](../knowledge/items/K1240-two-token-y17-parametric-closed-form-fit.md) を
observed→proved に昇格させた part2 出版（[part2 log](2026-11-23-y17-universal-verifier-part2.md)・
出版3コミット: 実験dir update `ab23d120`・K1240 昇格+K1241 part2 追記 `5e9dd65e`・knowledge README
bullet `72b9c07f`）に対する**独立第二検証**の実行記録である。第二検証機体は本レーンが
part2 出版と並走して pinned-source builder 主義で独立構築したものであり、出版を確認した
時点で自前出版を取りやめ、検証側に全面転用した。第二検証の判定は**健全**（全数値一致・
出版 bytes の完全再現・fail-closed 電池は別系統 8 種全検知）で、発見した欠陥は
published_run.txt の 1 件の点数誤記のみである。

## 経緯: 並走宣言と出版の譲渡

- 本レーンは part1 を pinned-source builder で独立複製（37,606 B・SHA-256 `76a73b6e…`・
  総 6,312,890 点 bad 0）して出版機体（総 6,343,825 点）と交叉検証した後、出版 part1 機体を
  base に採用する part2 実行宣言 note（commit `1fec2b1c`・amendment `2a885eca`）を
  2026-11-23T01:26:44Z に出版した。
- その後も pinned-source builder（参照元ピン 4 本: 出版 part1 検証器 SHA-256 `2110ecbb…`・
  出版 y16 part2 検証器 `bdf4fe04…`・出版 preflight_c1d_y16 `6a3094c1…`・出版 census_rows.py
  y16 版 `76e89fe9…`）で part2 マシンを完全独立構築し、下記の全検証を終えた。
- 自前出版の直前に最新 main を再取得したところ、part1 出版レーンが同一単一オーナー宣言
  `b099a974`（保持範囲 part1+part2）の継続として part2 全体を出版済み（01:33-01:35Z）
  だった。並走時の規約（無理に押し進めず）により本レーンの part2 出版を全面取りやめ、
  第二検証レーンに転換した。
- fetch-back で出版 [part2 log](2026-11-23-y17-universal-verifier-part2.md) の「並走宣言の扱い」
  節が本宣言を「先行宣言の予約実行系は本出版で完結・閉包・重複出版なし」と記録している
  ことを確認した。本 note はその裏側の独立実行の全記録である。

## 本レーンの独立 part2 機体（未出版・builder 成果・ローカル）

builder `build_verify_y17_part2.py` は y16→y17 変換 14 ハンク（出版 y16 part2 diff の正写し）
と anchor block（A8u..A17u verbatim）を count-asserted で適用し、3 実行 byte-identical
だった。生成物と独立実行成績:

- verify_y17_universal.py part2 版（本機体 SHA-256 `876d048f…`）・
  preflight_c1d_y17.py（`a32c5fa1…`）・census_rows.py（`b07d960d…`）。
  なお本機体は出版 part1 byte + 出版 y16 part2 byte からの count-asserted 変換で、
  出版 part2 bytes（`4253cf29…`）とは独立に生成した（docstring 折返し等の文言差あり）。
- 実行 tree は隔離構成（AGENTS.md 根 + 実験dir 配置 + pinned sources 配置）で、
  check_transcriptions_y17.py 再構成の SHA-256 `ac40c03c…` が出版引用と一致。
- 転写 check PASS・preflight PASS **12,789 + 9,438 点 bad 0**（3.1秒）・
  census **4,320 行 444,960 点 zero 221,578 misses 8,725,227**（18.6秒・census parts は
  出版 byte と一致: ordered `12234496…`/canonical `1ca205a5…`）・
  フル14チェック **overall PASS 総 6,926,065 点 total_bad 0 型 457,645**（35秒）。
  C4t clip 35 違反 1,300 (60,98,98) も一致。
- 決定性: 同一cwd 2回 + 隔離 tree/cwd/HOME で env -i・PYTHONHASHSEED=random の 1回の
  計 3 実行で全出力 byte-identical（audit.json SHA-256 `60c90f93…`・preflight pretty json
  `c8e0e0a9…`、census.txt 全体も両 tree で byte-identical）。
- fail-closed 電池 8 種（/tmp スクラッチ copy で実施・全検知・baseline 復元確認）:
  (B1) 検証器 C1d A8u pin 改ざん → bad=2 FAIL・(B2) census.txt T 集合改ざん → FAIL・
  (B3) census.txt idx 改ざん → FAIL・(B4) census.txt 欠落 → FAIL-CLOSED・
  (B5) 重複行注入 → FAIL-CLOSED duplicate census row (0,17)・
  (B6) 行欠落 → FAIL-CLOSED census rows 4319 != 4320・
  (B7) preflight A8u pin 改ざん → rc=1 anchor_bad=2・
  (B8) census part 点数改ざん → FAIL-CLOSED census points 440641 != 440640。

## 出版体の第二検証（fetch-back 監査・判定: 健全）

出版体 bytes（verify_y17_universal.py SHA-256 `4253cf29…` 51,925 B・
preflight_c1d_y17.py `fc1d4ec0…` 12,902 B・census_rows.py `1188bcd1…` 3,812 B）を
展開して監査した:

1. **コード監査（AST 抽出比較）**: part1 12 チェックの全 check 関数・エンジン・
   cand16/cand17 転写 block・A8u..A17u アンカーは本レーン機体と byte-identical
   （差異は main の 14 チェック配線のみ・当然）。check_C1d/check_C11r は
   box・gate・fail-closed セマンティクスが本レーン機体と完全一致（文言のみ差異）。
   census_rows.py は docstring 折返しのみの差でコード同一・preflight も docstring
   1 文の折返しのみ差で関数全 identical。
2. **数値交叉**: 出版 audit.json の全 14 チェックの points/bad・merge 1,182,632 /
   tail 193,096・total 6,926,065・types 457,645 が本レーン機体 audit.json と完全一致
   （差異は stage 文言と verifier_sha256 フィールドのみ・機体が異なるため当然）。
   census.txt 全体と preflight-c1d-y17.json は両機体で byte-identical。
3. **byte 再現**: 出版 bytes を別 tree で最初から完全実行（隔離・出版 byte のまま）
   したところ、出版 audit.json（SHA-256 `fd4b7d8c…`）が byte-identical に再現し、
   census parts も出版 byte と一致した。すなわち出版体は出版記録どおり決定的に
   再現可能である。

## 発見した欠陥（1 件・記録のみ・訂正はしない）

出版 `output/published_run.txt` の notes にある「+ 137,880 (C1d)」は誤記である。
C1d の正しい構成和は掃引 127,842 + preflight 低R 9,438 = **137,280** 点
（audit.json・part2 log・K1241 item はすべて正しい 137,280 を記録済みで、同 record の
総点 6,926,065 自体も正しい構成和）。よって実質的影響はなく、出版 byte は監査正本
として不変保持する本 repo 慣行に従い publish 済みファイルは変更せず、本記録のみを
残す。

## trust 境界

K1240 の observed→proved 昇格・K1241 part2 実績値は出版レーンの実行として完了して
おり、本 note はその状態を変えない。本レーンの寄与は (a) 独立 pinned-source builder
機体による全数値再現、(b) コード交叉監査、(c) 出版 bytes の byte-identical 完全再実行、
(d) 独立 fail-closed 電池 8 種 の 4 経路による独立確認の記録であり、K1240 昇格の
第二根拠である。本レーン機体は builder + 参照元ピン bytes から常時約 90 秒で再構築
可能。次段階の y=18 fit には新たな単一オーナー宣言が必須（part2 log レジューム
どおり）。標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
UNKNOWN のまま。3 トークン以上・y>=18 族・固定幅・q 点版は範囲外。
