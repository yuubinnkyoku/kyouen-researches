# 知識コーパス完全性インベントリ（tools/knowledge/check.py が失敗する全数原因）

実行: 2026-11-20 高速レーン（K1154出版後の検査で発見し、全数調査として整理）。
走査基準: main commit `a2cb93764410b346c75613ecac84a580c2d7bd3f`（K1154 frontmatter修正コミット直後）。
参照した repo 側正本: `tools/knowledge/common.py`（load_items / validate / checked）、`tools/knowledge/build.py`、`.github/workflows/knowledge.yml`（pin 094ef79642 でも同一）。

## 要約

`uv run --locked python tools/knowledge/check.py` は items 全ファイルを PyYAML で parse するため、
**1つでも loading できない item があると items 全体の検証が落ちる**。現在、下記クラスA〜Cの
障害が複数レーンにまたがって蓄積しており、CI の knowledge 系ステップ
（check.py → unittest → build.py → `git diff --exit-code -- README.md research/knowledge/generated`）
は少なくとも クラスA最小番号（K0919）出版以降ずっと失敗状態にある。クラスD（generated 停滞）は、
A〜Cを全て直した後でも最終 diff ステップを赤のままにする。

## 方法と限界

- 走査対象: item ファイル名一覧は GitHub tree ページ先頭1000件（K0001..K1018 相当）と
  `research/knowledge/README.md` の item リンク（K1019..K1155 相当）の和から237件を取得
  （K0895..K1155 の危険窓。K0894以前は最終成功ビルド時代のコーパスで無害とみなす）。
- 検出器: PyYAML の plain-scalar 規則（block 文脈で値に `": "` を含めると ScannerError
  "mapping values are not allowed here"、`" #"` でコメント誤認）を静的に再実装した
  frontmatter スキャナ。single-quoted（単行・複数行引用符バランス追跡）、flow 配列、
  block scalar（`|` `>`）に対応。green 時代（872項目で build 生成に成功した era）の
  コーパス慣行（`: ` を含む値は必ず引用符付き、例: K0785 `note: "K0791: …"`、K0843）と
  の照合で挙動を裏付けた。
- 限界: README からリンクされない K1019+ の item は見落とし得る。最終確認は
  uv 環境で `uv run --locked python tools/knowledge/check.py` を実行しエラーメッセージを
  本リストと照合すること。

## クラスA: plain scalar 内の ASCII ": "（ScannerError で load_items が item 単位で失敗）

該当40ファイル（`research/knowledge/items/` 直下、走査した237件中）。行番号は frontmatter 内。

- K0919-remo-uniform-factorial-period.md — L16 relations note「定理J…との対比: 本定理は…」
- K0923-remo-deceptive-pile-mechanism.md — L22「EXO（exotic11反鏡像: det ⟺ r < M）…」
- K0937-remo-sievegen-composite.md — L4 title「SIEVE構造の全称完結: 不変量INV-TRACK…」
- K0959-remo-firsthit-extreme.md — L2 title「初回ヒットの極値構造: F恒等式…」
- K0966-sixzone-sharpv.md — L10/L16「TWO-ZONE（t≥2）…（κ≥1: t·2^{2a}p₁²≤M−2・κ=0: …）」
- K1063-n11-residual78-post-saturation-full-cache-join-resolve6.md — L2 title「…resolve6再照合: K0863…」
- K1069-n11-residual78-39livewitness-depth10-sweep.md — L2 title「…depth-10全面掃引: WIN 1 / …」
- K1070-n11-residual78-seventeenth-win7-certificate.md — L2 title「…第17 WIN7-D10証明書: root …」
- K1071-n11-seventeenth-win7-receipt-fold.md — L2 title「…receipt fold（fold10）: 5親target…」
- K1072-n11-residual72-postfold-witness-recheck.md — L2 title「…（resolve7）: 78行計画…」
- K1075-n11-residual72-full-cache-join-candidate-supply.md — L2 title「…候補供給再構築: stage-1が…」
- K1079-two-token-z17-y4-second-verification.md — L2 title「…独立第二検証: 二つの独立導出…」
- K1085-n11-residual72-unsafe-classification-add2stones.md — L2 title「…拡張census: corpus era…」
- K1086-n11-residual72-addtwo-greedy23-d10-sweep.md — L2 title「…depth-10 掃引: WIN8-D10…」
- K1089-n11-residual72-replace16-d10-sweep.md — L2 title「…depth-10 掃引: WIN8-D10…」
- K1090-n11-residual72-safe8-refuted29-refsolve.md — L2 title「…第2ラウンド再解決: REFUTED-D10…」
- K1091-n11-residual72-replace15-d10-sweep.md — L2 title「…depth-10掃引: WIN8-D10…」
- K1094-n11-residual72-safe8-refuted41-refsolve.md — L2 title「…第3ラウンド再解決: REFUTED-D10…」
- K1095-n11-residual72-replace12-d10-sweep.md — L2 title「…depth-10掃引: WIN8-D10…」
- K1097-n11-residual72-safe8-refuted50-refsolve.md — L2 title「… 第4ラウンド: REFUTED-D10…」
- K1106-n11-residual72-win8-cert-extract-root8005021.md — L21「win16 footprint（root 8005021: …）」
- K1108-n11-residual65-win8-cert-extract-root9840004.md — L21「（root 9840004: …）」
- K1109-n11-residual65-win8-cert-extract-root9090022.md — L21「（root 9090022: …）」
- K1113-n11-residual58-win8-cert-extract-root8890020.md — L21「（root 8890020: …）」
- K1114-n11-residual58-win8-cert-extract-root120000038.md — L21「（root 120000038: …）」
- K1117-n11-residual55-win8-cert-extract-root22081000.md — L21「（root 22081000: …）」
- K1119-n11-residual51-win8-cert-extract-root1009000.md — L21「（root 1009000: …）」
- K1120-n11-residual48-win8-cert-extract-root00901010.md — 同上パターン
- K1121-n11-residual48-win8-cert-extract-root08d10000.md — 同上パターン
- K1123-n11-residual48-win8-cert-extract-root208090020004.md — 同上パターン
- K1124-n11-residual45-win8-cert-extract-root80880200.md — 同上パターン
- K1125-n11-residual45-win8-cert-extract-root840500.md — 同上パターン
- K1145-remo-survivor-minimal-period-r33to48.md — L36「…標準出力（…STATUS: COMPLETE checks:5…）」
- K1146-n11-residual72-replace9-d10-sweep.md
- K1147-n11-residual23-eight-root-cover-decision-external-second-verification.md
- K1149-n11-replace9-sweep-reexec-second-verification.md — L4「…独立第二検証: 24/24 gate PASS…」
- K1149-six-row-q5-q6-deficient-witness-band-extension.md — L48「…3系統再検証全PASS…（陽性対照）: …」
- K1151-n11-residual72-replace9-whole-record-second-verification.md
- K1153-n11-residual23-zero-triple-provider-reexec-third-verification.md
- K1155-n11-residual72-replace9-whole-record-reexec-third-verification.md — L4（K1151と同一生成由来）

