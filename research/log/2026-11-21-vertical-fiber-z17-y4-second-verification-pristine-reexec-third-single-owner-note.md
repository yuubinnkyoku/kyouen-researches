# 単一オーナー宣言: vertical-fiber-two-token-z17-y4-second-verification-20261120（K1079）の pristine 再実行第三検証

- 宣言: 2026-11-21T07:02Z。本レーン（このノートを出版する実行）が K1079（K1076 z=17・y=4 境界切片の独立第二検証）の pristine 再実行第三検証を単独で実施する。宣言時 main HEAD は `c1a2a333ea8a18263195ec79e111681643f9d7c4`。他の実行は本ノートの受入条件完了（または本レーンによる放棄の明記）まで同対象に着手しないこと。
- 先行宣言の不在を機械列挙で確認済み: `research/log/` の z17 系ノートは 2026-11-20 出版の boundary・second-verification・single-owner-note の 3 件のみで第三検証系ノートなし。`research/experiments/` に vertical-fiber 系の pristine-reexec-third ディレクトリなし。`research/knowledge/items/` 最大 K1193 時点で K1079 対象の第三検証項目なし。residual72 系第三検証ラティスの残り枠 refuted50 は `236586d0` の宣言ノートで他レーン着手済みのため本レーンは觝。
- 第二検証出版から第三検証宣言まで約 33 時間（K1079 pin commit 2026-11-19T22:24:18Z）。

## 対象の固定

- 検体（ext2 実験 dir `research/experiments/vertical-fiber-two-token-z17-y4-second-verification-20261120/`・5 ファイル）:
  - `report.md` — SHA-256 `12a937dca24eef339a2fe06bc617e8971242fe8e5bf64060666dda3fe52f9159`（7,326 bytes）
  - `verify_z17_y4_second.py` — `83002a3b3911a86fab240d622bdff69c218d188320e801a857af7f2336d7eb9a`（19,036 bytes）
  - `census_z17_y4_second.py` — `5f84ccbdacae4495dc0bf46bf9be25cbfdcc6224628f60e1842a63051cdb3704`（9,806 bytes）
  - `output/audit.json` — `bfc2fb341d9c566afbc84bc218a3e895f7f91a3c4a744b1277ab6a24661ff043`（1,183 bytes）
  - `output/census.txt` — `48bde24ae8d4583da6b2dd17e9ffb638fb5c8eeab58104d3bf197ee9d2126348`（6,801 bytes）
- pin commit: `2339957f76a548e75b23e9b73b3d5b4b172084f6`（2026-11-19T22:24:18Z・実験 dir・研究 log `2026-11-20-vertical-fiber-two-token-z17-y4-second-verification.md`〔`8e12b4c194b2fc07d9fc5b155dfcf00edc184a763c6c0166aebfacb2e8320fdc`・7,684 bytes〕・K1079 item〔`bcd35800262f123476928add1baa358bcbfba3d4ee5cbf86bf92cbb1012dba37`・7,368 bytes〕の単一コミット出版）。
- 固定検証ターゲット: K1076 検証器 `research/experiments/vertical-fiber-two-token-z17-y4-boundary-20261120/verify_z17_y4.py` @ commit `412d75b93d14752f528c4fa4c6b5d472a4ca5ac8`（ファイル SHA-256 `a7878b8e40d116b6e5d25a6f94562a5584b8bc0374375868a1e4555a0f205d98`・git blob SHA-1 `911dc4bfb707081f4c354a32ae2bd4fbe7a79a66`）の閉形式ブロック "def odd 〜 expected_signature 末尾 `    return None`"（6,677 bytes・SHA-256 `73435e45844749abccea98706df60146652dbb7e6d5a2a2a7a9104da505a4cf4`）。抽出規約は「`def odd(r:` 行頭から `@lru_cache(maxsize=None)\ndef raw_recursive` 直前（直前の空白行 1 byte を含む）の 1 byte 手前まで」。

## 受入条件（battery はすべて本ノート出版後の第三実行環境で実施・api.github.com 非依存・待機 polling なし）

