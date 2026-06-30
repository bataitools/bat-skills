# Step 1 — Extract (Crawl & English Metadata)

**Do NOT generate all languages in one step.** Only produce `base.json` + `i18n/en.json` in this step.

Your job is to **actively crawl and extract** — not summarize the homepage or rewrite it as generic AI marketing copy. Missing optional fields is acceptable only after you have **searched** for them (nav, footer, sitemap, common paths). Use `""` when genuinely not found; **never omit keys** from `links` or `social`.

**Voice rule:** Write like a careful editor quoting the product site — factual, specific, plain. If the site does not say it, you do not say it.

---

## 1.1 Setup & Schema (before writing files)

`<submit-dir>` = per-site folder, e.g. `./submits/www.example.com` (from `bat-cli site-dir <url>` — host lowercased only).

```bash
bat-cli init-site --website <url>
bat-cli schema en
```

- Taxonomy codes (`categorys`, `tags`, `audiences`) **must** come strictly from the `code` field in `bat-cli schema en` output — never invent codes, and never use numeric `id` or `slug` fields.
- **Taxonomy limits**: The maximum number of items allowed is: **10** for `categorys`, **10** for `audiences`, and **15** for `tags`. Select only the most relevant codes.
- `website` must be the canonical product URL **without query parameters**.

---

## 1.2 Mandatory website crawl checklist

Do **not** stop at the homepage. Visit and inspect (fetch HTML, follow nav/footer links):

| Priority               | What to find                                                              | Where to look                                                                                                                                                                                               |
| ---------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pricing**            | `pricingUrl` (in `base.json`)                                             | `/pricing`, `/plans`, `/price`, footer "Pricing"                                                                                                                                                            |
| **About / Docs**       | `docsUrl` (in `base.json`)                                                | `/docs`, `/documents`, `/about`, `/about-us`, `/company`, `/team`                                                                                                                                           |
| **Contact / email**    | `social.email`                                                            | Footer, `/contact`, `mailto:` links, privacy/terms pages                                                                                                                                                    |
| **Logo**               | Find remote logo URL                                                      | Find URL from `<link rel="icon">`, header logo `src`, JSON-LD `Organization.logo`, or `og:image` (prefer square logo over OG banner). (Keep this URL handy for Step 2)                                        |
| **Social profiles**    | `social.*` URLs                                                           | Footer icons, header, `/community`, press kit — see Social table below                                                                                                                                      |
| **Product media**      | `productMedia`                                                            | Homepage hero, features page, embedded YouTube/Vimeo, demo GIFs                                                                                                                                             |
| **Developer identity** | `developerType`, `developerCountry`, `developerProvince`, `developerName` | JSON-LD (`Organization`), About/Team, Privacy/Terms, Contact address, footer legal line, country-code TLD — see strict rules below                                                                          |

If the site uses a client-rendered SPA, try direct path URLs above even when nav is JS-only.

---

## 1.3 `base.json` field guide

### Required shape — always include **all keys** below

```json
{
	"website": "https://example.com",
	"developerName": "",
	"developerType": "",
	"developerCountry": "",
	"developerProvince": "",
	"pricingUrl": "",
	"docsUrl": "",
	"categorys": ["productivity"],
	"tags": ["ai-writing"],
	"audiences": ["developers"],
	"social": {
		"email": "",
		"twitter": "",
		"facebook": "",
		"linkedin": "",
		"instagram": "",
		"youtube": "",
		"tiktok": "",
		"github": ""
	},
	"productMedia": [
		{
			"type": "video",
			"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
			"thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
		},
		{
			"type": "image",
			"url": "https://example.com/assets/demo-screenshot.png"
		}
	]
}
```

`logo` and `websiteScreenshot` in `base.json` are **omitted or left as `""` during Step 1**. Local files (to be grabbed in Step 2) upload automatically at `pack` / `submit` unless `base.json` already has remote `https://...` URLs.

### `productMedia` — gallery items (video + image)

Array of **0–10** promotional demos (homepage carousel, features page, embedded YouTube, product tour). **Not** the website screenshot.

| `type`    | Fields (`url` is required) | Example                                                                                                                  |
| --------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `"video"` | `url`, `thumbnail` (opt)   | `url`: YouTube watch URL / Direct `.mp4` URL<br>`thumbnail`: `https://img.youtube.com/...` (YouTube auto-derived or native poster) |
| `"image"` | `url`                      | Direct image URL: `https://example.com/demo.png`                                                                         |

