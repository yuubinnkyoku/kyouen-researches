# 残余72行・36-rootの正確D4クラス→root所属再生と分割候補のクラスレベル評価

## 目的と境界

36-root worker partition candidate（`../n11-residual72-worker-partition-candidate-20261121/`）は
10-stone class-to-root membershipの正確な再生成がtime outし、pairwise表proxyのみで評価した
（「per-worker class-copy計数は主張しない」）。本実験はその測定ギャップを埋める:
出版census（`../n11-residual72-36root-three-ply-frontier-20261120/`）と同じ方法で
36 root×三手先（10石）を再列挙し、**正確なクラス→root所属マップ**を再構築して
(a) 出版正本との全数値照合、(b) 3-root共有5類の特定、(c) baseline・candidate両配分の
クラス単位worker統計、(d) 9石・8石層の同種統計（未測定だった層）を出版する。

幾何的なクラス簿記であり、DFPN節点数・表命中率・探索費用ではない。分割変更は提案しない。
36-root depth-10掃引（単一オーナー進行中）のファイル・assignmentには一切触れていない。

## 入力と方法のpin

- K1075正本: `../n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json`
  （SHA-256 `49b6f85f…`・git blob `45744d82…`起動時に照合）
- 方法pin: `../n11-residual72-36root-three-ply-frontier-20261120/audit_36_root_three_ply_frontier_20261120.mjs`
  （SHA-256 `7177a25a…`）。11×11・8変換D4正準形・BigInt `[x²+y²,x,y,1]` 行列式
  （余因子/Leibniz両展開の全点照合）・合法手のBitMask全数・root四点組安全性検査を正則に再現。
- 出版census正本: 36-root-three-ply-frontier-20261120.json（SHA-256 `94fdb0c6…`）を照合対象に固定。
- partition candidate正本: worker-partition-candidate-20261121.json
  （SHA-256 `09b394b8…`）の `root_groups` をcandidate配分に固定。
- 所属ビットは36 root分をBigIntビットマスクで保持する。

実行方法: `scripts/exact_membership_regen_20261121.mjs` は
`regen <k1075.json> <chunkdir>`（全36 root逐次列挙・root単位chunk出力）と
`assemble <k1075.json> <chunkdir> <census.json> <candidate.json> <outdir>`（照合gate・統計・出力）の
2段階。全出力は失敗時書き込まないfail-closed構成。

## 結果（全gate通過後に出力）

### 10石層（出版censusとの完全一致 + 正確な所属マップ）

| 指標 | 値 |
|---|---:|
| 一意D4クラス | 728,370 |
| root別membership合計 | 733,800 |
| root内D4併合 | 55 |
| 多重所属membership | 5,430（hist {1: 722,945, 2: 5,420, 3: 5}） |
| pairwise overlap総計 | 5,435（221組・出版正本と全件一致） |
| 再生成の実行時間（本sandbox・逐次） | 約3.5秒（point checks 16,007,211・三点組 132,291・root四点組 1,260、出版値と同一） |

多重所属5,425類（2-root共有5,420 + 3-root共有5）の全数を
`output/multi-root-classes-10stone-20261121.json` に出版した（`roots`欄はK1075 `witness_full`
配列の0-based index）。**3-root共有5類は本研究で初めて特定**された:

| クラス（D4正準形hex） | 所属root index |
|---|---|
| `00000000010002801202040020801000` | 1, 13, 23 |
| `00000000010004801302000000901000` | 1, 21, 22 |
| `00000000010008801202000000801401` | 1, 19, 20 |
| `00000010400000003820000008003100` | 1, 21, 33 |
| `00000010400000003820000008013000` | 21, 22, 33 |

### 分割のクラスレベル正確統計（10石層）

「worker内冗長コピー」= 同一worker内で同一クラスを複数rootが参照した回数 Σ(n_w−1)。
「worker横断コピー」= 複数workerにまたがるクラスの Σ(span−1)。両者の和は
多重membership 5,430に等しい（保存則）。