対策: 該当行の値を引用符で囲む（green 時代の慣行。K0785/K0843 参照）か、ASCII ": " を
全角 "：" に置換する。いずれも意味を変えない最小修正。

## クラスB: frontmatter 未閉鎖（load_items 正規表現不一致 → ValueError: missing front matter）

5ファイル。いずれも冒頭 `---` のみで閉じ `---` 行が存在しない（意図した本文が frontmatter 内に
取り込まれた状態の可能性があるため、単純に閉じるのではなく内容の確認を推奨）。

- K1046-n11-117pool-d10-completion-7th8th-win7-certificates.md
- K1057-n11-stranded86-43witness-sweep-ninth-twelfth-win7-certs.md
- K1059-n11-residual78-39witness-d10-sweep.md
- K1088-n11-residual72-safe8-refuted16-refsolve.md
- K1148-n11-residual23-zero-triple-provider-third-geometry.md

## クラスC: id 重複（validate: duplicate id。AGENTS「K番号」の後着再採番ルール未適用）

4組8ファイル。両方が `id: Kxxxx` を持つ（grep で実在確認）。

- K0936-remo-sieve7-uv-mod210.md ⇔ K0936-two-token-z6-y25-boundary.md
- K0974-p2207-full-drat-audit.md ⇔ K0974-two-token-z6-y-ge4-full-grundy.md
- K0975-p3251-full-drat-audit.md ⇔ K0975-two-token-z6-uniform-independent-verification.md
- K1149-n11-replace9-sweep-reexec-second-verification.md ⇔ K1149-six-row-q5-q6-deficient-witness-band-extension.md

対策: mainに先に存在する番号は変更せず、後着側の item を再採番し、該当 item を参照する
relation・Markdown 参照も更新（AGENTS「K番号」）。所有レーンが実施するのが望ましい。

## クラスD: generated views の停滞（build.py の git diff が赤）

`research/knowledge/generated/`（index.md 末尾 K0894・872項目）とroot `README.md` の自動生成
領域が K0894 時代から一度も再生成されていない。K0895以降出版の全 item（上記A〜C修正後を含む）
は build.py 実行で views に反映されるため、現状では最終 `git diff --exit-code` が確実に赤。
AGENTS は generated の手編集を禁止しており、uv 環境での
`uv run --locked python tools/knowledge/build.py` 実行・コミットが必要。

## 推奨される修復順序

1. 各所有レーンが自 item のクラスA・B・Cを修正（最小変更・番号は AGENTS ルール）。
2. uv 環境で `uv run --locked python tools/knowledge/check.py` が `0 errors` になることを確認。
3. `uv run --locked python -m unittest discover -s tools/knowledge/tests` → `uv run --locked python tools/knowledge/build.py` →
   `git diff --exit-code -- README.md research/knowledge/generated` が通ることを確認してコミット。

## 本インベントリの由来と本レーンの関与

K1154 出版後のCIパリティ確認で、本レーン自身の item（K1154）の artifact note に同じクラスA
障害があることを発見し、コミット `a2cb937644`（2026-11-20）で先に修正・fetch-back 検証済み。
その全数調査として本リストを作成した。他レーンの item の修正は本レーンでは実施していない
（単一コミットでの一括最小修正も可能だが、各レーンの所有物であるため本記録に留める）。
