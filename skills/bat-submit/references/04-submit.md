# Step 4 — Pack and Submit

Once all 28 language JSON files (`i18n/*.json`) and metadata files (`base.json`) are finalized and validated, perform packing, final validation, and submission.

---

## 4.1 CLI Commands

You can run each sub-step individually or execute them in a single command.

### Option A: Manual Step-by-Step (Recommended for debugging)

1. **Pack the directory** into a single bundle file:
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

## 4.2 Asset Processing & CDN Upload

At `pack` or `submit --dir`, the CLI automatically handles the local assets:

- **Upload Trigger**: If `base.json` has no remote asset URLs (i.e. `logo` and `websiteScreenshot` are empty or omitted), the CLI automatically uploads the local logo and website screenshot to the platform's CDN, and then writes the generated remote URLs back to `base.json`.
- **Logo Auto-Conversion & Compression**: The CLI automatically converts and compresses the local logo file (supporting formats: `webp`, `ico`, `png`, `jpg`, `jpeg`) into a standard `logo.webp` (256×256 pixels, WebP, 90% quality) prior to uploading. **Note**: If the logo is an `svg` or `ico` file, it will bypass this conversion and be uploaded directly in its original format (prioritizing SVG and ICO).
- **Screenshot Auto-Conversion & Compression**: The CLI automatically converts and compresses the local website screenshot (supporting formats: `webp`, `png`, `jpg`, `jpeg`) into an optimized `website-screenshot.webp` (maximum width 1920px, 80% quality) prior to uploading.
- **Skipping Remote Assets**: If `base.json` already contains remote `https://...` URLs for `logo` or `websiteScreenshot`, the CLI will skip uploading local files.

---

## 4.3 Check Submission Status

Once submitted, retrieve the submission ID (`submitId`) from the command output, and poll the processing status:

```bash
bat-cli status --id <submitId>
```

The platform will review and process the bundle. Make sure to monitor this status until it is marked as processed or returns an error.
