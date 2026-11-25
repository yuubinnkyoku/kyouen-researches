# 3×3〜6×6の安全局面サイズ分布の三系統再導出とSAT較正（2026-11-22、高速レーン）

標準共円盤（q=4）の 3×3〜6×6 について、**安全集合（禁止四点組を1つも含まない石集合）の
サイズ別個数（Z_n係数）**を、相互に独立な3系統の実装（Node DFS・独立Python DFS・2^N全走査）と
SAT（exactly-k・Sinz双方向カウンタ＋公式kissat 4.0.4）で再導出し、既刊・archived の値と
一致を確認した。あわせて極大側の全行・軌道センサスをcompact gate として記録する。

## 0. 位置づけ（先に読む）

- 本実験の単一オーナー宣言は
  [research/log/2026-11-22-n3-n6-maximal-complete-spectrum-single-owner-note.md](../../log/2026-11-22-n3-n6-maximal-complete-spectrum-single-owner-note.md)
  （開始時HEAD `6c142d53`・受入条件6項目）。受入条件は全て満たした。
- その後の確認で、宣言の中核（K0030全cell較正・全77行・D4軌道・三点共線統計）は
  **同日並走レーンが単一オーナー宣言 `b055d87f` の下で先行出版済み**であることが判明した
  （K1225、実験 [small-board-maximal-rows-20261122](../small-board-maximal-rows-20261122/README.md)）。
  本実験の全行値・軌道数は K1225 と完全一致しており、**極大側の正本出版は同実験に一任する**。
- 本ディレクトリの刊行対象は、宣言スコープのうち K1225 が含まない補完部分に絞る:
  1. **安全側（非極大を含む全安全集合）のサイズ別ヒストグラム**を3系統で再導出し、
     archived監査コーパス（round4_b228d の Z_n(lam) 係数）・K0004の安全集合総数・K0226本文のn5引用値と一致検査。
  2. **SAT exactly-k による K_3..K_6 の DFS 非依存確定**（k=K_n 行の充足全列挙と k=K_n+1 行のUNSAT）。
  3. **n3 を含む全 367,440 極大配置の独立 Leibniz 幾何検証**（K1225 の幾何検証は n4..6 の 367,384 配置で
     n3 k5 の 56 配置が範囲外だった。本実験が補完）。
- Z_n係数そのものは既知データの再検査であり、本実験の新規数学的主張ではない。
  唯一の新規記録は F_3=14（3×3禁止四点組カタログ、K1225はF_4=194まで記録）。

## 1. 結果

### 1.1 安全集合のサイズ別ヒストグラム（Z_n係数、n=3..6）

`output/safehist_n3_n6.jsonl`（Node DFS 2走行・Python DFS・2^N全走査の全系統一致）:

| n | k=0..n² の個数 | 総数 | 最大安全サイズ K_n |
|---|---|---:|---:|
| 3 | 1, 9, 36, 84, 112, 56 | 298 | 5 |
| 4 | 1, 16, 120, 560, 1,626, 2,360, 1,064, 64 | 5,811 | 7 |
| 5 | 1, 25, 300, 2,300, 11,824, 37,272, 59,192, 35,208, 5,172, 100 | 151,394 | 9 |
| 6 | 1, 36, 630, 7,140, 56,414, 301,952, 997,796, 1,783,296, 1,459,292, 438,952, 35,316, 464 | 5,081,289 | 11 |

- 総数は [K0004](../../knowledge/items/K0004-n1-n6-all-safe-grundy.md) の出版値（298/5,811/151,394/5,081,289）と一致。
- 級ごとの値は archived 監査コーパス
  [original-claims round4_b228d.txt](../original-claims/output/round4_b228d.txt) の Z_n(lam) 係数と
  全桁一致（n3..n6 全33係数byte一致検査）。n5 の級ごとの値は K0226 本文の引用値とも一致。
- K_n = 5/7/9/11 は [K0029](../../knowledge/items/K0029-n1-n9-maximum-safe-sizes.md) の既刊値と一致（値更新なし）。
  2n+1 (@n=2..6) という形の一致は観察として記録する（n7以降への外挿はしない）。

### 1.2 頂点サイズの自動極大性（補題の機械確認）

最大サイズ K_n の安全集合は包含極大である（真部分集合に石を足しても安全なら K_n を超え、K_n
の最大性に矛盾。包含極大性の定義と K_n の最大性から従う自明な補題）。機械確認として、
SATの k=K_n 行の全列挙個数（56/64/100/464）が極大行の k=K_n 分布
（[K0030](../../knowledge/items/K0030-n3-n6-maximal-safe-size-distributions.md)・K1225 の 56/64/100/464）と
一致することを全4盤で確認した。**k=K_n では safe と maximal の個数が一致する**。
一方、中部の行では一致しない（例: 6×6 の k=10 は safe 35,316 個に対し maximal 30,492 個。
差の 4,824 個は非極大の安全10石配置）。

