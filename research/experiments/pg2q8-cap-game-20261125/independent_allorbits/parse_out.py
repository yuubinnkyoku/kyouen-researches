"""Parser for the key=value output of pg8.exe."""


def read(path):
    recs = []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            toks = ln.split()
            if not toks:
                continue
            d = {}
            for t in toks:
                if "=" in t:
                    k, v = t.split("=", 1)
                    d[k] = v
            d["_tag"] = toks[0].split("=")[0]
            d["_bare"] = [t for t in toks if "=" not in t]
            d["_line"] = ln.rstrip("\n")
            recs.append(d)
    return recs


def by_tag(recs, tag):
    return [d for d in recs if d["_tag"] == tag]
