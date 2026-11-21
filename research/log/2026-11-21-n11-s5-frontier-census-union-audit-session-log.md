# セッション log: n11 S5 frontier census・グローバルunion監査・reconciliation測定（2026-11-21 14時台）

単一オーナー宣言: `2026-11-21-n11-s5-frontier-census-union-audit-single-owner-note.md`（14:42Z・宣言時HEAD `a423c2f0`・測定スナップショットbase `0a76535f`）。

## 経緯

1. **リポジトリ確認（毎回の最初の工程）**: 最新main（宣言時 `a423c2f0`・14:38Z）・AGENTS.md・knowledge README・11×11関連の直近コミットを確認。並走レーンの境界を確認し、reply27 two-target S5 probe（13 probe出版済み・継続中）、focus-class exclusive single-live-parent probe（35鍵宣言済み・probe未出版）、four-row q4 m35/witness hunt（`a423c2f0`）、s12/s13 constructive上界などのファイルには非接触とした。
2. **レーン選定**: 探索を進める前に、まず現行の証明基盤の健全性を測定する価値が最も高いと判断。(a) 13 probe連鎖の形式的検証、(b) cache corpus全体のunion監査、(c) 現行chainと歴史published corpusの差分の系統測定、の3点はいずれも未着手で、二石root closureに向かう全レーンの前提になる。
3. **実装**: `census_closure.py`（16,444 bytes・sha256 `81619dcf…`）・`audit_global_union.py`（8,087 bytes・`417caa5b…`）・`reconciliation_findings.py`（13,994 bytes・`4c613743…`）。すべて標準ライブラリのみ。入力はSHA-256 pin（不一致・quarantine鍵のchain内出現・verdict不整合はrc!=0でfail-closed）。
4. **検証**: 3スクリプトとも fresh 2回実行で output byte 一致（決定性）。`py_compile` 全PASS。**負対照**: pin済みchain cacheの1行のverdictを反転→ censusが verdict 一貫性ゲートで rc=1 即時fail。原状復元後、pin sha `60e0dc34…` 一致を再確認。
5. **実行・成果**: 実験README（`research/experiments/n11-s5-frontier-census-20261121/README.md`）のとおり。要点:
   - chain 13段検証 PASS（probe-1 5,744行→probe-13 5,756行、各段+1行・行削除なし・全段strictly sorted・probe-12/13のshaピン一致）。
   - グローバルunion監査: 326ファイル・760,504行・5,866 unique keys、**内部矛盾0・グローバルWIN/LOSS衝突0**。quarantine 2鍵は歴史ファイルのみに存在し現行chainへの再流入なし。
   - **reconciliation重大発見**: 現行chain・quarantineのいずれにもなく過去published cacheにある行が108行（107 LOSS + 1 WIN）あり、全108行が現行active供給に属する。うち99行は `1297036692683752448:0` のOct 12完了corpus（106子全LOSS→クラスLOSS）そのもので、**K0414（status: computed・二石root {60,27}=LOSS）のsolver-trusted系譜が依存する決定クラス**。WIN行 `1188950301626859520:603979776` はK0374由来（K0379が独立raw再構成published）。Nov 21 reply27ブート（Oct 10ベース）はこのcorpusを基底から除外しており、K0414系譜と現行UNKNOWN guardが矛盾したまま共存。**採否・判定は証拠オーナーに付託**（本レーンは判定しない）。再計算する場合のproxy費用概算 594,074,563 nodes。
   - 重複防止測定: focusレーン宣言35鍵との重複7鍵・reply27 13 probe targetとの重複0。
   - proxy較正: published raw 42行中15M決着27行（全LOSS）の nodes/proxy 比 min 0.698 / mean 1.347 / max 2.490。2M段階15行は全てUNKNOWN。
6. **境界遵守**: いかなるs5verdict cache・knowledge item・他レーン実験dirにも書き込んでいない。K itemは作成していない（worker-partition測定レーンの先例に従い、判定主張を含まない測定は実験dir + logで出版）。

