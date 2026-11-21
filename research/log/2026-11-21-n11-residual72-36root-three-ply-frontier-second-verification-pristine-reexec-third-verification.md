# 36root-three-ply frontier（K1084）独立第二検証のpristine再実行第三検証 研究log

## 経緯

- 2026-11-21 の本長期レーン実行は、K1191（replace16=K1089第二検証の第三検証）part3（commit `3ba28e88`）の直後から続行し、
  residual72系の次の未着手第三検証枠として36root-three-ply frontier（K1084）第二検証を選定した。
- 対象コミットのファイル構成を実機確認: commit `67766eac`（2026-11-19T23:25:16Z・単一コミット）は実験dir 3ファイル
  （README `bbc9b255…` 2,782・検証機 `verify_frontier.py` `d8876e5b…` 14,671・監査正本 `a6272056…` 55,614）+ K1084 item+ 研究logを
  一括出版しており、宣言時現main HEAD `3ba28e88` で3ファイルともpin byteと一致した。W 2入力（K1075候補供給正本 54,282 bytes・
  先行census正本 53,914 bytes）も現mainで検証機内SHA-256 pin とbyte一致した。
- 選定理由: 36root-three-ply frontierはresidual72の36 fresh-safe 7石root三手先census（三点組132,291個・点判定16,007,211回・
  root安全性四点組1,260個）の独立第二検証出版（K1084）で、19 gate・検証機1回約16秒の中堅規模かつW 2点の2入力でreconが軽い対象。
  直近コミット列挙・実験dir列挙で36root-three-ply分の第三検証宣言・実験の不存在を確認したうえで着手
  （fold11/17/18/19/23/25/26 ext2・round-5 refsolve・WIN8抽出・n9-ge19・n10 witness・five-row q7・four-row q6残・
  remo survivor・residual23 zero-triple・3行q4・four-row q6 band は宣言済み・着手禁止の他レーン作業）。
- **宣言前のbyte再生性予備実測（K1191のerratum教訓を運用化した適用第1号）**: 合成tree（ROOT = 検証機fileのparents[4]）で
  出版検証機+pin済みWをpristine実行すると rc=0・19/19 gate全PASS・約15.9秒/回・出力監査が出版正本 `a6272056…`（55,614 bytes）と
  byte-identical。stdoutは `status=second-verified・check_count=19・all_pass=true`（elapsed_seconds/maxrss_kibはstdoutのみで
  監査jsonには含まれない・監査はbyte決定）。→ 本対象は出版監査byte再生が成立しており、rerun受入条件3は**当初からbyte一致条件**
  で確定できた（replace16 K1191ではbyte再現不能がerratumとして確定されたため受入条件を修正版にした経緯との対照）。
- tamper予備探針（battery前・fresh tree）: t1 K1075候補供給正本 @51,234・t2 先行census正本 @8,765 の1 byte XOR 0x20がいずれも
  rc==1・stderr末行 `RuntimeError: K1075 source SHA-256 mismatch` / `RuntimeError: published frontier SHA-256 mismatch`・監査未書込で
  fail-closedすることを実測し、宣言時に挙動予測を記載。検証機は読み取り直後の最初のSHA不一致で**raise RuntimeError（Python traceback）**
  となり監査JSONを一切書かない「監査不書込」型fail-closed（fold10 gate-failed監査書込型・resolve7/replace16 SystemExit不書込型に続く
  **4種目の設計**）。tracebackに実行file絶対pathが含まれるため、第三検証gateは**stderr末行のRuntimeErrorメッセージ特定**で行い、
  stderr全文byte一致は要求しない設計を宣言ノートに明示した。
- 宣言出版: commit `ffba7985`（10,047 bytes・受入条件5項目・fetch-back byte一致・ref_a = 宣言時HEAD `3ba28e88`・ref_b = 宣言commit）。

## 結果

- harness `verify_t36v_third_20261121.py`（15,153 bytes・stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・
  byte決定的監査JSON出力・合成tree方式・erratum stageなし〔本対象はbyte再生成立のため〕）を構築。
- **4 batteryすべて56/56 PASS・監査JSON byte-identical**（SHA-256 `407d649dde8e791447d160dab39ebc71f50ea2aed704e7b145153b494c7b6156`・
  7,729 bytes・`cmp`完全一致）。B1 fresh base全stage（1m4.9s）→B2 同一base全stage再実行〔pin/recon再取得込み〕（1m2.7s）→
  B1f fresh base独立capture（1m2.9s）→B3 隔離fresh base+全体`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`+別cwd（1m3.3s）。
  B1fはB2が同一baseで共有監査pathを上書きしたあとのfresh base独立captureとして追加し、fresh baseでも監査が同一byteになることを
  実測した（B1==B1f==B2==B3）。
- rerun: 出版検証機pristine 4回/battery×4 battery（同一合成tree 2・隔離copytree+隔離env 1・+`PYTHONHASHSEED=random` 1）で
  全回rc=0・stdout JSON `status=second-verified・check_count=19・all_pass=true`・出力が出版正本 `a6272056…`（55,614 bytes）と
  byte-identical・battery内4回間でbyte一致（検証機1回約16秒）。
