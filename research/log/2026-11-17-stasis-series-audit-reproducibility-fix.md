# 2026-11-17 STASIS系列監査再現性欠陥の修正実施（K0900 recipe (a)・plain .jsonl版）

K0900が特定・提示した修正recipe (a)を所管レーンが実施した。
対象はK0895/K0897/K0898実験dirの監査再現性欠陥（fresh checkoutで
再生成監査のformatラベル2箇所のみがcommitted監査と異なり、検証器
run()のbyte比較がlive checks前にFATAL終了する欠陥）。

## 実施内容

- **full形式記録のplain `.jsonl` commit**: 3実験dirの
  `output/js_cap10_rN.jsonl`（r=10/r=11/r=12）をcommit。
  中身はcommitted packed記録からの可逆展開（packed記録が
  [index, 生存者mask, 第1敗者mask, states]を保持しatomsはindexの
  正準列挙の純関数であるため情報を落とさず復元できる）。展開の
  正しさは、正準化sha256（json.dumps(rec, sort_keys=True)結合の
  sha256）が3実験ともcommitted監査の出版ピン
  （r=10: fc5ed900…・r=11: 4d824a87…・r=12: 0cfdd64c…）と完全一致
  することで機械確認済み。commitされたraw .jsonlのsha256は
  r=10: 18c66349…（2,047,234 B）・r=11: 3d5176e3…（2,055,269 B）・
  r=12: 3b26294c…（2,055,811 B）で、いずれもpush後にraw CDN取得で
  byte同一を確認。load_jsonlは.gz→plain .jsonl→packedの順で
  読むため、fresh checkoutからformat:"full"監査がbyte再現可能に
  なり、K0895/K0897/K0898のworkflow audit stepはgreenになる。
- **push transportのバイナリ破損の発見と対処**: 当初recipe (a)は
  `js_cap10_rN.jsonl.gz`（gzip・mtime=0で決定的再生成）のcommitを
  試みたが、GitHub Appのpush transportがcontentをUTF-8文字列として
  扱いバイナリを必ず化けることが実証された（r=10の.gz 175,061 Bが
  remoteで263,113 Bに化け）。破損.gzは即座に削除し、recipe (a)を
  「full形式記録をASCII-onlyのplain .jsonlとしてcommitする」形に
  調整した。ASCII-onlyテキストはpush transportでbyte安全である
  ことをr=10/11/12の3ファイル全てでpush後byte照合により確認済み。
  なお .jsonl は .gz 展開結果そのもの（gzipを介さない）のため、
  可逆展開の正証明・出版ピン照合は影響を受けない。
- **K0900監査JSONの再生成**: 修正後のrepo状態ではC5 committed-audit
  再現性スキャンが4実験ともbyte_identicalを観測する
  （r=10: 8b375257…・r=11: a437de75…・r=12: 249ec902…・r=9対照:
  f407faee…と出版ピン同一）ため、committed監査JSON
  （欠陥状態のformat_only_differenceを記録・sha256 b66bfb12…）を
  修正後状態で再生成したもの
  （sha256 3cc276536f65fecb92e6390eebc113191adbe73235eec72d622882fe7a677f5c）
  に差し替えた。検証器は両状態を受け付ける設計のためC1-C7の機械
  チェック内容は不変（全合格）で、scanエントリのstateラベルのみが
  format_only_differenceからbyte_identicalに変化する。差し替え後の
  監査は2回実行でbyte同一（run3で確認）。
- **K0900 itemの更新**: 「修正実施」セクションの追加・限界行の
  更新・.jsonl artifactsの追記。

## 検証

ck/check.py（K0900検証器）を修正前後の両状態で実行: run1は旧
committed監査（欠陥状態のformat_only_differenceを記録・sha256
b66bfb12…・old_committed_audit.jsonとして保持）に対して、修正後の
ローカル状態から再生成した監査（sha256 3cc27653…）が一致せず
検証器run()最終のbyte比較がFATAL（旧監査と新監査の差分が
scanエントリのstateラベルのみであることの固定）、run2は修正後
状態の監査を書き出し（sha256 3cc27653…）てC1-C7全合格
（all_ok=true・AUDIT PASSED・C5 detailはr9/r10/r11/r12とも
byte_identical・C6 detailも4実験ともbyte_identicalを記録）、
run3は再生成監査とcommitted監査のbyte同一を確認（rc3=0）。

## 限界・次の課題

- 修正は監査再現性のみに触れる。計算内容・監査の機械チェック結果
  （census・34キー・STASIS4アンカー）は全く不変。
- workflow run queueの滞留により、修正後のgreenは次のworkflow実行で
  後から確認される（本ログ作成時点では未確認・構造上正常）。
- push transportがバイナリcontentを破損させる制約は残る。以後の
  成果物commitはASCII-onlyテキスト形式（plain .jsonl等）で行うか、
  所定の検証手順でbyte照合を行うこと。
