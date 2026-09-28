# -*- coding: utf-8 -*-
"""doormaster.co.kr — sitemap.xml / robots.txt 생성기

※ index.html 과 area-*.html 은 건드리지 않습니다.
   폴더 안의 html 파일을 훑어서 sitemap.xml 과 robots.txt 만 다시 만듭니다.

※ sitemap 에 넣는 주소 규칙 (2026-09-28 수정)
   - 실제로 열리는 주소는 확장자가 없습니다. 그래서 .html 을 떼고 넣습니다.
     (예: area-ansan.html  ->  https://doormaster.co.kr/area-ansan)
   - #앵커 주소는 페이지가 아니라 한 페이지 안의 위치라서 넣지 않습니다.
     넣으면 구글이 "색인 안 됨"으로 잡아냅니다.

사용법:  python build.py
"""
import os, glob, datetime

ROOT_DOMAIN = "doormaster.co.kr"
SITES = [
    ("main",   "",       "튼튼 문턱 문틀 문짝 수리"),
    ("cubicle","cubicle","튼튼 큐비클 화장실칸막이 수리"),
]
BASE  = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()

host = lambda sub: f"{sub}.{ROOT_DOMAIN}" if sub else ROOT_DOMAIN

def main():
    print(f"기준일: {TODAY}\n")
    for key, sub, brand in SITES:
        folder = os.path.join(BASE, key)
        index  = os.path.join(folder, "index.html")
        base   = "https://" + host(sub)
        if not os.path.exists(index):
            print(f"[건너뜀] {key}/index.html 없음"); continue

        # 파일이름에서 .html 을 뗀 것이 실제 주소입니다
        slug = lambda f: os.path.basename(f)[:-5]

        urls = [(base + "/", "1.0")]
        # 지역 허브 + 지역 페이지
        if os.path.exists(os.path.join(folder, "area.html")):
            urls.append((f"{base}/area", "0.9"))
        for f in sorted(glob.glob(os.path.join(folder, "area-*.html"))):
            urls.append((f"{base}/{slug(f)}", "0.8"))
        # 그 외 html
        for f in sorted(glob.glob(os.path.join(folder, "*.html"))):
            n = os.path.basename(f)
            if n in ("index.html", "area.html") or n.startswith("area-"):
                continue
            urls.append((f"{base}/{slug(f)}", "0.7"))

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