### 1.3 SAT exactly-k による安全行の独立確定

`output/safe_count_n*_k*.json`（CNF: 各禁止四点組の blocking 節 + exactly-k をSinz逐次カウンタ
2本（at-most-k 正側・at-most-(N-k) 負側）で符号化、充足全列挙、モデル重複除去; solver: kissat 4.0.4
公式binary を md5/sha256 ピン、MANIFEST §B）:

| cell | モデル数 | 対照 |
|---|---:|---|
| n3 k=1..5 | 9/36/84/112/56 | Z_3 係数・2^N全走査と一致（較正） |
| n3 k=6,7 | 0 (UNSAT) | Z_3 の k≥6 消滅 |
| n4 k=4..7 | 1,626/2,360/1,064/64 | Z_4 係数・2^N全走査と一致（較正） |
| n4 k=8 | 0 (UNSAT) | Z_4 の k≥8 消滅 |
| n5 k=9 | 100 | K0030 出版行・Z_5 係数と一致 |
| n5 k=10 | 0 (UNSAT) | 5×5 に安全10石集合は不在（K_n=9 の SAT 側裏付け） |
| n6 k=11 | 464 | K0030 出版行・Z_6 係数と一致 |
| n6 k=12 | 0 (UNSAT) | 6×6 に安全12石集合は不在（K_n=11 の SAT 側裏付け） |

k>K_n の UNSAT と k=K_n の正の充足を合わせれば **K_3..K_6 は SAT 単独で DFS 非依存に確定**する。
at-most-k については Sinzカウンタが一方向であることに注意（K1226と同じ方式の壁の記録）。
exactly-k は正負双方向の2本のカウンタで下限・上限の両方を強制する。

### 1.4 s_5/s_6 下側の SAT 再導出（at-most + 極大制約）

pinned enc_sat2 v2.1（安全+極大+D4 lex-leader、K1224出版正本とbyte同一）+公式kissatで
5×5のat-most-4は **UNSAT**、6×6のat-most-5は **UNSAT**（`output/spectrum_summary.json` の
`sat` ゲート、CNF指紋は MANIFEST §C の `exp/work/n5k4.cnf`・`n6k5.cnf`）。よって
s_5≥5・s_6≥6 の下側を DFS と独立な方法で再導出（上側は K0030 表・K1225 の行分布が与える。
値更新なし）。補助に `output/sat_enum_n5k5.json`/`sat_enum_n6k6.json`（lex-minモデル各1件、
DFS集合に所属）と `output/atmost_s_lower_*.meta.json`（CNFメタ情報）を刊行。

### 1.5 極大側の compact cross-check gate

`output/spectrum_summary.json`（master collation）と `output/verify_spectrum.jsonl` に、
K0030全cell・全77行（ゼロ行含む）の2走行決定性（cfg行byte一致・nodes bit一致）、
全15非零cell 367,440 配置の独立 Leibniz 幾何検証（V1安全/V2極大/1石除去破壊/陰性対照、全て0 bad）、
D4軌道センサス（fail-closed C1..C3）を記録する。生のenum raw・classify/census 大型jsonは
再刊行しない（指紋は MANIFEST §C）。極大側の値は全て K1225 出版と一致:

- 非零行: n3{k5:56}・n4{5:176,6:688,7:64}・n5{5:4,6:1136,7:11280,8:4340,9:100}・n6{6:8,7:3952,8:115496,9:199184,10:30492,11:464}
- 軌道数: n3k5: 8・n4: 22/87/8・n5: 1/143/1413/543/13・n6: 1/494/14441/24898/3814/58（安定化群ヒストグラム込み）

## 2. 方法と検証行列

1. **幾何の二系統 byte一致**: 禁止四点組カタログを pinned census.mjs系統（K0057アンカー）と
   独立Python Leibniz 4×4行列式実装（forbidgen.py由来だが行列式は独立Leibniz 24項展開）で生成し、
   テキストとして byte同一（F_3=14〔新規記録〕・F_4=194・F_5=826・F_6=2491。
   F_5/F_6 は出版sha256一致）。`output/quartets_n*.txt`。
