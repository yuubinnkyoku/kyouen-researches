# 2026-11-26 main ツリー大量削除事故と復旧の記録

## 事故

- 2026-11-26 01:00 頃、PG(2,8) 極大キャップ軌道の検証取り込みをコミットする際、
  一時インデックス方式で `git -c core.protectNTFS=false read-tree origin/main` と
  すべきところを **`protectNFTS` と誤記**した。read-tree が失敗して一時インデックスが
  実質空のまま `write-tree` → `commit-tree` → `push` され、
  **`d0755eccb` が 60,101 ファイルを削除**するコミットとして origin/main に載った。
- 直後に別レーンが被害報告 `dcc39babf`（main tip 大量削除の incident report）を追加。
- 復旧までの間、他のレーンも壊れたツリーの上に 1 コミット（K1325 の 2 ファイル）を追加した。

## 復旧

1. まず小さい push が通ることを確認（テストファイルのみの `5d3f64aa8`）。
2. 壊れたツリー（76 ファイル）から **2000 エントリずつ 31 回に分けて**、
   `e5cc9f8e6` のツリー内容を `update-index --index-info` で積み上げ、
   各チャンクを push（`ab78b6f` → `327b879` → `ca13291` → `567a84e4`）。
   1 コミットで 6 万ファイルのツリーを push すると HTTP 500 で失敗するため、
   差分の小さい段階的 push が必要だった。
3. `update-index --index-info` は **パスに `:` を含む 9 ファイルを無視**する
   （"Ignoring path ... krow=1:4..."）。そこで `read-tree e5cc9f8e6` で
   コロン入りパスを含む完全なツリーを一度 index に載せ、事故後の追加分
   （K1325・incident report・PG(2,8) 検証 artifact・K1324/ログの更新）を
   `index-info` で上書きして `722547b30` を push。
4. 最終状態: origin/main = `722547b30`、60,176 ファイル、
   `e5cc9f8e6` との差分は**削除 0**・追加/変更 17 件のみ（意図した変更だけ）。
   `PUSH_TEST_TMP.txt` は削除済み。

## 教訓

- 一時インデックスを使うときも、**設定キーの綴りを確認**し、
  `git write-tree` のファイル数と `git diff --cached --stat` を push 前に必ず検査する。
- `git add -A -- <paths>` は pathspec を誤ると危険。root から実行し、
  対象パスを絶対/明示的に渡す。
- 大量ファイルのツリー復旧はチャンク分割 push が有効。
- `:` を含むパスは `update-index` が無視するため、`read-tree` 併用が必要。
