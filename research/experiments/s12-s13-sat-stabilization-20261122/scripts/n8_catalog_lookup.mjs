// n8_catalog_lookup.mjs — K0032 全408八石極大安全カタログへの n=8 SAT witness 照合（2026-11-22 追記レーン）
//
// 目的: s12-s13-sat-stabilization-20261122 の n=8 witness 2点（wit_n8k8 / v3wit_n8k8）が
//   K0032（research/knowledge/items/K0032-n8-minimum-maximal-size.md）の全408カタログの
//   どの要素・どの D4 軌道に属するかを特定する。
//
// 精度に関する設計（重要）: 8×8 bitmask は 64 ビットで 2^53 を超えるものがあるため、
//   JSON.parse / jq の double 経路では値が壊れる。mask はすべて文中テキストから
//   正規表現で10進文字列として抽出し、Node BigInt（64ビット厳密）で比較する。
//   stones・embedding・histogram 等の小整数 JSON.parse は安全（すべて < 2^7）。
//
// 入力（repo 相対・main 直接、いずれも刊行済みテキスト成果物; binary round4_b371.bin は使用しない）:
//   research/experiments/original-claims/output/round10_small_saturation.json
//     （51 D4 軌道代表 stones+mask, source_sha256 = round4_b371.bin の sha256 を明記）
//   research/experiments/original-claims/output/round46_n8_to_n9_embeddings_probe.json
//     （1632 = 408 カタログ源 × 4 オフセット埋め込み。source_S_mask の distinct がカタログ復元）
//   output/wit_n8k8.json, output/v3wit_n8k8.json （本実験の witness）
//
// 出力: output/n8_k0032_lookup.json（mask は10進文字列で格納）
// 全検査 PASS でない限り exit 1（fail-closed）。

import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../../../..');
const P = (p) => join(ROOT, p);
const sha256 = (b) => createHash('sha256').update(b).digest('hex');
const fail = (msg) => { console.error('FAIL: ' + msg); process.exit(1); };

// --- 基本幾何: 盤 8×8, セル (x,y), bit p = x + 8y ---
const N = 8, NN = 64;
const maskOf = (stones) => {
  let m = 0n;
  for (const [x, y] of stones) {
    if (!(Number.isInteger(x) && Number.isInteger(y)) || x < 0 || x >= N || y < 0 || y >= N) fail(`bad stone ${x},${y}`);
    m |= 1n << BigInt(x + N * y);
  }
  return m;
};
// 盤面 D4（8変換、round70_scope_catalogue_check.py perms と同型）
const d4 = [
  ([x, y]) => [x, y],
  ([x, y]) => [y, x],
  ([x, y]) => [N - 1 - x, y],
  ([x, y]) => [x, N - 1 - y],
  ([x, y]) => [N - 1 - y, N - 1 - x],
  ([x, y]) => [y, N - 1 - x],
  ([x, y]) => [N - 1 - x, N - 1 - y],
  ([x, y]) => [N - 1 - y, x],
];
const d4Masks = (stones) => [...new Set(d4.map(g => maskOf(stones.map(g))))].map(m => m.toString());

// --- 入力読み込み ---
const r10raw = readFileSync(P('research/experiments/original-claims/output/round10_small_saturation.json'), 'utf8');
const r46raw = readFileSync(P('research/experiments/original-claims/output/round46_n8_to_n9_embeddings_probe.json'), 'utf8');
const witnesses = ['output/wit_n8k8.json', 'output/v3wit_n8k8.json'].map(p => {
  const j = JSON.parse(readFileSync(P('research/experiments/s12-s13-sat-stabilization-20261122/' + p), 'utf8'));
  if (j.n !== N || !Array.isArray(j.stones) || j.stones.length !== 8) fail(`${p}: n!=8 or stones!=8`);
  return { file: p, stones: j.stones, derived_from: j.derived_from };
});

const r10 = JSON.parse(r10raw); // stones/histogram 等の小整数のみに使用（mask は不使用）
const summary = {};
summary.input_sha256 = {
  round10_small_saturation_json: sha256(r10raw),
  round46_n8_to_n9_embeddings_probe_json: sha256(r46raw),
};

