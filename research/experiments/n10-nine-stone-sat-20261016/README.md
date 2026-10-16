# 10×10 九石極大安全集合の SAT 判定（2026-10-16）

## 背景

K0034 により 10×10（n=10）の極大安全集合の最小サイズは `9 <= s_10 <= 10`。

- 下限 `s_10 >= 9`: 8石以下の全排除は round56 の直接全探索（再開可能 C++、約19.5億節点）で完了。
- 上限 `s_10 <= 10`: round49 の10石極大安全集合の明示証人（本実験の検証器で再確認済み）。

残る問い（K0145 / K0149）は「9石の極大安全集合が存在するか」、すなわち `s_10 = 9` か `10` か。本実験はこれを SAT（curved 符号化）+ 独立検証で決着する試み。

定義（K0034 と同じ）: **安全** = 同一直線・同一円周上に4点がない。**極大安全** = どの空点を追加しても安全でなくなる。

## 曲線符号化（三つ組符号化の置き換え）

点変数 `x_p`（`p = y*10 + x`、100点）+ rich curve 変数 `z_C`。

- **rich curve** = 10×10 の格子点を4点以上含む直線または円。12324 本。3点ちょうどの曲線（78956 本）は blocker になり得ない（他の格子点を含まない）ので変数を作らない。
- `z_C -> |S∩C| >= 3`: 各2点ペア `{i,j} ⊂ C` について節 `¬z_C ∨ ∨(C∖{i,j})`。この節族は `|S∩C| >= 3` と同値（`|S∩C| <= 2` のとき違反するペアが存在し、`>= 3` なら常に充足）。安全節と合わせ `z_C=1 ⟺ |S∩C| = 3`。
- **被覆（極大性）**: 各点 `p` に節 `x_p ∨ ∨_{C∋p} z_C`。空点は必ず「S をちょうど3点含む曲線」上にある（その曲線は p を含むので4点以上、すなわち rich）ことと同値。任意の三つ組 `T ⊂ S` は曲線 `C(T)` を定め、`m(T) = C(T)` 上の空点数 として `Σ_T m(T) = Σ_{blocking C} m(C)` が成り立つため、被覆節の集合は極大性の必要十分条件。
- **安全**: 禁止四点 54441 個（`round25_forced_verify.geometry(10)` の行列式判定で確定）の no-all 節 `¬p∨¬q∨¬r∨¬s`。
- **基数**: 点変数への `atmost 9` / `equals 9`（pysat seqcounter）。

対称性制約（オプション、いずれも単独使用のみ健全）:

- `--wedge`: 各点軌道（rot90 と反射 s0 で生成）の代表点集合のうち少なくとも1点を S に含める。任意の軌道は rep を含む要素を持つため健全。
- `--lex`: 7つの群元 `g`（rot90^k, s0∘rot90^k、k=0..3）に対し `S <=lex g(S)`（点順序 `y*n+x`）。軌道の lex-最小元が同時に全制約を満たすため健全。
- **`--wedge` と `--lex` の併用は不健全**（「lex-最小元が rep を含む」は偽: ランダム300軌道中202で反例）。スクリプトは併用を `SystemExit` で拒否する。
- 不健全な旧 CNF `curve_eq9_w_lex.cnf`（wedge+lex、sha `0eae1159…`）は未使用・実行禁止。

### インスタンス

生成: `python scripts/build_curve_cnf.py --n 10 --bound 9 [--exact] [--wedge] [--lex]`

| tag | 意味 | vars | clauses | sha256 |
|---|---|---|---|---|
| `curve_le9.cnf` | n=10, ≤9 | 13243 | 145721 | `02f2e33623877ae4d4751e1a763a5afc01e81a5b3bbafadad89d5e11edaf509d` |
| `curve_eq9_w.cnf` | n=10, =9, wedge | 14062 | 147278 | `8dea611b40b2f5a2e9910c7d21380b0fa45ad630f627c9ba3e9240beb8708f70` |
| `curve_n10_eq9_lex.cnf` | n=10, =9, full-lex | 14762 | 151449 | `dfa58afa0d50196dafb5a7203f7d481d0d1d6c6b60a454843c059ecd27dddd8c` |
| `curve_n10_le9_lex.cnf` | n=10, ≤9, full-lex | 13943 | 149893 | `18d1afb6263d437235415af84128d0e71c0cdb44309b35a6a752e5857d6dc3c5` |
| `curve_n9_eq9_lex.cnf` | n=9, =9, lex（実装コントロール） | 8758 | 84623 | `314bd4be31b2e7e46334a9f20f1f1d746fa0ca5fe49a502c5ffd2423d3ff81b2` |
| `curve_n9_le8.cnf` | n=9, ≤8（既知 UNSAT 側の難易度確認） | 7479 | 79890 | `dc2763dd4936b2c25ef7149cffb5068ca9b1cc1e57aaf7e39a1ec23b878cee72` |
| `curve_n8_le7.cnf` | n=8, ≤7（既知 UNSAT 側の難易度確認） | 4018 | 41112 | `370164ef6cd32c21e7ba8e7fe38b25aed1a135a595a5db512497cce72c0cdcec` |

