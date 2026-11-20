# K1172第三検証recordのpart gate完全性ガード（2026-11-21）

## 着手時点と発見

最新mainは宣言commit `50d80188f3a4b187f20e5b9c99f99f025d3e360e`。AGENTS.md、knowledge README、K1172、K1172実験README、`assemble_third_record.py`、`reproduce.sh` を確認した。先行する同一対象の宣言・実験は見つからなかったため、単一オーナー宣言を [宣言ノート](2026-11-21-n11-k1172-third-record-assembler-gate-completeness-single-owner-note.md) として先に出版した。

既存組立器の `gates_all_pass()` は「partのgate辞書が空でない」「存在するentryがすべてpass」を確認する一方、期待するgate数・key集合・5 partの結合結果と最終auditの一致を確認していなかった。したがって、finalize後に同じgateを両batteryのpartから削除しても、残ったentryがpassでpart bytesが両battery間で一致すれば、この組立器のpart検査だけでは欠落を捕捉できない。

実際の出版auditを読むと、status PASS・gate_count 43・gates 43件・gates_orderedは辞書順と一致・missing_partsは空だった。prefixと件数で完全分割すると次のとおり。

| part | prefix | gate数 |
|---|---|---:|
| pin.json | g_pin_ | 1 |
| k1136.json | k1136_ | 13 |
| k1137.json | k1137_ | 13 |
| k1139.json | k1139_ | 13 |
| tampers.json | tamper | 3 |
| **合計** | | **43** |

## 補強

既存の20 gate recordとその正本（SHA-256 `a6a3e048…`）は変更せず、補助検証器 `scripts/verify_part_gate_completeness.py` を追加した。

- 各batteryのauditをSHA-256・byte数でpinし、schema・status・43 gate・sorted key list・missing_partsを確認。
- 5 partの件数・prefix・全entryのpassを検査。
- 5 partを結合した辞書が、pin済みauditの `gates` と**値まで完全一致**することを確認。欠落・余分・part間重複を拒否。
- JSON object内の重複keyも `object_pairs_hook` で拒否。
- 2 battery間の5 part bytes一致を再確認。
- 成功時だけ `output/part-gate-completeness.json` を書き、失敗時は正本を出力しない。

`tests/test_part_gate_completeness.py` に合成fixtureの8試験（正常分割、両battery同時欠落、余分、part間重複、値改変、battery間不一致、JSON重複key、audit順序改変）を追加した。`reproduce.sh` は元のbatteryと20 gate recordの後にこの試験と補助検証器を実行するよう更新した。

判定ロジックを43 gateの合成fixtureで別途実行し、正常分割はPASS、同一gateの両batteryからの削除・余分gate・重複gate・値改変はすべて拒否されることを確認した。重複JSON keyも拒否された。これは合成データでのロジック試験であり、repo同梱のunittestファイル自体や全batteryをこの実行環境で回したという意味ではない。

## 出版記録

- 単一オーナー宣言: `50d80188f3a4b187f20e5b9c99f99f025d3e360e`
- 補助検証器: `a1bd4414ce609a7ebd49fcacbb5ff6acd47fbb81`
- 合成回帰試験: `48ff274bd615af2c64d32a60274f99ac61d0fce6`
- `reproduce.sh` 接続: `b0af5133a90bf5b774596adb831dc355733c50a9`
- 本log: `afb110a9a4fe6f145b15fbeff08cb4ed89deecc7`
- K1172更新: `c05e1c2b2cce123b3521ff92583bd08c7bdbb8cb`、artifact注記更新 `a245c3f29a70fc3845d64984c92927033b6ba1e1`
- 実験README: `80c610768a0322d4723e9a789c78c0e37f79afb5`、同梱物一覧更新 `258929c706d4c93c942c79356a0ad727e687aa99`
- knowledge README索引: `30179483c5871dbe4bf3ad444e924f0b3b3823c9`

すべてmainへ直接反映し、branch/PRは作成していない。knowledge全体検査・unittest discover・生成処理・GitHub CIの完了は未確認であり、成功とは扱わない。

## 重要な制約

元の第三検証実行で使った `b1/run/parts` と `b2/run/parts` はGit管理されていない。公開済みなのは各batteryの最終auditである。このため、新しい補助検証器を**歴史的な2 batteryへ遡及適用した**とは主張しない。今後 `reproduce.sh` を実行した際に、実際のpartファイルへ完全性検査を適用するための補強である。

K1172の元の20 gate record・監査SHA・K1166の出版byteは変更していない。今回、新しいWIN/LOSS verdict・証明書・S6行閉鎖はない。標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はUNKNOWNのまま。全体Knowledge検査・全体CIも未実行であり成功とは扱わない。
