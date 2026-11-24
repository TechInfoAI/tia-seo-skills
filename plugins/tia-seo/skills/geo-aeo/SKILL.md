---
name: geo-aeo
description: Make a site and its pages easy for AI search (ChatGPT, Perplexity, Claude, Gemini, Google AI Overviews, Copilot) to find, understand and cite - GEO, AEO, LLMO. Checks AI crawler access, llms.txt, answer-first content, entities and citations. Use when the user asks about AI visibility, GEO, AEO, LLMO, AI Overviews, getting cited by ChatGPT, or llms.txt.
---

# GEO / AEO: Get Cited by AI Search

AI answer engines can only cite pages they can crawl, understand and trust. Check those three things in that order.

## Step 1: Can AI crawlers reach the site?

If you can run code: `python3 scripts/ai_access_check.py <domain>`
It reads robots.txt and lists which AI crawlers are allowed, whether `/llms.txt` exists, and whether a sitemap is listed.

Key points:
- Blocking `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, `Googlebot` or `Bingbot` removes the site from those answers. Blocking training-only bots (`GPTBot`, `ClaudeBot`, `Google-Extended`, `CCBot`) is a business choice and does not remove the site from search results.
- Check that a firewall or CDN bot rule is not blocking these crawlers even when robots.txt allows them (ask the user to check their Cloudflare or host settings).
- ChatGPT search leans on Bing's index: the site should be verified in Bing Webmaster Tools and submit URLs with IndexNow.

## Step 2: Can AI understand each page?

For each key page check:
- **Answer first**: a 40-60 word direct answer to the main question near the top.
- **Clear structure**: question-style H2s, short paragraphs, lists and tables for facts.
- **Specific facts**: numbers, dates, prices, names, each with a source. Vague pages do not get quoted.
- **Entities**: the brand, product and people named consistently, with an About page and Organization schema that links official profiles (`sameAs`).
- **Freshness**: a visible "last updated" date on content that changes.
- **Server-rendered text**: the main content is in the HTML, not only loaded by JavaScript.

## Step 3: Will AI trust it?

- Author name and bio with real experience; About and Contact pages.
- Mentions of the brand on other sites AI engines read: Reddit, YouTube, industry lists, review sites, Wikipedia where it qualifies.
- Original data (a survey, test results, a tool) that others cite.

## llms.txt

If the site has none, offer one at `/llms.txt`: a Markdown file with the site name, a one-paragraph summary, and short lists of the most important URLs with one line each. It is a proposed convention, not a ranking factor: present it as low effort, unknown impact.

## Output

1. AI crawler access table and any blocking problem first.
2. Page-level fixes as a table: page, problem, exact fix (with the rewritten answer block where needed).
3. Off-site actions: 3-5 places where the brand should be mentioned.
4. A ready-to-upload llms.txt if requested.

Do not promise citations or traffic numbers. AI answers change often; suggest the user test key questions in ChatGPT, Perplexity and Google before and after.
