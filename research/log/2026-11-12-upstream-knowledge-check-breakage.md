# 2026-11-12 origin/main 統合時の知識チェック異常（86 errors）の記録

## 状況

- ローカルが origin/main より 167 コミット遅れていたため `git merge origin/main` で統合した
  （コンフリクトは K0728 の note 文と generated/summary.md のみ。K0728 は origin 側を採用し、
  summary.md は再生成で解決）。
- 統合後 `tools/knowledge/check.py` が **749 items / 86 errors** を報告した。
  これらのエラーは origin/main 側の新規項目に由来する（本セッションの K0702/K0706/K0708/K0722 は
  エラー一覧に含まれない）。

## 主なエラー

1. **YAML の未引用コロン**（5 件）: `note: 2026-11-12監査: blocker総数は...` のように
   plain scalar 内に `: ` を含むため `mapping values are not allowed here` になる。
   対象: K0725, K0729, K0749, K0750, K0757。
2. **重複 ID**（K0730〜K0734）: 同じ ID の項目が複数存在。
3. **スキーマ違反**（K0751, K0752 など）: `depends`/`established`/`machine`/`verification` という
   未知フィールド、`kind: None`、`status: established` など、SCHEMA.md に合わない front matter。

## 対応方針（本セッションでは未修復）

- 重複 ID の解消は参照更新を伴うため、項目の所有者（並行レーン）が行うのが安全。
- 未引用コロンは機械的に修正可能（値を単一引用符で囲む）だが、対象項目が現在も編集中の
  可能性があるため、ここでは記録に留める。
- `build.py` も同じエラーで停止するため、生成物（README/generated）は origin の状態のまま。

## 再現

```sh
uv run --locked python tools/knowledge/check.py    # 749 items; 86 errors
uv run --locked python tools/knowledge/build.py    # stops on the same errors
```

## 次の一手

- 並行レーンでの ID 再採番と front matter 修正の後に再生成する。
- 本セッションの知見（4 素数の単一証明、A(2207)=1104、A(2647) の範囲）は影響を受けない。
