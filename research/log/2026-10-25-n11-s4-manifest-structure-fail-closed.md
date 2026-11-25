# 2026-10-25：S4証明書の空入力・欠損行の検査を厳格化

開始時main: `2a491b8e34daca9d440c9c191cdbe61cb5bff5fd`。AGENTS.md、research/knowledge/README.md、K0092/K0105/K0329/K0415、直近の11×11実験・log、S4検証器・S5 merge・対応する回帰試験を確認した。

## 発見

`dfpn_s4_manifest_verify.py` の `load_manifest` は `s4verdict` 以外の行を無条件に無視していた。入力が空でも `main` は `MANIFEST_VERIFIED` を出し、終了コード0を返す。したがって、空の証明書や行頭を壊された証明書を「検証済み」と誤認する余地があった。これは既存の具体的なS4証明書の勝敗に誤りを発見したという意味ではない。

## 修正

- 空・コメントのみの証明書を拒否し、未知の行種別も黙って飛ばさない。
- 8列の固定ヘッダ、整数、盤面範囲、異なる二石root、4石鍵のビット数、確定勝敗、非負の子数と正の被覆数を検査。
- `n_child` と実際の列数の一致を先に確認し、5石子鍵の範囲・ビット数を検査してから盤面の再列挙に渡す。
- `test_dfpn_s4_manifest_verify_cache.py` に空入力、未知行、列欠損、負の子数、子数不一致、範囲外鍵などの回帰を追加。

これらは**証明書入力の構造検査**であり、既存の幾何・合法子完全性・WIN/LOSS検査を緩めない。変更した `load_manifest` 関数と同内容をローカルPythonに写した単体確認では、正常1例を受理し、空入力・コメントのみ・未知行・短縮行・負数・過大子数・範囲外root・不正鍵・不正子の9例を拒否した（計10例）。ただし**リポジトリ内のPythonテストそのもの**と全体CIの完了は確認しておらず、これらを実行済みとは主張しない。

再現コマンド：

```sh
python3 -m unittest discover -s research/experiments/n11-search-methods/scripts -p 'test_dfpn_s4_manifest_verify_cache.py'
```

新規局面の勝敗確定・二石root閉鎖は0。標準11×11空盤の勝敗は **UNKNOWN**。
