# Step 3 — Pack and Submit

Once all 28 language JSON files (`i18n/*.json`) and metadata files (`base.json`) are finalized, perform packing, validation, and submission.

---

## 3.1 Authentication

Before submitting, you must authenticate using the CLI (pick one):
- Guest (no browser): `bat-cli login guest`
- Formal account (OAuth, like `gh auth login`): `bat-cli login`
- API key (CI): `bat-cli login --key <your-api-key>`

---

## 3.2 CLI Commands

You can run each sub-step individually or execute them in a single command.

### Option A: Manual Step-by-Step (Recommended for debugging)

1. **Pack the directory** into a single bundle file (automatically resolves CDN assets from the server):
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

## 3.3 Asset Handling & Server-side Capture

Because asset capture is offloaded to the server, local execution is fully automated:

- **Server-side Auto-Capture (Default)**: If `base.json` contains no remote asset URLs and local asset files (`logo.*`, `website-screenshot.webp`) do not exist, `bat-cli` automatically requests the API to assign server-resolved CDN assets. The Bataitools server will asynchronously crawl the site, capture the screenshot, optimize the logo, and link them to the submission.
- **Manual Override (Optional)**: If you need to enforce a custom logo or screenshot, you can manually place them in the `<submit-dir>` directory. `bat-cli` will detect and validate them during the `pack` command:
  - **Logo**: Must be **under 50KB** (preferably under 20KB). Supported formats: `svg`, `webp`, `ico`, `png`, `jpg`/`jpeg`.
  - **Screenshot**: Must be **under 200KB** and strictly in WebP format (`website-screenshot.webp`).
  If these local files exist, they will be uploaded to the CDN, overriding any server-resolved assets.

---

## 3.4 Check Submission Status

Once submitted, retrieve the submission ID (`submitId`) from the command output, and poll the processing status:

```bash
bat-cli status --id <submitId>
```

The platform will review and process the bundle. Make sure to monitor this status until it is marked as processed or returns an error.
