# -*- coding: utf-8 -*-
"""doormaster.co.kr — sitemap.xml / robots.txt 생성기

※ index.html 은 건드리지 않습니다.
   사이트마다 디자인이 달라서 index.html 은 각각 직접 편집합니다.
   이 스크립트는 index.html 안의 <section id="..."> 를 읽어
   sitemap.xml 과 robots.txt 만 다시 만들어 줍니다.

사용법:  python build.py
"""
import os
import re
import datetime

ROOT_DOMAIN = "doormaster.co.kr"

SITES = [
    ("main",   "",       "튼튼 욕실문턱 문지방 문틀 수리"),
    ("door",   "door",   "튼튼 방문 도어 문턱 수리"),
    ("marble", "marble", "튼튼 오래된 문턱 대리석 교체"),
    ("bath",   "bath",   "튼튼 욕실 안방 문짝 교체"),
]

BASE = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()


def host(sub):
    return f"{sub}.{ROOT_DOMAIN}" if sub else ROOT_DOMAIN


def section_ids(path):
    html = open(path, encoding="utf-8").read()
    ids, seen = [], set()
    for m in re.finditer(r'<section[^>]*\bid="([^"]+)"', html):
        i = m.group(1)
        if i not in seen:
            seen.add(i)
            ids.append(i)
    return ids


def make_sitemap(base_url, ids):
    urls = [(base_url + "/", "1.0")] + [(f"{base_url}/#{i}", "0.7") for i in ids]
    rows = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod>"
        f"<changefreq>monthly</changefreq><priority>{p}</priority></url>"
        for u, p in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + rows + "\n</urlset>\n")


def make_robots(base_url):
    return ("User-agent: *\nAllow: /\n\n"
            "User-agent: Yeti\nAllow: /\n\n"
            f"Sitemap: {base_url}/sitemap.xml\n")


def main():
    print(f"기준일: {TODAY}\n")
    for key, sub, brand in SITES:
        folder = os.path.join(BASE, key)
        index = os.path.join(folder, "index.html")
        base_url = "https://" + host(sub)
        if not os.path.exists(index):
            print(f"[건너뜀] {key}/index.html 없음")
            continue
        ids = section_ids(index)
        open(os.path.join(folder, "sitemap.xml"), "w", encoding="utf-8").write(
            make_sitemap(base_url, ids))
        open(os.path.join(folder, "robots.txt"), "w", encoding="utf-8").write(
            make_robots(base_url))
        print(f"[완료] {key:7s} {host(sub):26s} 섹션 {len(ids)}개  {brand}")
    print("\nsitemap.xml / robots.txt 갱신 완료")
    print("index.html 은 건드리지 않았습니다.")


if __name__ == "__main__":
    main()