// --- 1) round46 からカタログ復元（テキスト抽出・BigInt） ---
const maskRe = /"source_S_mask": *(\d+)/g;
const embeddingRe = /"embedding": *\[\s*(\d+),\s*(\d+)\s*\]/g;
const m46 = [...r46raw.matchAll(maskRe)].map(m => m[1]);
const e46 = [...r46raw.matchAll(embeddingRe)].map(m => `${m[1]},${m[2]}`);
if (m46.length !== 1632) fail(`round46 mask count ${m46.length} != 1632`);
if (e46.length !== 1632) fail(`round46 embedding count ${e46.length} != 1632`);
const cat = new Set(m46);
if (cat.size !== 408) fail(`round46 distinct masks ${cat.size} != 408`);
// 各カタログ源は4オフセット [0,0],[0,1],[1,0],[1,1] の各1回
const embByMask = new Map();
for (let i = 0; i < 1632; i++) {
  if (m46[i].length > 20) fail(`mask digit overflow at ${i}`); // uint64 上限検査
  const a = embByMask.get(m46[i]) ?? new Set();
  if (a.has(e46[i])) fail(`duplicate embedding ${e46[i]} for mask ${m46[i]}`);
  a.add(e46[i]); embByMask.set(m46[i], a);
}
for (const [m, s] of embByMask) {
  if (s.size !== 4 || !['0,0','0,1','1,0','1,1'].every(e => s.has(e))) fail(`mask ${m} embeddings != 4 offsets`);
}

// --- 2) round10 orbit 代表（stones は JSON.parse, mask はテキスト抽出で照合） ---
const repMasksText = [...r10raw.matchAll(/"mask": *(\d+)/g)].map(m => m[1]);
if (repMasksText.length !== 51) fail(`round10 mask count ${repMasksText.length} != 51`);
if (!Array.isArray(r10.orbits) || r10.orbits.length !== 51) fail('r10.orbits != 51');
const reps = r10.orbits.map((o, i) => {
  if (maskOf(o.stones).toString() !== repMasksText[i])
    fail(`round10 orbit ${i}: rep mask text ${repMasksText[i]} != stones-derived ${maskOf(o.stones)}`);
  if (o.orbit_size !== 8) fail(`orbit ${i} orbit_size != 8`);
  return { stones: o.stones.map(([x, y]) => [x, y]), mask: repMasksText[i], essential_curve_count: o.essential_curve_count };
});
// round10 の出典連鎖（binary round4_b371.bin の sha256 を明記している）
const srcSha = r10raw.match(/"source_sha256": *"([0-9a-f]{64})"/);
summary.round10_source_sha256_claim = srcSha ? srcSha[1] : null;

// --- 3) 構造検証: 51 代表 × D4 閉包 = 408、disjoint、カタログと完全一致 ---
const orbitOf = new Map();
for (let oi = 0; oi < 51; oi++) {
  for (const m of d4Masks(reps[oi].stones)) {
    const prev = orbitOf.get(m);
    if (prev !== undefined && prev !== oi) fail(`orbit overlap: mask ${m} in orbits ${prev},${oi}`);
    orbitOf.set(m, oi);
  }
}
if (orbitOf.size !== 408) fail(`orbit closure size ${orbitOf.size} != 408`);
const missing = [...cat].filter(m => !orbitOf.has(m));
const extra = [...orbitOf.keys()].filter(m => !cat.has(m));
if (missing.length || extra.length) fail(`catalog/orbit set mismatch: ${missing.length} missing, ${extra.length} extra`);

