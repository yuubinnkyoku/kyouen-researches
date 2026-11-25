# 2026-11-24 NCW class-enum closure 証明書: 実行・監査 log（単一オーナー）

宣言ノート `2026-11-24-ncw-class-enum-note.md`（commit `cb72a442`）で事前宣言した
publish-then-execute 手順の実行記録。作業種別は **K1310 への evidence addition**
（新規K番号なし・定理本文・status・relations 不変・11×11 verdict 消費なし）。

## 0. 出版 chain

| step | commit | 内容 |
|------|--------|------|
| 1 | `cb72a442` | 宣言ノート（期待 stdout sha・失敗閉鎖・変異表の事前宣言） |
| 2 | `a33ede53` | キット core: `enum_classes.py` + `eqcheck.py` + 凍結出力 `output/{frozen_default,frozen_deep,predry1..4,eqcheck}.out` + README |
| 3 | `076f7056` | tamper スクリプト `tamper/{t1,t2,t3}.py`（宣言どおりの1行変形） + `tamper/t3.out` |
| 4 | 本 commit | `tamper/{t1,t2}.out`（変異出力凍結） + 公式監査成果物 `output/audit_run1..4.out`・`output/audit_eq1..2.out` + `detcheck.json` + `MANIFEST-sha256` + 本 log |

## 1. fetch-back 検証（出版(bytes)の同一性）

step 2・3 で出版した 13 ファイルを `raw.githubusercontent.com` で取り戻し、
sha256sum で地元コピーと照合した結果、**全 13 ファイルが byte 一致**:

- `enum_classes.py` = `716b2976…becbad7`、`eqcheck.py` = `6c005154…f633ffa1`
- 出力 7 件（`4284f248…` ×5=default/predry1..4、`a4149b37…`=deep、
  `a7bfb3bb…`=eqcheck）
- `tamper/t1.py`=`f93aa62e…`、`t2.py`=`1e6a29a2…`、`t3.py`=`f09b2ef5…`、
  `t3.out`=`d8a4f3e8…`

以後の公式走はすべてこの fetch-back bytes から行った（地元 draft は不使用）。

## 2. 公式走（決定性の実機確認・全て fetch-back bytes から）

### enum_classes.py 4 走（全 rc=0）

| run | 環境 | PYTHONHASHSEED | stdout sha256 |
|-----|------|----------------|---------------|
| 1 | 同一 cwd | unset（毎回乱数） | `4284f248a319…160651` |
| 2 | 同一 cwd | `1` | `4284f248a319…160651` |
| 3 | 隔離コピー + `env -i` | `99` | `4284f248a319…160651` |
| 4 | 隔離コピー + `env -i` | `7` | `4284f248a319…160651` |

期待値（宣言ノート §2）どおり、hash seed・実行環境を変えても stdout は
byte 一致。内容は既定 census で
`pair_classes=280 pair_bad=0 bed_classes=39 bed_bad=0 xpair=0 xbed=0
census_pair=108000 census_pair_bad=0 census_bed=3150 census_bed_bad=0
missing_class=0`（深部走 `34 16 44 20` は kit core 出版時点で
`census_pair=203456 census_bed=5780 bad 0`、`output/frozen_deep.out` 参照）。

### eqcheck.py 2 走（全 rc=0）

`EQCHECK: comparisons=1031085 bad=0`、stdout sha `a7bfb3bb05dd…b917650` が
2 走とも byte 一致。

### 判定: **OFFICIAL-PASS**

## 3. tamper 電池（全て rc=1 の fail-closed が期待値・事前宣言どおり）

| id | 変形 | 実測 RESULT（凍結出力） |
|----|------|------------------------|
| t1 | zone-A 申立 `[g odd]` → `[g even]` | FAIL `pair_bad=110 xpair=110 census_pair_bad=57600` |
| t2 | `sym_cchild_kge2` から concession flip `1 ^ ` 除去（構築期バグ②の再現） | FAIL `pair_bad=205 xpair=230 census_pair_bad=100800` |
| t3 | witness 棄却 `gs >= 0` → `gs >= -1`（構築期バグ③ off-by-one の再現） | FAIL `pair_classes=277 census_pair_bad=12 missing_class=12` |

3/3 検出。検査器（cross-validation + coverage census + missing-class）が
宣言ノート §4 に開示した3種類の実バグ型を確実に捕捉することを確認した。

## 4. 証明書としての内容（再掲・詳細は宣言ノート §1）

- 分割: 実現可能ラベル組合せ **pair 280 クラス + bed 39 クラス**（全クラスに
  具象 witness）。閉包: 各クラスで `mex(children) == claim` が記号的に機械検証
  され、クラス毎閉包 + 分割により mex 閉包は全 cell に対し 280+39 場合分けで
  閉じる。これは公刊 K1310 手証明 SS2.4/SS2.5 の区域代数に対応する。
- census は有限実機照合（default 108,000+3,150 / 深部 203,456+5,780、bad 0）で
  あり証明ではない。eqcheck は法則実装の公刊 verify_k1310.py への転写照合
  （1,031,085 点・bad 0）。engine 接地は公刊 K1310 公式監査が確立済みで
  本キットは engine を import しない。
- **新規定理なし**。法則の全称性はあくまで公刊 K1310 手証明が担う。

## 5. 受入と反映

- 受入: fetch-back 13 ファイル byte 一致 + 公式 6 走 byte 一致 rc=0 +
  tamper 3/3 fail-closed → **OFFICIAL-PASS** と判定した。
- machine 可読な監査記録は `detcheck.json`、掲載ファイルの sha256 は
  `MANIFEST-sha256`（MANIFEST 自身を除く全キット掲載ファイルを網羅）。
- K1310 item（`research/knowledge/items/K1310-noncongruent-window-collapse.md`）
  の artifacts リスト末尾に本証明書を 1 エントリ追加する（定理本文・status・
  relations は変更しない）。
- 11×11 は UNKNOWN 維持。本キットの成果（クラス分割・typed 子評価器・
  枝刈り構造）が 11×11 レーンで使える場合は向先のレーンが参照する形を取る。
