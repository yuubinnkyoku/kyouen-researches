# 2026-11-16: 全t値3 witnessの最小幅構成を補正

## 作業前確認

- 作業開始時の最新main: 4be5f4050f5dfdea5a1451f12953d95dfc5643be。
- AGENTS.md: mainへ直接反映、正本はK項目、experiment/logは歴史的記録として書き換えない、生成物は直接編集しない。knowledge変更後はcheck・unit test・buildが必要。
- research/knowledge/README.md: K0832の全t最大値定理は既に記載済み。固定幅では4×m q=4/5、5×m q=5/6/7等が未確定。s_n単調性、K_10の20石存在もopen。今回の作業はこれらを重複探索せず、K0832の証明補足に限定。
- generated summaryの未解決一覧を確認。新しいK番号は作らない。
- 成果コミット: eb83bd80a8a0a9b3dc1830fed695b7d9b78fe05f。

## 発見

全t最大値定理の本文は、値3の最小幅を \(\lceil(cap+2)/t\rceil\) と正しく述べていた。しかし直後のwitness説明と旧V5検証器は、剰余 \(1\le r\le t-2\) でも「余剰レベルトークン」と「空ファイバー」を両方確保していた。

この場合、占有数 \(r\) のファイバー自身が余剰座標 \(t-1-r\ge1\) を与えるため、空ファイバーは不要。旧構成は1幅余分だった。これは全t定理の反例ではなく、最小幅証人の構成記述・監査範囲の不足。

## 補正

\(cap=2t+\mu t+r\) とし、常に占有 \(t,t-1\) と満杯 \(\mu\) 本を置く。\(r=0\) は空を1本、\(1\le r\le t-2\) は占有 \(r\) を1本、\(r=t-1\) は占有 \(t-1\) を追加して空を1本残す。幅はそれぞれ \(\mu+3,\mu+3,\mu+4\) で、\(\lceil(cap+2)/t\rceil\) と一致。

\(R=1\)、\(X\ne\varnothing\)、\(z\ge1\)、\(\kappa=1\) から \(H=\operatorname{mex}\{0,1\}=2\)。占有 \(t\) の鎖XORが1なので \(G=3\)。より小さい幅は \(q\ge tw\) レジーム補題で排除。

## 検証

- 新検証器は元の占有多重集合ゲームを直接再帰mex。
- 810 witness（\(2\le t\le16,\mu\le5\)、全剰余）で全てG=3、5,670状態。
- 最小幅直前の60盤面（\(2\le t\le6,\mu\le2\)、全剰余）を空盤から完全列挙し、最大G≤1、7,331状態。
- 2回の出力はbyte-identical。検証器SHA 39b2b0adf81079c3e756afd0ba3832d0cc97183a9ac60a91f623a0a9907a8294、監査SHA 70a8105054bdd9cd116a0e3a2cfe1aac87b52c20c6173ead101eed23868f9c59。

## 反映

- 新experiment vertical-fiber-all-t-minwidth-witness-20261116/ に報告・検証器・監査JSONを追加。
- K0832の既存witness段落を3剰余場合分けへ訂正し、同じK項目のartifactを追加。
- 手書きknowledge READMEに最小幅の系を追記。
- knowledge integrityとgenerated refresh workflowに新検証器を追加。refresh workflow自身の変更で生成ビュー更新を起動する。
- generatedファイルは手で編集しない。

## 未完了

この環境からGitHub上のActions実行結果はまだ確認していない。uv sync、knowledge check、unit tests、buildの最終成否はActionsで確認する。数学的未解決として、残余 \(H=2\) の完全分類は引き続き次の候補。