参考（旧・三つ組符号化、置き換え済み・実行打ち切り）: `n10_le9.cnf` sha `68b5f47d…`、`n10_eq9_wedge.cnf` sha `30899ca7…`。

再生成時の注意: `le9` / `eq9_w` は最終スクリプトで byte-identical 再生成を確認済み。lex 系は群元リスト順に依存するため sha は同一生成器での再現用。

## 実行

WSL Ubuntu（16 CPU）。cadical 1.7.4（`--no-binary` で ASCII DRAT）、kissat（source build `/root/kissat/build/kissat`）。

```
cadical --no-binary curve_le9.cnf proof_curve_le9.drat
cadical --no-binary curve_eq9_w.cnf proof_curve_eq9w.drat
cadical --no-binary curve_n10_eq9_lex.cnf proof_curve_eq9lex.drat
cadical --no-binary curve_n10_le9_lex.cnf proof_curve_le9lex.drat
kissat --quiet curve_le9.cnf
kissat --quiet curve_eq9_w.cnf
kissat --quiet curve_n10_eq9_lex.cnf
kissat --quiet curve_n10_le9_lex.cnf
kissat --quiet curve_n8_le7.cnf
kissat --quiet --sat --no-binary curve_n10_eq9_lex.cnf proof_kissat_eq9lex.drat
kissat --quiet --unsat --no-binary curve_n10_le9_lex.cnf proof_kissat_le9lex.drat
kissat --quiet --sat --seed=27 curve_n10_eq9_lex.cnf
```

方針: **UNSAT はソルバの申告だけでは証明としない**。`drat-trim <cnf> <drat>` で証明検査を通ったときのみ UNSAT 側の結論に使う。SAT は証人を下記の2実装で独立検証する。

## 独立検証器

- `scripts/verify_witness.py <witness.json>`: 新規 Python 実装。整数行列式（同次座標 `(x²+y², x, y, 1)` の 4×4 det）で四点の共線/共円を判定し、安全性（全四点 det≠0）と極大性（全空点が blocking 曲線で被覆される）を検証。blocker 一覧を出力。入力は `{"n": 10, "witness": [ids...]}`。
- `scripts/witness_check.cpp <n> <ids...>`: 独立 C++ 実装（`__int128` の 4×4 det、行 `(x²+y², x, y, 1)`）。python 版とは別コード。
- コントロール（両実装で一致）:
  - round49 の10石証人 → PASS（90/90 blocked）
  - n=9 SAT 証人 `[28,34,43,48,51,52,59,73,76]` → PASS
  - n=8 証人 → PASS
  - 10石証人から1点除いた9点集合（非極大）→ FAIL（未被覆点を報告）

## 独立局所探索（`scripts/local_search.cpp`）

全曲線（161700 三つ組シグネチャから 91280 曲線 = rich 12324 + 3点曲線 78956）を構築し、9点集合上で SA。目的関数 `covered − 10^4 × unsafe`。

```
g++ -O2 -std=c++20 -o local_search local_search.cpp
./local_search 9 <restarts> <steps_per_restart> [seed]
```

`escape_search.cpp` は `./escape_search <seed> <radius 1|2|3> [max_plateaus]`。SAで90-plateauに到達後、指定半径の全swapを網羅列挙する。

観測: `covered=90/91, unsafe=0`（= 空点は1点だけ未被覆）に3シードすべてが数万ステップ以内で到達。`covered=91` は未観測（2026-10-16 02:10 時点）。

**正例コントロール（k=10）**: 同ツールを `./local_search 10 ...` で走らせると既知の存在例（9≤s_10≤10 の上界証人）を再発見するはずで、実際に新たな10石極大安全集合

