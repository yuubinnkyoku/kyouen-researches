# 残余23行 8根被覆判定（K1147外部第二検証）のpristine再実行第三検証（2026-11-20）

単一オーナー宣言: [2026-11-20-n11-residual23-eight-root-cover-third-verification-single-owner-note.md](2026-11-20-n11-residual23-eight-root-cover-third-verification-single-owner-note.md)
（commit `887e594de7`・2026-11-20T15:21:00Z・先行出版）

対象: [K1147](../knowledge/items/K1147-n11-residual23-eight-root-cover-decision-external-second-verification.md)
（残余23行 8根被覆判定の外部第二検証・出版 commit `e8d6025745`）。

## 経緯

1. **最新mainの確認と着手判断（15:19-15:21Z）**: HEAD `a2cb937644` 時点で、fold26 receipt fold
   （宣言 `23bffdd4e4`）・第5ラウンドrefsolve（`ace38772d9`）・WIN8-D10証明書抽出 root `…40002001`
   （`63877ffd2e`）・zero-tripple直接第4幾何（15:11:59Z宣言 `b0db8dfec1`）はいずれも他レーン宣言済み
   ・未着地で着手禁止。同型第三検証（K1153=K1148検証・K1155=K1151検証）の残り候補
   K1147（wide stage）・K1149（18 probe再実行）のうち、K1147を first として単一オーナー宣言を先行出版。
2. **入力の再取得とpin照合**: GitHub raw（main）から7ファイルを取得しSHA-256機械照合。
   判定機 `da51063c…`（39,301 bytes）・判定正本 `c5aaf83e…`（16,324 bytes）・K1097 `2896deb0…`・
   K1102 `d0b5d845…`・下界監査 `1310ef74…`・外部検証機 `7bee45ec…`・出版監査 `17dbd6ab…` 全一致。
   事前の単発確認で判定機の再実行が本環境で約43秒・出版正本byte一致を確認済み。
3. **harness作成・2件の構造発見**:
   - (a) harness初版のK1102 pin定数にSHA-256転写ミス（`…f268…`）があり、**harness自身のfail-closed pinが
     初回実行（15:3xZ）で即捕捉**（`pin mismatch k1102-…`）。正本実byteからの機械抽出で修正し、
     7 pin全てを機械照合で確定してから再実行。
   - (b) 検証機V1初回実行（16:00Z頃）で出版監査と1箇所のSHA差（`c887ac11…`）。差分は71 checkのうち
     `pin-decision`/`pin-k1097`/`pin-k1102`/`pin-audit` 4件のdetailのみで、**入力スナップショットの
     ベース名が出版時に記録したものと異なる**ことが原因（K1147出版機は監査JSONに`os.path.basename()`を
     残す設計）。ベース名は原本stage（`published-decision.json`/`k1097-refsolve.json`/
     `k1102-second-verification.json`/`lower-bound-audit.json`）に統一して解決。隔離実行（V3）は
     「ディレクトリで隔離・ベース名は保存」設計に変更。
4. **第三検証の実行（harness正本）**: 4環境で実行し全出力byte-identical:
   - R1: 同一cwd 1回目（2m41s）・R2: 同一cwd 2回目（2m41s）
   - R3: 隔離tree（harness+入力の別dir複写）+隔離cwd+隔離HOME（2m42s）
   - R4: R3に加えて `PYTHONHASHSEED=random`（2m40s）
   - 監査正本 SHA-256 `2bb40f705f00b8bc24b24f9c133729a8f156f4f2285980d624568f610d64420d`（5,349 bytes）
   - 各実行内で: 判定機4回pristine再実行（A1/A2/B/B'各約43秒）全て出版正本 `c5aaf83e…` とbyte一致
     （UNSAT・18 gate・cover3 451・memo 211・Shape B 100）→外部検証機3回実行（V1/V2/V3）全て
     出版監査 `17dbd6ab…` とbyte一致（71/71 checks）→tamper gate 2件（判定正本 offset 7701/
     K1097 offset 77 の1 byte XOR）がともにfail-closed捕捉（returncode 2/1・出力未書込）。
