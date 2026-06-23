# BAT AI Tools — Agent Skills

A collection of portable Agent Skills (instructions, workflows, and schemas) designed to teach AI coding agents (such as Claude Code, Cursor, GitHub Copilot, and Gemini) how to interact with the BAT AI Tools ecosystem.

## Available Skills

| Skill | Path | Description |
| :--- | :--- | :--- |
| **bat-submit** | [`bat-submit/SKILL.md`](./bat-submit/SKILL.md) | Guides the AI agent through the 3-phase workflow (English crawl, translation, and packing) to submit AI tools to [bataitools.com](https://bataitools.com) via `bat-cli`. |

---

## Installation

You can install these skills directly into your local project environment using the community `skills` CLI or the official GitHub CLI.

### Option 1: Using `npx skills` (Recommended)

Run the following command in your project root to add the `bat-submit` skill:

```bash
npx skills add https://github.com/bataitools/bat-skills --skill bat-submit
```

This will download the skill and place it in your local configuration directory (e.g., `.cursor/skills/` or similar depending on your agent), allowing your AI assistant to automatically reference it.

To update installed skills to the latest version:
```bash
npx skills update
```

### Option 2: Manual Link / Copy

If you prefer manual setup, you can clone this repository and symlink or copy the desired skill directory to your project's AI config directory:

```bash
# E.g., for Cursor:
mkdir -p .cursor/skills
ln -s /path/to/bat-skills/bat-submit .cursor/skills/bat-submit
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