2. **列挙の3系統**: (a) Node DFS（pinned enum_catalog.mjs、n3のみ正準化の自由度を拡張した
   派生版 `scripts/enum_catalog_n3.mjs` を併用・`exp/scripts` 界隈の改変は MANIFEST §B の
   pinned指紋で区別）の2走行、(b) 独立Python DFS `scripts/dfs_py.py`（Leibnizカタログテキスト
   を自身の幾何として再検査）、(c) 2^N全走査 `scripts/brute_force_small.py`（n3/n4、独自Leibniz
   行列式付き、quartet内容の照合も実施）。safeヒストグラムと極大配置集合の両方で3系統一致。
3. **SAT系**: exactly-k符号化 `scripts/safe_subset_sat.py`、極大+lex-leader符号化は pinned
   enc_sat2 v2.1/sat_enum.mjs。SATの健全性較正として n3 k=1..7・n4 k=4..8 を
   2^N全走査のヒストグラムに対して照合（全一致）した上で、n5/n6 の tail 判定に適用。
4. **幾何検証**: `scripts/verify_spectrum.py` が全 found 配置をLeibnizカタログのみで
   SAFE+MAXIMAL検証（V1/V2/1石除去/C2陰性; tamper対照拒否は別途実施済み）。
5. **決定性**: Node 2走行の cfg 行 byte 一致・nodes bit 一致（`spectrum_summary.json` のrows）、
   Python行サマリ一致、SAT反復列挙の重複0（distinct==models）。

## 3. 非主張・trust境界

- 全体は有限計算であり形式証明ではない。実装と言う trust を含む（K1224/K1225 と同水準）。
- K0030・K0004・K0029・K0026 の値更新は一切ない。Z_n係数は archived corpus 既出のデータの再検査。
- nodes・elapsedMs は勝敗でも探索費用でもない。
- n7 k≤7の行（K1224）・n7 k≥8・n8の安全行の size 別分布（本実験は maximal 行の非空判定のみ
  K1226 既刊）・n≥9盤面・n2のZ係数の再検査は未着手。
- 標準11×11空盤・二石root・S2・closure class は本レーン非接触（UNKNOWN）。
- kissat 4.0.4 は公式 linux-amd64 binary を md5/sha256 ピンで参照し repo 内に再出版しない
  （s12-s13実験と同規約）。CNF本体も非刊行（MANIFEST §C に指紋）。

## 4. 刊行物

`scripts/`（本実験の派生・検証スクリプト7本）、`output/`（safeヒストグラム・SAT結果・
compact gate・quartetカタログ・brute force全走査結果・meta 35ファイル）、
`README.md`、`MANIFEST-sha256.txt`（刊行物のsha256・外部機材指紋・非刊行raw指紋の正本）。

## 5. 再現手順（要旨・刊行scriptsのみで書く）

```sh
# 独立Python DFS: 全安全部分集合のサイズ別ヒストグラム（例: 6×6）
python3 scripts/dfs_py.py 6 output/quartets_n6.txt --safehist

# 2^N 全走査（n=3/4・独自Leibniz行列式・quartet内容照合込み）
python3 scripts/brute_force_small.py 4 output/quartets_n4.txt out.json

# SAT exactly-k（例: 6×6 k=12 → UNSAT・k=11 → 464モデル）
#   usage: safe_subset_sat.py count <n> <k> <quartets.txt> <kissat> <out.json>
python3 scripts/safe_subset_sat.py count 6 12 output/quartets_n6.txt ./kissat out.json
python3 scripts/safe_subset_sat.py count 6 11 output/quartets_n6.txt ./kissat out.json

# 極大行の独立Python列挙（例: 6×6 k=8）
python3 scripts/dfs_py.py 6 8 output/quartets_n6.txt /tmp/py_n6_k8.csv --maximal
# Node側との配置集合一致ゲート: compare_impl.py <pass1_dir> <py_csv_dir> <n> <kmax>
# 幾何検証: verify_spectrum.py <quartets_dir> <pass1_dir> <out.jsonl>
# master collation: summarize.py（pass1/pass2・py行・各検証JSON → spectrum_summary.json）
```

禁止四点組カタログは `output/quartets_n*.txt` をそのまま使うか、
K1224実験（[n7-seven-stone-maximal-catalog-20261122](../n7-seven-stone-maximal-catalog-20261122/)）
刊行の census系統を pinned 指紋（MANIFEST §B）で用いて再生成する。
kissat 4.0.4 は公式 linux-amd64 binary を MANIFEST §B の md5/sha256 で検証して使用する。

実行環境: Node.js 22・Python 3.12。全スクリプトは決定的
（Math.random・時刻依存なし・固定列挙順）。