// --- 4) witness 照合 ---
const lookup = witnesses.map(w => {
  const m = maskOf(w.stones);
  const imgs = d4Masks(w.stones);
  const direct = cat.has(m.toString());
  const imagesInCatalog = imgs.filter(x => cat.has(x));
  const orbits = [...new Set(imgs.map(x => orbitOf.get(x)).filter(v => v !== undefined))];
  if (orbits.length > 1) fail(`${w.file}: witness images span multiple orbits ${orbits}`);
  const oi = orbits[0];
  const rep = oi !== undefined ? reps[oi] : null;
  return {
    file: w.file,
    derived_from: w.derived_from,
    stones: w.stones,
    mask: m.toString(),
    direct_member_of_catalog: direct,
    d4_image_masks_in_catalog: imagesInCatalog.length,
    d4_image_masks: imgs,
    round10_orbit_index: oi,
    round10_orbit_rep_mask: rep ? rep.mask : null,
    round10_orbit_rep_stones: rep ? rep.stones : null,
    witness_equals_orbit_rep_stones: rep ? JSON.stringify(rep.stones) === JSON.stringify(w.stones) : null,
    essential_curve_count: rep ? rep.essential_curve_count : null,
  };
});
if (lookup.some(l => !l.direct_member_of_catalog || l.d4_image_masks_in_catalog !== 8 || l.round10_orbit_index === undefined))
  fail('some witness not fully identified in catalog');
if (lookup[0].round10_orbit_index === lookup[1].round10_orbit_index)
  fail('the two witnesses fall in the same orbit (expected distinct per classification.json)');
// 陰性対照: witness を1石動かした非極大配置はカタログに入らない（大量の偽陽性があれば照合は区別力を持たない）
const moved = w0 => { // wit の1石を (0,0) に動かした対照
  const s = JSON.parse(JSON.stringify(w0.stones)); const [x0, y0] = s[0]; s[0] = [y0, x0 === 0 ? 1 : 0]; return maskOf(s).toString(); };
const negCtl = lookup.map(l => ({ witness: l.file, tampered_mask: moved({ stones: l.stones }), in_catalog: cat.has(moved({ stones: l.stones })) }));
if (negCtl.some(c => c.in_catalog)) fail('negative control unexpectedly in catalog');

// --- 出力 ---
const out = {
  generated: new Date().toISOString(),
  lane: 's12-s13-sat-stabilization-20261122 addendum: n=8 witness K0032 catalogue lookup',
  convention: { board: '8x8', cell: '[x,y]', bit: 'p = x + 8*y, mask bit p', masks_stored_as: 'decimal strings (values exceed 2^53; JSON double would corrupt them)' },
  catalog_recovery: {
    from: 'published text artifacts only (binary round4_b371.bin not read)',
    round46_probe: { embeddings: 1632, distinct_source_masks: cat.size, per_mask_offsets: ['[0,0]', '[0,1]', '[1,0]', '[1,1]'] },
    round10_orbits: { representatives: 51, rep_mask_rederivation_from_stones: 'ALL 51 EXACT MATCH (BigInt vs text)', source_sha256_of_b371_bin_claim: summary.round10_source_sha256_claim },
    cross_check: '51 reps x 8 board-D4 images = 408 distinct, disjoint, set-equal to round46 distinct source masks',
  },
  input_sha256: summary.input_sha256,
  witnesses: lookup,
  negative_controls: negCtl,
  notes: [
    'Catalog completeness (408 = all maximal safe 8-stone sets on 8x8) is K0032 established debt; this lookup identifies WHICH member each witness is, and does not re-prove completeness.',
    'Both witnesses are 3-way verified maximal-safe per the s12-s13 README; membership is logically implied once the K0032 enumeration is trusted.',
    's_8 = 8 unaffected. essential_curve_count values are per-set features from round10 (histogram over 408 sets: 13:8,14:8,15:48,16:32,17:32,18:96,19:40,20:56,21:24,22:24,23:24,24:8,27:8).',
  ],
};
const outPath = P('research/experiments/s12-s13-sat-stabilization-20261122/output/n8_k0032_lookup.json');
writeFileSync(outPath, JSON.stringify(out, null, 2) + '\n');
console.log('ALL CHECKS PASS');
for (const l of lookup) console.log(`${l.file}: mask=${l.mask} orbit=${l.round10_orbit_index} rep=${l.round10_orbit_rep_mask} rep_stones_equal=${l.witness_equals_orbit_rep_stones} ecc=${l.essential_curve_count}`);
console.log('wrote', outPath);
