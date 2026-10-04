from common import ROOT, checked, solution_table, update_readme, views


def main():
    items, errors, warnings = checked()
    if errors:
        raise SystemExit("\n".join(errors))
    # Validate README delimiters before writing any generated file.
    readme = ROOT / "README.md"
    raw = readme.read_bytes()
    text = raw.decode("utf-8")
    block = "## 解決状況\n\n"
    block += "現在の研究結果と未解決問題は [research/knowledge/](research/knowledge/README.md) に整理しています。各結果には参照用の `K0001` のような番号を付けています。以下は、そのうち盤面の解決状況に関する結果を自動生成した一覧です。\n\n"
    block += solution_table(items, ".")
    updated = update_readme(text, block)
    generated = ROOT / "research/knowledge/generated"
    generated.mkdir(parents=True, exist_ok=True)
    for name, content in views(items, warnings).items():
        path = generated / name
        data = content.encode("utf-8")
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
    if updated.encode("utf-8") != raw:
        readme.write_bytes(updated.encode("utf-8"))
    print(f"generated 6 views and README solution status from {len(items)} items")


if __name__ == "__main__":
    main()
