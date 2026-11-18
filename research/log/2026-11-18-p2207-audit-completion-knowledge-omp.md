# 2026-11-18: p=2207 全量DRAT監査の完了記録と K0693 昇格ドラフト（omp）

## 結論（先に書く）

- p=2207 の全1103 d について独立checker（drat-trim, binary sha256 `92f0aa95…`）によるDRAT監査が完了した。
  集約領収書 1,082件 + 先行の標本21件 = 全1,103 d、verdictは VERIFIED 1,082 / SAT 0 / UNKNOWN 0（progress.log 集計と一致）。
- これにより K0693 の昇格条件（全量監査の完了）が満たされた。本logは昇格コミットではなくドラフト作成までを成果物とする。
- K0693 の status は `needs-review` → `computed` とし、evidence と監査制限節を更新する差分案を §2 に示す。
- 全量監査そのものを表す新規K項目のドラフトを §3 に示す。仮番号 K0871（items/ 現在の最大番号 K0870 + 1。統合時に再採番する）。

（以下、節ごとに追記）

## §1 監査完了の記録

- **範囲**: p=2207（h=1103）、d=1..1103 の全1,103 d。CNFは各dについて
  `parabola_half_bound.clauses_for_pair(2207, edges, d)`（edges_2207.txt, sha256 `d1eb1385…`由来）で生成。
- **件数・verdict**: 集約領収書 `records` は 1,082件、全件 `verdict=VERIFIED`
  （SAT 0件・UNKNOWN 0件・その他 0件）。`progress.log` の verdict 行も
  `verdict=VERIFIED` 1,082行、SAT/UNKNOWN/REJECTED 等は 0行。両者一致。
- **被覆**: 集約1,082 d は d=2..1102 の範囲で一意（d=1, 1103 を含まない、標本との重複 0件）。
  先行標本21件（d={1,50,100,150,200,250,289,297,300,312,324,400,500,550,600,700,800,900,1000,1100,1103}、
  修正版増分チェッカー 34249932790a9e9d で全点 VERIFIED）と合わせて
  1,082 + 21 = 1,103 = 全 d。`drat_audit_full_2207_34249932790a9e9d.json` とは d 集合が互いに素。
- **checker**: drat-trim（marijnheule/drat-trim, commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`,
  source sha256 `d834b649…`）。binary sha256 `92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a`。
  verdict判定は「stdout に `s VERIFIED` を含み exit code 0」。solver（cadical）は証明生成のみに使用。
- **ドライバ**: `research/experiments/parabola-p2207-no-equality-witness-20261107/audit_full_2207.py`
  （W31構築。再起動耐性: dごとの原子的領収書＋証明gz sha256照合で再実行時はVERIFIED済みをskip。
  pilot d=2..6 は全件 VERIFIED）。パイロット含む稼働は progress.log 冒頭 2026-11-16T14:15 JST から
  最終行 2026-11-17T19:15 UTC（2026-11-18 04:15 JST）の `driver done` まで。
 本体の稼働記録は連続ではない（一時出力の再開を含む）。[INFERENCE] 完了日時 2026-11-18 04:15 JST は最終行の時刻換算。
- **領収書パス**:
  - 集約: `research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_trim_audit_full_2207_92f0aa9575ed519d.json`
  - per-d: `output/p2207-drat-full/d<d>/receipt.json`、CNF/proof の gz、progress.log
- 主張規律: 各VERIFIEDは「このCNFについてこのDRAT証明をdrat-trimが受理した」ことのみを意味し、
  UNKNOWN も SAT もない今回の範囲では、検査した証明すべてが UNSAT 証明として受理された。
  checker の一般健全性や他パラメータへの一般化は主張しない。

## §2 K0693 昇格ドラフト（差分案）

対象: `research/knowledge/items/K0693-p2207-no-parabola-equality-witness.md`

1. frontmatter `status: needs-review` → `status: computed`。
2. frontmatter `title`: 「（計算結果・監査待ち）」→「（計算結果・全d監査済み）」。
3. `evidence`（line 63）末尾の
   「全数監査未完了。旧チェッカーの受理記録は独立証拠への採用を保留。」を削除し、次で置換:
   「2026-11-17に独立checker drat-trim（binary sha256 92f0aa95…）による全1,103 dのDRAT監査が完了し、
   VERIFIED 1,082件（集約領収書 drat_trim_audit_full_2207_92f0aa9575ed519d.json）+
   標本21件（修正版増分チェッカー）= 全dでVERIFIED、SAT 0・UNKNOWN 0。
   監査そのものを表す項目は K0871（統合時に再採番）。」
4. artifacts に追加:
   - `.../audit_full_2207.py`（role: verifier, note: 再起動耐性のある全量監査ドライバ。W31構築、pilot d=2..6 全件VERIFIED）
   - `.../output/drat_trim_audit_full_2207_92f0aa9575ed519d.json`（role: data, note: drat-trimによる集約領収書1,082件、全件VERIFIED）
   - 本文追記一文（「現在の監査上の制限」節の末尾へ）:
     「追記（2026-11-18）: 独立checker drat-trimによる全量監査が完了した。
     標本21件を除く1,082 dがすべてVERIFIED（SAT 0・UNKNOWN 0）で、全1,103 dが監査済みとなった。
     旧チェッカーの標本21件も修正版増分チェッカーで再監査済みである。詳細は K0871（統合時に再採番）。」
   - 「限界（監査待ち）」節見出しを「限界」に変更し、「全数監査は未完了でstatusは needs-review」の一文を削除。
5. relations に追加: `- type: depends_on / target: K0871（統合時に再採番）/ note: 全1,103 d のDRAT監査（drat-trim）`。
6. なお本文中の `A(2207)` の正確な値が未確定である点、他素数への一般化を主張しない点はそのまま維持する
   （監査完了は「全d UNSAT 証明の受理」を確定させるもので、1104の達成可能性等は別問題）。

## §3 新規K項目ドラフト（全量DRAT監査そのもの）

仮番号 **K0871**（`research/knowledge/items/` の現在の最大番号 K0870 + 1）。
**統合時に再採番する。** relationのtarget番号も現時点の items/ 実物で確認したが、
過去にリモート再採番の経緯があるため統合時に再確認する。

```markdown
---
id: K0871
title: p=2207の全1,103 dのDRAT証明が独立checker drat-trimで監査済み（全件VERIFIED）
kind: proposition
status: computed
topics: [verification, search-methods]
aliases: []
relations:
- type: verifies
  target: K0693
  note: p=2207の全d UNSAT主張に対する独立DRAT監査。昇格条件を満たす
