#!/usr/bin/env python3
import argparse
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REQUIRED = ["会社名", "開催日", "開催時間", "開催場所", "予約方法"]


def validate(data):
    errors = []
    warnings = []
    for key in REQUIRED:
        if not str(data.get(key, "")).strip():
            errors.append(f"必須項目が未入力: {key}")

    method = str(data.get("予約方法", ""))
    if any(word in method for word in ("URL", "Web", "フォーム")):
        if not str(data.get("予約URL", "")).strip():
            errors.append("予約方法にWeb系を指定していますが、予約URLがありません")
    if "電話" in method and not str(data.get("電話番号", "")).strip():
        errors.append("予約方法に電話を指定していますが、電話番号がありません")

    permission = data.get("施主許諾", {}) or {}
    if not permission.get("写真使用", False):
        warnings.append("写真使用の施主許諾が未確認です")

    benefit = data.get("来場特典", {}) or {}
    if str(benefit.get("内容", "")).strip():
        for key in ("対象", "条件", "期限"):
            if not str(benefit.get(key, "")).strip():
                errors.append(f"来場特典の{key}が未入力です")

    if not str(data.get("掲載終了日", "")).strip():
        warnings.append("掲載終了日が未入力です")
    return errors, warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("event")
    args = parser.parse_args()
    with open(args.event, encoding="utf-8") as fh:
        data = json.load(fh)
    errors, warnings = validate(data)
    for message in errors:
        print(f"[FAIL] {message}")
    for message in warnings:
        print(f"[WARN] {message}")
    if not errors and not warnings:
        print("問題なし。")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
