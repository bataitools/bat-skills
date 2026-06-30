# Step 2 — Agent-Side Assets Generation & Phase 1 Validation

Once Step 1 text files are ready, the AI Agent must acquire the tool's logo and capture a screenshot using the unified `bat-cli` commands, then execute Phase 1 validation.

---

## 2.1 Retrieve Assets using `bat-cli` (Automated & Low-dependency)

The `bat-cli` provides native commands to download logos and capture website screenshots. These commands automatically manage headless browsers, dimensions, WebP conversion, and size compression.

### 1. Logo Retrieval
Run the following command to download the remote logo (e.g. from favicon or Organization JSON-LD Organization.logo extracted in Step 1) and automatically compress it to WebP format under 20KB:
```bash
bat-cli fetch-logo --url <logo-url> --dir <submit-dir>
```
*Note: If the logo exceeds size limits or is in a non-WebP/non-SVG format, the CLI will automatically optimize and compress it into `<submit-dir>/logo.webp`.*

### 2. Website Screenshot Capture
Run the following command to automatically launch a local headless browser, capture a 1080p screenshot of the site, and compress it to a WebP file under 100KB:
```bash
bat-cli capture-screenshot --website <url> --dir <submit-dir>
```
*Note: This command will attempt to use your local system browser (Chrome/Edge/Chromium/Firefox) first, falling back to Playwright only if none are found. It outputs a highly optimized WebP file directly under `<submit-dir>/website-screenshot.webp`.*

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
- [ ] `pricingUrl` and `docsUrl` are extracted in `base.json`
- [ ] `social` has all 8 keys
- [ ] `social.email` is a valid public email, or left as `""` (empty string) if truly unavailable
- [ ] Local logo file (`logo.webp`, `logo.svg`, etc.) exists in `<submit-dir>` and is **under 50KB** (preferably under 20KB)
- [ ] Local screenshot file `website-screenshot.webp` exists in `<submit-dir>`, is in **WebP format**, and is **under 200KB** (preferably under 100KB)
- [ ] Each `pricing[]` item has only `name`, `chargeType`, `priceNote`, `features`, `recommend`
- [ ] `chargeType` is one of: `free`, `recurring`, `flat`, `contact`
- [ ] `productMedia` uses only `"video"` / `"image"` types with valid URLs
- [ ] **`developerName`**: proper maker name cited on site, or `""`
- [ ] **`developerType`**: derived from `developerName` only (`company` / `team` / `individual`), or `""`
- [ ] **`developerCountry` / `developerProvince`**: cited on site, or both `""`
- [ ] `validate-phase1` passes

When `validate-phase1` passes, proceed directly to Step 3 (Translate) in the same session.
