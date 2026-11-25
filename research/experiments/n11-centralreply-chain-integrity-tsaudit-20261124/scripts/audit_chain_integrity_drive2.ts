// audit_chain_integrity_drive2.ts -- Part DD drive-2 (2026-11-24): extends the drive-1 audit
// by one waypoint: CU (6,317 rows, 30ddad9d...) -> DB (6,354 rows, 04b0a239...), i.e. the
// batch-29 37-LOSS canonical adoption increment-b29loss37-20261124. Same executor class as
// drive-1 (sandboxed TS, GitHub contents API, read-only, sha256/sha1 from scratch, no Python,
// no native host, no solver reruns). This file is the executed drive-2 program body with
// this header comment added; executable code unchanged.
async function main() {
  const REPO = { owner: "yuubinnkyoku", repo: "kyouen-researches" };
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
  function sha256(s: string): string {
    const bytes = utf8Bytes(s), H = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
    const ml = bytes.length;
    const padded = new Uint8Array(((ml + 9 + 63) >> 6) << 6);
    padded.set(bytes); padded[ml] = 0x80;
    const dv = padded.length - 8, bitLen = ml * 8;
    const hi = Math.floor(bitLen / 4294967296), lo = bitLen >>> 0;
    padded[dv]=(hi>>>24)&255;padded[dv+1]=(hi>>>16)&255;padded[dv+2]=(hi>>>8)&255;padded[dv+3]=hi&255;
    padded[dv+4]=(lo>>>24)&255;padded[dv+5]=(lo>>>16)&255;padded[dv+6]=(lo>>>8)&255;padded[dv+7]=lo&255;
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
        const ch=(e&f)^(~e&g), t1=(h+S1+ch+K256[t]+W[t])>>>0;
        const S0=((a>>>2)|(a<<30))^((a>>>13)|(a<<19))^((a>>>22)|(a<<10));
        const maj=(a&b)^(a&c)^(b&c), t2=(S0+maj)>>>0;
        h=g;g=f;f=e;e=(d+t1)>>>0;d=c;c=b;b=a;a=(t1+t2)>>>0;
      }
      H[0]=(H[0]+a)>>>0;H[1]=(H[1]+b)>>>0;H[2]=(H[2]+c)>>>0;H[3]=(H[3]+d)>>>0;
      H[4]=(H[4]+e)>>>0;H[5]=(H[5]+f)>>>0;H[6]=(H[6]+g)>>>0;H[7]=(H[7]+h)>>>0;
    }
    return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("");
  }
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
  async function listDir(path: string) {
    const r = await tools.github_app.get_file_contents({ ...REPO, path, fields: ["name", "size", "type"] }) as any;
    return r as any[];
  }
  const fetched: Record<string, string> = {};
  const fetchLog: any[] = [];
  const errors: string[] = [];
  async function get(path: string) {
    try {
      const r = await tools.github_app.get_file_contents({ ...REPO, path }) as any;
      const arr = Array.isArray(r) ? r : [r];
      const shaMatch = arr[0]?.text?.match(/SHA: ([0-9a-f]{40})/);
      const txt = arr[1]?.resource?.text ?? "";
      fetched[path] = txt;
      fetchLog.push({
        path, len: utf8Bytes(txt).length,
        gitBlobReported: shaMatch ? shaMatch[1] : null,
        blobChannelMatch: shaMatch ? (gitBlobSha1(txt) === shaMatch[1]) : null,
        asciiOnly: /^[\x00-\x7f]*$/.test(txt),
        sha256: sha256(txt),
      });
      return txt;
    } catch (e: any) { errors.push(path + " :: " + e.message); throw e; }
  }
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
    const deltaAllLoss = deltaKeys.every(k => to.map.get(k)!.verdict === 2);
    return {
      from: from.label, to: to.label, fromRows: from.rows, toRows: to.rows, rowDelta: to.rows - from.rows,
      subsetBad: subsetMismatch.length, keysMissingInTo: missingInTo.length,
      deltaKeyCount: deltaKeys.length, incrementKeyCount: incKeys.length,
      deltaEqualsIncrementKeys: deltaEqualsInc, incrementKeysAlreadyInBase: absorbHits,
      incrementRowMismatchInTo: rowMismatch, incrementNodesSum: nodesSum.toString(),
      deltaAllLoss,
      sampleDeltaKeys: deltaKeys.slice(0, 3),
    };
  }

  // claim check: drive-1 files intact, no other chain-integrity driver
  const commits = await tools.github_app.list_commits({ ...REPO, perPage: 8, fields: ["sha", "commit"] }) as any[];
  const headNow = commits[0].sha.slice(0, 8);
  const msgs = commits.map(c => (c.commit?.message || "").split("\n")[0]);
  const claimConflict = msgs.filter(m => /chain-integrity|Part DD|Part DC/i.test(m));
  if (claimConflict.some(m => !/Part DD|part-dd-chain-integrity/i.test(m))) {
    return { aborted: "another driver touched chain-integrity lane", msgs, headNow };
  }

  const CU = "research/experiments/n11-centralreply-class2251-loss16-adoption-reaudit-20261123";
  const DB = "research/experiments/n11-centralreply-class2251-loss37-adoption-reaudit-20261124";
  const cuOut = await listDir(CU + "/output");
  const dbOut = await listDir(DB + "/output");
  const pick = (d: any[]) => d.filter(x => x.name.startsWith("merged-exact-s5-chain") && x.name.endsWith(".cache")).map(x => x.name);
  const incs = (d: any[]) => d.filter(x => x.name.startsWith("increment-") && x.name.endsWith(".cache")).map(x => x.name);
  const cuCacheRel = pick(cuOut), dbCacheRel = pick(dbOut), dbIncRel = incs(dbOut);
  if (cuCacheRel.length !== 1 || dbCacheRel.length !== 1 || dbIncRel.length !== 1) {
    return { aborted: "name resolution failed", cuCacheRel, dbCacheRel, dbIncRel, errors };
  }
  const cuCachePath = CU + "/output/" + cuCacheRel[0];
  const dbCachePath = DB + "/output/" + dbCacheRel[0];
  const dbIncPath = DB + "/output/" + dbIncRel[0];
  await get(cuCachePath);
  await get(dbCachePath);
  await get(dbIncPath);
  const dbIncMan = JSON.parse(await get(DB + "/output/increments-manifest.json"));
  const dbManifest = await get(DB + "/MANIFEST-sha256.txt");
  const quarantine = JSON.parse(await get("results/n11-s5-evidence-quarantine.json"));

  const cuP = parseCache(fetched[cuCachePath], "CU_6317");
  const dbP = parseCache(fetched[dbCachePath], "DB_6354");
  const inc37 = parseCache(fetched[dbIncPath], "inc_b29loss37");
  const cuToDb = chainCheck(cuP, dbP, inc37);

  const qKeys = (quarantine.entries as any[]).filter(e => e.active).map(e => e.key.join(":"));
  const qHits = qKeys.filter(k => dbP.map.has(k));

  const fileSha = (p: string) => fetchLog.find(f => f.path === p)?.sha256;
  // parse DB MANIFEST-sha256.txt: "<sha>  <path>"
  const dbManMap: Record<string, string> = {};
  for (const line of dbManifest.split("\n")) {
    const m = line.trim().match(/^([0-9a-f]{64})\s+(\S+)$/);
    if (m) dbManMap[m[2].split("/").pop()!] = m[1];
  }
  const pins: any = {
    cuCache_30ddad9d_equalToDrive1: fileSha(cuCachePath) === "30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4",
    dbCache_vs_dbManifest: fileSha(dbCachePath) === (dbManMap[dbCacheRel[0]] ?? "ABSENT"),
    dbCache_prefix_04b0a239_fromKnowledge: (fileSha(dbCachePath) ?? "").startsWith("04b0a239"),
    dbManifest_vs_dbIncMan_base_cu30ddad9d: dbIncMan.base_cache_sha256 === "30ddad9dc0add7e21698e864b5c202b8e864".slice(0, 20) ? null : dbIncMan.base_cache_sha256 === "30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4",
    dbInc_sha_paths: (() => { const ex = fetched[dbIncPath]; return dbIncMan.sha256 && dbIncMan.sha256.loss ? fileSha(dbIncPath) === dbIncMan.sha256.loss : null; })(),
    merger_pin_90711961: dbIncMan.merger_sha256 === "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a",
  };
  const nm = dbIncMan.batches ? (Array.isArray(dbIncMan.batches) ? dbIncMan.batches[0] : dbIncMan.batches) : {};
  const nodesChecks = {
    b29loss37_sum: cuToDb.incrementNodesSum,
    manifest_total_nodes: String(nm.total_nodes_pass_one ?? nm.total_nodes ?? "ABSENT"),
    batch_desc: nm.description ?? nm.batch ?? nm.label ?? null,
  };
  const nodesSumsMatch = nodesChecks.b29loss37_sum === nodesChecks.manifest_total_nodes && nodesChecks.b29loss37_sum === "159325566";
  const blobChannelAll = fetchLog.every(f => f.blobChannelMatch === true);
  const asciiAll = fetchLog.every(f => f.asciiOnly === true);
  const countsVsPublished = {
    DB: { observedWin: dbP.verdictCount["1"], observedLoss: dbP.verdictCount["2"], expected: { win: 158, loss: 6196, rows: 6354 } },
  };
  const allPass = blobChannelAll && asciiAll
    && cuToDb.subsetBad === 0 && cuToDb.keysMissingInTo === 0 && cuToDb.deltaEqualsIncrementKeys === true
    && cuToDb.incrementRowMismatchInTo === 0 && cuToDb.incrementKeysAlreadyInBase === 0 && cuToDb.deltaAllLoss === true
    && dbP.conflicts.length === 0 && dbP.badRows === 0
    && dbP.verdictCount["1"] === 158 && dbP.verdictCount["2"] === 6196 && dbP.rows === 6354
    && qHits.length === 0
    && pins.cuCache_30ddad9d_equalToDrive1 === true
    && pins.dbCache_vs_dbManifest === true
    && pins.dbCache_prefix_04b0a239_fromKnowledge === true
    && pins.dbManifest_vs_dbIncMan_base_cu30ddad9d === true
    && (pins.dbInc_sha_paths === true || pins.dbInc_sha_paths === null)
    && pins.merger_pin_90711961 === true
    && nodesSumsMatch;

  const report = {
    schema: "n11-s5-chain-integrity-tsaudit-drive2-v1",
    generated: new Date().toISOString(),
    executor_note: "Part DD drive-2: extends the drive-1 independent TS chain audit (CH->CO->CU, commit 048b69c5) by one waypoint, CU -> DB, after the Part DB batch-29 37-LOSS adoption landed (2026-11-24). Read-only; no Python, no native host, no solver reruns, no verdict consumed. 11x11 stays UNKNOWN.",
    head_observed: headNow,
    files: fetchLog,
    pins,
    counts: {
      CU: { rows: cuP.rows, verdicts: cuP.verdictCount, conflicts: cuP.conflicts.length, badRows: cuP.badRows },
      DB: { rows: dbP.rows, distinct: dbP.distinct, verdicts: dbP.verdictCount, conflicts: dbP.conflicts.length, badRows: dbP.badRows },
      increment37: { rows: inc37.rows, verdicts: inc37.verdictCount },
    },
    counts_vs_published: countsVsPublished,
    chain: { cuToDb },
    quarantine: { activeKeys: qKeys, hitsInDb: qHits },
    nodesChecks,
    blob_channel: { allMatch: blobChannelAll, asciiOnlyAll: asciiAll },
    errors_during_fetch: errors,
    ALL_GATES: allPass ? "PASS" : "FAIL",
  };
  const reportText = JSON.stringify(report, null, 1);
  await (tools as any).file_system.write_file({ path: "/home/user/kr-exec/tsaudit/audit-report-drive2.json", content: reportText });
  return { allPass, headNow, pins, nodesChecks, cuToDb, counts: report.counts, qHits, blobChannelAll, asciiAll, errors, reportLen: reportText.length, claimConflictCount: claimConflict.length };
}
