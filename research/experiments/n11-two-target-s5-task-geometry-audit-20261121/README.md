# 11×11 二対象S5候補供給の独立幾何監査

既存の二対象設計（{60,27}の第三手100・108を同じS4 classへ束ねる研究）で使うS5候補一覧を、独立の整数幾何実装で全件照合した。これは探索結果ではなく、次のexact probeを選ぶための候補供給と台帳の検証である。

## 入力固定

- 入力snapshot: `d173632fc19a3d9f9abf8e66d0595f4629748bf0`
- 公開時のmain: `3b83004b0b0354fa48a60c402134ebe8063e78f8`。7入力blobはsnapshotと同一。
- 入力7点はすべてGit blob SHA-1でpin。検証機は一致しない入力で停止し、監査JSONを書かない。

| 入力 | Git blob SHA-1 |
|---|---|
| 初期S5 tasks | `366ff5cd673c09694c8b047e76291174e6c91cf4` |
| 初期S4 classes | `7e87281fb254d8e8ca85894f16ac29e3137e5b3d` |
| post-probe S5 tasks | `fa4ba4ab8b0f165c90945f7505de29aebb53d3ac` |
| post-probe S4 classes | `fc1e3bcf85857ec2248ea7311d5be0f556f19291` |
| probe前exact cache | `bcdba2d0ae3309e6e80702068ee5a64266f622ff` |
| merged exact cache | `5f20fea7993e1faef15b4bfc4219538858a3223a` |
| quarantine registry | `6a320237545874ddd841c90be095cccccc46249d` |

## 方法

標準ライブラリのみの検証機が、各5石キーについて次を直接再計算する。

1. 5石であること、D4の8変換に対する正準形。
2. 5石盤が安全（4点共円・共線の禁止を満たす）であること。
3. 全空点と既存3石組の整数4点行列式を調べ、合法手数が入力CSVと一致すること。
4. 5石から1石ずつ除いて得る4石parentをD4正準化し、UNKNOWNの親class一覧と数が入力に一致すること。
5. taskが該当cacheに存在せず、撤回済みquarantineにも入っていないこと。

初期tasksはprobe前cacheと、post-probe tasksはmerged cacheと比較する。初期一覧に残った2件の新exact verdictをpost一覧から除く関係、cacheの差分、各parent classのunknown/loss差分も照合する。

## 結果

- 初期一覧: 4,577 keys。7 gate×4,577 = **32,039 PASS**、違反0。
- post-probe一覧: 4,575 keys。7 gate×4,575 = **32,025 PASS**、違反0。
- 全件が5石・D4正準・安全。合法手数は80〜113で、一覧値と一致。
- live parent: 1 class共有2,688 keys、2 classes共有1,887 keys。
- cache: 5,741→5,743 exact entries。追加2件は両方LOSS。
- 初期一覧とmerged cacheの重複はこの2件だけ。post一覧のmerged-cache重複0。quarantine active 2件と候補/cacheの重複0。
- 2件のLOSSでactive unknown S5 incidenceは6,466→6,462、distinct unknown S5は4,577→4,575。更新parentは3 class（1 classに2件、残る2 classに各1件）。S4 statusは62 UNKNOWN / 53 WINのまま。

### 次のprobe候補（勝敗未確定）

`1306114260682670080:0` は2つのUNKNOWN S4 class（`1297107061427929088:0` と `1306043891938492416:0`）を共有する5石局面。合法手88、両親の残り未知子は101・102。key固有の過去探索は0件。

同じ「2 parent・key固有historyなし」1,887候補中、node費用proxyが最小の候補はこのkey（5,041,585）。次点は5,069,670で差28,085。proxyは打切り履歴から作った参考値で、上界・期待費用・勝敗確率ではない。legal-bandの765観測（WIN55/LOSS682/UNKNOWN28）もkey固有ではなく、選択偏りがあるため確率と解釈しない。

## 再現

```sh
python3 research/experiments/n11-two-target-s5-task-geometry-audit-20261121/scripts/audit_candidate_supply.py --root . --out research/experiments/n11-two-target-s5-task-geometry-audit-20261121/output/audit.json
```

- 検証機: `audit_candidate_supply.py`（13,221 bytes・SHA-256 `58d96602af1cb1ac5635cf96faebe922429c230d7b132cabdb66b645f173b952`）
- 監査正本: `audit.json`（8,182 bytes・SHA-256 `f2bcc59fd1f3ff51d71c96ce918cee74938340ebc6381fe352a100098e4627a1`）
- 2回の再実行でbyte一致。1 byte tamperの負対照はpin mismatchで拒否し、監査JSONを書かない（詳細は`reproduction.log`）。

この監査は候補一覧と幾何・cache台帳の整合性のみを保証する。S5 verdict、S4 closure、二石root、標準11×11空盤の勝敗は新たに確定しない。
