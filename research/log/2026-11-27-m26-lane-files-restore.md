# 2026-11-27 m26 4レーン scaffolding・class0 kit の欠落 file 修復 (incident 66e11623 残滓)

## 発見

2026-11-27T16:00Z の RESTORE commit `66e11623` は「good tree `783f6a2c` (15:44) 基準 + 再追加」で tree を再構築したが、
15:48-15:58 に出版された file 群の一部が main から落ちていた。本 session (高速レーン) が着手前の最新 main 確認で検出した。

## 修復対象 (全 file byte-exact・sha256 pin 照合済み)

- `six-row-q6-m26-class0-split-20261127` (class {0} completion kit, commit `d310d80c` 時点の tree `946155b0` に存在):
  - `scripts/sat.js` (sha256 `fcc0cfd8…`) / `scripts/sat2.js` (`14ceb854…`) / `scripts/sat3.js` (`e04581eb…`) /
    `scripts/verify_frac.py` (`837fe24b…`) — kit 自身の `MANIFEST-sha256.txt` 記載の 4 本。
  - `output/meta_6x25q6_c2k4p11.json` (`26676a4d…`) / `output/r6x25q6_c2k4p11_mine.txt` (`4070d7ad…`) —
    MANIFEST 記載・対照 (6x25 class{2} minpos=11 SAT 3,574,244) の meta と生ログ。
- `six-row-q6-m26-class0-lane-20261128` / `class1-lane-20261128` / `class2-rest-lane-20261128` の
  `scripts/sat.js/sat2.js/sat3.js` (class0-lane は verify_frac.py も):
  pre-restore commit `aa4bef59` に存在した byte-clone scripts (各 lane README が「保持する」と宣言する 4 本)。
  `deepdef-k3210-lane` は 4 本とも現存・無修復。class1/class2-rest の verify_frac.py は現存。

byte 照合は commit-pinned raw (`d310d80c` / `aa4bef59`) から取得し sha256sum で実施。
修復後の main から fetch-back し同一 sha256 を再確認する。

## 修復しないもの (正直な記録)

- `class2-rest-lane-20261128/output/rcalib-*.txt` (対照 bit-exact 再生の生ログ): この dir は
  `79ad283a`/`783f6a2c`/`aa4bef59` のいずれの tree にも存在せず、**出版されたことがない**。
  lane README・driver README の「生ログを出版」の記載は raw が存在しない未達の主張として残る
  (対照の数値主張 3,574,244 bit-exact 自体は class0 kit の `output/r6x25q6_c2k4p11_mine.txt` が別途出版しており、
  本修復で同 raw も main に戻る)。偽造して補完しない。

## scope

verdict 不消費・11x11 UNKNOWN・conflicts は bookkeeping。M_{6,6} ∈ [26, 495] 不変。
