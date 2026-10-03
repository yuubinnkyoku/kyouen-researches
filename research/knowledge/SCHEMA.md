# K項目schema v1

UTF-8 Markdownの先頭を `---` で囲むYAML front matterとする。ファイル名はIDと同じ。

必須: `id`, `title`, `kind`, `status`, `topics`, `aliases`, `relations`, `artifacts`。
本文には命題・対象範囲・現在の根拠・限界を記す。`scope` と `evidence` は任意の文字列。

- `kind` は定義/命題/有限計算/方式/検証/問い。`status: proved` は本文の量化全体への証明。
- `computed` は明示された有限範囲の完了計算、`observed` は標本・近似・測定。
- `conjectured`/`open` は数学的な未確定、`needs-review` は採用根拠の監査不足。
- `scope-unclear` は解釈不足、`withdrawn` は証拠無効による撤回。反例による否定は `refuted`。
- 語彙は `VOCABULARY.yaml`。statusは過去のイベントを表すために増やさない。

`relations` は `{type: ..., target: Knnnn, note: ...}` の配列。逆リンクは生成器に任せる。

| type | 向き・意味 |
|---|---|
| depends_on | 結論 → 必要な数学的・論理的前提 |
| supports | 有限計算・標本 → 支持する命題（証明を意味しない） |
| proves | 証明 → 証明される命題 |
| refutes | 反例・不可能性証明 → 否定される命題 |
| verifies | 独立検査・形式検証 → 検査する知識 |
| generalizes | より一般的な命題 → 特殊な命題 |
| supersedes | 置き換える知識 → 置き換えられる異なる旧知識 |

同じ命題の状態更新には `supersedes` や新番号を使わない。`depends_on`/`supersedes` は自己辺・循環禁止。

`artifacts` は `{path: repo相対POSIXパス, role: 語彙, note: 説明}` の配列。
任意で `commit`（完全40桁SHA）、`anchor`（見出し等）を付ける。現在repo内の実在ファイルを指す。
配布専用・ignored証明書は存在すると仮定せず、Git管理されたhash/manifestを指して所在を説明する。
絶対path・外部URL・ディレクトリ丸ごとの参照はartifactにしない。

`solution` は結果項目にのみ付ける。必須フィールド:

```yaml
solution:
  board: "9×9"
  level: weak
  outcome: first-player-win
  classification: [root, first-moves]
  coverage: "81/81 first moves"
  conditions: "標準q=4・完全指摘・通常プレイ"
  verification: [exact-search]
  certificate: "空盤面は独立検査済み。81初手全体は同一証明書に未収録"
  independent_check: "空盤証明書のC++検査。初手は別探索記録"
  note: "全81初手が先手勝ち"
```

一つの盤に弱解決・全初手・全局面など複数項目を許す。level一語からcoverageを推測しない。
一般定理は `outcome: conditional` と適用条件を記す。強解決の報告と独立監査完了を分離する。
生成表には未監査・撤回・反証もstatusを明示し、達成済み強解決へ昇格させない。
