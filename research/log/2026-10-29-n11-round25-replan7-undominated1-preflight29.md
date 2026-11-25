# 2026-10-29: N11第25回後の再計画・第26回候補1類を独立事前検証

[第25回の独立検証済みLOSS9証明](../experiments/n11-s9-post-round24-round25-20261029/certificate.json)を入力とし、[再計画CI 40878927470](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40878927470)で第9〜25回の証明書とLOSS9親閉包を再照合。第25回LOSS9 1類・親閉包10類、証明限定WIN8 5,859類、固定14根計画の未証明37辺、WIN/LOSS衝突0件を確認。成果物ZIP SHA-256 `13fc113be03d0a35610d89cf2f825be2a3c063061bcba7e1471e3ccee3992181`。結果は[固定計画](../experiments/n11-s9-post-round25-replan-20261029/next-plan.json)。

未証明9石候補8類から前回選定済み1類を除外、追加LOSS9親による除外0類。残り7類の支配削減後は1類で、次の候補 `00042010000100821080000000000020` を選定。潜在被覆1辺、合法10石子29本。潜在被覆は勝敗証明ではない。

[独立事前検証CI 40880266124](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40880266124)は、3×3差分行列式と4×4整数行列式9,534件を照合し成功。合法10石子29本・29類、重複0。成果物ZIP SHA-256 `68e7c8606f1561ada14fe583546929ad6f7e50e91366d569a18a5f0c7ebad0e1`。結果は[固定事前検証](../experiments/n11-s9-post-round25-replan-20261029/preflight.json)。

今回の作業は証明済み勝敗を増やしていない。次の限定終局証明は第26回候補1類の29合法子だけを対象にする。新規二石root閉鎖0件、**標準11×11空盤はUNKNOWN**。