**Video example (YouTube — preferred when available):**

```json
{
	"type": "video",
	"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
	"thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
}
```

Backend auto-derives `videoId` and thumbnail from YouTube URLs. Do **not** use `"type": "youtube"`.

**Video example (non-YouTube, optional thumbnail):**

```json
{
	"type": "video",
	"url": "https://example.com/assets/product-demo.mp4",
	"thumbnail": "https://example.com/assets/demo-poster.jpg"
}
```

#### 原生视频提取规范 (HTML5 Native Video)

如果在提取页面内容时，页面包含了原生 `<video>` 播放器（例如 `<video class="native-video-player" src="..." poster="..." ...>` 或者是带有 `<source>` 的原生 HTML5 视频），请务必按以下规则提取：
- **视频地址匹配**：提取 `<video>` 本身或子标签 `<source>` 中的 `src` 属性（或 `data-src` 延迟加载属性），作为 `productMedia` 中该项的 `url`。
- **海报封面匹配**：提取 `<video>` 本身中的 `poster` 属性（或 `data-poster`），作为 `productMedia` 中该项的 `thumbnail`。
- **链接规整绝对路径**：如果提取到的链接是相对路径，必须使用当前的网站 URL 进行拼接，保证其是合法的 `https://` 绝对路径。
- **自动化提取工具**：您可以直接在终端运行本 Skill 下的 Python 辅助提取脚本来进行提取，它会自动规整为标准格式：
  ```bash
  python3 bat-skills/skills/bat-submit/scripts/extract_video.py <url_or_local_file_path> [base_url]
  ```

**Image example (feature screenshot / demo slide):**

```json
{
	"type": "image",
	"url": "https://example.com/assets/feature-editor-ui.png"
}
```

Rules:

- `"type"` must be exactly `"video"` or `"image"` — no other values.
- `url` must be absolute `https://`.
- Prefer official promo content from the product site; order matters (first item = primary gallery slot).
- Use `[]` only after checking homepage, features, and docs for embeds or demo images.
- **禁止提取 Logo/Icon**：请勿将网站的 Logo 或应用图标作为 `productMedia` 中的一项进行提取（即使站点缺乏其它演示图片）。

### `pricingUrl` and `docsUrl` — extract primary URLs (in `base.json`)

| Field        | Required       | How to extract                                                                  |
| ------------ | -------------- | ------------------------------------------------------------------------------- |
| `pricingUrl` | Always present | Dedicated pricing/plans page. **Do not** use homepage if a pricing page exists. |
| `docsUrl`    | Always present | Dedicated documentation/about page.                                             |

Use full `https://` URLs. If not found after searching → `""`.

### `social` — extract every profile you can find

| Field       | Required                     | How to extract                                                                                 |
| ----------- | ---------------------------- | ---------------------------------------------------------------------------------------------- |
| `email`     | **Optional** | Public support/contact email from footer, contact page, or `mailto:`. If provided, it must be a valid email syntax. |
| `twitter`   | Always present               | `twitter.com` / `x.com` profile URL                                                            |
| `facebook`  | Always present               | Facebook page URL                                                                              |
| `linkedin`  | Always present               | LinkedIn company or product URL                                                                |
| `instagram` | Always present               | Instagram profile URL                                                                          |
| `youtube`   | Always present               | YouTube channel or official video URL                                                          |
| `tiktok`    | Always present               | TikTok profile URL                                                                             |
| `github`    | Always present               | GitHub org/repo URL                                                                            |

Use full `https://` URLs. If not found → `""`. **Never skip keys.**

### Developer identity — **STRICT: extract `developerName` first, then derive `developerType`**

Work in **two steps**. Never invent. When in doubt → `developerName` and `developerType` both stay `""`.

| Field               | File        |
| ------------------- | ----------- |
| `developerName`     | `base.json` |
| `developerType`     | `base.json` |
| `developerCountry`  | `base.json` |
| `developerProvince` | `base.json` |

#### Step A — `developerName` (strict)

Only write a name that appears **verbatim** on the site as the **maker** (not merely the product title).

**Where to look (in order):**

1. JSON-LD `Organization.legalName` / `name`
2. Privacy / Terms — "Copyright Holder", "operated by", registered entity
3. About / Team / Company pages
4. Footer — `© 2024 …` legal line (not the product tagline)
5. Contact page signature block

