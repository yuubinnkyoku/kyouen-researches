#!/usr/bin/env python3
"""Generate id/H/V/HV mirror images of a seed witness, bbox-normalized.

Usage: gen_images.py <seed.json> <prefix>   -> writes <prefix>_{id,H,V,HV}.json
"""
import json, sys

seed = json.load(open(sys.argv[1]))
prefix = sys.argv[2]

def norm(st):
    xs = [p[0] for p in st]; ys = [p[1] for p in st]
    x0, y0 = min(xs), min(ys)
    return sorted([[x - x0, y - y0] for x, y in st])

imgs = {
    "id": norm(seed),
    "H": norm([[x, -y] for x, y in seed]),      # flip y
    "V": norm([[-x, y] for x, y in seed]),      # flip x
    "HV": norm([[-x, -y] for x, y in seed]),    # flip both (180 rot)
}
for k, v in imgs.items():
    with open(f"{prefix}_{k}.json", "w") as f:
        json.dump(v, f, separators=(",", ":"))
    print(k, "span_x", max(p[0] for p in v), "n", len(v))
