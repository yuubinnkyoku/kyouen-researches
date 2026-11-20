# n11 残余72行 代替9根 depth-10掃引（K1146）whole-record独立第二検証（2026-11-20）

K1146（残余23行代替9根depth-10掃引・出版正本 SHA-256
`e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e`）の
whole-record独立第二検証。単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-replace9-whole-record-second-verification-single-owner-note.md`
（commit `edc231213f`・先行出版）の下で実施した。**DFPNエンジンの再実行は行わない**
（18 probesの全再実行は別宣言の並走レーン commit `3f34046621` 管轄）。本機は出版済み
正本・probe記録のみをSHA-256 pinで読み、元の掃引機械とは**別実装**で照合する
（K1102・replace16独立第二検証・candidate-supply whole-record第二検証と同じ枠組み）。

## 入力の固定（10 pin・全てfail-closed照合済み）

| 入力 | SHA-256 |
| --- | --- |
| K1085 base state/residual72 | `5fdd342d…` |
| K1086 greedy23掃引正本 | `3045e152…` |
| K1089 replace16掃引正本 | `808fbda1…` |
| K1091 replace15掃引正本 | `edd7ac84…` |
| K1095 replace12掃引正本 | `335eca5e…` |
| K1097 refsolve正本 | `2896deb0…` |
| K1146 replace9掃引正本 | `e8f5d674…` |
| K1146 18 probe記録JSONL | `bdacf0e7…` |
| 8根被覆判定正本（K1147検証対象） | `c5aaf83e…` |
| K1147外部検証監査正本 | `17dbd6ab…` |

## 何を検査したか（334 gate・全PASS・監査正本に機械全数記録）

1. **probe記録経路**: 18 probe記録と掃引正本 per_root の全数値一致
   （nodes / loss / capped / terminalStoneRange・msとwall_s を除く）・
   pilot_d6制御（nodes 3,402・loss=false・capped=false）・生child hex規約
   （child == root − 最低セットビット・bit一致）・両AND順序の順序整合・
   verdict 分類の再導入（WIN ⇔ 両順序 loss=true uncapped）・nodes総計
   3,574,172・terminal union [14,18]。
2. **残余行宇宙の連鎖独立再導入**: K1085 base 72行 →（K1086 WIN7根主張23行を控除）→
   49行 →（K1089 WIN3根主張9行）→ 40行 →（K1091 WIN3根主張10行）→ 30行 →
   （K1095 WIN3根主張7行）→ 23行 →（K1146 WIN1根主張3行）→ 20行。
   各ラウンドで WIN主張+REFUTED主張が**当時の残余宇宙の disjoint exactly-once 分割**
   であることを主張行使順に行ごとに機械検証（union一致・未被覆0・余剰0）。
   23行はK1097 per_row帳簿と集合一致。
3. **被覆幾何の再導入（新規実装）**: 9根すべて popcount 8・D4 min-canonical・
   quadruple-free（C(8,4)=70四点組の4×4整数行列式・Bareiss）・主張行は6石で
   rootのD4像の部分集合・9根27主張が残余23行のちょうど1回被覆・
   gains hist {3:6, 2:2, 1:1}。K1097 scope1 greedy選定と掃引9根の根本一致。
4. **5掃引横断verdict census（本検証の新規成果物）**: 掃引済み75根
   （23+16+15+12+9）の D4正準形一意性・75根全て quadruple-free 再検証・
   累積WIN候補17根（主張52行）と累積REFUTED 58根の正準形空間での
   **WIN/REFUTED衝突スキャン（衝突 0）**・pool算術
   safe8 120,474 − 50 = 120,424〔P‴〕、− 58 = **120,416〔P⁗〕**・
   K1097除外50根リストの恒等性・判定正本の宇宙簿計
   （生成事象150,765==23×C(115,2)・137,959==45,263+92,696・
   45,219==45,263−44・50==44+6・50,670==40,065·1+4,857·2+297·3）の独立再計算。
5. **WIN16 intrinsic footprint の独立再導入**: K1097 win16_intrinsic_footprints
   16根の intrinsic（base72宇宙上のsubsubset幾何）を再計算し、15根が
   intrinsic==主張、K1095第3根 `00000000000000003800000008003180` …ではなく
   `0000000800000000380000000810000a` が主張1行+余剰1行
   （K1086 WIN根 `00000000000000003800000008003180` の主張行）であることを再現。
6. **新WIN候補（K1146 root `00000000010000809002000040002001`）の intrinsic footprint
   の初計測**: base72宇宙上で intrinsic == 主張3行（余剰なし・residual23内の
   余剰被覆0行）。第5ラウンドrefsolve計画（並走レーン宣言済み commit `ace38772d9`）は
   この根の receipt fold が需要構造を主張3行分だけ変える前提で組める。

## 結果

**334/334 gate PASS**（fail-closed: gate失敗時exit 1・出力なし）。監査正本
`output/replace9-whole-record-second-verification-20261120.json`
（115,002 bytes・SHA-256
`5888afb3e1c07f8555fbafc73fc0b9d1006b0a31c88bbdd55a0d8975c0cabcb4`・
residual universe 72/49/40/30/23/20行hex全リスト・75根census表・17+58 verdict表・
interpretation_guard 5文言同梱）。同一cwd 2回+隔離cwd/隔離HOME・
`PYTHONHASHSEED=random` 1回の計3実行で**byte-identical**。実行は各0.2秒以下。
入力を1 byteでも改変するとpin gateが即座にfailすることを確認済み
（改ざんテスト: 正本ではnodesを+1した場合に `pin-replace9` gateで捕捉）。

## trust境界・解釈規約

- 本検証は出版記録の二次照合である。DFPN探索器そのもの・探索過程・verdictの健全性は
  本機の対象外（探査再実行は bulk re-execution レーン `3f34046621`）。
- WIN8-D10 candidateは証明書ではない（抽出・独立二重検証・8石receipt foldは別工程・
  抽出は宣言済み commit `63877ffd2e`）。REFUTED-D10はLOSS証明ではない。
  node数・solved数を勝敗として読まない。greedy選定は条件付き計画簿記である。
- 本検証は行を1行も閉じない。**標準11×11空盤・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4 はすべてUNKNOWNのまま。**

## 再現

```sh
python3 scripts/verify_replace9_whole_record_20261120.py
sha256sum output/replace9-whole-record-second-verification-20261120.json
# 5888afb3e1c07f8555fbafc73fc0b9d1006b0a31c88bbdd55a0d8975c0cabcb4
```

検証機 SHA-256: `e92fb7556a6f12c6e3cee06477e5387ddb6214cb58875e4ee3385010f9043e8a`
（stdlibのみ・乱数・時刻・環境依存の出力なし）。