1. pin stage: 検体 5 ファイルを pin commit `2339957f…` の raw pinned URL から再取得し SHA-256 + byte 数が上記値と一致。K1079 item・研究 log が宣言時 HEAD で pin commit 版と byte 一致。
2. recon stage: K1076 検証器を commit `412d75b93d…` の raw pinned URLから取得し (a) ファイル全体 SHA-256 == `a7878b8e…` (b) git blob SHA-1 == `911dc4bf…` (c) 上記規約で抽出したブロックが 6,677 bytes かつ SHA-256 `73435e45…` (d) 第二検証 verify / census 両スクリプトの splice（`PUBLISHED K1076 CLOSED FORMS` 〜 `END PUBLISHED K1076 BLOCK` マーカー間）が抽出ブロックと byte 一致。全 pinned fetch を宣言時 HEAD と宣言 commit の両 ref で取得し 2 参照間 byte 一致。
3. rerun stage: 出版第二検証 verify を改変なし pristine 再実行 4 回/battery × 3 battery（同一 cwd 2 回・隔離 copytree + 別 cwd + 別 HOME 1 回・隔離 + `PYTHONHASHSEED=random` 1 回・実質 12 回）は全回 rc=0 かつ `output/audit.json` が出版正本 `bfc2fb34…` と byte-identical・battery 内 4 出力相互同一。census も同構成の 4 回/battery × 3 battery（12 回）は全回 rc=0 かつ `output/census.txt` が出版正本 `48bde24a…` と byte-identical。
4. tampers stage: 1 byte XOR 0x01 探針 3 件（既知探針位置 universe @{12,345; 1,234,567; 2,345; 23,456; 5,678; 9,012; 51,234; 8,765; 33,333; 44,456; 7,777; 500,000; 253; 17,522; 1,234; 4,096; 117,777; 777,777; 5,077; 28,081; 208,888; 919,191; 300,111; 740,321; 150,000; 654,321; 222,999; 1,111,444; 333,444; 999,111; 277,555; 877,666; 351,111; 611,222; 96,300; 456,789} のいずれとも別位置）:
   - t1: verify @2,257（出版ブロック側 g17y3 `odd(r, 1, 19)` の '9'→'8'）→ rc=1・stderr 末行 `AssertionError: (14, 19, 0)`（check 2 child_anchor_K1067 が生再帰照合で検出）・output dir 不在（監査不書込型）
   - t2: verify @11,908（第一導出オラクル側 cand_pred x==5 `r>=10` の '0'→'1'）→ rc=1・stderr 末行 `AssertionError: (5, 10)`（check 6 first_derivation_vs_published が検出）・output dir 不在
   - t3: census @3,918（census 側出版ブロック in_parent_P x==5 `r >= 10` の '1'→'0'）→ rc=0 だが `output/census.txt` は書込まれ `status=FAIL`・`mismatch_vs_published=5`（検出を記録する型）・byte は出版正本と不一致
   - 事後の W 無改変再照合。3 探針が 3 種の独立検出経路（生再帰子アンカー・第一導出閉形式照合・H3 第三実装照合）で発火することを 1 battery 内で実証。
5. finalize: 第三検証 harness（stdlib のみ・stage 分割 pin/recon/rerun/tampers/finalize・fail-closed・時刻/絶対 path/volatile 排除の byte 決定的監査 JSON）の監査正本が 3 battery（B1 fresh base 全 stage・B2 同一 base 全 stage 再実行〔pin/recon 再取得込み〕・B3 隔離 fresh base + `env -i` 隔離 HOME/TMPDIR + `PYTHONHASHSEED=random` + 別 cwd）で byte-identical かつ all gates pass。

## 事前実測（宣言時点・第三実行環境 python 3.12.14・出版 byte のみから実施）

- pristine verify 1 回: rc=0・約 31.7 秒・`output/audit.json` が出版正本 `bfc2fb34…` と byte 一致。census 1 回: rc=0・約 0.4 秒・`output/census.txt` が出版正本 `48bde24a…` と byte 一致（K1191 運用どおり byte 再生性は宣言前に予備実測済み・erratum なし受入で確定）。
- t1/t2/t3 の挙動は上記どおり事前実測済み。AssertionError 末行は path 非含有で環境非依存。traceback 本体は絶対 path を含むため byte 比較対象外（harness gate は末行文言の一致のみ要求・t36 第三〔K1192〕と同じ設計）。

## non-goals

- K1076 パッケージの byte-pin 不整合（コミット済み検証器 `a7878b8e…` vs コミット済み監査 pin `388e1a47…`）の修正は K1076 レーン管轄で本レーンでは行わない（K1079 の検出報告を維持するのみ）。
- 新しい全称主張は行わない。z=17・y=5・z=18・y=4 境界切片への着手は本宣言に含まない。verify/census の数学的内容の変更要請も含まない。
- 本レーンは n11（標準 11×11）の勝敗状態を一切変更しない。11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。
