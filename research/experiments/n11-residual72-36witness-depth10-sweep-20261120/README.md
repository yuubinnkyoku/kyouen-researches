# n11-residual72-36witness-depth10-sweep-20261120

K1075 の `witness_full` が選んだ 36 本の fresh-safe 7 石 root を、runner v17 で depth 10・両 AND 順序により判定する単一オーナー実験。単一オーナー宣言は `research/log/2026-11-20-n11-residual72-36witness-sweep-single-owner-note.md`。

## 入力の固定

- main 起点: `412d75b93d14752f528c4fa4c6b5d472a4ca5ac8`
- K1075 正本: `research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json`
  - SHA-256 `49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa`
- K1075 独立幾何検証結果: `candidate-supply-second-verification-20261120.json`
  - SHA-256 `5511222b5385a2e57845b944e3607d2ac406203e4da827fb4e62b8e362b5a46d`
  - 44/44 gate PASS。36 root の安全性・D4正準形・72行完全1回被覆を再検査済み。
- runner v17: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_runner_v17.ts`
  - Git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`
  - 本実験の `runner_v17.ts` は同一bytesの固定コピー。

`prepare_roots.py` は K1075 正本の SHA-256 を照合し、36 root・72 residual 行・D4削除軌道・child/bit・1回被覆を再導出して `roots.json` と `residual72.json` を生成する。

## 探索条件

- 36 root × 2 ordering = 72 probe
- depth 10、node cap 30,000,000（全probe均一）
- `andclose1` / `andclose0` の両方
- runner 内蔵 `pilot_d6` 制御: `loss=false`, `nodes=3402` を必須
- child は RAW integer hex。`child = root - lowest set bit`、`bit` はその位置。`canon_hex` で置換しない（K1046事故規約）。
- 4 worker に `roots[W::4]` で分割。各probe timeout 280秒。worker別JSONL追記・成功probe再開対応。

## 再現手順

```sh
python3 prepare_roots.py
python3 -m py_compile prepare_roots.py driver.py assemble.py
for w in 0 1 2 3; do
  systemd-run --unit="kyouen-n11-residual72-36witness-w${w}" \
    --property=Nice=5 --property=CPUWeight=50 --property=CPUQuota=100% \
    --property=MemoryMax=768M --working-directory="$PWD" \
    /usr/bin/python3 "$PWD/driver.py" "$w"
done
```

全 worker 完了後:

```sh
python3 assemble.py
```

`assemble.py` は72 probeの完全性、両順序、cap、pilot制御、順序間矛盾、重複記録一致、root構造、D4削除被覆、残余72行の重複なし完全被覆を fail-closed で検査する。

## 解釈境界

- `WIN7-D10` は証明書抽出候補であり、証明書の独立検証とreceipt foldが済むまでS6行は閉鎖計上しない。
- `REFUTED-D10` はrunner v17の深さ10で先手勝ちが見つからなかったことを意味し、LOSS証明ではない。
- この実験は候補rootとS6行の被覆簿記であり、行・二石root・空盤のゲーム理論的勝敗を示さない。
- 標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4 は UNKNOWN のまま。

実行開始時点では未完了。結果JSONは全gate通過後にのみ生成する。
