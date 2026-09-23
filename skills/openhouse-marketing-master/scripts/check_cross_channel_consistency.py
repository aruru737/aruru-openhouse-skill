#!/usr/bin/env python3
import argparse
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CHECK_FIELDS = ["会社名", "開催日", "開催時間", "開催場所"]


def check(event, documents):
    rows = []
    for path, text in documents:
        for field in CHECK_FIELDS:
            value = str(event.get(field, "")).strip()
            if value and value not in text:
                rows.append((path, field, value))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("event")
    parser.add_argument("documents", nargs="+")
    args = parser.parse_args()
    with open(args.event, encoding="utf-8") as fh:
        event = json.load(fh)
    documents = []
    for path in args.documents:
        with open(path, encoding="utf-8") as fh:
            documents.append((path, fh.read()))
    rows = check(event, documents)
    for path, field, value in rows:
        print(f"[FAIL] {path}: {field}『{value}』が見つかりません")
    if not rows:
        print("媒体間の基本情報は一致しています。")
    return 1 if rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
