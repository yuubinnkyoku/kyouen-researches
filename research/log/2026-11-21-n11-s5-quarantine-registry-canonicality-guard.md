# 2026-11-21 n11 S5 quarantine registry canonical/safe guard

## 着手判断

最新main `2e9ec4c547d1bed5d277bda1eea37c39767f79ef`、`AGENTS.md`、`research/knowledge/README.md` と、K0329、S5 cache merge実装・回帰検査、11×11関連のknowledge・experiments・logを確認した。fold17/resolve7、残余72行の候補供給・36-root sweep、WIN8証明書抽出、fold24検証などは既存の単一オーナー宣言があるため、同じ探索・証明書・receipt作業には着手しない。

## 発見

S5 cache mergeは入力cacheの各キーについて、5石・D4正準形・四点共円なしを検査してから統合する。一方、共有関数 `quarantined_cache_keys()` は、quarantine registry側のキーについて石数と整数範囲は検査するものの、D4正準形と幾何安全性を検査していなかった。

この不一致は実害につながる。registryに非正準D4像が誤登録されると、cache側の正準キーと完全一致せず、撤回対象の古いverdictが除外されないまま統合され得る。これは「欠損・破損時は停止する」というregistryの役割と矛盾する。

## 修正

- D4正準形（比較順は既存mergeと同じ `(hi, lo)`）と、全10個の四点部分集合に対する整数行列式ゼロ検査を、`s5_evidence_policy.py` の共通関数 `is_canonical_safe_s5_key` に集約した。
- quarantine registryの全entry（inactiveを含む）に同じ検査を適用し、不正なD4 aliasまたはunsafe keyがあればmerge前に停止する。
- `dfpn_s5_merge.sh` も同じ共通関数をcache rowに使用し、cacheと除外表の判定条件を一つにした。
- shell回帰とPython単体回帰に、非正準D4 aliasと、D4正準だが5点が一直線上にある `(31, 0)` の2つの拒否試験を追加した。

## 事前検査と限界

現行mainのregistryは2 entry・2 activeで、独立再導出したD4正準性・安全性検査を両方とも通過した。別実装の事前検査では、既存のcanonical safe fixtureは受理し、反射D4 aliasと `(31, 0)` は拒否された。

この記録時点では、変更後のshell回帰・Python単体回帰・GitHub CIは未実行。CIが通るまでは、修正後コード全体の統合検証完了とは扱わない。現行registryの内容、cache verdict、WIN/LOSS分類、certificate、receipt、S6行は変更していない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWNのまま。**
