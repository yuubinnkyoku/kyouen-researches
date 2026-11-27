# 79ad283a 大量削除: 独立センサスと全復元監査 (2026-11-27)

## 経緯

- 79ad283a (2026-11-27T15:42:03Z, six-row q6 6x26 four-lane scaffolding) が working tree の大部分を削除して main に着地した (親 783f6a2c 基準)。
- f0bb2145 は 29 file (4 kit) を復元しただけだった (GitHub commit API の file list が先頭 30 件で打ち切られていたための部分センサス)。
- 941034718 が csv を修復した際、(6,6) 行に 6x26 class {0} full-split の新規結果記録 (six-row-q6-m26-class0-split-20261127, P=0..11 全 INDET) を追記した。
- 66e116238 が全 tree 復元を実施した。

## 本 session の独立センサス (方法が異なる機械測定)

- git trees API で親 783f6a2c と各時点 HEAD を subtree 単位で sha 比較した。
- 79ad283a 時点の未復元被害: research/experiments **124 kit dir**、research/knowledge items **26 file** (K1327..K1349)、research/log **255 file** (計 1,840,622 B)。results/docs/archive/generated は削除 0。
- 欠落 281 file を raw CDN (783f6a2c pin) から取得し、git blob sha (sha1("blob <len>\0"+bytes)) を 281/281 で照合して復元素材を機械検証済み (本 session の出版前 HEAD gate が並走の csv 修復と全復元を 2 度検出し、重複出版を回避した)。

## 66e116238 全復元の独立監査 (HEAD a1d337be 時点)

- research/knowledge: 再帰全比較 — **欠落 0** (26/26 復元)。changed 1 (K1349) は正当な後追い追記 (独立検証 artifact 追加)。
- research/log: 再帰全比較 — **欠落 0** (255/255 復元)。added 3・changed 2 は正当 (うち 1 は 2026-11-26-main-tree-restore-incident.md への本事故の追記)。
- research/experiments: dir 粒度比較 — **欠落 0** (124/124 復元・1638 dir 全存在 + 事故後の正当な 7 lane dir)。
- results / docs: subtree sha が親 783f6a2c と完全一致。
- これにより 79ad283a 被害は closed。

## 残回帰 1 件の特定と修復 (本 commit)

- 全復元が results を 783f6a2c 状態に戻したため、941034718 が csv (6,6) 行に追記した 6x26 class {0} full-split 記録が失われていた (kit・log は experiments/log 側で無事)。
- 本 commit で (6,6) 行のみを 941034718 版に戻した。修復後 csv は 941034718 の csv と byte-exact 一致 (70,501B, sha256 5f6b9cebef84abaa7fd4319abb5e7edaa7f2fb07c7347a7e42244b4c989e72b2)。機械検証: (6,6) 行は 941034718 行 = 復元時点行の閉引用符直前への class0 note 挿入であり、他の行は一切変更なし。
- verdict 影響なし (記録の復旧のみ)。11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・全 closure class は全時点 UNKNOWN。
