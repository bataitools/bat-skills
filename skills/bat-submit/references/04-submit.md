# Step 4 — Pack and Submit

Once all 28 language JSON files (`i18n/*.json`) and metadata files (`base.json`) are finalized and validated, perform packing, final validation, and submission.

---

## 4.0 Authentication

Before submitting, you must authenticate using the CLI (pick one):
- Guest (no browser): `bat-cli login guest`
- Formal account (OAuth, like `gh auth login`): `bat-cli login`
- API key (CI): `bat-cli login --key <your-api-key>`

---

## 4.1 CLI Commands

You can run each sub-step individually or execute them in a single command.

### Option A: Manual Step-by-Step (Recommended for debugging)

1. **Pack the directory** into a single bundle file (runs size/format checks on assets and uploads them if needed):
   ```bash
   bat-cli pack <submit-dir> -o <submit-dir>/submit.bundle.json
   ```
2. **Validate the bundle file** against API schemas and platform constraints:
   ```bash
   bat-cli validate -f <submit-dir>/submit.bundle.json
   ```
3. **Submit the bundle file** to the platform:
   ```bash
   bat-cli submit -f <submit-dir>/submit.bundle.json
   ```

### Option B: All-in-One Command

To execute packing, validation, and submission in a single run:
```bash
bat-cli submit --dir <submit-dir>
```

---

## 4.2 Asset Verification & CDN Upload

At `pack` or `submit --dir`, the CLI handles the upload of local assets with strict validation rules:

- **Strict Asset Rules**:
  - **Logo**: Must be **under 50KB**. Accepted formats: `svg`, `webp`, `ico`, `png`, `jpg` / `jpeg` — **WebP is not required**. The CLI may auto-compress oversized logos (>20KB) to `logo.webp` before upload; logos under 20KB or SVG logos under the size limit (50KB) are kept as-is.
  - **Website Screenshot**: Must be **under 200KB** and **strictly in WebP format** (`website-screenshot.webp`). Any size or format violations will abort packing/submission.
- **Upload Trigger**: If `base.json` has no remote asset URLs (i.e. `logo` and `websiteScreenshot` are empty or omitted), the CLI automatically uploads the local logo and website screenshot to the platform's CDN, and then writes the generated remote URLs back to `base.json`.
- **Skipping Remote Assets**: If `base.json` already contains remote `https://...` URLs for `logo` or `websiteScreenshot`, the CLI will skip uploading local files.

---

## 4.3 Check Submission Status

Once submitted, retrieve the submission ID (`submitId`) from the command output, and poll the processing status:

```bash
bat-cli status --id <submitId>
```

The platform will review and process the bundle. Make sure to monitor this status until it is marked as processed or returns an error.
