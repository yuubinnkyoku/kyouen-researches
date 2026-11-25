# 11×11：証明戦略比較（K0417基準・課題1〜5、2026-10-12）

分離worktree `D:\wk-krr`（`origin/main` 追従）で作業。ローカルmainの他エージェント未コミット変更には触れず。

## 実施

- 課題1：`verify_plans.py` 再実行で31,546計画を現行main上で再確認（失敗0）。`dual_certificate.py` でelement-only双対を厳密有理数化し証明書＋`--verify` を保存（総和2024529/308、整数下界6,574）。重み族内最適を単調性で確認。pool-disjoint packingは346で不採用。
- 課題2：`build_alt_roots.py` で非中央6 rootを同一index空間に構築（39.1秒）。`compare_alt_replies.py` で個別・joint-swapを測定し、中央が全指標で支配的と確定。拡大せず。
- 課題3：`win_side.py --firsts 49` で65応手軌道を全走査（約30分）。全閉鎖可能・証人約1.74k・AND幅7,503・dead 0。`win_witness_masks.py` で証人マスク化（約1分、tie-break差±1を記録）。
- 課題4：比較表と主軸判断（LOSS側維持＋WIN側パイロット実測の二段構え）をREADMEに記録。確率は置かず、S5数から時間予測もせず。
- 課題5：`pilot-candidates.json` にlegal分布・最安10件・両用16件を保存。cacheのnode記録65件のみでは外挿しない旨と開始条件（パイロット成功なしに大量探索なし）を明記。

## 失敗・注意

- `dual_certificate.py` 初版は `__main__` ガード漏れで無出力終了、deg全宇宙一致の表明も無料群のみの56要素で失敗。両方修正し、`--verify` で再検査できる形にした。
- `win_side.py` 初版の軌道代表キー（min値）は別軌道の衝突があり得たため、写像値のソートtupleに修正した。
- `compare_alt_replies.py` 初版に不用な `\n` 混じりのパス代入行があったため削除した（再代入で無害だったが清掃）。
- K0417実験dir内の `plan-verification.json` は再実行で更新された（secondsのみ変化）ため一緒に反映する。

## 引き継ぎ

- K0418（双対証明書・整数下界）、K0419（非中央否定結果）、K0420（WIN側計測・主軸判断・パイロット条件）を作成。
- 未実施：初手49以外のWIN側、3初手以外の非中央拡大、869群への分枝限定、証人・frontier S5の∀-閉包実測（＝次のパイロット本体）。
