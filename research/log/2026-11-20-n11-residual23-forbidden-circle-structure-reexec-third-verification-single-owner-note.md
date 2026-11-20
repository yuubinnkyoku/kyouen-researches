# 単一オーナー宣言: 残余23行 零triple-provider禁止円 D4軌道構造解析（2026-11-21追加出版）のpristine再実行第三検証

## 対象出版物

- 対象: commit `3ccde3e385137b1a51cd2821a078ede38a2b3dfb`（2026-11-20T16:41:05Z、nk11: explain residual23 zero-row forbidden circles as two D4 orbits）
- 実験dir: `research/experiments/n11-residual23-zero-triple-forbidden-circle-structure-20261121/`
  - README.md、scripts/derive_forbidden_circles.py、input/ 2件、output/forbidden-circle-structure.json
- 当該出版物は K1156 第四幾何（unsafe 10出現・3正準四点・2 D4円軌道への分類）の後解析を追加した独立実験であり、K1157 は本体第四幾何（ee150508 時点）までを対象とするため本追加解析は未検証のまま。

## pin（pinned commit 3ccde3e385137b1a51cd2821a078ede38a2b3dfb の出版byte）

| 正本 | SHA-256 |
|---|---|
| 検証器 derive_forbidden_circles.py | `45e5d7d61781e96e1e0afff8f457f06ff69a00a2b5e6777dc03d710e2a122951` |
| 監査正本 forbidden-circle-structure.json | `0e16f29b259eac1864ce826324f5a51dfe4d5bd5946a0ea5ef7998daaf39c638`（9,730 bytes） |
| K1156 fixture residual23-provider-input.json | `51e7a465e18646097073e4f8231f89cbff327d05f9bfeac102e57c754b4ff822` |
| K1156第四幾何監査 k1156-direct-fourth-audit.json | `c4e55dbe8d937dce93430f5804296dcd5cf42a9d42de14f8e90bbebe262eb61f` |

## 実施する第三検証

1. 出版byteのみをGitHub（pinned commit）から再取得し、pin 4/4を照合する。
2. 検証機をpristine再実行4回（runA/runB同一cwd、runC隔離tree/cwd/HOME入力複写、runD隔離+PYTHONHASHSEED=random）し、出力が出版監査正本 `0e16f29b…` とbyte-identicalであることを確認する。判定はbash curl+sha256sum+cmpを権威とする。
3. 1 byte tamper（入力2件のうちREADME検証済みoffset 100と異なるoffset）がreturncode 1・出力未書込でfail-closed捕捉されることを確認する。
4. 以上を単一の第三検証harness（stdlibのみ・fail-closed）にまとめ、harness監査正本の決定性（3実行byte一致）を確認した上で実験dir・item・log・knowledge README bulletを出版する。

## 解釈規約

- 本第三検証は有限構造解析の再現性確認であり、行は1行も閉じない（残余宇宙は本検証の着手時点のまま）。
- 候補被覆の簿記でありゲーム理論的証明書ではない。safe 4出現の除外はpin済みREFUTED-D10事実に依存し、幾何からは導かれない。
- nodes数・solved数を勝敗として読まない。REFUTED-D10はLOSS証明ではない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

宣言時刻: 2026-11-20T16:58:00Z
