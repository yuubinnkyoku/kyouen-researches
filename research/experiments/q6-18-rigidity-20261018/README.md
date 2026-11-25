# 18候補障害の剛性（2026-10-18）

新規成果：任意の3平行線・q=6で、各線18候補以上なのに15石未満の極大安全配置が存在するなら、石数は必ず(4,5,5)で、5石の2線の同和弦energyは14、かつ不足線の候補点数はちょうど18。14本の円は4石を起点として14個の異なる空候補点を一対一に塞ぐ必要がある。E=14の2線の交差構造も3種類に分類した。

**証明区分**：二点和一意復元とE=14分類は全称代数証明。18候補障害への帰着は全称計数証明と、別添19候補証明の有限1820代数型完全検査を併用。63,504組の検査は独立監査であって、全実数の代替証明ではない。

実行:

```
python research/experiments/q6-18-rigidity-20261018/verify.py
c++ -std=c++17 -O2 research/experiments/q6-18-rigidity-20261018/audit_independent.cpp -o /tmp/q6rigidity
/tmp/q6rigidity
python research/experiments/q6-18-rigidity-20261018/supporting-q6-19-verify.py
c++ -std=c++17 -O2 research/experiments/q6-18-rigidity-20261018/supporting-q6-19-audit.cpp -o /tmp/q6_19
/tmp/q6_19
```

既存のK0070の標準整数格子M3,6=9には影響しない。18候補が十分かどうかは未解決。最新main f0087e81 を確認。GitHub connectorからmainへの書き込みは安全検査で拒否され、未反映。番号K0442は仮番号。