- type: depends_on
  target: K0707
  note: 旧増分DRATチェッカーの偽受理(SAT偽UNSAT)発見に起因する再監査・checker分離の方針
- type: depends_on
  target: K0724
  note: assumptionベースDRATとUNSATのgap方針（本監査はassumptionを使わない単一CNF証明を検査）
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_trim_audit_full_2207_92f0aa9575ed519d.json
  role: data
  note: 集約領収書。records 1,082件、全件 verdict=VERIFIED。d=2..1102（標本21件との和集合で全1,103 d）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/audit_full_2207.py
  role: verifier
  note: 再起動耐性のある全量監査ドライバ（W31構築、pilot d=2..6 全件VERIFIED）。領収書方式で再実行を冪等にする
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/p2207-drat-full/
  role: data
  note: dごとのinput.cnf.gz・proof.drat.gz・receipt.json・drat-trim.log・progress.log（verdict行1,082、VERIFIED以外0）
- path: research/log/2026-11-18-p2207-audit-completion-knowledge-omp.md
  role: source
  note: 本監査の完了記録とK0693昇格ドラフト
scope: p=2207（h=1103）・標準q=4構成のd=1..1103各CNFについてのDRAT証明の受理。checkerの一般健全性や他素数への一般化は主張しない。
evidence: drat-trim（binary sha256 92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a、
source commit 2e3b2dc0ecf938addbd779d42877b6ed69d9a985）で1,082 dを検査し全件VERIFIED（SAT 0・UNKNOWN 0）。
標本21件（d={1,50,100,150,200,250,289,297,300,312,324,400,500,550,600,700,800,900,1000,1100,1103}）は
修正版増分チェッカー（source sha256 34249932790a9e9d…）で全点VERIFIED（2026-11-09）。
和集合で全1,103 d、両checkerのd集合は重複0。progress.log最終行 2026-11-17T19:15:29+0000（JST 2026-11-18 04:15）driver done。
---

## 命題

p=2207（h=1103）の等号否定CNF（各dについて `clauses_for_pair(2207, edges, d)` で生成、
節数31,868、edges sha256 d1eb1385…）に対し、dごとのDRAT UNSAT証明が
独立checker drat-trimで1,082件すべて受理され（`s VERIFIED` かつ exit 0）、
先行の標本21件（修正版増分チェッカー）と合わせて全1,103 dが監査済みである。

## 意味と限界

- 各VERIFIEDは「そのCNFについて、そのDRAT証明がdrat-trimにUNSAT証明として受理された」ことのみを意味する。
  UNKNOWNはUNSATではない（今回はUNKNOWN 0件）。SAT・checker異常も0件。
- solver（cadical）は証明生成にのみ使われ、検査はdrat-trimが行う（checker/solver分離）。
- 有限事例の監査であり、checkerの一般健全性、他素数・他構成への一般化は主張しない。
- この結果は K0693 の幾何命題（`A(2207) <= 1104`）の昇格条件を満たすが、
  `A(2207)` の正確な値（1104かそれ未満か）は確定させない。
```

（完）

