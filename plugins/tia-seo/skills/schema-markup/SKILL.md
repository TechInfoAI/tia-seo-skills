---
name: schema-markup
description: Detect, fix or generate Schema.org JSON-LD structured data (Article, Product, LocalBusiness, FAQPage, HowTo, SoftwareApplication, BreadcrumbList, Organization, Review and more). Use when the user asks for schema, structured data, rich results, JSON-LD, or why rich results are missing.
---

# Schema Markup

Write valid JSON-LD that matches what is visible on the page. Markup that describes content the visitor cannot see breaks Google's guidelines and can cost rich results.

## Step 1: Pick the type from the page

| Page | Schema |
|---|---|
| Blog post, news, guide | Article / BlogPosting / NewsArticle |
| Product page | Product with Offer (price, currency, availability) and AggregateRating only if real reviews show |
| Local business, service area | LocalBusiness subtype (Plumber, Dentist, LegalService...) with address, phone, hours, geo |
| Software, app, SaaS, AI tool | SoftwareApplication (applicationCategory, operatingSystem, offers) |
| Code repository | SoftwareSourceCode (codeRepository, programmingLanguage, license) |
| FAQ section | FAQPage (questions and answers exactly as shown) |
| Step-by-step guide | HowTo (steps as shown) |
| Every page | BreadcrumbList; Organization or Person on the home or about page |

## Step 2: Check existing markup

If you can fetch the page, read all `<script type="application/ld+json">` blocks. Report: invalid JSON, wrong or missing required properties, values that differ from the page (price, rating, dates), and duplicate blocks from two plugins.

## Step 3: Generate

- Use `@graph` when one page needs several types, and connect them with `@id`.
- Use absolute URLs, ISO 8601 dates (2026-11-24), and real values from the page. Leave a property out rather than invent it.
- Never add ratings, reviews or prices that the page does not show.

## Output

1. What is on the page now and what is wrong.
2. The full JSON-LD in one code block, ready to paste.
3. Where to put it: theme header, the SEO plugin's custom schema box (Rank Math: Schema > Schema Generator > Custom Schema), or Google Tag Manager.
4. How to test: Google Rich Results Test and the Schema.org validator.

Note: Google shows FAQ and HowTo rich results only for some sites now, but the markup still helps search engines and AI tools understand the page.
