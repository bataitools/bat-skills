# Step 2 — Capture Assets & Phase 1 Validation

Once Step 1 text files are ready, grab the visual assets and execute validation.

## 2.1 Environment Requirements (Playwright)

`bat-cli capture-screenshot` requires the Playwright chromium browser. Prior to running submission tasks, please ensure it is installed:

```bash
npx playwright install chromium
```

*(While the CLI will attempt to auto-install this browser on the first run of `capture-screenshot`, pre-installing is highly recommended to avoid execution delays or environment-specific timeout issues).*

---

## 2.2 Capture Screenshot & Fetch Logo

Capture the product screenshot locally:

```bash
bat-cli capture-screenshot --website <url> --dir <submit-dir>
```

After finding a logo URL from the site (see crawl checklist in Step 1), fetch and process it locally:

```bash
bat-cli fetch-logo --url <absolute-logo-url> --dir <submit-dir>
```

- **Logo:** save as `<submit-dir>/logo.svg`, `logo.ico` or `logo.webp` (SVG and ICO will not be converted to WebP; other formats will be converted to 256×256 WebP via `fetch-logo` / `pack`). **Do not put a remote URL in `base.json` during Step 1 & Step 2** unless the user supplied a custom CDN URL.
- **Screenshot:** save locally as `<submit-dir>/website-screenshot.png` (same level as `base.json`). **Do not upload in Step 2.** Upload happens automatically at Step 4 `pack` / `submit` unless `base.json` already has a remote `websiteScreenshot` URL.

---

## 2.3 Execute Phase 1 Validation

Run the validation command against the site directory:

```bash
bat-cli validate-phase1 <submit-dir>
```

**Fail-Fast Rule:**
If `validate-phase1` fails (Exit Code != 0), **stop the workflow immediately** and report the errors to the user. Do **not** proceed to Step 3 (Translate), avoiding wasteful LLM translation calls.

---

## 2.4 Pre-validation self-check

Before stopping Step 2, verify:

- [ ] `code` field from `bat-cli schema en` used for taxonomy (do not use numeric `id` or `slug` fields)
- [ ] `pricingUrl` and `docsUrl` are extracted in `base.json` — searched nav/footer/common paths
- [ ] `social` has all 8 keys — searched footer/social icons/contact page
- [ ] `social.email` is a valid public email (or flagged to user if truly unavailable)
- [ ] Local logo file (`logo.svg`, `logo.webp`, etc.) exists in `<submit-dir>` **or** `base.json` has a remote `logo` URL
- [ ] `website-screenshot.png` exists in `<submit-dir>` (via `capture-screenshot --dir`) **or** `base.json` has a remote `websiteScreenshot` URL
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
