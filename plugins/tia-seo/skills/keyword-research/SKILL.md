---
name: keyword-research
description: Turn seed keywords or a keyword export (Google Search Console, Ahrefs, Semrush, Google Keyword Planner CSV) into a clustered keyword plan with search intent and one target page per cluster. Use when the user asks for keyword research, keyword clusters, a content plan from keywords, or uploads a keyword CSV.
---

# Keyword Research

Build a plan the user can act on: which pages to create or update, and which keywords each page targets. One page per search intent, never one page per keyword.

## Inputs

- Seed keywords, a niche, or a CSV export. Ask for the site URL and the target country if missing.
- If a CSV is given, read the real columns (keyword, volume, KD/difficulty, CPC, position, clicks, impressions, URL). Never invent volumes. If there is no volume data, say so and rank by intent and relevance instead.

## Step 1: Clean

- Remove duplicates, misspellings, and keywords for brands the site cannot serve.
- Keep the user's main keyword exactly as written.

## Step 2: Label intent

| Intent | Signals | Page type |
|---|---|---|
| Informational | how, what, why, guide, ideas | Blog post or guide |
| Commercial | best, top, vs, review, alternative | Comparison or list post |
| Transactional | buy, price, hire, near me, coupon | Product, service or local page |
| Navigational | a brand or product name | Brand or product page |

## Step 3: Cluster

Group keywords that one page could rank for: same intent, and the same results would show for them on Google. If you can search, compare the top results for two keywords; heavy overlap means one cluster. Name each cluster by its primary keyword (highest volume, or the clearest wording).

## Step 4: Prioritize

Score each cluster High, Medium or Low on:
- Business value (does it lead to a sale, lead or affiliate click?)
- Difficulty against the site's strength (new sites: low KD and long-tail first)
- Quick wins: keywords where the site already sits in positions 5 to 20 (from GSC); updating that page is faster than writing a new one.

## Output

A table, highest priority first:

| Cluster (primary keyword) | Supporting keywords | Intent | Volume (sum) | Difficulty | Action | Target URL |
|---|---|---|---|---|---|---|

- Action is "Update existing page", "New page" or "Merge pages".
- Flag cannibalization: two of the user's pages ranking for the same cluster.
- Then list the first 5 pages to work on, with a suggested title for each.
- Offer the table as a CSV if the user wants to load it into a sheet.
