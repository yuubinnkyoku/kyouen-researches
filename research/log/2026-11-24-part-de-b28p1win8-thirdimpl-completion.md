# Part DE 完了: batch-28 (class 5343) b28-win46 queue registry P1パッケージ8行 第三実装交叉検証 — 全工程green・323 gates PASS

- 2026-11-24T03:45Z (authoring time; commit timestampはGitHub側)
- 宣言: `research/log/2026-11-24-part-de-b28p1win8-thirdimpl-declaration.md` (出版 `5de0f35f`・訂正 `707be9a5`)
- 実験dir: `research/experiments/n11-centralreply-closure-b28p1win8-thirdimpl-20261124/`
  (scaffold A1-A3 = `b96ce14b`/`04e2d5fe`/`451de93a` はrepo root誤配置→path repair R1 `a3b6361f` /
  R2 `fd1eb53f` / R3 `5465b6da` で正pathへbyte同一再出版・root側完全除去。記録
  `research/log/2026-11-24-part-de-b28p1win8-thirdimpl-pathrepair.md`)

## 結果 (D1-D8 全green)

- D1 rules gate: quads 95,670 一致・triples 195,044 mismatches 0 (rc=0)。
- D2 val-gate fresh 4本 (2M/2M/15M/15M): published baselineと wall_s 以外 node-exact 4/4
  (first-15m LOSS nodes 3,651,923 / second-15m LOSS nodes 5,040,200 / at2m 2行 budget-exhausted 再現)。
- D3 negatives: ng1 GATE_FAIL "legal count mismatch: derived=87 declared=88"・
  ng2 GATE_FAIL "stone count mismatch: bits=5 declared=6" (期待どおり fail-closed・rc=1)。
  実行注記: 初回はtag "ng1x"/"ng2x" で実行したが audit read_run が tag "a" を読むため
  ng1.a.out/ng2.a.out として再実行 (GATE_FAIL内容同一)。出版は宣言どおり negative 2 (tag "a" 側)。
- D4 anchors a/b det-pair: k02a result 1・exp 9,106,337・ttHits 4,991,527 / l1a result 2・
  exp 7,660,202・ttHits 3,951,175 (a=b同一・published pin一致)。
- D5 replica 8キー×2-pass fresh-cold (budget 15M): 16/16 pass rc=0・det-pair 8/8・
  published raw (PIN_RAW_DE 16) と node-exact 16/16 (result・nodes完全一致)。
- D6 third-impl 8キー×2 run: 16/16 rc=0・det-pair 8/8・verdict agree 8/8 (third result 1 ==
  published WIN)。expansions (a=b): aa046 2,503,964 / aa016 3,029,875 / aa025 3,527,308 /
  aa033 3,911,275 / aa027 5,653,876 / aa038 5,727,888 / aa012 5,888,866 / aa042 6,797,666。
- D7 audit ×3 byte-identical (stdout + audit-summary.json `38b46204…`): **ALL 323 GATES PASS**・
  verdict agreements 8/8 (WIN=8 LOSS=0)・wall-inconclusive 0・pass-one third-impl expansions計
  37,040,718。
- D8 tamper battery 4/4捕捉 (各rc=1・期待gate発火: replica-aa046-det-pair /
  target-aa016-det-pair / anchor-k02a-a-expansions / replica-aa046-verdict-vs-published) +
  復帰green (ALL 323 GATES PASS・summary byte完全復元)。

## 出版 (全fetch-back sha256照合 117/117 byte一致 at `8680355b`)

- B1 `c67c52d0` output 44 (status.log / rules-gate.txt / audit-summary.json / audit-run1-3.txt
  (byte同一) / replica 16 / targets 16 / anchors 4 / negative 2)
- B2 `f29eca5a` val-gate host 4 (`val-gate/*.de-host.out`)
- C `8680355b` README.md (成果物要約・実行注記込み) + MANIFEST-sha256.txt (116ファイル)

## 主張の限定 (宣言と同一・変わらず)

- 本Partは交叉検証のみで**完結**。**verdict不消費**: 対象8行 (aa046/aa016/aa025/aa033/aa027/
  aa038/aa012/aa042) は honest WIN labels のまま。adoption は scrutiny owner C++第二実装 gate
  `9193f5b6…` 通過後・pinned merger `90711961…` 経由の別adoption Part 専権。
- 閉鎖・被覆・secured・root勝敗の主張はしない。nodes数・expansions数・ttHits数を勝敗や
  距離として読まない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・
  class 5343 (54キーすべて・対象8キー含む) は本Partの前後を通じてすべてUNKNOWNのまま。**

## 次のcandidates (本レーン外参考)

- queue registry P2/P3/P4パッケージ (open 25行) は未着手・未宣言 (それぞれ別宣言が必要)。
- Part CX claimed5 (aa005/aa030/aa031/aa047/aa053) は本Partでは一切触れていない
  (takeover規約時刻 2026-11-24T04:19:31Z 時点での取り扱いはCX側)。
- batch-29 (class 2251) はPart DC他の進行中レーン所属・非接触。