- tampers: t1 候補供給正本 @51,234（stderr末行 `RuntimeError: K1075 source SHA-256 mismatch`）・t2 先行census正本 @8,765
  （末行 `RuntimeError: published frontier SHA-256 mismatch`）がいずれもrc==1・stdout空・監査未書込（事前不在+事後不在の両assert）・
  本番tree W無改変。**2つのstderr末行は互いに異なる入力を特定し、2入力pin gateが互いに独立して発火する**ことを1 battery内で実証
  （gate `tamper-independent-errors`・t1は読み取り1点目・t2は2点目のfailで読み取り順独立性を含む）。
  offset @{51,234,8,765} は既知の全レーン探針位置（fold12〜16第三・fold20/21/22/24第三・各出版社試験・fold10 ext2第三・
  resolve7第三・replace16第三 @{5,678,9,012}）とすべて別位置。
- part1実験dir（README・scripts harness・output 監査正本・output reproduction.log・4ファイル）を単一コミット出版
  （commit `1b19e7fc`・fetch-back 4/4 byte一致）。
- part2として本item（K1192）と本logを出版。K番号はpush直前の3点確認（search_commits `K1192 repo:yuubinnkyoku/kyouen-researches` 0ヒット・
  README最大K番号 K1191〔part3でbullet追記済み〕・HEAD `1b19e7fc`〔part1出版のまま並走なし〕）で採番した。

## 実験事実・知見

1. **「rerun受入のbyte再生性は宣言前に予備実測してから課す」運用の適用第1号（K1191知見）**: 本対象は予備実測で出版監査byte一致を
   確認できたため、宣言ノート受入条件3を修正版なしのbyte一致条件で当初から確定した。replace16（K1191）がbyte再現不能のerratum型
   だったのと対照的に、本対象はpristine再実行17回（予備1+本battery 16）すべて出版正本とbyte-identicalでerratumなし。
   対象ごとにbyte再生性が変わるため、**予備実測を宣言時に必ず行う運用が正しい**ことを2例対照（K1191 erratum型・K1192 通常型）で確定。
2. **fail-closed設計の4種目の実測**: fold10（gate-failed監査書込型）・resolve7（SystemExit不書込型）・replace16（SystemExit不書込型）に続き、
   本対象は**raise RuntimeError traceback型（監査不書込）**。tracebackは絶対pathを含み非byte決定的だが、末行メッセージは入力名で決定的であり、
   「末行特定でgateを機械記録し、stderr全文byte一致は要求しない」設計が有効であることを実測した。
3. **中堅規模の第三検査コスト**: 検証機1回約16秒・battery 1巡約63〜65秒・4 batteryで約4.5分。軽量対象（replace16・1巡約1.1〜1.7秒）と
   比べてもbattery設計（4回/battery、うち1回は隔離copytree+`PYTHONHASHSEED=random`）が変わらず機能する。
   第二検証出版（2026-11-19T23:25Z）から約1.6日で第三検証確定。
4. **part1 README再実行回数文言の数え誤り（機械確定・出版byteは不変）**: part1実験READMEの実験事実1「本battery 12回」・実験事実3「12回のrerun」は
   数え誤り。harness監査はcapture 4組（B1/B2/B1f/B3）がいずれもrerun 23 gate（r1〜r4×5 gate+相互3 gate）を含み、battery所要時間
   （1巡約63〜65秒 ≒ rerun 4回×約16秒+fetch/tampers）とも整合するため、**正しくは4回/battery×4 battery=16回**。
   B1/B2/B3の3巡でREADME本文を執筆し、あとからB1f（fresh base独立capture）を追加した際に実験事実の回数を更新しなかったことが
   発生源。検証の信頼性には影響せず（監査byte一致・全gate PASSは回数に依らない）、K1191と同じ扱い（対象出版の遡及修正は不要、
   第三検証記録で機械確定）とする。**教訓: 実験録の実測回数はharness監査のgate構成から機械的に写すこと**。

## 解釈規約（不変）

- 本検証は36root-three-ply frontier第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、探索・根の新規判定・
  行の閉鎖・候補universe再構築・receiptの再発行・36-root depth-10 sweep（別単一オーナーレーン所属）の起動・変更は一切行わない。
- 幾何censusの重複率はDFPN節点数・共有表命中率・証明状態再利用性を測るものではない。nodes数・solved数・coverage数を勝敗として読まない。
  REFUTED-D10はLOSS証明ではない。36 rootは候補rootであってWIN証明書ではない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手

- 残るresidual72系の第三検証未着手枠は **candidate-supply分（K1075正本側第二検証・verifier 35,127 bytes・audit 16,462 bytes）** と
  **refuted50分（verifier 48,898 bytes・audit 38,056 bytes）** の2つ。最新mainの宣言状況を確認のうえ各レーン個別宣言で着手する。
  （本Kのpart3としてknowledge README bullet追記〔K1192〕も単独コミットで出版する。）