**✅ Valid `developerName` examples:**

| Source on site                             | `developerName`      |
| ------------------------------------------ | -------------------- |
| `Copyright Holder: Acme Inc.`              | `Acme Inc.`          |
| `© 2024 OpenAI, L.L.C.`                    | `OpenAI, L.L.C.`     |
| `Built by Pixel Forge Studio`              | `Pixel Forge Studio` |
| About: `John Smith, independent developer` | `John Smith`         |

**❌ Never use as `developerName`:**

| Bad value                                      | Why                        |
| ---------------------------------------------- | -------------------------- |
| Product name only (`Image to STL`, `Notion`)   | Marketing name ≠ developer |
| Bare domain (`imagetostl.me`, `acme.com`)      | Domain ≠ legal entity name |
| Invented suffix (`Imagetostl.me`, `Acme Team`) | Not on the site verbatim   |
| Generic label (`The team`, `Our company`)      | Not a proper name          |
| Email local-part (`support`, `hello`)          | Not a name                 |

If no proper name passes the rules → `developerName: ""`.

#### Step B — `developerType` (derive **only** from `developerName`)

Set `developerType` **only when** `developerName` is non-empty. **Never guess** from product category, pricing, or page tone.

| `developerType` | When `developerName` matches                                                                                                                                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `"company"`     | Official name includes a **legal entity marker**: `Inc`, `Inc.`, `Ltd`, `Ltd.`, `LLC`, `L.L.C.`, `Corp`, `Corporation`, `GmbH`, `S.A.`, `Pty`, `PLC`, `Co., Ltd`, `Limited`, or Privacy/Terms explicitly name a **registered company** with that exact string |
| `"team"`        | Official name includes **Team / Studio / Labs / Collective / Group** as part of the proper name on site (e.g. `Stripe Labs`, `Figma Studio`) — the word must appear in the cited `developerName` string                                                       |
| `"individual"`  | About/team page identifies a **single named person** as the maker and `developerName` is that person's name (no company suffix)                                                                                                                               |

| Situation                                  | `developerType`                      |
| ------------------------------------------ | ------------------------------------ |
| `developerName` is `""`                    | `""`                                 |
| Name is product/brand only (failed Step A) | `""` (keep `developerName` `""` too) |
| Name fits none of the rows above           | `""` — do not default to `company`   |

**Examples:**

| `developerName`                | `developerType`                          |
| ------------------------------ | ---------------------------------------- |
| `Acme Inc.`                    | `company`                                |
| `Pixel Forge Studio`           | `team`                                   |
| `Jane Doe` (solo dev on About) | `individual`                             |
| `Imagetostl.me`                | `""` — domain string, not a company name |
| `Image To STL`                 | `""` — product name only                 |

#### Step C — `developerCountry` / `developerProvince`

Only from **explicit** address or jurisdiction on site. May be `""`. Never guess from TLD, currency, or language.

**Agent submit:** all four fields may be `""` when the site does not disclose them.

---

## 1.4 `i18n/en.json` field guide

### Writing voice — extract first, minimal rewrite

All text fields in `i18n/en.json` must read like **catalog copy grounded in the website**, not like ChatGPT product marketing.

| Priority | Rule                                                                                                                        |
| -------- | --------------------------------------------------------------------------------------------------------------------------- |
| 1        | **Quote or tight-paraphrase** text that already appears on the site (hero, features, pricing, FAQ, docs).                   |
| 2        | **Preserve specifics** — numbers, formats, integrations, limits, platform names exactly as the site states them.            |
| 3        | **Match the site's tone** — if the site is casual/technical/legal, mirror that; do not upscale to corporate brochure voice. |
| 4        | **Synthesize only when needed** to connect facts across pages — still no hype, no invented benefits.                        |
| 5        | If a field has **no source** after search → use `""` (or skip optional prose) rather than inventing filler.                 |

#### Where to pull each field

