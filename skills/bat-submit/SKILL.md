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

See `references/01-extract.md` for the complete crawl checklist, field guides, and voice rules.

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
AI must self-check all written fields before proceeding. Ensure all mandatory fields (like pricing tiers, category tags) are fully filled and align with the rules in `references/01-extract.md`. Do not execute screenshot tools yet.

**Key rules for Step 1:**

- Taxonomy codes (`categorys`, `tags`, `audiences`) must come from `bat-cli schema en` — never invent
- `website` must be canonical URL without query parameters
- `social` object must always include all 8 keys (`email`, `twitter`, `facebook`, `linkedin`, `instagram`, `youtube`, `tiktok`, `github`); use `""` when not found, never omit keys
- Do **not** set `logo` or `websiteScreenshot` in `base.json` during Step 1 (local files upload automatically at pack/submit)
- Developer fields: extract `developerName` first (verbatim maker name from site); derive `developerType` only from that name; `""` when not found — never guess

---

## Step 2 — Capture Assets & Phase 1 Validation

Once Step 1 text files are ready, grab the visual assets and execute validation. See `references/02-capture.md` for asset capturing commands and the pre-validation self-check list.

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

See `references/03-translate.md` for localization rules, priceNote rules, and examples.

All 28 languages required: `en zh tw es ar id pt fr ja ru de ko tr vi it nl pl th hi uk fa bn ur sv no da fi he`

**Steps:**

1. **Direct Translation & Diff Merge**:
   AI must read `i18n/en.json` (as the sole source — do not re-crawl or fetch from the web) and generate or update the other 27 required language files (`i18n/<lang>.json`).
   - **If the target file does not exist**: Translate the entirety of `en.json` and save the complete translated JSON.
   - **If the target file already exists**: Load its existing translation, perform an in-memory diff merge to preserve existing translations, translate only new or modified keys, and save the updated JSON back.
   - **Constraint**: Strictly follow all format constraints, translation rules, and skipped fields detailed in `references/03-translate.md`.

2. **Execution Order & Self-Check**:
   Translate and save the files in batches of 3–4 languages in the following order. After writing each batch, immediately verify the corresponding JSON files for syntax and structure validity before moving to the next batch:
    1. `zh`, `tw`, `ja`, `ko`
    2. `de`, `fr`, `it`, `nl`
    3. `es`, `pt`, `vi`, `id`
    4. `ru`, `pl`, `uk`, `tr`
    5. `ar`, `he`, `fa`, `ur`
    6. `hi`, `bn`, `th`
    7. `sv`, `no`, `da`, `fi`

---

## Step 4 — Pack and Submit

See `references/04-submit.md` for bundle packing guides, WebP conversion details, and status checking constraints.

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

- `references/01-extract.md` — Full crawl checklist, `base.json` & `i18n/en.json` field guide, voice rules, and constraints for Step 1 (Extract).
- `references/02-capture.md` — Asset capture commands (`capture-screenshot`/`fetch-logo`), local layout rules, and `validate-phase1` self-check checklist for Step 2 (Capture).
- `references/03-translate.md` — Multi-language localization rules, 28 languages batching strategy, and `priceNote` translations for Step 3 (Translate).
- `references/04-submit.md` — CLI commands, bundle packing guides, automatic WebP assets conversion, CDN uploads, and status checking for Step 4 (Submit).
