---
name: bat-submit
description: Submit an AI tool to BAT AI Tools (bataitools.com) via bat-cli CLI. Use a continuous 4-step workflow — extract, assets, translate, then pack and submit.
agent_created: true
triggers:
    - submit AI tool to bataitools
    - submit AI tool to bat ai tools
    - publish to BAT AI Tools directory
    - add tool to bataitools.com
    - bat-cli submit
    - 提交 AI 工具到 bataitools
    - 提交 AI 工具到 bat
---

# BAT AI Tools — Submit Skill

Submit or update an AI tool listing on [bataitools.com](https://bataitools.com) using the `bat-cli` command-line tool. The workflow always runs in **4 sequential steps** without pausing for user confirmation between them.

## Prerequisites

1. **Install bat-cli:**
    ```bash
    npm install -g @bataitools/bat-cli
    # or
    bun add -g @bataitools/bat-cli
    ```
2. **Authenticate** (pick one):
    - Guest (auto-created on first submit): `bat-cli login-guest`
    - Formal account (OAuth, like `gh auth login`): `bat-cli login`
    - API key (CI): `bat-cli login --key <your-api-key>`
3. API endpoint default: `https://api.bataitools.com` (override via `BAT_API_URL` env or `--api` flag).
4. **Environment Requirements**:
    - **Playwright Chromium**: `bat-cli capture-screenshot` requires the Playwright chromium browser. Prior to running submission tasks, please ensure it is installed:
        ```bash
        npx playwright install chromium
        ```
        _(While the CLI will attempt to auto-install this browser on the first run of `capture-screenshot`, pre-installing is highly recommended to avoid execution delays or environment-specific timeout issues)._

---

## Core Rule: Never generate all languages in one step

Large single-file JSON causes truncation and validation failures. Always run the 4 steps back-to-back:

| Step             | What happens                                              | Output                                       |
| ---------------- | --------------------------------------------------------- | -------------------------------------------- |
| **1. Extract**   | Crawl site, fill `base.json` + `i18n/en.json` (no assets) | `base.json`, `i18n/en.json`                  |
| **2. Capture**   | Capture screenshot & fetch logo, validate Phase 1         | local logo & screenshot, validation check    |
| **3. Translate** | Translate `en.json` into 27 other languages (batches)     | `i18n/zh.json`, `i18n/ja.json`, … (28 total) |
| **4. Submit**    | Merge, final validate, upload assets, POST                | `submit.bundle.json`, submission confirmed   |

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

See `references/01-generate-en.md` for the complete crawl checklist, field guides, and voice rules.

**Steps:**

1. Initialize directory and fetch schema:
    ```bash
    bat-cli init-site --website <url>
    bat-cli schema en
    ```
2. Crawl and write metadata files:
    - `<submit-dir>/base.json` — shared metadata (links, social, developer identity, taxonomy)
    - `<submit-dir>/i18n/en.json` — English text fields only

**Semantic Self-Check:**
AI must self-check all written fields before proceeding. Ensure all mandatory fields (like pricing tiers, category tags) are fully filled and align with the rules in `references/01-generate-en.md`. Do not execute screenshot tools yet.

**Key rules for Step 1:**

- Taxonomy codes (`categorys`, `tags`, `audiences`) must come from `bat-cli schema en` — never invent
- `website` must be canonical URL without query parameters
- `social` object must always include all 8 keys (`email`, `twitter`, `facebook`, `linkedin`, `instagram`, `youtube`, `tiktok`, `github`); use `""` when not found, never omit keys
- Do **not** set `logo` or `websiteScreenshot` in `base.json` during Step 1 (local files upload automatically at pack/submit)
- Developer fields: extract `developerName` first (verbatim maker name from site); derive `developerType` only from that name; `""` when not found — never guess

---

## Step 2 — Capture Assets & Phase 1 Validation

Once Step 1 text files are ready, grab the visual assets and execute validation.

**Steps:**

1. Capture and fetch assets:
    ```bash
    bat-cli capture-screenshot --website <url> --dir <submit-dir>
    bat-cli fetch-logo --url <absolute-logo-url> --dir <submit-dir>
    ```
2. Execute validation:
    ```bash
    bat-cli validate-phase1 <submit-dir>
    ```

**Fail-Fast Rule:**
If `validate-phase1` fails (Exit Code != 0), **stop the workflow immediately** and report the errors to the user. Do **not** proceed to Step 3, avoiding wasteful LLM translation calls.

_(Note for Agent: Capturing screenshot and fetching logo are performed in Step 2 to ensure we only spend screenshot wait time on text-validated listings, while the validate-phase1 check ensures we do not run expensive translations if validation fails)._

---

## Step 3 — Translate from English

See `references/02-translate-i18n.md` for localization rules, priceNote rules, and examples.

All 28 languages required: `en zh tw es ar id pt fr ja ru de ko tr vi it nl pl th hi uk fa bn ur sv no da fi he`

**Steps:**

1. **Generate isomorphic translation templates**:
   Run the following command to automatically generate `i18n/<lang>.json` template files with placeholders for the other 27 languages:

    ```bash
    bat-cli translate-template <submit-dir> --from en --to all
    ```

    _This command recursively reads the English JSON structure. For new translation items, it populates placeholders like `[TODO: TRANSLATE] English original`. If the file already exists, it only merges and fills missing fields, never overwriting existing translations._
    _It also intelligently skips core validation properties that do not need translation, such as `chargeType`, `recommend`, `url`, `type`, etc._

2. **Translate template placeholders**:
   The AI agent reads these 27 translation template files, replaces the placeholders containing `[TODO: TRANSLATE]` with translations in the respective language, and writes them back.
   It is recommended to translate in batches of 3–4 languages per LLM call in the following order:
    1. `zh`, `tw`, `ja`, `ko`
    2. `de`, `fr`, `it`, `nl`
    3. `es`, `pt`, `vi`, `id`
    4. `ru`, `pl`, `uk`, `tr`
    5. `ar`, `he`, `fa`, `ur`
    6. `hi`, `bn`, `th`
    7. `sv`, `no`, `da`, `fi`

**Key rules:**

- Read only `i18n/en.json` as source — never re-crawl
- Keep array lengths identical to `en.json`
- Never translate `chargeType` values, JSON keys, URLs, or taxonomy slugs
- `priceNote`: translate period/label words only (`month`→`月`); keep currency symbols and amounts unchanged (`$19 /month` → `$19 /月`)
- Localize naturally — rewrite for fluency, not word-for-word
- **Batch self-check:** After writing each translation batch (e.g. `zh, tw, ja, ko`), AI must verify the corresponding JSON files for syntax validity and structure integrity before moving to the next batch.

---

## Step 4 — Pack and Submit

`bat-cli submit` auto-detects new vs update by checking if `website` is already listed.

```bash
# 1. Pack the directory into a single bundle file
bat-cli pack <submit-dir> -o <submit-dir>/submit.bundle.json

# 2. Validate the bundle file against schemas and constraints
bat-cli validate -f <submit-dir>/submit.bundle.json

# 3. Submit the bundle file to the platform
bat-cli submit -f <submit-dir>/submit.bundle.json

# OR execute packing, validation, and submission in a single command:
bat-cli submit --dir <submit-dir>

# 4. Check the processing status of your submission
bat-cli status --id <submitId>
```

At `pack` / `submit --dir`: if `base.json` has no remote asset URLs, the CLI uploads the local logo and website screenshot to CDN and writes the URLs back to `base.json`:

- **Logo auto-conversion**: The CLI automatically converts and compresses the local logo (supporting `webp`, `ico`, `png`, `jpg`, `jpeg`) into a standard `logo.webp` (256×256 WebP, 90% quality) prior to uploading.
- **Screenshot auto-conversion**: The CLI automatically converts and compresses the local website screenshot (supporting `webp`, `png`, `jpg`, `jpeg`) into a optimized `website-screenshot.webp` (max width 1920px, 80% quality) prior to uploading.
- Already-set remote URLs skip the upload.

---

## Reference files

- `references/01-generate-en.md` — Full Phase 1 crawl checklist, `base.json` field guide, `i18n/en.json` field guide, voice rules, pricing tier guide, developer identity rules
- `references/02-translate-i18n.md` — Full Phase 2 localization rules, batching strategy, `priceNote` translation rules with examples
