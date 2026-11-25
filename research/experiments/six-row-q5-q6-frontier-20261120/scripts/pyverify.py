import json, subprocess, sys
w, m, q, file = sys.argv[1:5]
stones = json.load(open(file))
p = subprocess.run([sys.executable, '/home/user/kr65/scripts/verify_witness.py', w, m, q],
                   input=json.dumps(stones), capture_output=True, text=True)
try:
    out = json.loads(p.stdout.strip().splitlines()[-1])
except Exception:
    print(p.stdout, p.stderr); sys.exit(3)
print(json.dumps(out))
sys.exit(0 if out.get('ok') else 1)
