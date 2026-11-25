# 残余23行 零triple-provider禁止円 D4軌道構造解析（2026-11-21追加出版）のpristine再実行第三検証（2026-11-20）

## 対象

commit `3ccde3e385137b1a51cd2821a078ede38a2b3dfb`（2026-11-20T16:41:05Z）で出版された
`research/experiments/n11-residual23-zero-triple-forbidden-circle-structure-20261121/`。
K1156第四幾何の後解析（unsafe 10出現を2つのD4円軌道へ分類）を追加した独立実験で、
本体第四幾何はK1157で第三検証済みだが、本追加解析（検証器・監査正本とも新規byte）は未検証だった。

単一オーナー宣言: `research/log/2026-11-20-n11-residual23-forbidden-circle-structure-reexec-third-verification-single-owner-note.md`
（commit `b7d2880cdf66b2a30ad3e5cc8ebe36481ea8eba3`、2026-11-20T16:58:00Z発表）。

## pin（対象出版物の出版byte・pinned commitから再取得）

| 正本 | SHA-256 | bytes |
|---|---|---:|
| 検証器 derive_forbidden_circles.py | `45e5d7d61781e96e1e0afff8f457f06ff69a00a2b5e6777dc03d710e2a122951` | 16,831 |
| 出版監査正本 forbidden-circle-structure.json | `0e16f29b259eac1864ce826324f5a51dfe4d5bd5946a0ea5ef7998daaf39c638` | 9,730 |
| K1156 fixture residual23-provider-input.json | `51e7a465e18646097073e4f8231f89cbff327d05f9bfeac102e57c754b4ff822` | 3,105 |
| K1156第四幾何監査 k1156-direct-fourth-audit.json | `c4e55dbe8d937dce93430f5804296dcd5cf42a9d42de14f8e90bbebe262eb61f` | 7,627 |

## 第三検証の内容と結果（第三検証harness `verify_reexec_third.py`・stdlibのみ・fail-closed）

1. **pin gate 4/4**: 出版byteをGitHub（pinned commit 3ccde3e385…）から再取得し、上表4 SHA-256が全一致。
2. **fresh-run gate 4/4**: 検証機をpristine再実行4回
   - runA/runB: 同一cwd・staging treeで2回
   - runC: 隔離tree（複写）・隔離cwd・隔離HOME・入力複写
   - runD: runCと同じ隔離に加えて `PYTHONHASHSEED=random`
   の全4回が、いずれも出版監査正本 `0e16f29b…`（9,730 bytes）と **byte-identical** の出力を生成（returncode 0）。
3. **tamper gate 2/2**: 出版社READMEが検証済みのoffset 100とは異なる位置の1 byte XOR 0x01
   - fixture offset 200（改変後 `f5c6a73d…`）
   - K1156監査 offset 150（改変後 `954843ee…`）
   がともにreturncode 1・出力未書込（`FAIL-CLOSED: … SHA-256 mismatch`）で捕捉。
4. **harness決定性**: 第三検証harnessの監査正本（本dir `output/third-verification-audit.json`・3,321 bytes・SHA-256 `f12abd19d0171977a65e403ef6a73257c0fac3d0e8be9ffedf0d9a8483904520`）は
   同一cwd 2回＋隔離tree/cwd/HOME+`PYTHONHASHSEED=random` 1回の3実行でbyte-identical
   （sorted keys・時刻・実行時間・パスを含まない）。

以上により、**出版byteだけをGitHubから再取得するだけで第三者が第三検証の全gate結果を新規に再生成できる**こと
（輸送・転写・ローカル記憶を介さない独立検証可能性）が確定した。検証は数秒で終わり、DFPN探索は含まない
（対象解析は14出現のD4埋込み再導出と有理数円当てはめのみ）。

## 再現コマンド

```sh
python3 scripts/verify_reexec_third.py --root .
```

`stage/` には出版byteの複写（検証器・入力2点・出版監査）が置かれている。harnessは
pin → fresh-run 4回 → tamper 2件 → 監査JSON生成を1コマンドで再実行する。
byte検証の権威はbash curl+sha256sum+cmp。

## 解釈の境界

- 本第三検証は有限構造解析の再現性確認であり、行は1行も閉じない。
- safe 4出現の除外はpin済みREFUTED-D10事実に依存し、幾何からは導かれない。REFUTED-D10はLOSS証明ではない。
- 候補被覆の簿記でありゲーム理論的証明書ではない。P'''最大3行被覆はK1147から継承し再証明しない。
- 新しいDFPN probe、WIN8証明書、receipt fold、S6行閉鎖、勝敗判定は一切含まない。
- nodes数・solved数を勝敗として読まない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWN。**
