# Step 2 — Agent-Side Assets Generation & Phase 1 Validation

Once Step 1 text files are ready, the AI Agent must generate visual assets locally, perform the necessary formatting and compression, and execute Phase 1 validation.

---

## 2.1 Generate Assets (Agent-Side Responsibility)

The `bat-cli` does **not** handle web screenshot capturing or logo formatting anymore. It strictly acts as a validation and upload channel. The AI Agent must generate and prepare the visual assets locally using its own scripts/tools.

### 1. Logo Specifications
- **Locate and Download**: Search for the tool's logo on the target site (or favicon), download it using a simple fetch request, and save it under `<submit-dir>` as `logo.webp` (preferred), `logo.svg`, or `logo.png`.
- **Constraint**: The final logo file size **must be under 50KB**. If it exceeds 50KB, the Agent must write a lightweight script (e.g., Python PIL/Pillow or Node.js canvas) to compress it down to under 50KB.
- **base.json check**: Do not put a remote logo URL in `base.json` unless the user explicitly requested a custom CDN URL.

### 2. Website Screenshot Specifications
- **Dimension**: The screenshot must be captured at **1080p resolution** (typically width `1920` pixels, height dynamically adjusted).
- **Format**: It **must be in WebP format** (saved strictly as `<submit-dir>/website-screenshot.webp`). PNG or other formats will be rejected by the CLI.
- **Constraint**: The screenshot file size **must be under 200KB** (recommended size is several tens of KBs). If the captured WebP is too large, the Agent must write a Python/Node script to compress it (e.g., setting WebP quality to 75-80, or resizing dimensions) until it is under 200KB.
- **base.json check**: Do not put a remote websiteScreenshot URL in `base.json`.

---

## 2.2 Execute Phase 1 Validation

Run the validation command against the site directory:

```bash
bat-cli validate-phase1 <submit-dir>
```

**Fail-Fast Rule:**
If `validate-phase1` fails (Exit Code != 0), **stop the workflow immediately** and report the errors to the user. Do **not** proceed to Step 3 (Translate), avoiding wasteful LLM translation calls.

---

## 2.3 Pre-validation self-check

Before stopping Step 2, verify:

- [ ] `code` field from `bat-cli schema en` used for taxonomy (do not use numeric `id` or `slug` fields)
- [ ] `pricingUrl` and `docsUrl` are extracted in `base.json` — searched nav/footer/common paths
- [ ] `social` has all 8 keys — searched footer/social icons/contact page
- [ ] `social.email` is a valid public email (or flagged to user if truly unavailable)
- [ ] Local logo file (`logo.svg`, `logo.webp`, etc.) exists in `<submit-dir>` and is **under 50KB** (or `base.json` has a remote `logo` URL)
- [ ] Local screenshot file `website-screenshot.webp` exists in `<submit-dir>`, is in **WebP format**, and is **under 200KB** (or `base.json` has a remote `websiteScreenshot` URL)
- [ ] Each `pricing[]` item has only `name`, `chargeType`, `priceNote`, `features`, `recommend` (no `price` / `plan` typos)
- [ ] `chargeType` is one of: `free`, `recurring`, `flat`, `contact`
- [ ] Pricing tiers match the live pricing page
- [ ] `productMedia` uses only `"video"` / `"image"` types with valid URLs (or `[]` after search)
- [ ] **`developerName`**: proper maker name cited on site, or `""` (not product name, not domain)
- [ ] **`developerType`**: derived from `developerName` only (`company` / `team` / `individual`), or `""` — never guessed
- [ ] **`developerCountry` / `developerProvince`**: cited on site, or both `""`
- [ ] `validate-phase1` passes
- [ ] **Voice:** `tagline` / `description` / features cite real site facts; no banned AI-isms unless on the site verbatim
- [ ] **FAQs:** every Q&A traceable to FAQ/docs/help — none invented
- [ ] **Specifics:** numbers, formats, limits match the pricing/features pages

When `validate-phase1` passes, proceed directly to Step 3 (Translate) in the same session.
