from common import checked


def main():
    items, errors, warnings = checked()
    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}")
    print(f"{len(items)} items; {len(errors)} errors; {len(warnings)} warnings")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