5. **part1の出版（15:57:56Z）**: 実験dir
   `research/experiments/n11-residual23-eight-root-cover-decision-reexec-third-verification-20261120/`
   （README + scripts/harness + output/監査正本 + inputs/ 7 snapshot・計10ファイル・200,366 bytes）を
   commit `43512c4ba1f4a33d3a2a657ad030dc9327b86ae6` で単一コミット出版。
   同commitのraw CDNから全10ファイルを再取得してcmp照合 **10/10 byte-identical**。
6. **採番**: part2出版直前に3点確認（items tree一覧にK1158前方一致0件・item path 404・
   knowledge README grep `items/K1158-` 0件）で **K1158** を取得。K1153=自レーン（K1148検証）・
   K1155=自レーン（K1151検証）・K1156=zero-triple直接第4幾何（並走15:26Z出版）・
   K1157=K1156の第三検証（並走15:54Z出版）に続く次の空き番号。

## 実験事実（本検験固有の新規性）

- **散在stageの「出版byteのみからの独立再検証可能性」確定**: K1147の入力5正本は5個所の別実験dirに
  散在する（`n11-residual23-eight-root-cover-decision-20261120/`の判定機と判定正本・
  `n11-residual72-safe8-refuted50-refsolve-20261120/`のK1097正本・
  `n11-residual72-refuted50-refsolve-second-verification-20261120/`のK1102正本・
  `n11-residual23-cover-lower-bound-strengthening-20261120/`の下界監査・外部第二検証dirの検証機と監査）。
  出版byte（SHA-256 pin群）だけを起点に第三者がこの再構成を完結し、
  判定機43秒/回×4・検証機3回を新規に走らせて、出力が2段とも出版正本とbyte一致することを確認した。
- **ベース名依存の再現性注意（出版検証機の設計上の性質・新規記録）**: 外部検証機は入力の
  `os.path.basename()` を監査JSONのpin-* detailに記録する。第三者がstageを再構成するとき
  ベース名の違いだけでbyte再現が崩れる（差分は4 detailのみ・全checkの判定はPASSのまま）。
  実験dirのsnapshotベース名は原本stageと同一に統一して自完結させた。
- **fail-closedの作動3例（透明性）**: (i) harness自体のSHA転写ミスをharnessのpinが捕捉、
  (ii) 判定正本1 byte tamperを検証機pinが捕捉、(iii) K1097正本1 byte tamperを判定機pinが捕捉。
  いずれもreturncode非零・出力未書込。

## 成果の位置づけとtrust境界

- 本検証は「判定機・外部検証機の2段の出版機械の出力が、出版byteの再取得のみから新規に再生される」
  ことの独立確定である。触れる宇宙・safe8/unsafe8述語の第三実装再導入は行っていない
  （判定機が2独立述語で全数実施・本検証はその決定性を4環境で確認）。
- 8根被覆判定（UNSAT・最小被覆9根）は候補root計画の簿記であり行閉鎖ではない（rows_closed 0）。
- REFUTED-D10はLOSS証明ではなく、nodes数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手

- fold26・第5ラウンドrefsolve・WIN8証明書抽出（root `…40002001`）の着地を待って正本の第二検証が
  最優先（いずれも他レーン宣言済みで着手禁止）。
- 次の同型第三検証候補は **K1149（18 probe再実行第二検証・runner v17 git blob必要・判定機Smith
  passA/passB形式）**。本レーンのK1155・K1158の手法（自snapshot入れて実験dir自己完結）が適用可能。
- 器材は `/home/user/work/lab/`（再取得・harness・4実行のrun/log一式）にあり、環境リセットで消失可。
  全成果はrepo出版済み（宣言 `887e594de7`・part1 `43512c4b`）。
