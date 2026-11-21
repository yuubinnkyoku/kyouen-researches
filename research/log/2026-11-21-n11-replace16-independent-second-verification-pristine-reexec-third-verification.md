# replace16（K1089）独立第二検証のpristine再実行第三検証 研究log

## 経緯

- 2026-11-21 の本長期レーン実行は、K1190（resolve7=K1072第二検証の第三検証）part3（commit `4c3dd3af`）の直後から続行し、
  residual72系の次の未着手第三検証枠を選定した。
- 対象コミットのファイル構成を実機確認: commit `45a3f3b2`（2026-11-20T00:44:22Z・単一コミット）は実験dir 3ファイル
  （README `e304a654…` 1,691・検証機 `c43ab3ac…` 9,270・監査 `1486d35e…` 5,728）+ K1093 item + 研究logを一括出版しており、
  最新mainで3ファイルともpin byteと一致した。W 5入力（K1085/K1086/K1088/K1089の4 JSON+runner_v17.ts）も現mainで
  検証機内pin（JSON SHA-256・runner Git blob SHA-1 `c132cc64…`）とbyte一致した。
- 選定理由: replace16は残余72行の代替16根掃引の中核出版（K1089）であり、16 gate・検証機9,270 bytesの軽量対象。
  直近50コミット列挙と実験dir列挙でreplace16分の第三検証宣言・実験の不存在を確認したうえで着手
  （fold11/17/18/19/23/25/26 ext2・round-5 refsolve・WIN8抽出・n9-ge19・n10 witness・five-row q7・four-row q6残・
  remo survivor・residual23 zero-triple・3行q4・four-row q6 band は宣言済み・着手禁止の他レーン作業）。
- **宣言前の重大な予備発見**: 合成tree（t16/）で出版検証機+pin済みW入力をpristine実行すると
  rc=0・stdout `PASS 16/16 roots=16 rows=49 probes=32 nodes=6339079`・16/16 gate全PASS するが、
  **出版監査 `1486d35e…`（5,728 bytes）はbyte再現不能**（機械出力は3回再実行でbyte安定・master `1741ca01…`・5,730 bytes）。
  差分は正確に2箇所のみ: (a) gainsHistキー順（出版ソート順 vs 機械挿入順）・(b) interpretation_guard最終文の文末句点
  （ASCII `.` vs `。` U+3002）。JSON構造全体（checks・summary・inputs・runner）は意味完全一致。
  → 出版監査はファイナル前ビルドの出力と推定。**「検証結果の再現（16/16 PASS・全数値一致）」と「監査jsonのbyte再生」
  を区別し、受入条件3を修正版（機械master一致×4回×3巡 + 出版監査との差分が記録済み2点のみをassert）**として
  単一オーナー宣言を出版（commit `19c4eea1`・fetch-back byte一致・10,990 bytes）。
- tamper予備探針（battery前・fresh tree）: t1 K1086 @5,678・t2 K1089 @9,012 の1 byte XOR 0x20がいずれも
  rc==1・stderrに入力名+改変後SHA-256全文・**監査不書込**でfail-closedすることを実測し、受入条件4の予測を宣言時に記載。
  ただし探針treeがrerun監査を copy で持つ場合は「監査不書込」assertが壊れるため、受入条件4に
  「監査不在のfresh treeで事前不在+事後不在をassert」と明示した（fold10 gate-failed書込型・resolve7不書込型に続く3種目の設計実測）。
- **宣言ノートの例示値誤記の発見**: harnessのerratum assert（gainsHist値 `{"2":2,"3":11,"4":3}`）を実装中に、
  宣言ノートの例示値が `{"2":2,"3":1,"4":3}` に誤記されていることをharness実装中の出力実測で発見。宣言本文byteは不変のまま
  addendum（commit `f89d5ae6`・2,021 bytes・fetch-back byte一致）で訂正した（fold10 addendum先例と同じ運用）。

## 結果

- harness `verify_replace16v_third_20261121.py`（18,919 bytes・stdlibのみ・stage分割 pin/recon/rerun/erratum/tampers/finalize・
  fail-closed・byte決定的監査JSON出力・ROOTを検証機fileのparents[3]から解決する合成tree方式）を構築。
  開発中のバグ2件は初回battery失敗で捕捉し修正した: (1) erratumのguard文末チェックの文字列指定誤り
  （`UNKNOWN.` でなく「まま.」に一致させ末尾1文字で比較する方式へ）・(2) tamper探針treeがrerun後監査を持つ問題
  （copy後に監査を除去し事前不在をassert）。修正後は全gateが指定挙動をassertする形に固めた。
