// audit_chain_integrity.ts -- Part DD (2026-11-24): read-only independent integrity audit
// of the published n11 central-reply canonical S5 chain waypoints CH(6,294) -> CO(6,301,
// 854800f3...) -> CU(6,317, 30ddad9d...) via the GitHub contents API, executed inside the
// Vibe sandboxed TypeScript environment (no Python, no native host, no solver reruns).
// This file is the executed program body with this header comment added; executable code
// is unchanged. Re-run: a sandboxed TS runtime with tools.github_app.get_file_contents
// (read-only) against yuubinnkyoku/kyouen-researches main.
async function main() {
  // ---------- pure-TS crypto ----------
  function utf8Bytes(s: string): Uint8Array {
    const bytes: number[] = [];
    for (let i = 0; i < s.length; i++) {
      const c = s.charCodeAt(i);
      if (c < 0x80) bytes.push(c);
      else if (c < 0x800) bytes.push(0xc0 | (c >> 6), 0x80 | (c & 63));
      else bytes.push(0xe0 | (c >> 12), 0x80 | ((c >> 6) & 63), 0x80 | (c & 63));
    }
    return new Uint8Array(bytes);
  }
  const K256 = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
  function sha256Bytes(bytes: Uint8Array): string {
    const H = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
    const ml = bytes.length, bitLen = ml * 8;
    const padded = new Uint8Array(((ml + 9 + 63) >> 6) << 6);
    padded.set(bytes); padded[ml] = 0x80;
    const dv = padded.length - 8;
    const hi = Math.floor(bitLen / 4294967296), lo32 = bitLen >>> 0;
    padded[dv]=(hi>>>24)&255;padded[dv+1]=(hi>>>16)&255;padded[dv+2]=(hi>>>8)&255;padded[dv+3]=hi&255;
    padded[dv+4]=(lo32>>>24)&255;padded[dv+5]=(lo32>>>16)&255;padded[dv+6]=(lo32>>>8)&255;padded[dv+7]=lo32&255;
    const W = new Array(64);
    for (let off = 0; off < padded.length; off += 64) {
      for (let t = 0; t < 16; t++) { const i=off+t*4; W[t]=((padded[i]<<24)|(padded[i+1]<<16)|(padded[i+2]<<8)|padded[i+3])>>>0; }
      for (let t = 16; t < 64; t++) {
        const w15=W[t-15], s0=((w15>>>7)|(w15<<25))^((w15>>>18)|(w15<<14))^(w15>>>3);
        const w2=W[t-2], s1=((w2>>>17)|(w2<<15))^((w2>>>19)|(w2<<13))^(w2>>>10);
        W[t]=(W[t-16]+s0+W[t-7]+s1)>>>0;
      }
      let a=H[0],b=H[1],c=H[2],d=H[3],e=H[4],f=H[5],g=H[6],h=H[7];
      for (let t = 0; t < 64; t++) {
        const S1=((e>>>6)|(e<<26))^((e>>>11)|(e<<21))^((e>>>25)|(e<<7));
        const ch=(e&f)^(~e&g);
        const t1=(h+S1+ch+K256[t]+W[t])>>>0;
        const S0=((a>>>2)|(a<<30))^((a>>>13)|(a<<19))^((a>>>22)|(a<<10));
        const maj=(a&b)^(a&c)^(b&c);
        const t2=(S0+maj)>>>0;
        h=g;g=f;f=e;e=(d+t1)>>>0;d=c;c=b;b=a;a=(t1+t2)>>>0;
      }
      H[0]=(H[0]+a)>>>0;H[1]=(H[1]+b)>>>0;H[2]=(H[2]+c)>>>0;H[3]=(H[3]+d)>>>0;
      H[4]=(H[4]+e)>>>0;H[5]=(H[5]+f)>>>0;H[6]=(H[6]+g)>>>0;H[7]=(H[7]+h)>>>0;
    }
    return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("");
  }
  const sha256 = (s: string) => sha256Bytes(utf8Bytes(s));
  function sha1(s: string): string {
    const bytes = utf8Bytes(s), ml = bytes.length;
    const padded = new Uint8Array(((ml + 9 + 63) >> 6) << 6);
    padded.set(bytes); padded[ml] = 0x80;
    const dv = padded.length - 4, bitLen = ml * 8;
    padded[dv]=(bitLen>>>24)&255;padded[dv+1]=(bitLen>>>16)&255;padded[dv+2]=(bitLen>>>8)&255;padded[dv+3]=bitLen&255;
    let h0=0x67452301,h1=0xefcdab89,h2=0x98badcfe,h3=0x10325476,h4=0xc3d2e1f0;
    const w = new Array(80);
    for (let off = 0; off < padded.length; off += 64) {
      for (let t = 0; t < 16; t++) { const i=off+t*4; w[t]=((padded[i]<<24)|(padded[i+1]<<16)|(padded[i+2]<<8)|padded[i+3])>>>0; }
      for (let t = 16; t < 80; t++) { const v=w[t-3]^w[t-8]^w[t-14]^w[t-16]; w[t]=((v<<1)|(v>>>31))>>>0; }
      let a=h0,b=h1,c=h2,d=h3,e=h4;
      for (let t = 0; t < 80; t++) {
        let f: number, k: number;
        if (t<20){f=(b&c)|((~b)&d);k=0x5a827999>>>0;}
        else if(t<40){f=b^c^d;k=0x6ed9eba1>>>0;}
        else if(t<60){f=(b&c)|(b&d)|(c&d);k=0x8f1bbcdc>>>0;}
        else {f=b^c^d;k=0xca62c1d6>>>0;}
        const tmp=((((a<<5)|(a>>>27))>>>0)+(f+k+w[t]+e))>>>0;
        e=d;d=c;c=((b<<30)|(b>>>2))>>>0;b=a;a=tmp;
      }
      h0=(h0+a)>>>0;h1=(h1+b)>>>0;h2=(h2+c)>>>0;h3=(h3+d)>>>0;h4=(h4+e)>>>0;
    }
    return [h0,h1,h2,h3,h4].map(x=>(x>>>0).toString(16).padStart(8,"0")).join("");
  }
  const gitBlobSha1 = (s: string) => sha1("blob " + utf8Bytes(s).length + "\0" + s);

  const REPO = { owner: "yuubinnkyoku", repo: "kyouen-researches" };
  async function listDir(path: string) {
    const r = await tools.github_app.get_file_contents({ ...REPO, path, fields: ["name", "size", "type"] }) as any;
    return r as any[];
  }
  const fetched: Record<string, string> = {};
  const fetchLog: any[] = [];
  const errors: string[] = [];
  async function get(path: string, optional = false) {
    try {
      const r = await tools.github_app.get_file_contents({ ...REPO, path }) as any;
      const arr = Array.isArray(r) ? r : [r];
      const shaMatch = arr[0]?.text?.match(/SHA: ([0-9a-f]{40})/);
      const txt = arr[1]?.resource?.text ?? "";
      fetched[path] = txt;
      fetchLog.push({
        path, len: utf8Bytes(txt).length, chars: txt.length,
        gitBlobReported: shaMatch ? shaMatch[1] : null,
        gitBlobRecomputed: gitBlobSha1(txt),
        blobChannelMatch: shaMatch ? (gitBlobSha1(txt) === shaMatch[1]) : null,
        asciiOnly: /^[\x00-\x7f]*$/.test(txt),
        sha256: sha256(txt),
      });
      return txt;
    } catch (e: any) { errors.push(path + " :: " + e.message); if (!optional) throw e; return ""; }
  }
  const CH = "research/experiments/n11-centralreply-class5343-loss1-adoption-reaudit-20261123";
  const CO = "research/experiments/n11-centralreply-class5343-loss7-adoption-reaudit-20261123";
  const CU = "research/experiments/n11-centralreply-class2251-loss16-adoption-reaudit-20261123";
  // resolve cache file names from dir listings (no hand transcription)
  const chOut = await listDir(CH + "/output");
  const coOut = await listDir(CO + "/output");
  const cuOut = await listDir(CU + "/output");
  const pick = (d: any[]) => d.filter(x => x.name.startsWith("merged-exact-s5-chain") && x.name.endsWith(".cache")).map(x => x.name);
  const chCacheRel = pick(chOut), coCacheRel = pick(coOut), cuCacheRel = pick(cuOut);
  if (chCacheRel.length !== 1 || coCacheRel.length !== 1 || cuCacheRel.length !== 1) return { error: "cache name resolution failed", chCacheRel, coCacheRel, cuCacheRel, errors };
  const incNameOf = (d: any[]) => d.find(x => x.name.startsWith("increment-") && x.name.endsWith(".cache")).name;
  const manNameOf = (d: any[]) => d.find(x => x.name === "increments-manifest.json").name;

  const chCachePath = CH + "/output/" + chCacheRel[0];
  const coCachePath = CO + "/output/" + coCacheRel[0];
  const cuCachePath = CU + "/output/" + cuCacheRel[0];
  const chIncPath = CH + "/output/" + incNameOf(chOut);
  const coIncPath = CO + "/output/" + incNameOf(coOut);
  const cuIncPath = CU + "/output/" + incNameOf(cuOut);
  await get(chCachePath); await get(chIncPath);
  const chIncMan = JSON.parse(await get(CH + "/output/" + manNameOf(chOut)));
  await get(coCachePath); await get(coIncPath);
  const coIncMan = JSON.parse(await get(CO + "/output/" + manNameOf(coOut)));
  await get(cuCachePath); await get(cuIncPath);
  const cuIncMan = JSON.parse(await get(CU + "/output/" + manNameOf(cuOut)));
  const quarantine = JSON.parse(await get("results/n11-s5-evidence-quarantine.json"));

  function parseCache(txt: string, label: string) {
    const map = new Map<string, { verdict: number, nodes: string }>();
    const verdictCount: Record<string, number> = { "1": 0, "2": 0 };
    let rows = 0, badRows = 0;
    const conflicts: any[] = [];
    for (const raw of txt.split("\n")) {
      const line = raw.trim();
      if (!line || line.startsWith("#")) continue;
      const f = line.split(",");
      if (f.length !== 6 || f[0] !== "s5verdict" || f[3] !== "5" || (f[4] !== "1" && f[4] !== "2") || !/^\d+$/.test(f[5])) { badRows++; continue; }
      const key = f[1] + ":" + f[2];
      const row = { verdict: Number(f[4]), nodes: f[5] };
      const prev = map.get(key);
      if (prev && (prev.verdict !== row.verdict || prev.nodes !== row.nodes)) conflicts.push({ key, prev, row });
      map.set(key, row);
      verdictCount[f[4]]++; rows++;
    }
    return { label, map, rows, distinct: map.size, badRows, verdictCount, conflicts };
  }
  const chP = parseCache(fetched[chCachePath], "CH_6294");
  const coP = parseCache(fetched[coCachePath], "CO_6301");
  const cuP = parseCache(fetched[cuCachePath], "CU_6317");
  const incL1 = parseCache(fetched[chIncPath], "inc_b28loss1");
  const incL7 = parseCache(fetched[coIncPath], "inc_b28loss7");
  const incL16 = parseCache(fetched[cuIncPath], "inc_b29loss16");

  function chainCheck(from: any, to: any, incr: any) {
    const subsetMismatch: any[] = [];
    const deltaKeys: string[] = [];
    for (const [k, v] of to.map) {
      const f = from.map.get(k);
      if (f) { if (f.verdict !== v.verdict || f.nodes !== v.nodes) subsetMismatch.push({ key: k }); }
      else deltaKeys.push(k);
    }
    const missingInTo: string[] = [];
    for (const [k] of from.map) if (!to.map.has(k)) missingInTo.push(k);
    const incKeys = [...incr.map.keys()];
    let absorbHits = 0;
    for (const k of incKeys) if (from.map.has(k)) absorbHits++;
    const deltaSet = new Set(deltaKeys), incSet = new Set(incKeys);
    const deltaEqualsInc = deltaKeys.length === incKeys.length && incKeys.every(k => deltaSet.has(k)) && deltaKeys.every(k => incSet.has(k));
    let rowMismatch = 0;
    for (const k of incKeys) {
      const inTo = to.map.get(k), inInc = incr.map.get(k);
      if (!inTo || inTo.verdict !== inInc.verdict || inTo.nodes !== inInc.nodes) rowMismatch++;
    }
    let nodesSum = 0n;
    for (const k of incKeys) nodesSum += BigInt(incr.map.get(k)!.nodes);
    return {
      from: from.label, to: to.label, fromRows: from.rows, toRows: to.rows, rowDelta: to.rows - from.rows,
      subsetBad: subsetMismatch.length, keysMissingInTo: missingInTo.length,
      deltaKeyCount: deltaKeys.length, incrementKeyCount: incKeys.length,
      deltaEqualsIncrementKeys: deltaEqualsInc, incrementKeysAlreadyInBase: absorbHits,
      incrementRowMismatchInTo: rowMismatch, incrementNodesSum: nodesSum.toString(),
      sampleDeltaKeys: deltaKeys.slice(0, 3),
    };
  }
  const chToCo = chainCheck(chP, coP, incL7);
  const coToCu = chainCheck(coP, cuP, incL16);
  let l1InCh = true;
  const l1Detail: any[] = [];
  for (const [k, v] of incL1.map) { const inCh = chP.map.get(k); if (!inCh || inCh.verdict !== v.verdict || inCh.nodes !== v.nodes) { l1InCh = false; l1Detail.push({ k }); } }

  const qKeys = (quarantine.entries as any[]).filter(e => e.active).map(e => e.key.join(":"));
  const qHits: any = { ch: [], co: [], cu: [] };
  for (const k of qKeys) { if (chP.map.has(k)) qHits.ch.push(k); if (coP.map.has(k)) qHits.co.push(k); if (cuP.map.has(k)) qHits.cu.push(k); }

  const fileSha = (p: string) => fetchLog.find(f => f.path === p)?.sha256;
  const pins: any = {
    chCache_vs_chManifest_3124461b: fileSha(chCachePath) === "3124461b14e4f73a7248cbf5b96c7ff59ebfdcc05258adeb9c81791d86cc461e",
    chCache_vs_coManifest_base_cache_sha256: fileSha(chCachePath) === (coIncMan.base_cache_sha256 ?? "ABSENT"),
    coCache_854800f3: fileSha(coCachePath) === "854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d",
    coCache_vs_cuManifest_base_854800f3: fileSha(coCachePath) === cuIncMan.base_cache_sha256,
    cuCache_30ddad9d: fileSha(cuCachePath) === "30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4",
    cuInc_vs_cuManifest_bab011e3: fileSha(cuIncPath) === "bab011e376090f9f4732d63f0084f326ba72dada5cf699d5aabc7e014c29ae24",
    cuInc_vs_cuManifestJsonLoss: fileSha(cuIncPath) === cuIncMan.sha256.loss,
    coInc_bd5ef7d7: fileSha(coIncPath) === "bd5ef7d7632816006bd5a74349bf703a8dd3251e3a550a33e7ae7a0253abe382",
    coInc_vs_coManifestJsonLoss: coIncMan.sha256 && coIncMan.sha256.loss ? fileSha(coIncPath) === coIncMan.sha256.loss : null,
    chInc_dc857bfd: fileSha(chIncPath) === "dc857bfd2ecd00deaea3dbe214e0eec0e5b9d7704104a8721d046f262f170487",
    merger_pin_90711961_shared: cuIncMan.merger_sha256 === "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a",
  };
  const cm = coIncMan.batches ? coIncMan.batches[0] : {};
  const nodesChecks = {
    b28loss7_sum: chToCo.incrementNodesSum,
    b28loss7_manifest_total: String(cm.total_nodes_pass_one ?? "ABSENT"),
    b29loss16_sum: coToCu.incrementNodesSum,
    b29loss16_manifest_total: String(cuIncMan.batches[0].total_nodes_pass_one ?? "ABSENT"),
  };
  const nodesSumsMatch = nodesChecks.b28loss7_sum === nodesChecks.b28loss7_manifest_total
    && nodesChecks.b29loss16_sum === nodesChecks.b29loss16_manifest_total;
  const blobChannelAll = fetchLog.every(f => f.blobChannelMatch === true);
  const asciiAll = fetchLog.every(f => f.asciiOnly === true);

  const countsVsPublished = {
    CO: { observedWin: coP.verdictCount["1"], observedLoss: coP.verdictCount["2"], expected: { win: 158, loss: 6143, rows: 6301 } },
    CU: { observedWin: cuP.verdictCount["1"], observedLoss: cuP.verdictCount["2"], expected: { win: 158, loss: 6159, rows: 6317 } },
  };
  const allPass = Object.values(pins).every(Boolean) && nodesSumsMatch && blobChannelAll && asciiAll
    && chToCo.subsetBad === 0 && chToCo.keysMissingInTo === 0 && chToCo.deltaEqualsIncrementKeys === true && chToCo.incrementRowMismatchInTo === 0 && chToCo.incrementKeysAlreadyInBase === 0
    && coToCu.subsetBad === 0 && coToCu.keysMissingInTo === 0 && coToCu.deltaEqualsIncrementKeys === true && coToCu.incrementRowMismatchInTo === 0 && coToCu.incrementKeysAlreadyInBase === 0
    && l1InCh && qHits.ch.length + qHits.co.length + qHits.cu.length === 0
    && chP.conflicts.length === 0 && coP.conflicts.length === 0 && cuP.conflicts.length === 0
    && chP.badRows === 0 && coP.badRows === 0 && cuP.badRows === 0
    && coP.verdictCount["1"] === 158 && coP.verdictCount["2"] === 6143 && coP.rows === 6301
    && cuP.verdictCount["1"] === 158 && cuP.verdictCount["2"] === 6159 && cuP.rows === 6317;

  const report = {
    schema: "n11-s5-chain-integrity-tsaudit-v1",
    generated: new Date().toISOString(),
    executor_note: "independent non-owner verification: sandboxed TypeScript re-implementation (sha256/sha1 from scratch, FIPS vectors + published-pin agreement), GitHub text channel only, no Python, no native host, no solver reruns. Read-only audit; no verdict consumed. 11x11 stays UNKNOWN.",
    sha_impl_selftest: {
      sha256_empty: sha256("") === "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      sha256_abc: sha256("abc") === "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
      sha256_nist2block_prefix120bit: sha256("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq").slice(0, 30) === "248d6a61d20638b8e5c026930c3e60",
      sha1_abc: sha1("abc") === "a9993e364706816aba3e25717850c26c9cd0d89d",
      sha1_empty: sha1("") === "da39a3ee5e6b4b0d3255bfef95601890afd80709",
      decisive: "tool correctness is settled by 256-bit agreement with three independent published pin sources (MANIFEST-sha256 registers, increments-manifest internal fields, published completion-log pins)",
    },
    files: fetchLog,
    pins,
    counts: {
      CH: { rows: chP.rows, distinct: chP.distinct, verdicts: chP.verdictCount, conflicts: chP.conflicts.length, badRows: chP.badRows },
      CO: { rows: coP.rows, distinct: coP.distinct, verdicts: coP.verdictCount, conflicts: coP.conflicts.length, badRows: coP.badRows },
      CU: { rows: cuP.rows, distinct: cuP.distinct, verdicts: cuP.verdictCount, conflicts: cuP.conflicts.length, badRows: cuP.badRows },
      increments: { l1: incL1.rows, l7: incL7.rows, l16: incL16.rows },
    },
    counts_vs_published: countsVsPublished,
    chain: { chToCo, coToCu },
    b28loss1_increment_inside_CH: l1InCh,
    quarantine: { activeKeys: qKeys, hits: qHits },
    nodesChecks,
    blob_channel: { allMatch: blobChannelAll, asciiOnlyAll: asciiAll },
    errors_during_fetch: errors,
    ALL_GATES: allPass ? "PASS" : "FAIL",
  };
  const reportText = JSON.stringify(report, null, 1);
  let saved: any = null;
  try {
    await (tools as any).file_system.write_file({ path: "/home/user/kr-exec/tsaudit/audit-report.json", content: reportText });
    saved = true;
  } catch (e: any) { saved = "ERR:" + e.message; }
  return { allPass, pins, nodesChecks, chain: report.chain, quarantineHits: qHits, counts: report.counts, countsVsPublished, blobChannelAll, asciiAll, errors, reportLen: reportText.length, saved, sampleFetch: fetchLog[0] };
}
