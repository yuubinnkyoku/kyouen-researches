# 2026-11-19 n11 長期レーン: 117-rootプールdepth-10完全判定と第7・第8 WIN7-D10証明書・第7/第8レシートフォールド

## 経緯

- K番号は当初K1045を予定していたが、出版直前のmain再取得で並走two-tokenレーンがK1045（z=13 y=5資料群）を出版済みと確認できたためK1046に繰り下げた（part 1コミットメッセージ「K1045 part 1」は履歴としてそのまま残す）。

- 前回のこのレーン実行（2026-11-19 12:57Z時点）はGitHub push手段を持たない実行で、本成果（掃引35+6・証明書2枚・fold・再解決3種・K1039再現）を知識フォルダ
  `n11-117pool-d10-sweep-7th8th-win7-certs-20261119/`（58ファイル・MANIFEST.md付き）に保存して終了した。今回はその出版実行。
- 出版前の最新main取り直しで、並走n11レーンが **K1041**（第5・第6fold+K1039/K1040-join refold・残余87行・witness 18 root・commit 87e0bc37）を出版済み、さらに **bf65d8c2/15d54369**（18-root sweep用 pinned single-worker driver `probe_driver18.py`）を検出した。
- **K1041の未試験witness 18 rootと本成果の掃引29候補の突き合わせの結果、18 root全件が本掃引に含まれることを確認**（17 REFUTED-D10＋G WIN7-D10）。並走の18-root sweepは本成果で完全に下請け済み。この事実をitem/log/READMEに明記し、並走レーンが証明書抽出を二度行わなくて済むようにした。

## 出版した成果（K1046）

1. **117-root候補プールのdepth-10完全判定**: 109 REFUTED-D10 + 8 WIN + 0未検証（resolve4）。残余86行（5親target 26/112）はこのプール内では全行stranded（resolve3: witness 0・matching 0・lower bound 43）。
2. **第7 WIN7-D10証明書**（G=`00000000040080801202000000100000`, 51/51合法手, 552,457 nodes, 21,829行, SHA-256 `7049f7cb…`）と**第8 WIN7-D10証明書**（H=`00000000040000801202000000100001`, 58/58, 2,655,359 nodes, 39,163行, SHA-256 `7e0599f7…`）。BigInt 3×3余因子展開と4×4 Bareissの二重独立検証（union差分0/0・状態流量一致）。
3. **第7/第8レシートフォールド**: K1041状態（6,224/492,830・solved 1,624・25/112）→ 第7（6,223/492,762・1,625・26/112）→ 第8（6,222/492,688・1,626・26/112のまま）。第4〜第6foldのPython再実装はK1041の出版mjs記録と全数値一致（fold実装の二重独立確定）。
4. **canon_hex事故の記録**: probe driverが(child,bit)分解のchildにcanon_hexを被せた場合に別局面をprobeする。K1040出版node数との不一致で検出・修復し、5件をround1-quarantine/に隔離。**runnerは生整数hexのみを扱うこと**。round-1有効24件+再probe 5件の生per-root記録は環境消滅で喪失（判定は組立JSON+3 rootのK1040 byte照合+node総計で裏付け。透明性のためここに明記）。
5. **K1039の完全再現**: 28-root witness sweep 56 probe全件（3 WIN=C/D/E・25 REFUTED・0 CAPPED・C-root node数出版値一致）。

## 出版運用の知見（今回の環境固有）

- 今回の軽量bashは `sha256sum`/`sha1sum` が破損スタブ（"Cannot read properties of undefined (reading 'digest')"）で、`md5sum` のみ動作。着地検証は以下の組み合わせで実施: (a) sandbox内自作SHA-256（FIPS多ブロックベクトル2種でセルフテスト後、証明書2枚のSHA-256が保存記録値と一致することを確認）、(b) push後に get_commit の files[].sha（git blob SHA-1）と sandbox内自作SHA-1（"blob <len>\0"+UTF-8バイト列）の照合。この2つでCDNを経由せずbyte着地検証が完結する。
- file_system.read_fileはbyte正確（ページングchunkの直接連結）。jqはこの環境で日本語を含むJSONテキストの抽出を二重エンコードして書き出すことがあるため、README等の大ファイルは「tool結果resource textをJSON.parseして取り出す」経路でsandboxに読ませ、絶対にjq書き出しを経由しない。
- README追記は「最新mainに対するdiffが純追加であること」の確認をpush前に行う（既存レーンとの和集合規約）。

## 次の一手（次回実行・着手前に必ず最新mainを取り直す）

1. **残余86行の候補拡張**: 117-rootプールはdepth-10で枯渇した。86行各行に対し「 undone-add-one-stone からの新規7石root候補」のD4正準形を列挙・安全フィルタ・既知verdict除外して、新候補被覆 universe を測定する。ここでambitious候補（被覆行数の大きいroot）が見つかれば coordinator の次の証明書候補にする。
2. **並走18-root sweepの回収**: 並走レーンが掃引を実行・出版した場合、本項の (9) と node数で照合する（期待値: 17 REFUTED-D10 + G WIN・証明書は本項出版済み）。
3. depth-10でstrandedな 행の depth>10 探索は、候補拡張でも閉じない行が出てから検討（計算量の壁は現在の計測から非常に大きい）。
4. **11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4はすべてUNKNOWNのまま**。REFUTED-D10はLOSSではない。
