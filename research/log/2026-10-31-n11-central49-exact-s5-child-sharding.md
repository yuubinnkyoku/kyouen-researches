# 2026-10-31：中央49の未判定S5を子局面単位で4分割し、重複なし・最大632類を達成

作業前にmain `107e43c09c8a8c3a3e0966d234bd30a84acda564`、AGENTS.md、research/knowledge/README.md、K0023、中央19初手の実験README、中央49の31証人・五石依存・worker分割の直近logを確認した。11×11空盤の勝敗は **UNKNOWN**。

## 動機と計算

既存の証人単位の平準化は、28個の未証明四石証人を4 workerへ割り当て、最大負荷689類、worker間の重複157類だった。重複を0にすると13証人の共有成分が不可分になり、最大1,042類が下界となる。

しかし、必要な仕事を証人単位にする必要はない。五石正準クラスを一度だけ計算し、その結果を全親証人から参照すればよい。

固定31証人の合法五石子を整数幾何・D4正準化で再列挙し、固定二系統の厳密S5判定cache（Git blob `2dccf42b92337cbcbfb62ea5c77db487b1ad8ead` / `9887a18c0788d26507be7e8e191c26817634a6b6`）と照合した。

- 未証明S4：28類。
- その合法S5子：相異なる2,528類。既知LOSS5は3類、未判定は**2,525類**。
- 別途、既知LOSS4の3類には全て既知LOSS5の子があり、相異なる既知S5の総数は315類。
- 未判定S5を正準鍵の辞書順に並べ、順位 `mod 4` で分配する。worker別件数は**632、631、631、631**。各鍵は一度だけ出現し、共有301類も重複実行しない。
- 4workerに2,525個の独立単位仕事を配ると最大件数は少なくとも `ceil(2525/4)=632`。今回の割当はこの下界を達成するため、**均一件数モデルでは厳密最適**。
- 既存の証人単位平準化（最大689、重複157）と比較して、最大件数57類（約8.3%）および重複157類を同時に削減。証人単位・重複0案（最大1,042）との比較では最大件数410類減。

## 再現と信頼境界

`research/experiments/n11-central-19-cover-20261031/audit_central49_worker_partition.js` に、既存の幾何・共有構造監査に加え、cacheのblob SHA-1固定、重複・WIN/LOSS衝突拒否、S5子単位の厳密4分割、証人別依存検査、worker別SHA-256出力、`--worker 0..3` の一覧出力を実装した。CIの既存「N11 central WIN4-safe cover audit」に含まれるため、push後の監査で再実行される。

```sh
node research/experiments/n11-central-19-cover-20261031/audit_central49_worker_partition.js
node research/experiments/n11-central-19-cover-20261031/audit_central49_worker_partition.js --worker 0
```

これは**仕事一覧の構造的な最適化**であって、探索の実測速度や証明済みS5の増加ではない。S5間で計算費用は異なり、共有TTや通信の実装も未検証。workerの出力を統合するときは鍵・極性の衝突を拒否し、未完やsolver-trusted結果を独立終局証明に取り違えないこと。新規LOSS4=0、二石root閉鎖=0、**11×11空盤はUNKNOWN**。
