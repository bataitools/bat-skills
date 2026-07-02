---
name: bat-submit
description: Submit an AI tool to BAT AI Tools (bataitools.com) via bat-cli CLI. Use a continuous 4-step workflow — extract, assets, translate, then pack and submit.
agent_created: true
triggers:
    - submit AI tool to bataitools
    - submit AI tool to bat ai tools
    - publish to BAT AI Tools directory
    - add tool to bataitools.com
    - list my tool on BAT AI
    - list tool on bataitools
    - list my tool on bataitools.com
    - List my tool on BAT AI TOOLS
    - bat-cli submit
    - 提交 AI 工具到 bataitools
    - 提交 AI 工具到 bat
---

# BAT AI Tools — Submit Skill

Submit or update an AI tool listing on [bataitools.com](https://bataitools.com) using the `bat-cli` command-line tool. The workflow always runs in **4 sequential steps** without pausing for user confirmation between them.

## Prerequisites

1. **Install bat-cli (Ensure latest version):**
    ```bash
    npm install -g @bataitools/bat-cli@latest
    # or
    bun add -g @bataitools/bat-cli@latest
    ```
2. API endpoint default: `https://api.bataitools.com` (override via `BAT_API_URL` env or `--api` flag).

---

## Core Rule: Never generate all languages in one step

Large single-file JSON causes truncation and validation failures. Always run the 4 steps back-to-back:

| Step             | What happens                                              | Output                                       |
| ---------------- | --------------------------------------------------------- | -------------------------------------------- |
| **1. Extract**   | Crawl site, fill `base.json` + `i18n/en.json` (no assets) | `base.json`, `i18n/en.json`                  |
| **2. Capture**   | Agent captures webp screenshot & fetches logo, validate   | local logo & screenshot, validation check    |
| **3. Translate** | Translate `en.json` into 27 other languages (batches)     | `i18n/zh.json`, `i18n/ja.json`, … (28 total) |
| **4. Submit**    | Merge, final validate, upload assets, POST                | `submit.bundle.json`, submission confirmed   |

> [!WARNING]
> **[Strict Hard Constraint] You are STRICTLY FORBIDDEN from translating more than 4 languages in a single Prompt! Running scripts (such as Python scripts) to batch-request or process more than 4 languages at once is also strictly prohibited.**
> You are only allowed to translate 2 to 4 languages at a time. You must strictly process them in batches, and you must verify that the current batch is successfully written to local files before proceeding to the next batch.

---

## Per-site directory isolation (mandatory)

Every website gets its own directory keyed by URL hostname (lowercased only — no stripping `www`).

```bash
bat-cli site-dir https://www.Example.com   # → ./submits/www.example.com
bat-cli init-site --website https://www.Example.com
```

Throughout this skill, `<submit-dir>` = `./submits/<hostname>`, e.g. `./submits/www.example.com`.

**Never write site B's data into site A's directory.** Always call `bat-cli site-dir <url>` per site.

---

## Multiple sites

When the user lists N websites, process **one site at a time** — full Step 1→2→3→4 per site before starting the next. Never batch-crawl or batch-translate across sites.

---

## Step 1 — Extract

Initialize the directory, crawl the target website, and extract the English metadata.

For the exact CLI commands, website crawl checklist, and comprehensive field guides (including taxonomy, social profiles, and developer identity rules), refer entirely to **[references/01-extract.md](references/01-extract.md)**.

**Semantic Self-Check:**
AI must self-check all written fields before proceeding. Ensure all mandatory fields (like pricing tiers, category tags) are fully filled and align with the rules in [references/01-extract.md](references/01-extract.md). Do not execute screenshot tools yet.

---

## Step 2 — Capture Assets & Phase 1 Validation

Once Step 1 text files are ready, grab the visual assets and execute validation.

For the exact CLI commands, local asset rules, and the mandatory pre-validation self-check checklist, refer entirely to **[references/02-capture.md](references/02-capture.md)**.

**Fail-Fast Rule:**
If `validate-phase1` fails (Exit Code != 0), **stop the workflow immediately** and report the errors to the user. Do **not** proceed to Step 3, avoiding wasteful LLM translation calls.

---

## Step 3 — Translate from English

Read **only** the English `i18n/en.json` to localize into the other 27 target languages.

For the natural localization rules, priceNote translation guidelines, and diff merge logic, refer entirely to **[references/03-translate.md](references/03-translate.md)**.

> [!IMPORTANT]
> **[Strict Translation Batching Constraint]**
> - **You are STRICTLY FORBIDDEN from processing more than 4 languages at once.** The number of languages processed per session (single prompt, single API request, or a single run cycle of a script) **must be restricted to 2–4**. Do NOT attempt to merge batches or translate all 27 languages at once.
> - **Do NOT write or execute any automation scripts** that attempt to translate 5 or more languages in a single run.
> - You must complete one batch (2–4 languages), successfully write the generated files (e.g., `i18n/zh.json`, `i18n/ja.json`) to the local directory, and verify their correctness before starting the next batch.

**Execution Order & Self-Check**:
Strictly follow the order below to translate and save files in batches (maximum of 4 languages per batch). After writing each batch, immediately verify the corresponding JSON files for syntax and structural validity before moving to the next batch:

1.  `zh`, `tw`, `ja`, `ko` (Batch 1: Max 4 languages)
2.  `de`, `fr`, `it`, `nl` (Batch 2: Max 4 languages)
3.  `es`, `pt`, `vi`, `id` (Batch 3: Max 4 languages)
4.  `ru`, `pl`, `uk`, `tr` (Batch 4: Max 4 languages)
5.  `ar`, `he`, `fa`, `ur` (Batch 5: Max 4 languages)
6.  `hi`, `bn`, `th`         (Batch 6: Max 3 languages)
7.  `sv`, `no`, `da`, `fi` (Batch 7: Max 4 languages)

---

## Step 4 — Pack and Submit

This is the final stage to package, validate, authenticate, and submit the site to the platform.

**Authentication**:
Before submitting, you must authenticate. If not already authenticated, perform login at this step. See [references/04-submit.md](references/04-submit.md) for authentication choices.

For the exact CLI commands, validation workflow, and automatic WebP assets conversion rules, refer entirely to **[references/04-submit.md](references/04-submit.md)**.

---

## Reference files

- `references/01-extract.md` — Full crawl checklist, `base.json` & `i18n/en.json` field guide, voice rules, and constraints for Step 1 (Extract).
- `references/02-capture.md` — Agent-side assets generation/compression guidelines, local layout rules, and `validate-phase1` self-check checklist for Step 2 (Capture).
- `references/03-translate.md` — Multi-language localization rules, 28 languages batching strategy, and `priceNote` translations for Step 3 (Translate).
- `references/04-submit.md` — CLI commands, bundle packing guides, CDN uploads, and status checking for Step 4 (Submit).