- **3 batteryすべてall-gates-pass（gate 75〔pin 9・recon 22・rerun 23・erratum 10・tampers 11〕）・監査JSON byte-identical**
  （SHA-256 `569c6bbda909d4f3993ffaee64395d9a62911e7cddb49added51abb87393e545`・10,189 bytes・`cmp`完全一致）。
  B1 fresh base（1.7秒）・B2 同一base全stage再実行〔pin再取得込み〕（1.1秒）・B3 隔離fresh base+全体`env -i`隔離HOME/TMPDIR+
  `PYTHONHASHSEED=random`+別cwd（1.3秒）。
- rerun: 出版検証機pristine 4回/battery×3（同一合成tree 2・隔離copytree+隔離env 1・+`PYTHONHASHSEED=random` 1）で
  全回rc=0・stdout `PASS 16/16 roots=16 rows=49 probes=32 nodes=6339079`・出力が機械master `1741ca01…`（5,730 bytes）と
  byte-identical・4出力相互同一（検証機1回約0.2秒）。**出版監査はbyte不一致のままerratumとして機械確定**
  （差分2点のみ・それ以外の全構造〔checks 16 gate・summary・inputs・runner〕がcanonical化比較で完全一致）。
- tampers: t1 K1086 @5,678（stderr `K1086 SHA-256 mismatch: 28e251b7…`）・t2 K1089 @9,012（stderr `K1089 SHA-256 mismatch: afb50484…`）
  がいずれもrc==1・監査不書込（事前不在+事後不在の両assert）・本番tree W無改変。
  **2つのstderrは互いに異なる入力名・異なる改変SHAを指し、K1086/K1089の2入力pin gateが互いに独立して発火する**ことを
  1 battery内で実証（gate `tamper-independent-errors`）。offset @{5,678,9,012} は既知の全レーン探針位置
  （fold12〜16第三・fold20/21/22/24第三・各出版社試験・fold10 ext2第三 @{12,345,1,234,567}・resolve7第三 @{2,345,23,456}）
  とすべて別位置。
- part1実験dir（README・scripts harness・output 監査正本・output reproduction.log・4ファイル）を単一コミット出版
  （commit `791e8868`・fetch-back 4/4 byte一致）。

## 実験事実・知見

1. **出版監査jsonのbyte再生性は対象ごとに予備実行で確認すべき**（運用知見）: resolve7（K1190）では出版監査と
   機械masterがbyte一致したが、replace16では不一致（差分2点）だった。rerun受入条件で「出版監査byte一致」を
   無条件に課すと、この種のerratumで第三検証が不正帰結着する。**「機械masterのbyte決定性」+
   「出版監査との差分が記録済みの有限集合と一致」という2本立て**が運用として正しい（本Kで確定）。
2. **erratumメタ観察**: 出版側gainsHistがキーソート済みで点在する差分が句点のみ、はファイナル前ビルドが
   別のJSON整形で監査を書いた痕跡と整合する。検証数値は全一致しているため検証の信頼性は不変であり、
   該当出版のREADME・itemに遡及修正は不要、第三検証記録（本K・宣言・addendum・part1監査）で機械確定する。
3. **宣言文書の誤記はharness実装段階で自然に捕捉される**: 受入条件の例示値は安易に手書きせず、
   実測値を宣言に写す。誤記が発生した場合も宣言byteを不変に保ちaddendumで訂正する運用が確立した（3例目）。
4. **fail-closed設計の3種目の実測**: fold10（gate-failed監査書込型）・resolve7（不書込型）・replace16（不書込型）。
   harnessは「監査不在のfresh treeで事前不在+事後不在をassert」することで、どちらの型でも探針証明が壊れない。

## 解釈規約（不変）

- 本検証はreplace16独立第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性（および監査jsonのerratum確定）の
  第三検査であり、探索・根の新規判定・行の閉鎖・候補universe再構築・receiptの再発行は行わない。
- REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を勝敗として読まない。WIN8-D10 candidateは証明書ではない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手

- 残るresidual72系の第三検証未着手候補（candidate-supply分・refuted50分・36root-three-ply分）は最新mainの宣言状況を
  確認のうえ各レーン個別宣言で着手する。fold17〜19/23/25/26 ext2は他レーン完了待ち。
- replace16第二検証の出版監査byte不整合は本Kでerratum確定済み。対象側（出版社レーン）での監査再出版は必須ではなく、
  必要がある場合は機械master `1741ca01…` との差分2点を明示して実施する。
