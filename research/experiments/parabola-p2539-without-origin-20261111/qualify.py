"""Bind origin-retaining and origin-free certificates to one four-deletion theorem."""
import argparse
import gzip
import json
from pathlib import Path
from audit import HERE, sha, save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();assert not args.output.exists()
    old=HERE.parent/'parabola-p2539-origin-local-audit-20261111'
    prior=json.loads((old/'qualification.json').read_text());seed='454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb'
    assert prior['seed_sha256']==seed and prior['origin_retained'] and prior['all_three_classes_bound']
    assert prior['excluded_size_at_least']==1259 and prior['max_removed']==4
    assert sha((old/'README.md').read_bytes())==prior['subset_argument_sha256']
    assert sha((old/'qualify.py').read_bytes())==prior['source_sha256']
    assert sha((old/'replay.json').read_bytes())==prior['replay_sha256']
    rep=json.loads((HERE/'replay.json').read_text());assert rep['both_verified'] and rep['seed_sha256']==seed
    assert sha((HERE/'replay.py').read_bytes())==rep['replay_source_sha256']
    rows=[];assert len(rep['cases'])==2 and {r['complete_pairs'] for r in rep['cases']}=={0,1}
    for r in rep['cases']:
        d=HERE/'audit-output'/f"B{r['complete_pairs']}";m=json.loads((d/'manifest.json').read_text())
        assert m['seed_sha256']==seed and m['schema_geometry_rup_lrat_verified']
        assert (m['origin'],m['target_size'],m['total_deletion_bound'],m['nonzero_deletion_bound'])==(0,1259,4,3)
        assert r['schema_verified'] and r['geometry']['returncode']==0
        assert r['rup']['returncode']==0 and 's VERIFIED' in r['rup']['stdout'].splitlines()
        assert sha(gzip.decompress((d/'input.cnf.gz').read_bytes()))==m['input_sha256']==r['input_sha256']
        packed=(d/'verified-proof.drat.gz').read_bytes();assert sha(packed)==m['drat_gzip_sha256']
        assert sha(gzip.decompress(packed))==m['drat_raw_sha256']==r['drat_raw_sha256']
        rows.append(dict(complete_pairs=r['complete_pairs'],manifest_sha256=sha((d/'manifest.json').read_bytes()),input_sha256=r['input_sha256'],proof_sha256=r['drat_raw_sha256']))
    save(args.output,dict(seed_sha256=seed,max_removed=4,excluded_size_at_least=1259,unrestricted_four_deletion_local_optimum=True,
        origin_retaining_qualification_sha256=sha((old/'qualification.json').read_bytes()),origin_free_cases=rows,
        replay_sha256=sha((HERE/'replay.json').read_bytes()),subset_argument_sha256=sha((HERE/'README.md').read_bytes()),
        source_sha256=sha(Path(__file__).read_bytes()),scope='No safe improvement can delete at most4 points from this fixed1258 seed, irrespective of origin or complete pair. Not a global maximum.'))
    print('PASS origin-retaining/free proof binding; unrestricted four-deletion local optimum')


if __name__=='__main__':main()
