# K0351 エンジンの第三実装再生と3行q=4コーパス・リコンサイル（M_{3,4}=24先行確定の確認）2026-11-21

- 単一オーナー宣言: `research/log/2026-11-21-three-row-q4-k0351-replay-single-owner-note.md`
- 対応 knowledge item: `K1203`（verification / verified）
- 宣言時参照 HEAD: `e9e3bea57fe67e252520a389192ee4a3c888de1d`（2026-11-21T13:05:35Z）

## 主張（2件）

### 1. コーパス・リコンサイル（knowledge 整合の確認事実）

**M_{3,4}=24 は K0351 で先行して証明・出版済みである**（2026-10-03）。

- `K0351`（status: proved）: M_{3,4}=24。上界 m≥69 は一般証明、m=24..68 は有限完全排除、下界は m=23 の8石極大安全 witness。
- `K0302`（proved）: 5閾値 24, 12, 16, 13, 11 のひとつとして M_{3,4}=24 を主張。
- `K0068`（proved）: 下界 witness M_{3,4}≥24（rows {0:[4,15,18], 1:[18,19], 2:[9,12,18]}）。
- `results/fixed-width/mwq_stabilization.csv` 行: `exact-threshold,3,4,4,24,proved,K0351;K0302;K0068`。
- 証明構造（`reports/q34-exact-threshold.md`）: 一般上界69 → 外部2行の安全な完了 → 対象行の一行被覆問題への正確な縮約（root積恒等式 p0−2p1+p2=2）→ 2つの安全な枝刈り → m=24..68 完全排除 → m=23 witness 8個（2 D4軌道×4）。

一方、2026-11-21 の3行 q=4 レーン群はいずれも K0351/K0302/K0068 を参照していない（HEAD `e9e3bea5` の items 確認による）:

- `K1183`（computed・m28 レーン）: witness band m=4..23・witness-free {24..31}・title は「M_{3,4} ∈ [24, 69]（m≥32 未掃引）」。
- `K1202`（proved）: def-mode は m≤68 のみ（自己完結第2 certificate）・「37幅32..68の有限掃引は依然必要」と記述。
- m≥32 治具拡張レーン（宣言 `3aa6fb7f`・wsearch35 系）: m=32 family 11/12 chunk zero を出版済みの掃引中レーン。

**整合判定: 反証・矛盾は皆無**。両者の成果はすべて M_{3,4}=24 と整合する（witness band は 23 で終端・witness-free 24..31・def-mode m≤68・m≥69 は K0024/K1202 の一般上界）。したがって K1183/K1202 の区間表記「M_{3,4} ∈ [24,69]」は**レーン内の有限検証範囲に関する有効な記述**であり、M の確定値としては K0351/K0302 が先行する。m≥32 治具レーンの掃引は先行証明に対する**第3の独立検証**として位置づけられる。

**矛盾検出インターフェース（明示）**: 何らかの手法が m≥24 の任意の幅で行欠損極大安全配置（被覆）を発見した場合、それは K0351（proved）との material conflict であり、status の retraction 審査対象となる。本レーンの全幅再生はこの方向の反例を一切発見していない。

### 2. K0351 計算背骨の第三実装による全幅再生（本レーンの新規検証成果）

K0351 の掃引エンジン `q34_support_exclusion.cpp`（出版 sha256 `6960331d…`）を Node.js に文対文移植し、閉区間 **m=24..68 全45幅**を新規実行環境で再掃引した:

