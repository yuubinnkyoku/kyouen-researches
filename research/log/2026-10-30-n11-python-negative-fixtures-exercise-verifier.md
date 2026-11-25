# 2026-10-30: 11×11の独立Python証明検査で偽証人の拒否試験を実効化

最新main・AGENTS.md・research/knowledge/README.md・K0023・第20候補LOSS9証明と全37行の独立伝播監査を確認した。空盤勝敗はUNKNOWN。

## 発見した検証上の欠陥

`research/experiments/n11-s9-full-child-top20-loss9-20261030/verify_python.py` の旧 `--negative` 試験は、改変した証人が正しい値と異なることを `assert` するだけだった。**改変証明書を実際の検証器に渡していなかった**ため、仮に本体から該当する拒否条件が消えても試験は通り得た。これは証明の勝敗が誤りだったことを示すものではなく、改変拒否試験の有効性の問題である。

## 修正

- 正規の20葉・親閉包の再計算を `verify_certificate(cert)` に分離し、通常検査と改変試験で同じ経路を使う。
- `--negative` で証明書の複製を1項目ずつ改変し、**実際の `verify_certificate` が拒否すること**を確認する。対象は (1) 別の終局証人、(2) 範囲外の証人番号、(3) 終局再帰状態数、(4) 合法手数、(5) 親閉包SHA-256、(6) 親閉包類数、(7) 選定9石局面。
- 改変を受理した場合は `AssertionError` でCIを失敗させる。通常の正規証明書の検査内容と固定結果は変更していない。
- mainに直接反映。branch・PRは作成していない。

## 検証結果

- [修正コミット](https://github.com/yuubinnkyoku/kyouen-researches/commit/aaee47b090e43ebdd3a115ef8c007b741690ff25)
- [独立証明CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40936665830): **成功**（2026-10-30 JST）。Nodeによる幾何・親閉包、Pythonの20葉・改変拒否、Pythonの第9〜27回証人と全37行の独立伝播再計算が完走。

新しいWIN9/LOSS9は発見していない。既存の証明限定8石WIN **5,859類**、固定14根計画の未証明8石 **37類**、全合法子の未確定9石 **750類・760辺**、新規二石root閉鎖 **0件**を変更しない。37類は空盤全体の未解決局面数ではない。**標準11×11空盤の勝敗はUNKNOWN。**
