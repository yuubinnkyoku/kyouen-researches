# 2026-10-30: 11×11第20候補LOSS証明の全37行をPythonで独立監査

最新main・AGENTS.md・knowledge正本K0023・全合法子監査と第9〜27回の証明書を確認し、既存のNode検証器だけが再計算していた「第20候補LOSS9の全37個の8石親への伝播」をPythonでも独立再計算できるようにした。

## 新しい検証範囲

- `research/experiments/n11-s9-full-child-top20-loss9-20261030/verify_full_incidence.py` を追加。Nodeの幾何・勝敗cacheを読み込まず、既存の独立Python整数幾何を利用する。
- 第9〜27回の19組の選択計画・証明書を読み、選択キー・証人番号のSHA-256連鎖を検査し、過去のWIN9集合・LOSS10証人から導かれるLOSS9親閉包を再構成する。過去の終局葉の勝敗そのものはこの追加検査では再探索せず、既存の独立検証済み証明に依存する。
- 今回の20個のLOSS10葉はPythonで終局再帰を再計算する。その親閉包192類・既存証明との重複除外184類・WIN/LOSS衝突0件を確認する。
- 固定14根計画の未証明8石37行について全合法9石子を再列挙し、旧LOSS9辺259、新規LOSS9辺69、未確定辺760、異なる未確定9石750類、純減49類を検査する。偽の増分を与えた場合の拒否試験も追加した。
- `.github/workflows/n11-s9-full-child-top20-loss9-verify.yml` に新しいPython全行監査を必須段階として追加し、`set -euo pipefail` で失敗を隠さない。

## 実行結果と証拠

- [独立監査CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40928046920) **成功**（2026-10-30 JST）。Node、従来のPython終局検証、新しいPython全37行監査、改変拒否試験の全段階が成功。
- [検証器追加コミット](https://github.com/yuubinnkyoku/kyouen-researches/commit/1946b12fcdfb4fa09c46d12e9b6f12d1681b9dc2)、[CI強制コミット](https://github.com/yuubinnkyoku/kyouen-researches/commit/3971292cfec638c4bcbf0e8efe282bbb51ff96b6)。branch/PRなしでmainに直接反映。
- 追加したのは**独立検証範囲の拡大**であり、新しい勝敗証人の発見ではない。第20候補の既存結果（9石LOSS20類、LOSS9純増184類、未確定9石799→750類、未確定辺829→760本）を別実装で裏づけた。
- 証明限定8石WINは5859類、固定14根計画の未証明8石37類、二石root新規閉鎖0件。11×11空盤の勝敗は**UNKNOWN**。

## 次の判断

750類のうち、WIN9の可能性がある候補とLOSS10証人による親閉包を多く得られる候補を別々に評価する。今回の追加監査で再計画の入力値を2言語から独立に確認できるようになった。37類は固定14根計画の局所的な未証明義務であり、空盤の全義務ではない。
