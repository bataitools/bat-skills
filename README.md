# BAT AI Tools — Agent Skills

A collection of portable Agent Skills (instructions, workflows, and schemas) designed to teach AI coding agents (such as Claude Code, Cursor, GitHub Copilot, and Gemini) how to interact with the BAT AI Tools ecosystem.

## Available Skills

| Skill | Path | Description |
| :--- | :--- | :--- |
| **bat-submit** | [`skills/bat-submit/SKILL.md`](./skills/bat-submit/SKILL.md) | Guides the AI agent through the 4-step workflow (extract, assets, translate, and submit) to submit AI tools to [bataitools.com](https://bataitools.com) via `bat-cli`. |

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
ln -s /path/to/bat-skills/skills/bat-submit .cursor/skills/bat-submit
```

---

## How to Use

Once the skill is installed in your project, it will be automatically loaded by your AI coding assistant (such as Cursor, Claude Code, Cline, or Gemini). You can trigger it in your chat using natural language.

### Triggering the Skill

Simply ask your AI assistant to submit or list a website. For example:
- *"Submit AI tool https://example.com to bataitools"*
- *"提交 AI 工具 https://example.com 到 bataitools"*
- *"Run bat-cli submit for https://example.com"*

The AI agent will automatically detect the trigger, load the workflow defined in `SKILL.md`, and execute the 4-step process (extract metadata, capture assets, translate, and package submit) autonomously.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