- **全45幅で出版正本 `q34_exact_threshold.json`（sha256 `e08c4aba…`）と bit-exact 一致**: three_sets・cover_exists [0,0]・両 kind の候補計数（例: m=24 [2,385,880 / 1,321,971]・m=33 [1,510,604 / 429,791]・m=44 [0,3]・m=58 [0,0]）・witness は全域 null。
- 検証機 `verify_port_vs_published.py`（gate: three_sets / cover_exists / candidates_exact / witnesses_equal ×45幅）: **45/45 PASS**（`output/verify_24_68.json`）。
- 決定性: m=24, 34, 40 の再実行で比較可能フィールド全一致（`output/rerun_24.jsonl`）。
- m=23（閾値の下界側）: 移植版は出版 `q34_audit.json` の `m23_outer_witness`（[[1,17],[7,10,13],[9,10,12]]）と `m23_middle_witness`（[[4,7,18],[3,4],[4,10,13]]）を**座標レベルで同一の優先順序で再発見**した（`output/m23_rediscovery.jsonl`）。
- witness の3系統検証: (a) `q34_deficient_witness_audit.py`（出版スクリプトの新環境再実行・管理 witness 3/3 PASS・determinant と Fraction 幾何の一致検証込み）、(b) kit `witness_check.py`（整数行列式の第三系・3 witness すべて ok=true size=8）、(c) `q34_independent_recheck.py` 全再実行（3独立述語 A/B/C 全一致・出版出力と意味同一の出力を再生成）。

## 移植と実行の詳細

- アルゴリズムは不変対訳: `unsigned __int128` → 3×32bit 語（m≤68 で bit 67 まで）、`__builtin_popcountll` → SWAR popcount、`std::sqrt` 整数補正 → `Math.sqrt` + 同一補正ループ。唯一の表現上の変更は cover() 内の9スラブ隣接マージの (i,j,k) 依存性の正面化（純粋な因数分解）。
- ループ順序・枝刈り閾値（|base| < m−32、|base∪support| < m・k=1 の `j<i` 対称カット・候補計数の位置）は C++ 原本どおり。
- 実行時間: JS 単独で 3.5〜116.4 秒/幅（出版 C++ 値 1.4〜149.6 秒と同程度。実行環境が異なるため速度比は主張外）。
- 幅ごとに独立した決定的実行（状態は幅をまたがない）。44..68 は分割起動（bash 1 コマンド 300 秒制約のため 44..47 / 48..50 / 51..53 / 54..55 / 56..57 / 58 / 59 / 60 / 61 / 62 / 63 / 64 / 65..66 / 67 / 68 の15分割・全出力連結で24行+欠落なし）。

## 事故・制限（誠実記録）

1. **ポートバグ（修正済み）**: JS のシフト演算は shift 量 mod 32 で評価されるため、初版の `fullW[0]=(1<<m)-1` は m=32 で 0 になり、被覆判定が空集合で自明成立→偽 witness→早期 break で m=32 の候補計数破損（m=64 も同型）。出版値との一致検証で即検出し、`2**m` 表現に修正。修正後 m=32 は出版値 [2,854,244 / 1,031,094] と bit-exact（`output/m32_rerun.jsonl`）。**偽 witness は出版されたことのある出力には含まれない**（破損は本レーンの作業中出力のみ）。
2. **背景実行の同時書き込み事故（破棄済み）**: 最初の 44..68 掃引を nohup 二重起動してしまい中間ファイルが破損したため、当該ファイルは全て破棄して単一起動でやり直した。出版する `output/port_sweep_44_68.jsonl` は最終の単一起動系列のみ。
3. **翻訳共通誤りの検出不能性**: 移植はアルゴリズム忠実度が高いため、C++ から翻訳された誤りが両系で同一に現れる場合 bit-exact 一致では検出できない。この制限は (a) 独立手法（K1183 の列挙閉包・SAT・K1202 の計数上界）との交叉、(b) witness に対する決定因子/Fraction/rank の独立述語群、(c) m23 再発見の座標一致で実質的に補われる。
4. **本項が確定しないもの**: K0351 証明の数学的部分（外部2行完了補題・一行被覆縮約の健全性・m≥69 の一般上界）の再証明、P の幅単調性、標準 11×11 空盤・二石 root・S2・class 1/2/4（すべて UNKNOWN 不変）。有限掃引は「第三実装による再生」であり、手法の新規性は検証のみにある。