| Field                        | Primary sources (in order)                                                                                        |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `name`                       | Official product name in `<title>`, header logo alt, JSON-LD `SoftwareApplication.name` — not a rewritten variant |
| `tagline`                    | Homepage hero subhead / H1 adjacent line — **copy verbatim** when ≤120 chars; light trim only                     |
| `description`                | About + Features intro paragraphs — stitch facts; 2–4 short sentences; no opener like "X is a powerful…"          |
| `instruction`                | Getting started / docs / onboarding steps — numbered workflow the site actually describes; `""` if none           |
| `coreFeatures[].title`       | Feature section headings on site                                                                                  |
| `coreFeatures[].description` | First sentence under that heading, or bullet list compressed — keep technical terms                               |
| `useCases[]`                 | "Use cases", "Who it's for", customer stories, industry tabs — one concrete scenario per string                   |
| `faqs[]`                     | **Only** Q&A from FAQ / Help / Docs — do not invent questions                                                     |
| `seo.title`                  | `name` + shortest real value phrase from site (not a new slogan)                                                  |
| `seo.description`            | Factual one-liner from meta description or first substantive paragraph — not a sales pitch                        |

#### Banned AI-isms — never use unless the **site itself** uses the exact phrase

`revolutionize`, `game-changer`, `cutting-edge`, `state-of-the-art`, `leverage`, `unlock`, `empower`, `seamless`, `robust`, `innovative solution`, `next-generation`, `harness the power`, `in today's fast-paced`, `whether you're a … or a …`, `look no further`, `designed to help you`, `take your … to the next level`, `comprehensive suite`, `all-in-one platform` (unless on site), `streamline your workflow` (generic), `boost productivity` (without a specific mechanism from the site).

Also avoid:

- Empty superlatives: `best`, `leading`, `world-class`, `ultimate` (unless in official product name)
- Three-part rhetorical lists that add no fact: "fast, reliable, and secure"
- Opening with `Introducing` / `Meet` / `Discover how`
- Questions in `description` or `tagline` unless the site does

#### Good vs bad (same product)

| Field                        | ❌ AI-flavored                                                              | ✅ Extracted                                                                                                                    |
| ---------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `tagline`                    | "Revolutionize your 3D workflow with our cutting-edge AI converter"         | "Convert PNG and JPG images to STL files for 3D printing"                                                                       |
| `description`                | "ImageToSTL is a powerful, seamless solution designed to empower creators…" | "Upload a heightmap image, adjust scale and depth, download an STL. Supports PNG/JPG up to 20MB. No account for the free tier." |
| `coreFeatures[].description` | "Leverage advanced algorithms for unparalleled mesh quality"                | "Exports watertight STL meshes; slider controls height scale from 0.1× to 10×"                                                  |
| `useCases[]`                 | "Perfect for professionals and hobbyists alike"                             | "Print lithophanes from family photos", "CNC heightmaps for terrain models"                                                     |
| `faqs[].question`            | "What makes us different?"                                                  | "What file formats are supported?" (from site FAQ)                                                                              |

```json
{
	"name": "",
	"tagline": "",
	"description": "",
	"instruction": "",
	"coreFeatures": [{ "title": "", "description": "" }],
	"useCases": ["", "", ""],
	"pricing": [
		{
			"name": "Free",
			"chargeType": "free",
			"priceNote": "Free",
			"features": ["5 conversions per day", "PNG/JPG input", "Standard STL export"]
		},
		{
			"name": "Pro",
			"chargeType": "recurring",
			"priceNote": "$19 /month",
			"recommend": true,
			"features": ["1,750 credits per month", "Max 20MB per file", "High-resolution export"]
		},
		{
			"name": "Flat",
			"chargeType": "flat",
			"priceNote": "$59 one-time",
			"features": ["1,750 credits", "Credits do not expire", "No subscription"]
		}
	],
	"faqs": [{ "question": "...", "answer": "..." }],
	"seo": { "title": "...", "description": "..." }
}
```

### Content minimums (validation)

| Field           | Minimum                                  |
| --------------- | ---------------------------------------- |
| `name`          | ≥ 2 characters                           |
| `tagline`       | ≥ 10 characters                          |
| `description`   | ≥ 50 characters                          |
| `developerName` | ≥ 2 characters                           |
| `coreFeatures`  | ≥ 3 items, each with title + description |
| `useCases`      | ≥ 3 string items                         |
| `pricing`       | ≥ 1 tier                                 |
| `faqs`          | ≥ 3 items                                |

### Pricing tiers (`i18n/en.json` → `pricing[]`)

Crawl the **pricing page** and map **every real tier** the product offers (typically 1–6 plans).

#### Required shape — each tier has **4 or 5 fields**

```json
{
	"name": "Pro",
	"chargeType": "recurring",
	"priceNote": "$19 /month",
	"recommend": true,
	"features": ["Feature A", "Feature B"]
}
```