```
13 50 56 59 63 68 77 83 85 98
```

を発見した（round49 の証人 `[21,27,31,35,36,46,65,81,29,48]` とは別集合）。両検証器で PASS（`unsafe_quads=0, unblocked=0`、90 blockers）。これにより FOUND 経路と検証器の両方が実データで校正された。

**局所閉性の観測**: `escape_search.cpp` は90-plateauに到達後、全ての1-swap（819通り）と2-swap（147,420通り）を網羅列挙して91到達を試みる。異なる5つの90-plateauで2-swap閉（escapeなし）。3-swap網羅（10,204,740通り/plateau）は実行中。

注意: std::array ローカル+ラムダ+`nt++` 添字の組み合わせが g++ `-O1/-O2` で誤コンパイルを誘発したため、現行版は flat な `std::vector` と明示文に書き直してある（-O0 で再現しない最適化依存バグ。修正版は -O2 で正常動作を確認済み）。

## 独立全域探索（決定的経路）

`scripts/nine_stone_exact_search.cpp` は round56 の辞書式再開可能な厳密探索（`kmin_cover`）を、九石の問いに向けて一般化したもの。

- 変更点: depth=0（最初の石）の制限を「k≤8 の全幅論法（初石 0..4）」から、**D4 軌道代表15点**（10×10: `0 1 2 3 4 11 12 13 14 22 23 24 33 34 44`）に変更。任意の集合 S に対し D4 の元 g で g(min S) を代表点に移せるため、n, k を問わず健全。対称変換は安全性・極大性を保つ。
- それ以外（安全判定、三点補完数上界、被覆可能性、辞書式再開）は round56 と同じ。
- `scripts/nine_run.py` が代表ごとの安全なチャンク実行（node limit + `timeout_prefix` からの再開）を回し、毎チャンクの JSON を保存する。全代表が `complete:true, found:false` なら `(n,k)` の厳密な不在。
- 検証済み: n=8 k=7（不在, s_8=8）、n=8 k=8（発見）、n=9 k=9（発見, round46証人と別経路）、**n=10 k=8: 全15代表が完了し「8石極大なし」**（11,994,745,675節点 / 12,072プロセス秒。round56 の五root結論と一致。一般化した depth-0 制限と辞書式再開の交差検証）。
- n=10 k=9 実行中（2026-10-16 06:50 時点）: 10代表（11,12,13,14,22,23,24,33,34,44）は完了・不在。残る中央5代表（0,1,2,3,4）は 42 チャンク（8.4e9 ノード/代表）まで到達。推定総ノード ~1.1e11（k=8 の約9倍）。
- 事故記録: 06:33頃、WSL のファイルシステム全体が読み取り専用になり（/root も /tmp も書き込み不可）、実行中の5代表が停止。原因は**ホスト C: ドライブ枯渇（残り0.1GB）**。Ubuntu の ext4.vhdx（C: 上で93GB）が DRAT 証明などで成長し、C: が満杯になって vhdx の新規割り当てが失敗し ext4 が RO 化した。対処: vhdx 内の古い DRAT（~25GB）を削除し（ext4 内 932GB 空きに回復）、以後 cadical の DRAT は Z: ドライブ（2.3TB 空き）へ出力する。
- 再開の健全性: 再開は「辞書式順序で小さい接頭部だけ飛ばす」round56 の保存された境界規則の通り。resume は保守的（その節点の部分木を丸ごと再探索）。chunk JSON は全326件無事だった。

s_10=10 を結論するには、全15代表での九石不在 + round49 の十石証人（=s_10≤10）が必要。逆に九石証人が見つかれば s_10=9。

## 結果: s_10 = 10

**10×10 に九石の極大安全集合は存在しない。** したがって s_10 = 10（round49 の十石証人が s_10 ≤ 10、round56 の八石以下全域排除が s_10 ≥ 9、本実験の九石全域排除が s_10 ≠ 9）。

### 厳密全域探索（決定的経路）

`nine_stone_exact_search`（D4 第一石代表 15 点 `0 1 2 3 4 11 12 13 14 22 23 24 33 34 44`、辞書式再開・三点補完数上界・被覆可能性の枝刈りは round56 と共通）を n=10, k=9 で実行。**全15代表が `complete:true, found:false`**。

