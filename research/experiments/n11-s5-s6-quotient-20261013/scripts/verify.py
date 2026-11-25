"""Invoke independent C++ checker and compare every row and aggregate."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('census',type=Path)
    parser.add_argument('--binary',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    with (gzip.open(args.census,'rt') if args.census.suffix=='.gz' else args.census.open()) as stream:
        data=json.load(stream)
    root=Path(__file__).resolve().parents[4]
    for path,digest in data['source_sha256'].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest, f'stale source: {path}'
    lines=[' '.join(map(str,[r['s5_index'],*r['mask'],r['legal'],len(r['stabilizer']),r['stabilizer_orbits'],r['canonical_children']])) for r in data['rows']]
    assert len(lines)==data['parents'] and len({r['s5_index'] for r in data['rows']})==len(lines)
    proc=subprocess.run([str(args.binary.resolve())],input='\n'.join(lines)+'\n',text=True,capture_output=True,check=True)
    checked=json.loads(proc.stdout)
    assert checked['passed']
    for key,value in checked.items():
        if key!='passed':
            assert data[key]==value,(key,data[key],value)
    # A changed legal count must be rejected by the independent checker.
    first=lines[0].split(); first[3]=str(int(first[3])+1)
    bad=subprocess.run([str(args.binary.resolve())],input=' '.join(first)+'\n',text=True,capture_output=True)
    assert bad.returncode!=0 and 'mismatch parent=' in bad.stderr
    checked.update(census_sha256=hashlib.sha256(args.census.read_bytes()).hexdigest(),
                   cpp_source_sha256=hashlib.sha256(Path(__file__).with_name('verify.cpp').read_bytes()).hexdigest(),
                   rejection_check='changed legal count rejected',
                   geometry='translated integer 3x3 determinant; no Board or solver imports')
    args.output.write_text(json.dumps(checked,sort_keys=True,indent=2)+'\n')
    print(json.dumps(checked,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
