#!/usr/bin/env python3
"""Quick on-page SEO check for one URL. Standard library only.

Usage:
    python3 page_check.py https://example.com/page [--json]

Prints status, redirects, title/meta lengths, robots, canonical, headings,
word count, images without alt, link counts, JSON-LD types, hreflang and
Open Graph tags, plus a list of issues found.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; TIA-SEO-PageCheck/1.0; +https://techinfoai.net/)"


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.in_title = "", False
        self.meta, self.links, self.imgs = [], [], []
        self.headings, self._h = [], None
        self.jsonld, self._ld = [], None
        self.text, self._skip = [], 0
        self.html_lang = ""
        self._svg = 0
        self._title_done = False

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.html_lang = a.get("lang", "")
        elif tag == "svg":
            self._svg += 1
        elif tag == "title" and not self._svg and not self._title_done:
            self.in_title = True
        elif tag == "meta":
            self.meta.append(a)
        elif tag == "link":
            self.links.append(("link", a))
        elif tag == "a":
            self.links.append(("a", a))
        elif tag == "img":
            self.imgs.append(a)
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._h = [tag, ""]
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._ld = ""
        if tag in ("script", "style", "noscript"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "svg" and self._svg:
            self._svg -= 1
        if tag == "title" and self.in_title:
            self.in_title = False
            self._title_done = True
        elif self._h and tag == self._h[0]:
            self.headings.append((self._h[0], " ".join(self._h[1].split())))
            self._h = None
        elif tag == "script" and self._ld is not None:
            self.jsonld.append(self._ld)
            self._ld = None
        if tag in ("script", "style", "noscript") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self._h is not None:
            self._h[1] += data
        if self._ld is not None:
            self._ld += data
        elif not self._skip:
            self.text.append(data)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=25) as r:
        body = r.read(5_000_000)
        charset = r.headers.get_content_charset() or "utf-8"
        return r.status, r.geturl(), dict(r.headers), body.decode(charset, "replace"), round(time.time() - t, 2)


def ld_types(blocks):
    types = []

    def walk(o):
        if isinstance(o, dict):
            t = o.get("@type")
            if t:
                types.extend(t if isinstance(t, list) else [t])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    bad = 0
    for b in blocks:
        try:
            walk(json.loads(b))
        except ValueError:
            bad += 1
    return sorted(set(map(str, types))), bad


def check(url):
    try:
        status, final, headers, html, secs = fetch(url)
    except urllib.error.HTTPError as e:
        return {"url": url, "status": e.code, "issues": [f"HTTP {e.code}: page did not load"]}
    except Exception as e:  # noqa: BLE001
        return {"url": url, "status": None, "issues": [f"Fetch failed: {e}"]}

    p = Parser()
    p.feed(html)
    host = urllib.parse.urlparse(final).netloc
    meta = {}
    for m in p.meta:
        key = (m.get("name") or m.get("property") or "").lower()
        if key:
            meta[key] = m.get("content", "")
    canon = next((a.get("href") for t, a in p.links if t == "link" and "canonical" in a.get("rel", "").lower()), "")
    hreflang = [a.get("hreflang") for t, a in p.links if t == "link" and a.get("hreflang")]
    internal = external = nofollow = 0
    for t, a in p.links:
        if t != "a" or not a.get("href") or a["href"].startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        h = urllib.parse.urlparse(urllib.parse.urljoin(final, a["href"])).netloc
        if h == host:
            internal += 1
        else:
            external += 1
        if "nofollow" in a.get("rel", "").lower():
            nofollow += 1
    words = len(re.findall(r"\w+", " ".join(p.text)))
    no_alt = sum(1 for i in p.imgs if not i.get("alt", "").strip())
    types, bad_ld = ld_types(p.jsonld)
    h1 = [h for t, h in p.headings if t == "h1"]
    title = " ".join(p.title.split())
    desc = meta.get("description", "")
    robots = meta.get("robots", "")
    xrobots = headers.get("X-Robots-Tag", headers.get("x-robots-tag", ""))

    issues = []
    if status != 200:
        issues.append(f"Status {status}")
    if final.rstrip("/") != url.rstrip("/"):
        issues.append(f"Redirects to {final}")
    if not title:
        issues.append("Missing <title>")
    elif not 30 <= len(title) <= 60:
        issues.append(f"Title is {len(title)} characters (aim for 30-60)")
    if not desc:
        issues.append("Missing meta description")
    elif not 70 <= len(desc) <= 160:
        issues.append(f"Meta description is {len(desc)} characters (aim for 70-160)")
    if "noindex" in (robots + " " + xrobots).lower():
        issues.append("Page is set to noindex")
    if not canon:
        issues.append("No canonical tag")
    elif urllib.parse.urljoin(final, canon).rstrip("/") != final.rstrip("/"):
        issues.append(f"Canonical points elsewhere: {canon}")
    if len(h1) != 1:
        issues.append(f"{len(h1)} H1 tags (use exactly one)")
    if words < 300:
        issues.append(f"Thin content: about {words} words")
    if no_alt:
        issues.append(f"{no_alt} of {len(p.imgs)} images have no alt text")
    if not types:
        issues.append("No JSON-LD structured data")
    if bad_ld:
        issues.append(f"{bad_ld} JSON-LD block(s) are not valid JSON")
    if not meta.get("viewport"):
        issues.append("No viewport meta tag (mobile)")
    if not p.html_lang:
        issues.append("No lang attribute on <html>")
    if not meta.get("og:title") or not meta.get("og:image"):
        issues.append("Open Graph title or image missing (social sharing)")
    if secs > 2.5:
        issues.append(f"Slow server response: {secs}s for the HTML")

    return {
        "url": url, "final_url": final, "status": status, "response_seconds": secs,
        "title": title, "title_length": len(title),
        "meta_description": desc, "meta_description_length": len(desc),
        "robots": robots, "x_robots_tag": xrobots, "canonical": canon,
        "lang": p.html_lang, "h1": h1,
        "headings": [f"{t.upper()}: {h}" for t, h in p.headings][:40],
        "word_count": words, "images": len(p.imgs), "images_missing_alt": no_alt,
        "internal_links": internal, "external_links": external, "nofollow_links": nofollow,
        "schema_types": types, "hreflang": hreflang,
        "og_title": meta.get("og:title", ""), "og_image": meta.get("og:image", ""),
        "issues": issues,
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(1)
    res = check(args[0])
    if "--json" in sys.argv:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return
    for k, v in res.items():
        if k in ("issues", "headings"):
            continue
        print(f"{k}: {v}")
    print("\nheadings:")
    for h in res.get("headings", []):
        print("  " + h)
    print(f"\nissues ({len(res['issues'])}):")
    for i in res["issues"]:
        print("  - " + i)


if __name__ == "__main__":
    main()
