# 2026-11-14 class4-batch3 child#8 sweep（第20セッション後半）

- S6 child `00000000020000003800000088000000`（cost 74・c1=0,c2=1,c4=2・
  両open blockerへのdual-use・cost74帯で唯一のc2>0）の74非退化候補を全走査 —
  **全74候補 REFUTED-D10・WIN7-D10 0件・capped 0**・総318,695,735 nodes・
  pilot d6 5,949 PASS・決定制御は最重量5候補（bit120/88/116/4/79）が独立再実行で
  node-exact。全候補 terminal range [13,17]。
- **child#6（cost 73）に次ぐ2例目の WIN7-D10-sterile child**。
  しかも本orbitは初の「class-2需要を持つsterile orbit」で、
  c2=1,c4=2 の需要は他のrootに立つ証明書で被覆するしかない。
  記録: output/class4-batch3-child8-sweep.json（コミット3f7c2427・
  一度PUTが502を返したが実際にはコミット成立していた既知パターン）。
- child#7の5証明書のcoversが本orbitを閉じている可能性はあるが、
  manifest-level再計算がまだなので「sterile」はあくまで
  「同child由来の深さ10以内証明書は作れない」という事実のみを意味する。
- 解釈ガード: REFUTEDは「深さ10以内のWIN7の否定」のみで、より深い勝ちは排除しない。
  **class 4・S2 {59,60}・二石 root {49,60}・11×11 空盤はいずれも UNKNOWN**。
- レジューム: (1) 次の最安未sweepは `00000000020000003801000080000000`
 （cost 74・c4=3）と `00000000020000003800000080000020`（cost 74・c1=2,c4=3）。
  並走レーンの最新mainを取り直してから。(2) manifest-level frontier再計算が優先。