| 代表 | チャンク | 節点 | 秒 |
|---|---:|---:|---:|
| 0 | 91 | 18,157,334,494 | 18,636 |
| 1 | 81 | 16,066,311,019 | 16,862 |
| 2 | 73 | 14,472,912,882 | 15,581 |
| 3 | 66 | 13,019,590,525 | 14,198 |
| 4 | 60 | 11,922,169,988 | 13,184 |
| 11 | 28 | 5,545,289,949 | 6,834 |
| 12 | 24 | 4,772,431,100 | 5,836 |
| 13 | 21 | 4,169,518,181 | 5,272 |
| 14 | 19 | 3,728,365,220 | 4,812 |
| 22 | 7 | 1,327,202,189 | 1,703 |
| 23 | 6 | 1,129,107,646 | 1,572 |
| 24 | 6 | 1,001,344,455 | 1,326 |
| 33 | 2 | 251,926,901 | 403 |
| 34 | 2 | 216,255,250 | 347 |
| 44 | 1 | 37,117,003 | 60 |
| **計** | **487** | **95,816,876,802** | **106,626** |

`output/audit-nine_k9.txt`（連番チャンクの連鎖・`resume_prefix == 前 chunk の timeout_prefix`・最終 chunk `complete:true`・全 chunk `found:false` を機械検査）→ **AUDIT PASS**。`output/manifest_nine_k9.json` に全487チャンクの sha256 とノード数・時刻を保存。

D4 還元の根拠: 任意の極大安全集合 S に対し、min(S) を代表点に写す D4 の元が存在し、対称変換は安全性・極大性を保つ。第一石を代表に固定しても各軌道の集合がちょうど1回列挙される。

### 検証

1. **正例コントロール**: 同ツールは n=9, k=9 で証人 `[0, 1, 5, 29, 40, 47, 51, 56, 61]` を発見。`verify_witness.py`（72 blocked, bad quads なし）と `witness_check`（unsafe=0, unblocked=0, PASS）の両独立実装で極大安全を確認。葉条件 `blocked == P-K` が独立検証器と一致。
2. **交差検証**: 同ツールで n=10, k=8 を全15代表実行 → 全て不在（11,994,745,675 節点、AUDIT PASS）。round56 の別還元（初石0..4の五root）での八石全域排除と一致。`output/audit-cross_k8.txt`, `output/manifest_cross_k8.json`。
3. **SAT 側（符号化の正しさ）**: 曲線符号化（14,762 vars / 151,449 clauses）で n=9 =9 を kissat が SAT。証人は両検証器で PASS。n=10 ≤9 は cadical 4 系統 ~8 時間・kissat 複数 ~3 時間でも SAT/UNSAT 未着 — 不在と整合するが、この符号化自体は九石探索に不向きだった。
4. **独立反証路（不成立）**: cadical 4系統に DRAT 証明を Z: へ出力させ約5.5時間（~19,700秒）並行実行したが、いずれも SAT/UNSAT に到達せず。その後ホスト C: の残量枯渇で WSL の ext4 が I/O エラーを起こして停止し、当該実行は失われた（途中までの DRAT は不作動のため破棄）。**この経路は独立証明を与えていない**。本結論は上記 1-3（完全列挙・交差検証・正例コントロール）に依拠する。曲線符号化はこの規模の UNSAT には不向きと判断。
5. **局所探索（参考・非決定的）**: 9石 SA は全シードで `covered=90/91, unsafe=0` に到達（=空点1点が未被覆）。61 個の plateau から 1/2/3-swap 全数（~1億評価）で escape なし。九石不在と整合。

### 十石証人の再発見（別経路）

局所探索 k=10 が新たな十石極大安全集合 `13 50 56 59 63 68 77 83 85 98`（round49 証人と別集合）を発見、両検証器で PASS（`unsafe_quads=0, unblocked=0`）。s_10 ≤ 10 の第二証人。`output/witness_k10_new.json`, `output/witness_round49.json`, `output/n9_control.json`。

## 実行・再現

```sh
# 厳密探索（代表ごと並列、時間無制限）
g++ -O3 -std=c++17 -o nine_stone_exact_search scripts/nine_stone_exact_search.cpp
python3 scripts/nine_run.py 10 9 nine_k9 200000000 0 <root>
# 中断後は最後の chunk から
python3 scripts/nine_run_resume.py 10 9 nine_k9 200000000 <root>
# 監査
python3 scripts/audit_chunks.py nine_k9
python3 scripts/nine_manifest.py nine_k9
```