## push 記録（2026-11-21T14:45Z）

- 事前の最新main再取得: 宣言時 `a423c2f0` → push直前も `a423c2f0`（1コミットも動かず・競合なし）。
- commit `e4aae3b4`: 実験dir 7ファイル（README・scripts 3・outputs 3）。push後、commit固定raw URLでfetch-backし**全7ファイル sha256 byte一致を確認**。
- 順序の特記（誠実記録）: 先例では宣言ノートが先に出版されるが、本レーンは実験dirが先（`e4aae3b4`）となった。宣言の実体（レーン選定・受入条件・非接触境界の確定）は14:42Zより前の本セッション内で完了しており、宣言ノート出版は追いかけとなる。並走レーンとのファイル衝突は全経路新規パスのため生じない（`n11-search-methods/README.md` の1行追加を除き既存ファイル非変更）。
- 後続: 宣言ノート + 本session log を1コミットで、続けて `research/experiments/n11-search-methods/README.md` への参照行（節見出し+1行）を1コミットで main に直接push（branch/PRなし・新規パスのため競合不可能）。`n11-search-methods/README.md` は既存行を1行も変更しない。上記各commitのfetch-back byte検証実施後にshaを追記する。

## 追記（2026-11-21T14:45Z・fetch-back検証完了）

- コミット列: 実験dir `e4aae3b4` → 宣言ノート+本log `6f858074` → `n11-search-methods/README.md` 参照行 `47a23c25`。branch/PRなし・main直接。
- fetch-back検証: 各commit固定raw URLで取得しsha256照合。実験dir 7ファイル・宣言ノート・本log 全byte一致。`n11-search-methods/README.md` は追加後 sha256 `c0fc94c8…`、先頭2,453 bytes（既存全文）は追加前の `c02180fc…` と不変を確認。
- 課題の所有権: backward-only 108行（K0414系譜のOct 12完了corpus 99行を含む）の採否はreply27レーン・focusレーン・K0414/K0416系譜オーナーへ付託済み。本レーンに残務なし。

**標準11×11空盤・二石root {60,27}・第三手100/108は本レーンの後も UNKNOWN のまま。node数・proxy・closure距離はscheduling測定であり判定ではない。**

## 追記2（2026-11-21T14:48Z・第二実装による交叉検証）

- union監査のヘッドライン主張（矛盾ゼロ・backward-only 108行）の**独立検証**として、Node.js v22.20.0による第二実装 `union_audit_node_crosscheck.mjs`（sha256 `d036bed9…`）を作成・実行した。Python実装（`csv`モジュール）に対し、行分割・`JSON`の安全性（duplicate-key拒否・2^53超え整数の精度保護）・集計をすべて独立に再実装。published監査出力をsha pinして直接比較するゲート付き。
- 結果: **全13項目一致・rc=0**（326 files / 760,504 rows / 5,866 unique / 内部矛盾0 / global衝突0 / has_WIN 161 / LOSS-only 5,705 / chain 5,756=158+5,598 / backward-only 108行の鍵・verdict・出所完全一致 / quarantine所在完全一致 / suspect rows 0）。決定性2回byte一致。負対照（疑似conflict cache注入）rc=1 fail-closed・除去でbyte一致復元。
- **実装事故の誠実記録**: 初版は鍵をJS `Number`へ正規化し、64ビット鍵の丸め（`10448351135499552768`→`…553000`）でquarantine除外が2鍵分落ち、backward-onlyが110行と誤計上していた。生テキスト鍵+BigInt比較に修正し全一致。出版版のみが正本。JS移植の「2^53超え`Number`/`JSON.parse`丸め」は今後の移植律としてREADMEに記録した。
- 出版: 実験dir 3ファイル追加（mjs・output json・README追記）+ 本log追記を1コミットでpush。fetch-back byte検証後にsha追記。
