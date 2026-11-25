# 2026-11-18：receipt-harvest global fold（head 1476 → 1589）と presweep census v20

## 結果

これまでのfoldは各bandのreceiptを1本ずつ・都度精算していたが、公開済みWIN7-D10 root全体×未解決worklist全体の大域subsetスキャンは実施されていなかった。今回、census v1の79 sourceから収穫したpre-64h harvest（3,548 canon = 353 WIN7-D10 / 3,195 REFUTED-D10、v19出版値と一致）、post-64hの9証明書manifest（66i/66j/69j/71e/72d/73i/73j/73k/73l）、cost64h/cost76c fold receipt、そして第三実装監査・BigInt再検証済みのdual root（cost73i bit97 root `00000000020001003810000008000000`、cost66j bit9 root `00000000000000c09002000000001200`）を合わせた全482 WIN rootを、head1476のopen manifest行6,372行すべてに対してD4 orbit-levelで照合した。

- **113行がreceiptで閉鎖可能**と判明し、全て閉じた（dual root 7行 + 大域scan 106行）
- 全行 category=unswept、35行STERILE registryとの交差0、closed合計edge cost 8,882
- needed行（c1==0）は102行・cost 8,076を除去
- 影響S5親53、parent-row incidence 225、親edge-cost差分17,697、**親の完全閉鎖0件**
- **最良class-2親 `00000000000000403800000008000000` は12行 → 1行**（edge cost 806 → 78）。残る最後の1行は `00000000000000403800000008000008`（cost 78）

なお、このfoldは73i bit97 / 66j bit9 dual fold（7行分）を吸収する形で出版した。单独のdual fold出版は行わない。

## frontier

| 指標 | head1476 | global fold後 |
|---|---:|---:|
| solved S6 manifest rows | 1476 | 1589 |
| remaining S5 orbits | 174 | 174 |
| unique remaining S6 | 6372 | 6259 |
| sum remaining edge cost | 504389 | 495507 |
| open-class S6 demand | 4645 | 4543 |
| open-class edge-cost demand | 368303 | 360227 |

## 監査・再現

- 監査スクリプト: `scripts/audit_receipt_harvest_global_fold_20261118.py`（**この実行環境で実行済み、全assertion PASS**）
- fold記録: `output/class-frontier-receipt-harvest-global-fold-20261118.json`（113行それぞれのreceipt root・D4変換σ・extra bit・demand・parents、112 source blob pin込み）

監査スクリプトは79 source harvest再構築（3,548/353/3,195 assert）、head-1476 frontier 6組の独立再計算（出版値 [1476, 174, 6372, 504389, 4645, 368303] と全桁一致）、482 root×open行の大域scan（113行 assert）、簿記（needed 102行/8,076 assert、frontier後 [1589, 174, 6259, 495507, 4543, 360227] assert）をすべて pinned sourceのみから再現する。engine runは不要。

コントロール（すべてPASS）:

- C1: 既fold済み66i bit19 rootはhead1476のopen行を0行しか閉じない（fold完備性の検証）
- C2: 同rootのmanifest部分集合は出版fold行3件+ledger整合
- C3: サンプル5行全件で σ(root) ⊃ row のD4変換が存在、root 7石・候補数53〜58で合法
- C4: 113行と35行STERILE registryの交差なし

## census v20（worklist全体の再構築）

v19の3-family pool枯渇を受けて、coordinator修正通り**worklist全体**をhead1589基準で再構築した。

- 適格プール: unswept 6,223行（STERILE 35行・transfer_partial 1行 `00000000000000801222000000800000` は除外。後者は両親partial_sterileで3 transferred refuted bitsのengine確認待ち、watch item）
- head1589で完全STERILE化した親: 4親・33行・cost 2,502（うち2親は今回のfoldで新規fully-sterile）
- 大域最安適格行: cost 50 `00000000000002901002000000002000`
- **選定target: `00000000000000403800000008000008`（cost 78）**。parent-closure-first オーバーライド: この1行をsweepすれば親 `00000000000000403800000008000000` が**最初の完全receipt-closed S5親**になる可能性があり、remaining_s5_orbits 174→173 は行sweep単独では到達できない唯一のfrontier次元。WIN bit発見なら証明書抽出→fold、全REFUTEDなら行がSTERILE化し親はD10自己閉鎖不能（いずれも確定的構造事実）
- targetの既知verdict: 既知WIN 0 bit、harvest confirmation 2 bits（bit 13, 115）、fresh 76 bits

- v20記録: `output/class2-lane-next-target-presweep-1589-v20-20261118.json`
- v20スクリプト: `scripts/next_target_presweep_head1589_v20_20261118.py`（監査モジュールをimportしてfold状態を再deriveしてから ranking）

## 解釈の境界

これは公開済み・独立検証済みWIN7-D10証明書の簿記foldとtarget選定であり、新しい探索結果ではない。foldは新しいengine verdictを1つも作らず、S5親を1つも完全に閉じない。REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はすべて**UNKNOWNのまま**。

次はtarget行（cost 78）のsweep（ev82e流儀: 9bitバッチ、v17 runner、v15 crosscheck、決定性再実行、cap 1e9/bit、andclose 1、terminal範囲[13,17]）。
