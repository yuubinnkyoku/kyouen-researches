#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconstruct harness master/ from the published repository bytes at the pinned
commit (pin-manifest.json), either via raw.githubusercontent.com (default) or
from a local git clone (--clone PATH).

Fetches the 61 published files of the three K1136/K1137/K1139 certificate
extraction experiment dirs into master/<repo layout>. The verification
harness then checks each fetched file against the pinned git blob SHA and
size (fail-closed), so transport errors cannot pass unnoticed.

stdlib only.
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = json.load(open(os.path.join(HERE, "pin-manifest.json"), "r", encoding="utf-8"))
PIN_COMMIT = MANIFEST["pin_commit"]
REPO = MANIFEST["repo"]


def write_at(master, repo_path, data):
    p = os.path.join(master, repo_path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", default=os.path.join(HERE, "master"))
    ap.add_argument("--clone", default=None,
                    help="path to a git clone; reads blobs via 'git cat-file' at the pinned blobs")
    ap.add_argument("--force", action="store_true", help="overwrite existing master/")
    args = ap.parse_args()
    if os.path.exists(args.master):
        if args.force:
            shutil.rmtree(args.master)
        else:
            print("master/ already exists; use --force to replace")
            return 0
    n = 0
    for repo_path, meta in MANIFEST["files"].items():
        if args.clone:
            blob = subprocess.run(
                ["git", "-C", args.clone, "cat-file", "blob", meta["sha"]],
                stdout=subprocess.PIPE, check=False)
            data = blob.stdout
        else:
            url = "https://raw.githubusercontent.com/%s/%s/%s" % (REPO, PIN_COMMIT, repo_path)
            with urllib.request.urlopen(url, timeout=120) as r:
                data = r.read()
        if len(data) != meta["size"]:
            print("SIZE MISMATCH", repo_path, len(data), meta["size"])
            return 1
        got = hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()
        if got != meta["sha"]:
            print("GIT BLOB MISMATCH", repo_path, got, meta["sha"])
            return 1
        write_at(args.master, repo_path, data)
        n += 1
    print(json.dumps({"fetched": n, "pin_commit": PIN_COMMIT, "all_blob_pins_ok": True}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