| 配分 | worker内冗長 | worker横断コピー | 横断類数 | span分布 |
|---|---:|---:|---:|---|
| baseline（roots[W::4]） | 1,241 | 4,189 | 4,188 | {1: 724,182, 2: 4,187, 3: 1} |
| candidate（root_groups） | 3,432 | 1,998 | 1,997 | {1: 726,373, 2: 1,996, 3: 1} |

candidateはworker横断コピーを4,189→1,998（−52.32%: pairwise proxyの52.30%減と一致）に
減らす代わりに、worker内冗長コピーを1,241→3,432に増やす。per-workerのユニーククラス数は
`output/exact-class-membership-20261121.json` の `partition_stats` に収録。

### 9石・8石層（新規測定）

| 層 | 一意クラス | 多重所属 | baseline(内/横) | candidate(内/横) |
|---|---:|---:|---|---|
| 9石（2手先） | 56,464 | 133（hist {1: 56,331, 2: 133}・最大多重度2） | 29 / 104 | 84 / 49 |
| 8石（1手先） | 2,251 | 0 | 0 / 0 | 0 / 0 |

9石層ではcandidateはworker横断コピーを104→49に減らすが、worker内冗長を29→84に増やす
（10石層と同じ傾向）。8石層では36 root間の共有は完全に0（全2,251類が単一root専属）。
9石の訪問数合計はroot別56,597（出版値）と等しく、root内併合は9石層では0。

## 検査

assembleは20 gateを全通過した場合のみ出力する（fail-closed）:

1. 36 roots / root四点組1,260
2. 行列式展開: point checks = 三点組×121（16,007,211 = 132,291×121）
3. 9石総数 56,597 / 4. raw 10石総数 733,855 / 5. D4 membership総数 733,800
6. root内併合 55 / 7. 終局9石 0 / 8. 第三手恒等式 third = 3×raw
9. 全体D4類 728,370 / 10. 多重所属 5,430 / 11. 最大多重度 3
12. pairwise 221組 / 13. **pairwise全件値一致（shared・worker割当・並び順含めて出版正本と同一）**
14. baseline worker別pairwise 1,242/4,193 / 15. 出版summary全数値一致
16. worker_statsは出版censusと同一 / 17. candidate配分のexactly-once（36 root・各worker 9）
18. baseline cross/withinがcandidate JSON出版値と一致 / 19. candidate cross/withinが出版値と一致
20. d4 per-worker負荷がcandidate JSON出版値と一致

決定性: 別cwd・別プロセスで再実行した4出力物はすべてbyte-identical。
per-root計数（first・n9・raw10・d4・within・terminal9・min3・max3・third）は36 root全件で
出版censusのper_rootと同一。

## 再現手順

```sh
node scripts/exact_membership_regen_20261121.mjs regen \
  ../n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json \
  /tmp/chunks
node scripts/exact_membership_regen_20261121.mjs assemble \
  ../n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json \
  /tmp/chunks \
  ../n11-residual72-36root-three-ply-frontier-20261120/output/36-root-three-ply-frontier-20261120.json \
  ../n11-residual72-worker-partition-candidate-20261121/output/worker-partition-candidate-20261121.json \
  output
```

出力物: `output/exact-class-membership-20261121.json`（統計・gate・5類の3-root共有）
`output/multi-root-classes-10stone-20261121.json`（5,425類の全多重所属表）
`output/multi-root-classes-09stone-20261121.json`（133類）
`output/multi-root-classes-08stone-20261121.json`（0類）。

## 解釈規約

- クラスの幾何共有はDFPN節点数でも表命中率でもない。同一D4類が探索の同深さ・同証明境界で
  hitするとは限らない。
- candidateの優位はクラス簿記上のものであり、分割変更の提案ではない。実測TT hit率との比較は
  36-root depth-10掃引の完了後に行うべきで、本実験は掃引の前提を変えない。
- 勝敗・行閉鎖・候補rootの資格は本実験の対象外。REFUTED-D10はLOSS証明ではない。
- 標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。
