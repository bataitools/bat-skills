# Step 2 — Agent-Side Assets Generation & Phase 1 Validation

Once Step 1 text files are ready, the AI Agent must generate visual assets locally, perform the necessary formatting and compression, and execute Phase 1 validation.

---

## 2.1 Generate Assets (Agent-Side Responsibility)

The `bat-cli` does **not** handle web screenshot capturing or logo formatting anymore. It strictly acts as a validation and upload channel. The AI Agent must generate and prepare the visual assets locally using its own scripts/tools.

### 1. Logo Specifications

- **Locate and Download**: Search for the tool's logo on the target site (or favicon), download it using a simple fetch request, and save it under `<submit-dir>` as `logo.webp` (preferred), `logo.svg`, or `logo.png`.
- **Constraint**: The final logo file size **must be under 20KB**. If it exceeds 20KB, the Agent must write a lightweight script (e.g., Python PIL/Pillow or Node.js canvas) to compress it down to under 20KB.
- **base.json check**: Do not put a remote logo URL in `base.json` unless the user explicitly requested a custom CDN URL.

### 2. Website Screenshot Specifications

- **Dimension**: The screenshot must be captured at **1080p resolution** (typically width `1920` pixels, height dynamically adjusted).
- **Format**: It **must be in WebP format** (saved strictly as `<submit-dir>/website-screenshot.webp`). PNG or other formats will be rejected by the CLI.
- **Constraint**: The screenshot file size **must be under 100KB** (recommended size is several tens of KBs). If the captured WebP is too large, the Agent must write a Python/Node script to compress it (e.g., setting WebP quality to 75-80, or resizing dimensions) until it is under 100KB.
- **base.json check**: Do not put a remote websiteScreenshot URL in `base.json`.
- **Recommended Capture Method (Do NOT install Playwright/Puppeteer inside virtual environments to prevent OOM)**:
  Since the agent runs on the user's host machine (which may be macOS, Windows, or Linux), you should avoid downloading and installing heavy browser runtimes like Playwright or Puppeteer. Instead, use these lightweight, multi-platform approaches:
  
  **Option A: Multi-Platform System Browser Headless (Recommended & Safest)**:
  First, detect the host OS and find the first executable browser path that exists:
  - **macOS**:
    1. `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`
    2. `"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"`
    3. `"/Applications/Chromium.app/Contents/MacOS/Chromium"`
  - **Windows**:
    1. `"C:\Program Files\Google\Chrome\Application\chrome.exe"`
    2. `"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"`
    3. `"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"`
  - **Linux**:
    - Query commands available in PATH: `google-chrome`, `google-chrome-stable`, `chromium-browser`, `chromium`

  Once a browser binary path is resolved, execute it in headless mode to capture a PNG screenshot (the syntax is identical for Chrome, Edge, and Chromium):
  ```bash
  "<resolved-browser-path>" --headless --disable-gpu --screenshot=<submit-dir>/temp.png --window-size=1920,1080 <url>
  ```
  Then, convert and compress the PNG image to WebP (under 100KB) and clean up the temporary file:
  - **On macOS (Native tool)**:
    ```bash
    sips -s format webp <submit-dir>/temp.png --out <submit-dir>/website-screenshot.webp
    rm <submit-dir>/temp.png
    ```
  - **Cross-Platform (Python Pillow)**: If Python is available, execute a lightweight Python script:
    ```python
    from PIL import Image
    im = Image.open("<submit-dir>/temp.png")
    im.save("<submit-dir>/website-screenshot.webp", "WEBP", quality=75)
    ```
    This only requires installing Pillow (`pip install Pillow`), which is fast, lightweight, and prevents OOM.
  - **Cross-Platform (Node.js)**: If global or local `sharp` is available, write a quick script to do the conversion.

  **Option B: Direct `npx playwright` (Fallback)**:
  If Playwright is already installed globally, or you prefer to run it as a global utility without downloading browsers into the local virtual environment:
  ```bash
  npx playwright screenshot --viewport-size=1920,1080 <url> <submit-dir>/website-screenshot.webp
  ```
  Fallback to Option A immediately if any installation or OOM errors occur.



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
- [ ] Local logo file (`logo.svg`, `logo.webp`, etc.) exists in `<submit-dir>` and is **under 20KB** (or `base.json` has a remote `logo` URL)
- [ ] Local screenshot file `website-screenshot.webp` exists in `<submit-dir>`, is in **WebP format**, and is **under 100KB** (or `base.json` has a remote `websiteScreenshot` URL)
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
