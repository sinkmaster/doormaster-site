# -*- coding: utf-8 -*-
"""doormaster.co.kr — sitemap.xml / robots.txt 생성기

※ index.html 과 area-*.html 은 건드리지 않습니다.
   폴더 안의 html 파일을 훑어서 sitemap.xml 과 robots.txt 만 다시 만듭니다.

사용법:  python build.py
"""
import os, re, glob, datetime

ROOT_DOMAIN = "doormaster.co.kr"
SITES = [
    ("main",   "",       "튼튼 욕실문턱 문지방 문틀 수리"),
    ("door",   "door",   "튼튼 방문 도어 문턱 수리"),
    ("marble", "marble", "튼튼 오래된 문턱 대리석 교체"),
    ("cubicle","cubicle","튼튼 큐비클 화장실칸막이 수리"),
    ("bath",   "bath",   "튼튼 욕실 안방 문짝 교체"),
]
BASE  = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()

host = lambda sub: f"{sub}.{ROOT_DOMAIN}" if sub else ROOT_DOMAIN

def section_ids(path):
    html = open(path, encoding="utf-8").read()
    out, seen = [], set()
    for m in re.finditer(r'<section[^>]*\bid="([^"]+)"', html):
        i = m.group(1)
        if i not in seen:
            seen.add(i); out.append(i)
    return out

def main():
    print(f"기준일: {TODAY}\n")
    for key, sub, brand in SITES:
        folder = os.path.join(BASE, key)
        index  = os.path.join(folder, "index.html")
        base   = "https://" + host(sub)
        if not os.path.exists(index):
            print(f"[건너뜀] {key}/index.html 없음"); continue

        urls = [(base + "/", "1.0")]
        # 지역 허브 + 지역 페이지
        if os.path.exists(os.path.join(folder, "area.html")):
            urls.append((f"{base}/area.html", "0.9"))
        for f in sorted(glob.glob(os.path.join(folder, "area-*.html"))):
            urls.append((f"{base}/{os.path.basename(f)}", "0.8"))
        # 그 외 html
        for f in sorted(glob.glob(os.path.join(folder, "*.html"))):
            n = os.path.basename(f)
            if n in ("index.html", "area.html") or n.startswith("area-"):
                continue
            urls.append((f"{base}/{n}", "0.7"))
        # 메인 페이지 섹션 앵커
        urls += [(f"{base}/#{i}", "0.6") for i in section_ids(index)]

        rows = "\n".join(
            f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod>'
            f'<changefreq>monthly</changefreq><priority>{p}</priority></url>'
            for u, p in urls)
        open(os.path.join(folder, "sitemap.xml"), "w", encoding="utf-8").write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + "\n</urlset>\n")
        open(os.path.join(folder, "robots.txt"), "w", encoding="utf-8").write(
            "User-agent: *\nAllow: /\n\nUser-agent: Yeti\nAllow: /\n\n"
            f"Sitemap: {base}/sitemap.xml\n")

        n_area = len([u for u, _ in urls if "/area-" in u])
        print(f"[완료] {key:7s} {host(sub):26s} URL {len(urls)}개 (지역페이지 {n_area}개)  {brand}")
    print("\nsitemap.xml / robots.txt 갱신 완료 · html 파일은 건드리지 않았습니다.")

if __name__ == "__main__":
    main()