## 他レーンへの接続・非干渉

- K1183 / K1202 / K0351 / K0068 / K0302 の本文・status・relations は**不変**（relations は K1203 側にのみ記述。逆リンクは生成器負担）。
- m28 レーンに委譲された欠落 artifact（`three-row-q4-frontier-20261121/output/wit_3x23_outer_4.witness.json`・repo 全域 404）には触れない。参考記録: 本レーンの m=23 再発見結果（`output/m23_rediscovery.jsonl`）は当該 witness の座標内容を独立に再現しており、3系統検証済みの等価 witness として利用可能（所有者の処方判断に委ねる）。
- m≥32 治具レーン（`3aa6fb7f`・wsearch35 系）のファイルには 1 byte も触れない。彼らの掃引が m≥24 で witness を発見した場合は上記の material conflict インターフェースに従う。
- AGENTS.md ワークフロー規約（長時間探索の push 起動禁止）は不変。本実験はすべて受動的な単発掃引である。

## 再現手順（pub したファイルのみで完結）

```
# 1. ポート掃引（m=24..68・幅ごとに決定的・アルゴリズム本体は scripts/q34_exclusion_port.js）
node scripts/q34_exclusion_port.js 24 43          # output/port_sweep_24_43.jsonl 相当
node scripts/q34_exclusion_port.js 44 68          # output/port_sweep_44_68.jsonl 相当
node scripts/q34_exclusion_port.js 23 23           # m=23 witness 再発見

# 2. 出版正本との bit-exact 照合（検証機）
python3 scripts/verify_port_vs_published.py output/port_sweep_24_43.jsonl output/port_sweep_44_68.jsonl
#  -> widths_checked 45, widths_ok 45, all_ok true

# 3. witness 3系統検証（ピンされた出版スクリプト）
python3 research/experiments/fixed-width/scripts/q34_deficient_witness_audit.py
python3 research/experiments/fixed-width/scripts/q34_independent_recheck.py
python3 research/experiments/three-row-q4-enumeration-20261121/scripts/witness_check.py 3 23 4 '[[1,0],[17,0],[7,1],[10,1],[13,1],[9,2],[10,2],[12,2]]'
```

## ファイル構成

| path | 内容 sha256（頭12字） |
|---|---|
| `scripts/q34_exclusion_port.js` | ポート正本・`a11e0091d5c3` |
| `scripts/verify_port_vs_published.py` | 検証機・`3942c9313197` |
| `output/port_sweep_24_43.jsonl` | 24..43 全幅20行・`aae3cebdbb25` |
| `output/port_sweep_44_68.jsonl` | 44..68 全幅25行・`ab24c3bcca68` |
| `output/rerun_24.jsonl` | m=24,34,40 再実行・`695f57d20ba0` |
| `output/m23_rediscovery.jsonl` | m=23 witness 座標再発見・`df6b0d6e3626` |
| `output/m32_rerun.jsonl` | バグ修正後 m=32 bit-exact 証拠・`5b5f7787dd29` |
| `output/verify_24_43.json` / `verify_24_68.json` | 検証機 gate 出力・`ade7f1d06520` / `3128590e1b5b` |
| `output/deficient_witness_audit_rerun.out` | 管理 witness 3/3 PASS・`c4d660f8033f` |
| `output/witness_check_3system.out` | 第三系 witness 3件 ok・`7072ce497084` |
| `output/q34_independent_recheck_rerun.json` | 独立再検証の再生成出力・`88461251cc76` |
| `output/sha256_manifest.txt` | 全入出力 sha256 表 |
| `input-pins.md` | 使用した出版正本の pin 表 |

## 解釈規約

計算結果の全称主張は行わない。本実験の水位は「第三実装・第三環境での bit-exact 再生」および「コーパス整合の確認」であり、K0351 の数学的証明自体の再証明ではない。checked 数・seconds 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は本レーンと無関係で UNKNOWN のまま。**
