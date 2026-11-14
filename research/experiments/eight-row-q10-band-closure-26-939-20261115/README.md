# eight-row-q10-band-closure-26-939-20261115

IN FLIGHT (claim). (8,10) の現状: 行欠損極大 witness は m=10..25
（`eight-row-bands-20261114` w8q10 witness-search・m=25 SAT 1,221,994 conflicts）、
上界 **U_{8,10}=940**（K0318 曲線パッキング代入・`seven-row-inband-families-20261114`
の w7_upper_bounds.json で w=8 行・controls PASS 済み）。本実験は残る帯
**m=26..939** を掃引し、**M_{8,10} を {26,27} にまで決着**（全幅 UNSAT なら
M_{8,10}=26 exact・w=8 で初の真の安定化長の完全確定。帯内 SAT 幅が出た場合は
そこで停止し witness を dual-verify して前線を進める）を目指す。

フロンティア観察（本 claim 時点・`output/controls/frontier-probes.jsonl`）:
m=26..28, 30 の def-mode は kissat 4.0.4 で 250s INDET（m=26 は eight-row-bands
の rowY=3/rowY=3lexH/rowY=4 符号化でも INDET — "witness frontier resists all
four encodings")。(6,8) m=22 と同じ遷移帯難所の様相。よって本実験は
**(a) 易しい帯 m=31..939（遷移帯より上）の掃引**を先行し、
**(b) 難所 m=26..30 は lex 交差符号化・長時間 cap・rowY 細分割で継続攻略**する。
(a) 全幅 UNSAT + (b) が決まれば完全決着、(a) のみでも M_{8,10} ∈ {26,27}
（厳密には last-SAT-width+1 以上の区間確定）に改善される。

## 手法

- CNF 生成: **genfast3.js**（弦対抽象円 census・q≥w+2 限定・
  `seven-row-q9-band-extension-201-612-20261114` から verbatim・md5 12c2bd9c）。
  (8,10) は q=10 ≥ w+2=10 で適用条件を満たす（q ≥ w+2）。
  生成 O(C(w,2)·m²·w) — m=939 で数十秒級。
- ソルバ: kissat 4.0.4 official linux-amd64・200s cap・def 単一節符号化
  （「ある行が q-1 石以下の極大安全配置が存在」の完全符号化・K0820/eight-row-bands
  と同一）。
- スクリプト: `scripts/leanband3.sh`（1 幅: genfast3 生成 + kissat + JSONL record +
  SAT 時 decode/dual-verify・`seven-row-q10-band-closure-201-586-20261115` から
  パス修正のみ）・`scripts/batchband3.sh`（wall-clock guard 付き連続実行）。
- decode/dual-verify: `scripts/decode_verify.js`（eight-row-bands-20261114 から
  verbatim）+ `seven-row-inband-families-20261114/scripts/verify_witness.py`
  （SEVEN_SCRIPTS 経由・Python Fraction 独立検証）。

## 較正（本実験で実施・`output/controls/` に記録）

- **CNF byte-identity vs genfast.js**（cmp・同一 CLI オプション）:
  8x26 def / 8x32 def / 8x32 def+lex=H,V,HV — 全 3 サンプル **MATCH**
  （genfast.js は eight-row-bands-20261114 の w8 witness 探索で実績のある
  半整数中心 census 生成器）。
- **instance-identity**: 8x26 def の meta（vars 8,963 / clauses 32,612 /
  curves 129）が eight-row-bands の m=26 frontier record と bit-exact。
  陽性対照 8x20 def SAT 703 conflicts・8x25 def SAT 1,221,994 conflicts —
  いずれも eight-row-bands w8q10 records と bit-exact 一致。

## スコープ

有限機械検証（census 完全性は q≥w+2 の弦対引数・CNF byte-identity・
instance-identity 較正、kissat 正確性まで）。m=26..939 の各幅 UNSAT は
その幅の行欠損極大非存在の完全証明。全幅 UNSAT の場合、witness 幅集合
{10..25}（eight-row-bands）・m≥940 witness-free（K0318 代入 U=940）と
合わせて **M_{8,10} = 26 が exact に決着**する。SAT 幅が出た場合は
そこで停止し、witness を dual-verify（decode_verify.js + verify_witness.py）
して下界更新として記録する。INDET 幅は honest negative として残り、
決着主張から除外する。

## scripts

- `leanband3.sh` — 1幅 def-mode 実行（genfast3 CNF + kissat 200s + records.jsonl
  append + SAT なら decode+dual-verify）。KISSAT_BIN / SEVEN_SCRIPTS / GENFAST3_JS
  環境変数でバイナリ・検証器・生成器のパスを上書き可。
- `batchband3.sh` — 連続幅帯掃引（wall-clock GUARD 付き）。
- `decode_verify.js` — verbatim from eight-row-bands-20261114/scripts。
  （sat.js を自ディレクトリに要求するため実行は SEVEN_SCRIPTS 配下の同一コピー
  を使用。leanband3.sh の DV はそれを指す。）
- genfast3.js は複製せず `seven-row-q9-band-extension-201-612-20261114/scripts/`
  （md5 12c2bd9c）を GENFAST3_JS で指定して使用。
- sat.js / sat2.js / verify_witness.py は複製せず
  `seven-row-inband-families-20261114/scripts/` を SEVEN_SCRIPTS 経由で使用。

## 進捗

- 2026-11-15: IN FLIGHT claim。較正完了（CNF byte-identity 3/3・
  instance-identity 3/3・フロンティアプローブ m=26..30 INDET 記録）。
  帯掃引 31..939 と難所 26..30 の攻略は後続コマンドで実施。
