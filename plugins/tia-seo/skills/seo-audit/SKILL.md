---
name: seo-audit
description: Audit a web page or site for technical and on-page SEO and return a prioritized fix list. Use when the user shares a URL or domain and asks to audit, check, review SEO, find SEO issues, or asks why a page is not ranking or not indexed.
---

# SEO Audit

Find what stops a page or site from ranking, then hand back fixes in the order that matters most. Every finding must come from something you actually checked, never from a guess.

## Inputs

- A URL (one page) or a domain (site audit). Ask for one if none was given.
- Optional: the target keyword, a Google Search Console export, or a crawl CSV. Use them if provided.

## Step 1: Collect facts

1. If you can run code, run the page check for each URL you audit:
   `python3 scripts/page_check.py <url>` (add `--json` for machine output).
   It reports status, redirects, title and meta lengths, robots, canonical, H1s, headings, word count, images without alt, links, JSON-LD types, hreflang and Open Graph tags.
2. If you cannot run code, fetch the page with your browsing tool and read the same items from the HTML.
3. For a site audit, also check:
   - `/robots.txt`: is anything important blocked? Is the sitemap listed?
   - The XML sitemap: does it load, and does it list only indexable 200 URLs?
   - 5 to 10 key URLs: home, top categories, top posts or products.
4. Note anything you could not check and say so in the report.

## Step 2: Check these areas

| Area | What to look for |
|---|---|
| Indexing | noindex, robots.txt blocks, canonical pointing elsewhere, 4xx/5xx, redirect chains |
| Titles and meta | missing, duplicate, too long or short, keyword missing or not near the start |
| Headings | zero or several H1s, skipped levels, headings that do not describe the section |
| Content | thin pages, duplicate pages, intent mismatch with the keyword, no clear answer near the top |
| Links | orphan pages, few internal links to money pages, broken links, generic anchor text |
| Images | missing alt text, huge files, no width/height |
| Structured data | missing schema for the page type, invalid JSON-LD |
| Mobile and speed | no viewport, slow server response; suggest PageSpeed Insights for Core Web Vitals |
| Trust (E-E-A-T) | no author, no about or contact page, no dates on time-sensitive content |

## Step 3: Report

Start with a one-line verdict, then a table sorted by priority:

| Priority | Issue | Where | Fix | Why it matters |
|---|---|---|---|---|

- **Critical**: blocks indexing or ranking (noindex, blocked, 5xx, wrong canonical).
- **High**: clear ranking loss (missing title, wrong intent, thin money page, no internal links).
- **Medium**: improvement (meta length, schema, alt text).
- **Low**: polish.

Rules:
- Give the exact fix, ready to paste: the new title, the new meta description, the canonical URL.
- Group repeated issues ("23 images without alt") instead of listing each one.
- End with the 3 fixes to do first.
- Do not invent numbers such as traffic or rankings. If data is missing, say what to export.

## WordPress notes

- Title, meta, canonical, robots and schema usually live in the SEO plugin (Rank Math or Yoast) per post, not in the theme.
- "Discourage search engines" under Settings > Reading adds noindex to the whole site: check it first when nothing is indexed.
