# BAT AI Tools — Agent Skills

> **Tell your AI agent one sentence. Your tool gets listed on [bataitools.com](https://bataitools.com) in 28 languages — no web forms, no platform fees.**

Portable [Agent Skills](https://skills.sh/) that teach AI coding agents (Cursor, Claude Code, Windsurf, Cline, and 14+ more) how to submit AI tools to the BAT directory via [`bat-cli`](https://www.npmjs.com/package/@bataitools/bat-cli).

[![skills.sh](https://skills.sh/b/bataitools/bat-skills)](https://skills.sh/bataitools/bat-skills/bat-submit)

---

## Available Skills

| Skill | Description |
| :--- | :--- |
| [**bat-submit**](./skills/bat-submit/SKILL.md) | 3-step workflow — extract metadata, translate into 28 languages, pack & submit to bataitools.com |

---

## Quick Start

### 1. Install `bat-cli`

```bash
npm install -g @bataitools/bat-cli@latest
# or
bun add -g @bataitools/bat-cli@latest
```

### 2. Install the Skill

```bash
# Project scope
npx skills add bataitools/bat-skills --skill bat-submit

# Global — available in every project (recommended)
npx skills add bataitools/bat-skills --skill bat-submit -g -y

# Target specific editors at once
npx skills add bataitools/bat-skills --skill bat-submit -g -y -a cursor,claude-code,codex,windsurf
```

### 3. Submit with one prompt

Open your AI agent and say:

```
Submit https://your-product.com to BAT AI Tools
```

Or in Chinese:

```
提交 https://your-product.com 到 bataitools
```

The agent runs the full workflow automatically. First `bat-cli` use creates a guest device account — no sign-up required.

---

## What the Skill Does (3 Steps)

| Step | Action | Output |
| :--- | :--- | :--- |
| **1. Extract** | Crawl the target site, fill English metadata | `base.json`, `i18n/en.json` |
| **2. Translate** | Localize into 27 other languages (batched, 2–4 per round) | `i18n/*.json` (28 total) |
| **3. Submit** | Pack, validate, authenticate, POST to BAT API | Submission queued for review |

Logo and screenshots are resolved on the BAT server during submit — no local browser capture required.

Typical review time: **~24 hours**. Live URL: `https://bataitools.com/tools/{slug}`

---

## Supported Agents

Any editor that loads `SKILL.md` skills:

Cursor · Claude Code · Windsurf · Cline · GitHub Copilot · Gemini CLI · Codex CLI · Continue · Roo Code · Antigravity · Kiro · VS Code · Zed · and more.

Full list on the [submit page](https://bataitools.com/submit).

---

## Update Installed Skills

```bash
npx skills update
```

---

## Manual Setup (Alternative)

```bash
git clone https://github.com/bataitools/bat-skills.git
mkdir -p .cursor/skills
cp -r bat-skills/skills/bat-submit .cursor/skills/bat-submit
```

---

## Releases

Tag a version to trigger CI packaging:

```bash
git tag v1.x.x && git push origin v1.x.x
```

Skill zips are attached to [GitHub Releases](https://github.com/bataitools/bat-skills/releases).

---

## Links

- **Directory:** [bataitools.com](https://bataitools.com)
- **Submit guide:** [bataitools.com/submit](https://bataitools.com/submit)
- **skills.sh listing:** [skills.sh/bataitools/bat-skills](https://skills.sh/bataitools/bat-skills)
- **CLI package:** [@bataitools/bat-cli on npm](https://www.npmjs.com/package/@bataitools/bat-cli)

---

## License

MIT — see [LICENSE](LICENSE).
