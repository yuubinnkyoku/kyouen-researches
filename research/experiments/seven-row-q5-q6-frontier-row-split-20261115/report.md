# seven-row-q5-q6-frontier-row-split-20261115 — rowY 固定分割による (7,5) 7x32・(7,6) 7x27 前線の解決

Date: 2026-11-15 (UTC 2026-11-14 late)
Lane: 高速レーン（seven-row-q4-q6 witness frontiers の後続）
Status: COMPLETED

## 主張

1. **(7,5) m=32 に行欠損の極大安全配置（witness）が存在** —
   rowY=0 固定分割（sat2.js `--rowY=0`）で **SAT・129,923 conflicts**（250s cap）。
   27石・rows **[3,4,4,4,4,4,4]**（単一欠損）。
   **M_{7,5} ≥ 33**（上界 1142・K0318 代入）。前線 7x32 → **7x33**。
   前線負記録（seven-row-q4-q6-witness-frontier-20261115: def-mode OR 200s
   INDET 329,844 conflicts）を解決。
2. **(7,6) m=27 に witness が存在** —
   rowY=3 固定分割で **SAT・230,973 conflicts**（250s cap）。
   34石・rows **[5,5,5,4,5,5,5]**（単一欠損）。
   **M_{7,6} ≥ 28**（上界 862・K0318 代入）。前線 7x27 → **7x28**。
   前線負記録（同実験: OR 200s INDET 744,027 conflicts）を解決。
3. **(7,4) 構成witnessファイル m=22..35 の2系統再検証**: 14/14 PASS
   （jsVerify = sat.js verifyConfig・pyVerify = Python Fraction）。

いずれの SAT witness も2系統検証（census 不使用 sat.js verifyConfig +
Python Fraction 独立実装）で safe + maximal + 行欠損 PASS。

## 手法

- `rowsplit.sh` — sat2.js `--rowY=Y` rowfixed CNF 生成 → kissat 4.0.4（CAP s）→
  SAT 時 decode_verify.js + verify_witness.py 二重検証 → JSONL。
  record schema は seven-row-q7-witness-search-20261114/output/row-split/records.jsonl
  と同一。
- def-mode OR（∃欠損行）を「欠損行 = rowY」で固定した w 個のインスタンスに分解。
  完全な分解（OR インスタンス SAT ⟺ いずれかの rowY SAT）だが、
 今回は SAT 発見が目的で全 rowY を実行した（下記）。
- sat2.js / sat.js / verify_witness.py / decode_verify.js は既存実験から verbatim
  （K0810 census core・七行族と同一の較正履歴）。
- kissat 4.0.4 official linux-amd64 release binary (GitHub rel-4.0.4)、
  sha256 21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1。
  変更なし（環境リセット後の再取得で同一ハッシュを確認）。

## 較正（環境リセット後の再構築）

- (7,5) m=31 def-mode CNF 再生成 → kissat **SAT 31,000 conflicts bit-exact**
  （seven-row-q4-q6-witness-search-20261114/output/q5-frontier-extension の
  公開 record と一致）。
- 公開 (7,5) m=31 witness（27石 rows [3,4,4,4,4,4,4]）が pyVerify PASS。
- (7,5) m=32 rowY=0 CNF は生成ごとに決定的（md5 e4850754f3a78e16d95e2673ccd1e754）。

## 正直な負記録（いずれも不在主張ではない）

- (7,6) m=27 def-mode OR: 175s cap INDET **703,590 conflicts**
  （同一レーンの別実行で 240s cap INDET 904,521 conflicts も観測 —
  cap 到達時の conflicts は実行速度依存）。
- (7,6) m=27 rowY=0/1/2: 250s cap INDET **989,735 / 1,078,304 / 1,074,595**。
- rowY=3 のみ SAT に到達（230,973 conflicts）。rowY=3 は (7,8) m=24・
  (7,7) m=25/26 と同じミラークラス。

## (7,4) 構成witnessファイルの2系統再検証

seven-row-q4-extension-band-20261114/output/witnesses/ の
s7x22..35q4_none.witness.json（C22/CA/CB 由来・tsVerify 済み）全14幅を
sat.js verifyConfig + Python Fraction で再検証 → **14/14 PASS**
（output/q4band-witness-dual-verification/records.jsonl）。
m=28..35 は sat3-20261115 の独立配置 SAT witness による存在証明と
本再検証により、**構成ファイルそのものも4系統検証**となった。

## スコープと限界

有限機械検証。witness 帯は (7,5) m=5..32・(7,6) m=6..27。
7x33 / 7x28 以降の不在は主張しない。M の確定には前線評価と
上界改善（K0342 型 tail 評価）が残る。INDET 記録は cap 到達であり
不在を意味しない。

## ファイル

- `scripts/rowsplit.sh` — rowfixed 1インスタンス実行パイプライン（本実験で新規）
- `scripts/README.md` — 出所・較正の説明
- `output/q5-m32-row-split/` — records.jsonl + meta + kissat 生ログ + witness（rowY=0 SAT）
- `output/q6-m27-row-split/` — records.jsonl（OR + rowY 0..3・5レコード）+ meta + kissat 生ログ + witness（rowY=3 SAT）
- `output/q4band-witness-dual-verification/records.jsonl` — 14幅×2系統の検証記録