| Field        | Type     | Rules                                                                                                                                     |
| ------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `name`       | string   | **Required.** Short plan name, ≤ 30 chars (e.g. `"Free"`, `"Pro"`, `"Enterprise"`, `"Lifetime"`).                                         |
| `chargeType` | string   | **Required.** Must be exactly one of: `"free"`, `"recurring"`, `"flat"`, `"contact"` (lowercase).                                         |
| `priceNote`  | string   | **Required.** Human-readable price text, 1–100 chars. Shown on the product page.                                                          |
| `recommend`  | boolean  | **Optional.** Set to `true` if this plan is marked as "Best Value", "Popular", "Recommend" on the site. Omit or set to `false` otherwise. |
| `features`   | string[] | **Required.** Non-empty array; each item is a non-empty string describing what the tier includes.                                         |

**Do NOT use other field names** — these are common mistakes that fail validation:

| ❌ Wrong                                       | ✅ Use instead                                         |
| ---------------------------------------------- | ------------------------------------------------------ |
| `price`, `plan`, `planName`, `tier`            | `priceNote` for display price                          |
| `charge_type`, `billingType`                   | `chargeType`                                           |
| `featureList`, `benefits`                      | `features`                                             |
| `"Free"`, `"Paid"`, `"Freemium"` as chargeType | `"free"`, `"recurring"`, `"flat"`, or `"contact"` only |

#### `chargeType` — when to use which

| Value         | Use when                                       | `priceNote` examples                               |
| ------------- | ---------------------------------------------- | -------------------------------------------------- |
| `"free"`      | $0 tier, free forever, no payment              | `"Free"`, `"$0"`, `"0"`                            |
| `"recurring"` | Monthly/yearly subscription                    | `"$19 /month"`, `"$199/year"`, `"€9/mo"`           |
| `"flat"`      | One-time purchase, lifetime deal, credit packs | `"$59 one-time"`, `"$29"`, `"$10 for 500 credits"` |
| `"contact"`   | Enterprise / custom pricing only               | `"Contact sales"`, `"Custom"`                      |

Put plan limits (credits, seats, API calls, export quality) in **`features`**, not in `priceNote`.

#### Full example — four tier types on one product

```json
"pricing": [
  {
    "chargeType": "free",
    "priceNote": "Free",
    "features": [
      "5 conversions per day",
      "Standard STL export",
      "Community support"
    ]
  },
  {
    "chargeType": "recurring",
    "priceNote": "$19 /month",
    "features": [
      "1,750 credits per month",
      "High-resolution meshes",
      "Priority queue",
      "Cancel anytime"
    ]
  },
  {
    "chargeType": "flat",
    "priceNote": "$59 one-time",
    "features": [
      "1,750 credits",
      "One-time payment",
      "No subscription",
      "Credits never expire"
    ]
  },
  {
    "chargeType": "contact",
    "priceNote": "Contact sales",
    "features": [
      "Custom volume pricing",
      "Dedicated support",
      "SLA & invoicing"
    ]
  }
]
```

Only include tiers that **actually exist** on the website — do not invent plans.

### SEO

- `seo.title`: `name` + shortest factual value phrase from the site (≤ ~60 chars) — not a new slogan
- `seo.description`: one factual sentence from meta description or About/features lead (≤ ~160 chars) — no hype words from the banned list

---

## 1.5 Semantic Self-Check

Before ending Step 1, you must perform both manual and automated verification:

1. **Manual Check**: Verify that all mandatory fields are fully filled, and taxonomy codes (`categorys`, `tags`, `audiences`) come strictly from the `code` field in `bat-cli schema en` (do **NOT** use numeric `id` or `slug` fields, and ensure their counts do not exceed limits: **10** for `categorys`, **10** for `audiences`, and **15** for `tags`).
2. **Automated Verification**: **Run the validation command against the site directory:**
   ```bash
   bat-cli validate-phase1 <submit-dir>
   ```
   *Note: This command only validates text fields in `base.json` and `i18n/en.json` (placeholder references will stand in for missing screenshots/logos during this step).*

**Fail-Fast Rule**:
If `validate-phase1` fails (Exit Code != 0), **you must fix the errors in this step first**. Do **NOT** proceed to Step 2 (Capture) or any subsequent steps until `validate-phase1` passes successfully.

