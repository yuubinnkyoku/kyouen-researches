# n11 残余72行 4掃引（greedy23・replace16・replace15・replace12）depth-10 probe全件再実行による独立第二検証（2026-11-20）

K1086（addtwo greedy23・46 probe）・K1089（replace16・32 probe）・K1091（replace15・30 probe）・
K1095（replace12・24 probe）の計132 probeの出版depth-10記録を、pinned runner v17の
**再実行**によって独立検証する。単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-verdict-sweeps-reexec-second-verification-single-owner-note.md`
（commit `259e4019db88395a1b8ca48fda9d0b842665653a`）を先行出版済み。branch/PRは作らず
mainに直接出版。

既存の第二検証（K1093 replace16・K1102 refuted50-refsolve・whole-record検証など）はいずれも
「DFPNエンジンの再実行は対象外」と明示している。本検証はその空白を埋める: 出版記録の
幾何・台帳照合ではなく、全132 probeを同一runner・同一protocol定数で再実行し、
決定論的フィールド（nodes・loss・capped・terminalStoneRange）を出版値と全件比較する。

## 入力の固定

| 対象 | record JSON SHA-256 | probe-records JSONL SHA-256 |
| --- | --- | --- |
| K1086 greedy23 | `3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced` | `773fef4262a9c69766402d3c0f846f5569ce095107efedaa02a76690ab35b8f3` |
| K1089 replace16 | `808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc` | `75fda6ade767e731ba4e42049230bcea6498eee6e9b2348a9d909a1832f329f6` |
| K1091 replace15 | `edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25` | `47165331b68f10684db9217a18fd3a2aab6748ecf1191f0216905981737a773a` |
| K1095 replace12 | `335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707` | `89e2c30d93fc26b5f760c3f9f00c6190595e6adc2fd6320fd2ac69a2603f9c56` |

- runner v17 Git blob SHA-1: `c132cc6425eee3feaeef1d697dd74f968cfedb59`
  （`runner_v17.ts` として本実験dirにpinned copyを同梱し、起動前にblob照合）
- protocol定数: depth 10・cap 30,000,000・timeout 280秒・両AND順序（andclose0/andclose1）・
  全probeにpilot_d6 control（nodes 3,402・loss=false・capped=false）を要求

## 何をしたか

1. **fail-closed固定読み出し**: 4正本のrecord JSONとprobe-records JSONLをSHA-256 pinで
   読み出し、runner v17をgit blob SHA-1で照合。事業とrunnerのprotocol定数の一致
   （depth/cap/timeout/ordering/pilot_d6）を132 record全件で検査。
2. **独立再導入**: 各recordのrootからchild指定ルール（child = root − 最小セットビットのhex）
   を再導出して台帳と照合。root popcount 8・child popcount 7を全件確認。
   raw child hexは識別簿記であり、engineには同一の石集合が渡る。
3. **出版内部整合**: probe-records JSONLの値と正本per_root表を全132 probeで照合。
   正本classificationのpin（WIN8-D10 candidate 7/3/3/3根・REFUTED-D10 16/13/12/9根・
   nodes総計 18,032,471/6,339,079/7,383,022/5,700,222・capped 0・error 0）を再導入照合。
4. **pass A（132 probe再実行）**: このtree内でrunner v17を再実行
   （`python scripts/verify_sweeps_reexec_20261120.py run 240 --pass A`、resume-safe、
   ~117秒、error 0・timeout 0・capped 0）。
5. **pass B（132 probe再実行・隔離環境）**: 実験dirと4掃引dirの複製を別cwd・別HOMEに置き、
   pinned入力も隔離側複製からSHA-256照合のうえ再実行（~119秒、error 0・timeout 0・capped 0）。
6. **assemble（6 gate、fail-closed）**: runner blob pin・出版内部整合・出版classification pin・
   passA-vs-出版全132 probe全field一致・passB-vs-出版同様・passA-vs-passB全field一致。
   審査JSONはtiming非依存でbyte-identical再現することを同一cwd 2回＋隔離cwd/HOME 1回の
   3実行で確認（SHA-256 `6297c646c32a0b1e0643f9f727fe712d1135dad15c0f5b0418ba8b3350596637`）。

## 結果

**6/6 gate PASS。**

- 132 probe × 2 pass = 264回の再実行で、nodes・loss・capped・terminalStoneRangeが
  出版記録と**全件完全一致**（不一致0・欠落0）。
- pass A・pass Bともnodes総計 37,454,794（= 4掃引の出版nodes総計と正確に一致）。
- 再導入した分類も出版と一致: WIN8-D10 candidate 7+3+3+3=16根、REFUTED-D10
  16+13+12+9=50根、ordering衝突0、capped/timeout/error 0。
- 全probeのpilot_d6 controlが両passで同一（nodes 3,402・loss=false・uncapped）。

## 検証境界（interpretation guard）

- 本検証は出版probe事実の再実行検査であり、これ以上のwin/loss主張は一切しない。
- `loss=true`（未打切り）はその8石rootのWIN8-within-depth-10 candidateを意味するのみ。
  行の閉鎖には別の証明書抽出・三重検証・receipt foldが必要。
- `loss=false`（未打切り）はREFUTED-D10 probe事実であり、**どの前段局面のLOSS証明でもない**。
  代替プールの浸食にしか寄与しない。
- capped/timeout probeは一方向の証拠にもならないコスト下界である（本検査では0件）。
- node数・solved数は勝敗の読みではない。
- 標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべて**UNKNOWN**。
- fold26・残余23行greedy9掃引など並走タスクの着手には本検証は影響しない。

## 再現

```bash
python3 scripts/verify_sweeps_reexec_20261120.py run 240 --pass A
# pass B: 実験dir+4掃引dirを別cwd・別HOMEに複製し
REEXEC_INPUT_ROOT=<隔離>/experiments HOME=<隔離>/home \
  python3 scripts/verify_sweeps_reexec_20261120.py run 240 --pass B --root <隔離output>
python3 scripts/verify_sweeps_reexec_20261120.py assemble --pass-b <隔離output>
```

- 出力（audit JSON）: `output/verdict-sweeps-reexec-second-verification-20261120.json`
- pass A生記録: `output/probe-records-reexec-passA.jsonl`（SHA-256 `1ade916b06f887c622449613f068f99bd2bf93404527a397ee2438c0f22f6f12`）
- pass B生記録: `output/probe-records-reexec-passB.jsonl`（SHA-256 `e351f6cc64eca23f1b68d1811a65779e20d1ab727f0ac48e9c4a7b3624845897`）
- wall_s等の計時値は決定論的比較対象から除外している（pass間で値は異なる）。
