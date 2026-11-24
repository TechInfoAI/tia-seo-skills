#!/usr/bin/env python3
"""Check whether AI crawlers can reach a site. Standard library only.

Usage:
    python3 ai_access_check.py https://example.com [--json]

Reads robots.txt and reports, for each known AI crawler, whether the home
page is allowed. Also checks for /llms.txt and the sitemap.
"""
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser

UA = "Mozilla/5.0 (compatible; TIA-SEO-AICheck/1.0; +https://techinfoai.net/)"

# crawler: what it is used for
BOTS = {
    "OAI-SearchBot": "ChatGPT search results",
    "ChatGPT-User": "ChatGPT browsing on a user's request",
    "GPTBot": "OpenAI model training",
    "ClaudeBot": "Anthropic model training",
    "Claude-SearchBot": "Claude search results",
    "Claude-User": "Claude fetching on a user's request",
    "PerplexityBot": "Perplexity search index",
    "Perplexity-User": "Perplexity fetching on a user's request",
    "Google-Extended": "Gemini training and grounding (not Google Search)",
    "Googlebot": "Google Search and AI Overviews",
    "Bingbot": "Bing search and Copilot",
    "Applebot-Extended": "Apple Intelligence training",
    "CCBot": "Common Crawl (used by many models)",
    "Bytespider": "ByteDance crawler",
    "Meta-ExternalAgent": "Meta AI",
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read(2_000_000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(1)
    base = args[0] if "://" in args[0] else "https://" + args[0]
    p = urllib.parse.urlparse(base)
    root = f"{p.scheme}://{p.netloc}"

    rs, robots = get(root + "/robots.txt")
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(robots.splitlines() if rs == 200 else [])
    bots = {b: {"use": u, "allowed": rp.can_fetch(b, root + "/")} for b, u in BOTS.items()}

    ls, llms = get(root + "/llms.txt")
    sitemaps = rp.site_maps() or []
    res = {
        "site": root,
        "robots_txt_status": rs,
        "bots": bots,
        "llms_txt": ls == 200 and bool(llms.strip()),
        "sitemaps_in_robots": sitemaps,
    }
    issues = []
    for b in ("OAI-SearchBot", "Claude-SearchBot", "PerplexityBot", "Googlebot", "Bingbot"):
        if not bots[b]["allowed"]:
            issues.append(f"{b} is blocked: the site cannot appear in {bots[b]['use']}")
    if not res["llms_txt"]:
        issues.append("No /llms.txt file")
    if not sitemaps:
        issues.append("No Sitemap line in robots.txt")
    res["issues"] = issues

    if "--json" in sys.argv:
        print(json.dumps(res, indent=2))
        return
    print(f"site: {root}  robots.txt: {rs}  llms.txt: {'yes' if res['llms_txt'] else 'no'}")
    for b, v in bots.items():
        print(f"  {'ALLOWED' if v['allowed'] else 'BLOCKED':8} {b:20} {v['use']}")
    print(f"sitemaps: {', '.join(sitemaps) or 'none listed'}")
    print(f"\nissues ({len(issues)}):")
    for i in issues:
        print("  - " + i)


if __name__ == "__main__":
    main()
