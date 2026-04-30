# Interoperability

Humanizer is one markdown file. That makes it portable. This doc covers how to use it outside of Claude Code.

---

## Claude Code (primary)

Drop into `.claude/skills/humanizer/SKILL.md` — user-wide (`~/.claude/skills/...`) or project-scoped (`./.claude/skills/...`).

```bash
./install.sh             # user-wide
./install.sh --project   # current project
./install.sh --target /custom/path
```

Invoke with `/humanizer` or by saying "humanize this draft," "scrub AI tells," "final review."

---

## Cursor

Cursor reads project-level rules from `.cursorrules` or the newer `.cursor/rules/` system.

Option A — paste into `.cursorrules`:

```bash
cat SKILL.md >> .cursorrules
```

Option B — newer rules format (`.cursor/rules/humanizer.mdc`):

```bash
mkdir -p .cursor/rules
cat > .cursor/rules/humanizer.mdc <<'EOF'
---
description: Humanizer skill — invoke when user asks to humanize, scrub AI tells, do a final review
globs: ["**/*.md", "**/*.mdx"]
alwaysApply: false
---
EOF
cat SKILL.md >> .cursor/rules/humanizer.mdc
```

Then ask Cursor: "Humanize the highlighted text."

---

## Continue

Continue uses `~/.continue/config.json` and `.continuerc` for project-scoped customization. Add Humanizer as a custom slash command:

```jsonc
{
  "customCommands": [
    {
      "name": "humanize",
      "description": "Scrub AI tells from a draft",
      "prompt": "<paste the contents of SKILL.md here>\n\nApply this skill to the user's draft."
    }
  ]
}
```

Trigger with `/humanize` in the Continue chat.

---

## Aider

Aider reads `.aider.conf.yml` and respects per-project conventions. The cleanest pattern is to keep `SKILL.md` in the repo and ask Aider to load it:

```bash
aider --read SKILL.md
> Use the rules in SKILL.md to humanize the file ./draft.md
```

For repeated use, add to `.aider.conf.yml`:

```yaml
read:
  - SKILL.md
```

---

## Raw Anthropic API

```python
import anthropic
import pathlib

client = anthropic.Anthropic()
system = pathlib.Path("SKILL.md").read_text()

draft = """
[your draft here]
"""

response = client.messages.create(
    model="claude-opus-4-7",   # or claude-sonnet-4-6 for cost savings
    max_tokens=4096,
    system=system,
    messages=[
        {"role": "user", "content": f"Humanize this draft:\n\n{draft}"}
    ],
)

print(response.content[0].text)
```

For best results enable prompt caching on the system prompt — Humanizer's content is stable across calls and caching cuts cost by ~90% after the first call.

```python
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    system=[
        {
            "type": "text",
            "text": system,
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": draft}],
)
```

---

## Raw OpenAI API

The skill is provider-agnostic. Use it as the system message:

```python
from openai import OpenAI
import pathlib

client = OpenAI()
system = pathlib.Path("SKILL.md").read_text()

response = client.chat.completions.create(
    model="gpt-5",          # or whichever current model
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": f"Humanize this draft:\n\n{draft}"},
    ],
    max_tokens=4096,
)

print(response.choices[0].message.content)
```

GPT-class models do reasonable work with this prompt but tend to be more aggressive on rewriting than Claude — leaning toward full rewrites where Claude would patch. Adjust if this matters for your use case (the skill itself doesn't need changes; it's the model's interpretation that differs).

---

## Local models (Ollama, LM Studio, llama.cpp)

The skill works on local models too, with two caveats:

1. **Context window.** `SKILL.md` is ~5K tokens. Plus your draft. Plus output. Use a model with at least 16K context; 32K+ is comfortable.
2. **Pattern recognition quality.** Smaller open-weight models (7B, 13B) catch the obvious vocabulary tells but miss most structural patterns. The skill is calibrated for frontier-class models. If you're running local, expect to use it more as a checklist than an automated pass.

```bash
ollama run llama3.1:70b "$(cat SKILL.md)\n\nHumanize this draft:\n\n$(cat draft.md)"
```

---

## CLI wrapper (community)

There's no official CLI yet (planned for v1.1 — see CHANGELOG). The simplest interim option is a shell function:

```bash
# add to ~/.zshrc or ~/.bashrc
humanize() {
    if [[ -z "$1" ]]; then
        echo "Usage: humanize <file.md>"
        return 1
    fi
    cat ~/.claude/skills/humanizer/SKILL.md > /tmp/humanize-prompt.txt
    echo "" >> /tmp/humanize-prompt.txt
    echo "Humanize this draft:" >> /tmp/humanize-prompt.txt
    echo "" >> /tmp/humanize-prompt.txt
    cat "$1" >> /tmp/humanize-prompt.txt
    # Pipe to your CLI of choice — claude, llm, etc.
    claude --print < /tmp/humanize-prompt.txt
}
```

Adapt to whatever LLM CLI you use (`claude`, `llm`, `anthropic`, `oai`, etc.).

---

## GitHub Actions

See [`docs/integration.md` Pattern 2](integration.md#pattern-2-detect-only-mode-in-ci) for a sketch.

The skill is just markdown, so the action is "load the markdown, prepend it to the changed file, call an LLM API, post the response as a PR comment." No special tooling needed.

---

## Slackbot / chat integration

See [`docs/integration.md`](integration.md) — Slack integration sketch.

The Composio Slack connector, Bolt SDK, or any custom webhook works. The skill content goes in the system prompt; the user's message is the draft.

---

## What does NOT work

- **Browser-based "AI humanizer" SaaS tools that take a paragraph and spit one back.** Different problem space — those run paraphrasing models to lower detector scores. Humanizer is meant to be inside your editing/agent pipeline, not a one-shot paraphrase service.
- **Text editors with no LLM access.** The skill needs an LLM to execute. There's no version that works without one.
- **Real-time streaming inline in editors.** The output format requires the model to see the full draft and produce a structured response. Word-by-word streaming inline doesn't fit the pipeline.

---

## Adding new harness support

If you wire Humanizer into a tool not listed here, open a PR — I'd like the docs to reflect what people are actually doing. The format is loose; one short subsection per harness is plenty.
