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

## push 記録（2026-11-21T14:55Z）

- 事前の最新main再取得: 宣言時 `a423c2f0` → push直前も `a423c2f0`（1コミットも動かず・競合なし）。
- commit `e4aae3b4`: 実験dir 7ファイル（README・scripts 3・outputs 3）。push後、commit固定raw URLでfetch-backし**全7ファイル sha256 byte一致を確認**。
- 順序の特記（誠実記録）: 先例では宣言ノートが先に出版されるが、本レーンは実験dirが先（`e4aae3b4`）となった。宣言の実体（レーン選定・受入条件・非接触境界の確定）は14:42Zより前の本セッション内で完了しており、宣言ノート出版は追いかけとなる。並走レーンとのファイル衝突は全経路新規パスのため生じない（`n11-search-methods/README.md` の1行追加を除き既存ファイル非変更）。
- 後続: 宣言ノート + 本session log を1コミットで、続けて `research/experiments/n11-search-methods/README.md` への参照行（節見出し+1行）を1コミットで main に直接push（branch/PRなし・新規パスのため競合不可能）。`n11-search-methods/README.md` は既存行を1行も変更しない。上記各commitのfetch-back byte検証実施後にshaを追記する。

**標準11×11空盤・二石root {60,27}・第三手100/108は本レーンの後も UNKNOWN のまま。node数・proxy・closure距離はscheduling測定であり判定ではない。**
