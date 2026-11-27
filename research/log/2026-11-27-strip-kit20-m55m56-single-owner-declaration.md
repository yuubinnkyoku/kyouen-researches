# 単一オーナー宣言: kit-20 (m55/m56 frontier first-contact + m53/m54 windows + ladder 次深度 + 偶m z=3m+20) (2026-11-27)

- 宣言日時: 2026-11-27T06:12Z
- 宣言時 HEAD: `2d3c43f1d8954fa0a0e1913fcff4c6daefac8ed4` (main)
- 単一オーナー: 高速レーン (本実行)。他の hourly 実行は本宣言の作業領域 (kit-20 build) に着手しないこと。
- 並走回避の確認: 同一時刻帯に 7行 q=4 m69 band extension の単一オーナー宣言
  (`2026-11-27-seven-row-q4-band-m69-single-owner.md`, 532ed4df) が出ているため
  本実行は同領域に触れない。seventh-cost 長期レーン (Part SZ wave E 完結済み) とも disjoint。

## 登録源 (register-before-measure・公開 SSOT のみ)

- 登録源: published kit-19 凍結 .out
  `research/experiments/strip-newband-m53m54-frontier-windows-evenlife-20261127/explore_m53m54_frontier_windows_evenlife.out`
  (sha256 `12277fd483aac7dfed4e3b687f3eb2433de44706d74377b08cd4c7db7acd623f`, 626,727 bytes, commit fe78f9ba) の
  `future_slice_registration_constants` 34 項を機械抽出 (本実行で byte 再取得・sha 照合済み)。

## 測定対象 (受入条件・全 49 行)

1. **frontier 42nd/43rd (初の m>54 行)**: m=55@z=109 R=165 `{55,56}@S=111 UP 2v0` (collapse v(111,109,165)=0) /
   m=56@z=110 R=167 `(56,56)@S=112 UP 2v1` (collapse v(112,110,167)=1)。
   z*(55)=2*55-2+1=109, z*(56)=2*56-2+0=110 per K1268。
2. **in-band 窓**: m=53 z{97..104} / m=54 z{98..105} 各 8 行・計 16 行 (0 分離候補・登録後に測定)。
3. **ladder 次深度 28 行**: m19..m32 の one-past/birth 各 1 行 (登録文の z に厳密従う):
   m19 z80/81, m20 z81/82, m21 z76/77, m22 z77/78, m23 z78/79, m24 z79/80, m25 z80/81, m26 z81/82,
   m27 z80/81, m28 z81/82, m29 z86/87, m30 z87/88, m31 z84/85, m32 z85/86
   (one-past/birth の予測文は登録文 28 項に byte 由来で従う)。
4. **偶m z=3m+20 (kit-19 の z=3m+18 3/3 EXACT で条件成立)**: m=14/16/18 の 3 行
   (stick {m,2m+20} DOWN 0v2 + NEW {m,2m+22} UP 2v1 候補・NON-BINDING 側の測定)。

## 手順 (publish-then-execute)

1. wave A: 本宣言 (HEAD pin) → kit-20 の README/audit_kit20/derive_check_kit20/engine_block を出版。
2. wave B: explorer `explore_m55m56_frontier_windows_evenlife.py` を gen_kit20 (kit-19 generator の変換・fail-closed 変換対) で生成・出版。
3. wave C: chunked runner による測定 4 走 byte 同一を determinism 根拠とし、凍結 .out・audit (20 gate)・tamper 3/3 fail-closed・derive DERIVE-PASS を経て出版。

## 主張の範囲

- 全行は有限観測 (完全有限列挙) であり、パリティ計数・frontier 前進・rule v2・偶m テンプレを法則として過大主張しない。
- **標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・全 closure class は本作業と無関係で全時点 UNKNOWN・verdict 不消費。**
- kit-19 の battery/anchors/frontier 値は再検証 (anchor recheck) に回すが書き換えない。
