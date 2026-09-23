#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""完成見学会の告知原稿を検査する。

    python scripts/lint_output.py 原稿.txt
    python scripts/lint_output.py 原稿.txt --event event.json
    cat 原稿.txt | python scripts/lint_output.py -

FAIL が1件でもあれば出さない。WARN は目で見て判断する。
判定の根拠は references/legal-housing.md にある。

--event に 0番で入力した開催情報のJSONを渡すと、
入力していない日付・電話番号・URLが原稿に出ていないか（＝創作していないか）も見る。

    {"開催日": "11月8日(土)〜9日(日)", "開催時間": "10:00〜17:00",
     "開催場所": "熊本市南区", "予約方法": "LINE・電話",
     "電話番号": "096-000-0000", "予約URL": "https://example.com/reserve",
     "会社名": "○○工務店"}
"""
import argparse
import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---- 検査の定義 -------------------------------------------------------------

# 1. 使ってはいけない言葉（特定用語の使用基準）
NG_WORDS = [
    ("完全", "完全性を意味する語。『予約制』などに言い換える"),
    ("完ぺき", "完全性を意味する語"),
    ("完璧", "完全性を意味する語"),
    ("絶対", "完全性を意味する語"),
    ("万全", "完全性を意味する語"),
    ("日本一", "最上級。客観的な出典が無ければ使わない"),
    ("業界一", "最上級。客観的な出典が無ければ使わない"),
    ("地域一番", "最上級。客観的な出典が無ければ使わない"),
    ("No.1", "最上級。客観的な出典が無ければ使わない"),
    ("NO.1", "最上級。客観的な出典が無ければ使わない"),
    ("ナンバーワン", "最上級。客観的な出典が無ければ使わない"),
    ("最高級", "最上級。客観的な出典が無ければ使わない"),
    ("最安", "有利さを意味する語。根拠が要る"),
    ("激安", "有利さを意味する語。根拠が要る"),
    ("格安", "有利さを意味する語。根拠が要る"),
    ("破格", "有利さを意味する語。根拠が要る"),
    ("掘り出し物", "有利さを意味する語。根拠が要る"),
    ("特選", "優良性を意味する語。選定の基準が要る"),
    ("厳選", "優良性を意味する語。選定の基準が要る"),
]
# 「最高」は「最高級」と重複するため単独で後から見る（「最高気温」などを避ける）
NG_WORDS_WORD = [
    (r"最高の", "最上級。客観的な出典が無ければ使わない"),
    (r"最上級", "最上級。客観的な出典が無ければ使わない"),
]

# 2. 写真から分からない性能（根拠の併記が無ければ WARN）
PERF_WORDS = [
    "高気密", "高断熱", "耐震等級", "断熱等級", "UA値", "C値", "ZEH",
    "長期優良住宅", "省エネ性能", "制震", "免震", "床暖房", "全館空調",
]
PERF_EVIDENCE = ["相当", "住宅性能評価", "認定", "取得", "自社", "第三者", "評価書"]

# 6. 特典に条件の記載があるか
BENEFIT_WORDS = ["特典", "プレゼント", "ギフト", "商品券", "クオカード", "QUOカード",
                 "進呈", "差し上げ", "もれなく"]
BENEFIT_CONDITION = ["対象", "条件", "まで", "限り", "初回", "先着", "組様", "名様",
                     "要予約", "ご予約", "アンケート"]

DATE_RE = re.compile(r"\d{1,2}\s*月\s*\d{1,2}\s*日|\d{4}[/-]\d{1,2}[/-]\d{1,2}")
TEL_RE = re.compile(r"0\d{1,4}[-(]\d{1,4}[-)]\d{3,4}|0\d{9,10}")
URL_RE = re.compile(r"https?://[\w./?=&%#~+-]+")
WALK_RE = re.compile(r"徒歩\s*(?:約)?\s*(\d+)\s*分")


class Report:
    def __init__(self):
        self.rows = []

    def add(self, level, line_no, text, message):
        self.rows.append((level, line_no, text, message))

    def show(self):
        order = {"FAIL": 0, "WARN": 1}
        fails = sum(1 for r in self.rows if r[0] == "FAIL")
        warns = sum(1 for r in self.rows if r[0] == "WARN")
        for level, line_no, text, message in sorted(self.rows, key=lambda r: (order[r[0]], r[1])):
            where = f"{line_no}行目" if line_no else "全体"
            snippet = text.strip()
            if len(snippet) > 40:
                snippet = snippet[:40] + "…"
            print(f"[{level}] {where}: {message}")
            if snippet:
                print(f"         > {snippet}")
        print()
        if fails:
            print(f"FAIL {fails}件 / WARN {warns}件 — この原稿は出さない。")
        elif warns:
            print(f"FAIL 0件 / WARN {warns}件 — 目で見て判断する。")
        else:
            print("問題なし。")
        return 1 if fails else 0


def lint(text, event=None):
    rep = Report()
    lines = text.splitlines()

    for i, line in enumerate(lines, 1):
        # 1. 禁止語
        for word, why in NG_WORDS:
            if word in line:
                rep.add("FAIL", i, line, f"禁止表現「{word}」— {why}")
        for pattern, why in NG_WORDS_WORD:
            if re.search(pattern, line):
                rep.add("FAIL", i, line, f"禁止表現「{pattern}」— {why}")

        # 2. 性能の記載
        for word in PERF_WORDS:
            if word in line and not any(e in line for e in PERF_EVIDENCE):
                rep.add("WARN", i, line,
                        f"性能の記載「{word}」— 写真からは分からない。"
                        "事実として入力されたものか、評価の種類（性能評価／相当）を併記しているか確かめる")

        # 3. 徒歩○分
        m = WALK_RE.search(line)
        if m:
            minutes = int(m.group(1))
            rep.add("WARN", i, line,
                    f"徒歩{minutes}分 — 道路距離80m=1分で計算したか。"
                    f"およそ{minutes * 80}m以内であること")

        # 4. 新築
        if "新築" in line:
            rep.add("WARN", i, line,
                    "「新築」— 建築後1年未満かつ未入居のときだけ。"
                    "引き渡し前の施主の家なら「完成したばかりの家」に言い換える")

    # 6. 特典の条件
    if any(w in text for w in BENEFIT_WORDS):
        if not any(c in text for c in BENEFIT_CONDITION):
            rep.add("FAIL", 0, "", "来場特典を書いているが、対象・条件・期限が書かれていない")

    # 5. 架空情報の検出（--event があるときだけ）
    if event is not None:
        blob = "".join(str(v) for v in event.values())
        for regex, label in ((DATE_RE, "日付"), (TEL_RE, "電話番号"), (URL_RE, "URL")):
            for i, line in enumerate(lines, 1):
                for found in regex.findall(line):
                    normalized = re.sub(r"\s", "", found)
                    if normalized not in re.sub(r"\s", "", blob):
                        rep.add("FAIL", i, line,
                                f"入力されていない{label}「{found}」が出ている（創作の疑い）")
    else:
        rep.add("WARN", 0, "",
                "--event が渡されていないため、日付・電話番号・URLの突き合わせを省略した")

    return rep


def main():
    ap = argparse.ArgumentParser(description="完成見学会の告知原稿を検査する")
    ap.add_argument("path", help="原稿のテキストファイル。- で標準入力")
    ap.add_argument("--event", help="0番で入力した開催情報のJSON")
    args = ap.parse_args()

    if args.path == "-":
        text = sys.stdin.read()
    else:
        with open(args.path, encoding="utf-8") as f:
            text = f.read()

    event = None
    if args.event:
        with open(args.event, encoding="utf-8") as f:
            event = json.load(f)

    sys.exit(lint(text, event).show())


if __name__ == "__main__":
    main()
