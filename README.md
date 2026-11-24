# TIA SEO Skills

**Free SEO, GEO/AEO and Local SEO skills for AI agents.** Add them to Claude, Claude Code, Codex, Cursor or any agent that reads `SKILL.md` files, then ask in plain words: *"audit this page"*, *"build a keyword plan from this CSV"*, *"optimize my Google Business Profile"*.

No API keys. No accounts. No extra runtime. Two small helper scripts use only the Python standard library.

Made by [Tech Info AI](https://techinfoai.net) · Listed in the [Tech Info AI open-source directory](https://techinfoai.net/open-source/)

---

## The 9 skills

| Skill | What it does | Ask it like |
|---|---|---|
| `seo-audit` | Technical and on-page audit with a prioritized fix list. Includes `page_check.py`. | "Audit https://example.com/pricing" |
| `keyword-research` | Clusters keywords by intent from seeds or a GSC/Ahrefs/Semrush CSV, one page per cluster. | "Turn this Ahrefs export into a content plan" |
| `on-page-seo` | Ready-to-paste title, meta, slug, H1, outline, internal links and FAQ for one keyword. | "Optimize this post for *best crm for startups*" |
| `content-brief` | SERP-based brief: intent, angle, outline, entities, questions, links. | "Brief for *how to start a podcast*" |
| `schema-markup` | Detects, fixes and writes JSON-LD for the page type. | "Write Product schema for this page" |
| `geo-aeo` | AI search visibility: AI crawler access, llms.txt, answer-first content, entities. Includes `ai_access_check.py`. | "Can ChatGPT and Perplexity cite my site?" |
| `local-seo` | Google Business Profile audit, citations, reviews and reply templates, local pages, LocalBusiness schema. | "Local SEO plan for a dentist in Austin" |
| `internal-linking` | Orphans, weak money pages and an exact link plan (source, anchor, target). | "Plan internal links from my sitemap" |
| `link-building` | Tactics, site vetting checklist, outreach email and follow-up. | "Write an outreach email for a resource page link" |

## Install

### Claude Code (plugin)

```
/plugin marketplace add TechInfoAI/tia-seo-skills
/plugin install tia-seo@tia-seo-skills
```

Then just ask, or call a skill directly: `/tia-seo:seo-audit https://example.com`

### Claude.ai (web and desktop)

1. Download a skill's zip from the [`dist/`](dist/) folder, for example `seo-audit.zip`.
2. In Claude, open **Settings → Capabilities → Skills** and upload the zip.
3. Start a new chat and ask for the task.

### Codex, Cursor and other agents

Copy the skill folders into your agent's skills folder:

```
git clone https://github.com/TechInfoAI/tia-seo-skills.git
cp -r tia-seo-skills/plugins/tia-seo/skills/* .claude/skills/   # or .agents/skills/
```

No skills support? Paste the contents of a `SKILL.md` into the chat as instructions.

## Helper scripts

Both run with Python 3.8+ and nothing else.

```
python3 plugins/tia-seo/skills/seo-audit/scripts/page_check.py https://example.com/page
python3 plugins/tia-seo/skills/geo-aeo/scripts/ai_access_check.py example.com
```

- `page_check.py`: status, redirects, title and meta length, robots, canonical, H1s, headings, word count, missing alt text, links, JSON-LD types, hreflang, Open Graph, plus an issue list. Add `--json` for JSON.
- `ai_access_check.py`: which AI crawlers robots.txt allows (OAI-SearchBot, GPTBot, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended and more), whether `/llms.txt` exists, and sitemap lines.

## Why another SEO skill pack?

There are great SEO skill repos already. This pack fills the gaps we kept running into:

- **Light**: no headless browser, no Python environment to build, no third-party connector or API key.
- **Works everywhere**: plain `SKILL.md` files for Claude.ai, Claude Code, Codex and Cursor.
- **Local SEO and link building** built in, from real agency work.
- **Ready-to-paste output**: final titles, metas, schema and emails, not just advice.

Want more depth? These projects inspired the scope of this pack (no code or text was copied):
[AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) (full Claude Code SEO suite),
[coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (marketing skills),
[Ryze-AI-Adgent/open-seo-mcp-skills](https://github.com/Ryze-AI-Adgent/open-seo-mcp-skills) (skills for live GSC and ads data).

## Contributing

Issues and pull requests are welcome: new checks, better prompts, fixes for wrong advice.

## License

MIT © Tech Info AI
