# resolve7（K1072）第二検証のpristine再実行第三検証 研究log

## 経緯

- 2026-11-21 の本長期レーン実行は、K1189（fold10=第17WIN7 receipt ext2第三検証）part3（knowledge README bullet・commit `566acc7c`）の直後から続行し、次の未着手枠を選定した。
- 最新mainの機械列挙（実験dir 20件の「second-verification」・「third-verification」対照・logパスコミット2ページ200件・searchコミット検索）で、residual72系第二検証群のうち
  **resolve7（K1072）第二検証（commit `e836dd12`・76 gate・4独立経路）の第三検証が未着手・宣言なし**と確認した。
  対照的に4-sweep（K1144）・replace9 sweep/whole-record・verdict-sweepsの第三検証は確定済みで、
  replace16・candidate-supply・refuted50・36root-three-plyは各レーン個別宣言の対象外とした
  （fold11/17/18/19/23/25/26 ext2は宣言済み他レーンで着手禁止）。
- 選定理由: resolve7は残余72行導出鎖（78−4−2=72・割当34×2+4×1の1回被覆・39-root計画からのdepth-10 witness供給ゼロ）
  を4独立経路で固定する中核簿記であり、その第二検証の第三検証は共有基盤の独立検証可能性を直接強化する。
  また検証機1回約0.07秒（予備実測）でn11検証ラティス最小級の軽量対象である。
- 単一オーナー宣言ノートを先行出版（commit `86c6d546…`・受入条件5項目・Wは12出版正本の2参照raw再取得のみ）。
  宣言時HEAD `12eefdeae…`・宣言commit自体をref_bとする2参照固定。probes-w*/roots.jsonはmain@`ba5f9f4aad`基準の
  snapshot pinだが、宣言時点mainで12点すべて機械pinとbyte一致することを取得実測で確認済み
  （append-resume corpusの現況安定・第二検証出版時観察の15→20重複成長はその後停止している）。
- 予備探針（battery前）: t1 (`sweep39.json` @2,345)・t2 (`resolve6.json` @23,456) の1 byte XOR 0x01がいずれも
  rc≠0・stderr `pin mismatch for <対象名>`・**監査未書込**でfail-closedすることを実測。
  fold10 ext2第三検証のt1（31 gate走行後に監査gate-failed書込）と対照的な「監査不書込」型fail-closedであり、
  宣言ノートの受入条件4にこの予測をbattery前の実測に基づいて先に書いた（今回addendum修正は不要・予測と実測一致）。

## 結果

- harness `verify_resolve7v_third_20261121.py`（14,754 bytes・stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・
  fail-closed・byte決定的監査JSON）を構築。開発中の軽微バグ（stage_recon重複消去時のsha256_bytes境界・未使用helper）は
  py_compile+探針で捕捉修正し、全gateが指定挙動をassertする形に固めた。
- **3 batteryすべてall-gates-pass（gate 90〔pin 6・recon 48・rerun 25・tampers 11〕）・監査JSON byte-identical**
  （SHA-256 `0797c44e1df1ce7bbc16873da335e888110b3db2a0822d152a5f28074fecfdee`・11,948 bytes・`cmp`完全一致）。
  B1 fresh base・B2 同一base全stage再実行〔pin再取得込み〕・B3 隔離fresh base+全体`env -i`隔離HOME/TMPDIR+
  `PYTHONHASHSEED=random`。battery 1巡約1.1秒（主にraw取得）。
- rerun: 出版検証機pristine 4回/battery×3（同一cwd 2・隔離copytree+`env`隔離HOME/TMPDIR 1・+`PYTHONHASHSEED=random` 1）で
  全回rc=0・出力が出版監査正本 `42861008…`（21,842 bytes）とbyte-identical・4出力相互同一（検証機1回約0.07秒）。
- tampers: t1 `sweep39.json` @2,345・t2 `resolve6.json` @23,456 がいずれもrc≠0・stderrが対象入力名を特定・監査未書込で
  fail-closed捕捉（W復帰後byte無改変）。**2つのstderrは互いに異なる入力を指し、2種の入力pin gateが互いに独立して
  発火する**ことを1 battery内で実証（harness gate `tamper-independent-gates`）。
  offsetは既知の全レーン探針位置（fold12〜16第三・fold20/21/22/24第三・各出版社試験・fold10 ext2第三）とすべて別位置。

## 実験事実・知見

1. **fail-closed設計の多様性の実測**: resolve7第二検証機は最初のpin不一致でSystemExitし監査を書かない
   （fold10第二検証機は全gate走行後に監査gate-failed書込）。第三検証harnessはstderrの対象入力名特定と監査不書込の
   両方をgateでassertし、設計の違いそのものを機械記録に残した。
2. **snapshot pinの静止確認**: probes-w{0..3}.jsonl/roots.json（main@`ba5f9f4aad`基準）が宣言時点mainで
   12入力すべて機械pinと一致・2参照byte一致。append-resume protocolの成熟した実験のrecordは静止しており、
   第三検証の2参照固定が成立する（成長中corpusではsnapshot refの明示が必須という運用知見と合わせて記録）。
3. **軽量対象の第三検証運用**（K1189リコメンドの追試）: 対象検証機0.07秒・battery 1.1秒で、
   「軽量対象ほど早期に第三検証を潰す」運用が再び機能した。第二検証出版（2026-11-19T21:33Z）から
   約1.5日で第三検証が確定（fold10 ext2と同程度の空白期間）。

## 解釈規約（不変）

- 本検証はresolve7第二検証の再現性・入力pin・fail-closed防衛・監査byteの第三検査であり、探索・根の新規判定・
  行の閉鎖・候補universe再構築・receiptの再発行は行わない。
- REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手

- 残るresidual72系の第三検証未着手候補（replace16分・candidate-supply分・refuted50分・36root-three-ply分）は
  最新mainの宣言状況を確認のうえ各レーン個別宣言で着手する。fold17〜19/23/25/26 ext2は他レーン完了待ち。
