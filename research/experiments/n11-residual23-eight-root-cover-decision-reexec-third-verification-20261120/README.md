# 残余23行 8根被覆判定（K1147外部第二検証）のpristine再実行第三検証: 4実行byte-identical・出版監査のGitHub byteのみからの完全再生（2026-11-20）

単一オーナー宣言: [../../log/2026-11-20-n11-residual23-eight-root-cover-third-verification-single-owner-note.md](../../log/2026-11-20-n11-residual23-eight-root-cover-third-verification-single-owner-note.md)
（commit `887e594de7`・先行出版・宣言 2026-11-20T15:21:00Z）

対象: [K1147](../../knowledge/items/K1147-n11-residual23-eight-root-cover-decision-external-second-verification.md)
残余23行8根被覆判定の外部第二検証（commit `e8d6025745` 出版・実験dir `n11-residual23-eight-root-cover-decision-external-second-verification-20261120/`）。

本検証はK1153（K1148第三検証）・K1155（K1151第三検証）と同型の「出版byteのみからの第三検証」で、
K1147の入力5正本が**5個所の異なる実験dirに散在するwide stage**である点がK1153/K1155と異なる。
第三者がGitHubから正本byteを再取得するだけで、判定機の4回再実行出力も71チェック監査も
新規に再生できること（輸送・ローカル記憶に依存しない独立検証可能性）を確定した。

## 実施内容と結果

1. **入力7ファイルのpin照合（fail-closed・全一致）**: GitHub rawから再取得した
   - 判定機 `eight-root-cover-decision-machine.py`（SHA-256 `da51063c…`・39,301 bytes）
   - 判定正本 `published-decision.json`（`c5aaf83e…`・16,324 bytes）
   - K1097再解決正本 `k1097-refsolve.json`（`2896deb0…`・43,540 bytes）
   - K1102第二検証正本 `k1102-second-verification.json`（`d0b5d845…`・38,056 bytes）
   - 下界強化監査正本 `lower-bound-audit.json`（`1310ef74…`・2,931 bytes）
   - 外部検証機 `verify_external_cover8_decision_20261120.py`（`7bee45ec…`・17,544 bytes）
   - 出版監査 `external-verification-audit.json`（`17dbd6ab…`・11,150 bytes）

   の7 SHA-256が出版pin（判定機・外部検証機の埋込み定数・K1147 README）とすべて一致した
   （正本実byte由来の機械照合・輸送打ち切りなし）。
2. **判定機のpristine再実行4回・全てbyte-identical**: 1byteも改変せず
   - passA1/passA2: 同一cwd 2回（各約43秒）
   - passB: 隔離tree・隔離cwd・隔離HOME・入力複写（別path）
   - passB': passBに加えて `PYTHONHASHSEED=random`

   出力は**4回すべて出版正本とbyte-identical（SHA-256 `c5aaf83e…`）**。判定 UNSAT・18 gate全ok・
   cover3呼び出し451・メモ211・Shape B試行100も全実行でK1147出版記録と同一。
3. **外部検証機の再実行3回・全てbyte-identical**: 上記4再実行出力を入力として外部検証機を
   - V1/V2: 同一cwd
   - V3: 隔離tree/cwd/HOME（複写は出版stageと同一ベース名を保持）

   の3回実行し、**出力は3回すべて出版監査（SHA-256 `17dbd6ab…`）とbyte-identical・71/71 check PASS**。
   交差恒等式 triple availability 891==3×297・provider hist {1:40,065, 2:4,857, 3:297}・
   greedy 9根 gains {3:6,2:2,1:1}・exactly-once 23行分割などK1147の全記録事実が新規出力にも現れた。
4. **tamper gate 2件・fail-closed捕捉**:
   - 判定正本の1 byte XOR反転（offset 7701）→ 外部検証機のpin-decision gateが捕捉
     （returncode 2・監査未書込・終了）。改変後SHA-256 `（監査JSON記録値）`。
   - K1097正本の1 byte XOR反転（offset 77）→ 判定機自体のfail-closed pinが捕捉
     （returncode 1・出力未書込・`Fail: K1097 sha256 pin FAIL`）。
5. **第三検証harness自身の決定性**: 同一cwd 2回 + 隔離tree/cwd/HOME 1回 +
   隔離+`PYTHONHASHSEED=random` 1回の計4回実行で、harnessの監査正本（本実験の正本）が
   **全4回byte-identical**（SHA-256 `2bb40f70…`・5,349 bytes）。乱数・時刻・絶対path出力なし・
   stdlibのみ。各回の所要時間は約2分41秒（判定機4回+検証機3回+tamper 2件を含む）。

## 本Third検証で新たに確定した2点の実験事実（透明性記録）

- **(a) ベース名依存の再現性注意（出版外部検証機の設計上の性質）**: 出版外部検証機は
  監査JSONのpin-*チェックdetailに入力レコードの`os.path.basename()`を記録する。
  したがって出版監査のbyte再現には4正本の**ベース名がK1147原本stageと同一**
  （`published-decision.json` / `k1097-refsolve.json` / `k1102-second-verification.json` /
  `lower-bound-audit.json`）であることが必要。SHA-256 pin自体は内容照合でベース名非依存。
  第三検証初回にこの差異（ベース名違いで唯一resultsのpin-* detailのみが変化・全71 check内容PASS）
  を検出・分析し、本実験dirのsnapshot命名から宣言ノートまで統一した。V3隔離実行の複写も
  「ディレクトリで隔離・ベース名は保存」設計。
- **(b) harness作成過程のSHA-256転写ミスの捕捉**: 初版harnessのK1102 pin定数に約1年ぶり率直に
  言えば典型的な転写ミス（`…f268…`）があり、**harness自体のfail-closed pinが初回実行で即座に捕捉**
  （K1149の出版時と同種・K1155 leapsと同じ防止策が効いた）。修正は正本実byteからの機械抽出で行い、
  7 pin全てを機械照合で確定してから4回実行した。

## 器材・収穫物

- harness `scripts/verify_k1147_reexec_third_20261120.py`
  （SHA-256 `a9dcc35616ad5d649646bcb41c3853ac420c63923028e566fa31b2a8e9598f13`・stdlibのみ・決定性）
- 監査正本 `output/third-verification-audit-20261120.json`
  （SHA-256 `2bb40f705f00b8bc24b24f9c133729a8f156f4f2285980d624568f610d64420d`・5,349 bytes）
- 入力snapshot `inputs/` 7ファイル（上記pin一式・本dir自体が自己完結し再実行可能）

## trust境界

- 本検証は「判定機・外部検証機という2段の出版機械の出力が、出版byteの再取得のみから新規に
  再生される」ことの確定である。触れる宇宙・safe8述語の第三実装再導入は本検証の範囲外
  （判定機が最終実行主体として2独立述語で全数実施済み）。
- 被覆数は候補root計画の簿記であり証明書ではない。証明書抽出・receipt foldは含まない。
- REFUTED-D10はLOSS証明ではなく、nodes数・solved数を勝敗として読まない。
- 行は1行も閉じていない（rows_closed: 0）。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手への影響

なし。fold26（先行レーン `23bffdd4e4` 所有）・第5ラウンドrefsolve（`ace38772d9`）・
WIN8証明書抽出 root `00000000010000809002000040002001`（`63877ffd2e`）・zero-triple直接第4幾何
（K1156出版済み）はいずれも本検証の着手権に影響しない。残余宇宙は不変（fold26未着地なら残余20行）。
