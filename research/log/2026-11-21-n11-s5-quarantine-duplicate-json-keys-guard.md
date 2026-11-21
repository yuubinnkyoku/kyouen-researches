# S5 quarantine registryのJSON重複キーを拒否する

## 発見

`json.loads`はJSON object内の重複keyを黙って受け入れ、最後の値を採用する。S5 quarantine registryでは、たとえば1つのentryに `"active": true, "active": false` と重複記載すると、撤回済みverdictをactiveでないように見せてcache filterから外せる。これはregistryの「破損時はfail closed」という目的に反する。

## 修正

- `s5_evidence_policy.py` に `reject_duplicate_json_keys` を追加。
- `quarantined_cache_keys()` の `json.loads` に `object_pairs_hook` を指定し、root・nested objectの重複を拒否。
- 既存K0329を更新。新しいK項目は作らない。

## 検証

- rootの重複 `schema` key：拒否。
- nested entryの重複 `active` key（true→false）：拒否。
- 同じ修正を組み込んだ隔離環境のunittest：2/2 PASS。
- 修正前の標準JSON解析で重複 `active` の後値falseが採用されることを確認し、回避可能だった撤回状態を再現。
- mainへ直接commit。CI run 44874127773 は現時点でqueued。

これはcache統合の勝敗データを変更しない。撤回台帳の読取を厳格化する修正であり、新しいWIN/LOSS verdictや証明書は生まれていない。

**11×11空盤の弱解決はUNKNOWNのまま。**
