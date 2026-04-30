# Humanizer

> A drop-in skill for Claude Code (and any LLM agent) that scrubs AI tells out of your writing before it ships.

Humanizer is a **portable writing skill** — a single markdown file you can install into Claude Code, paste into Cursor, or use as a system prompt with the Anthropic, OpenAI, or any other API. It catches the structural and vocabulary patterns that make AI-generated writing read as obviously AI-generated, then rewrites the offending spans without flattening the writer's voice.

It's not a stylechecker. It's a final pre-delivery pass that runs before you click send.

---

## What it does

Given a draft, Humanizer:

1. **Detects the channel** (email, Slack, LinkedIn, blog, case study, landing page, newsletter, agenda, etc.) and picks the right strictness profile.
2. **Scans for AI tells in priority order:**
   - **Structural** — dramatic reframes ("This isn't X. This is Y."), manufactured punchlines, staccato uniformity, runway sentences, performative directness, copula avoidance, anaphora, and more.
   - **Vocabulary** — three-tier word system (always-replace, cluster-flag, density-flag).
   - **Positive checks** — does the draft have a point of view, a specific number, a named entity?
   - **Context** — punctuation budgets, banned openers, register-appropriate forms.
3. **Decides patch vs. full rewrite** based on hit density.
4. **Rewrites** at the chosen depth, preserving the writer's voice and argument.
5. **Self-audits** the rewrite by asking *"What makes this still obviously AI generated?"* — and revises again if the answer isn't "nothing."
6. **Emits** a final draft + a structured report (issues found, what changed, residual tells, channel detected, voice loaded).

The output shape is stable, so other agents in your pipeline can parse it.

---

## Why it exists

LLMs don't write badly because they pick the wrong words. They write badly because they default to a small set of structural patterns: dramatic reframes, neat tricolons, runway sentences before the real sentence, and inspirational pivots that weren't earned. A draft can use zero "banned" words and still read like a robot.

Most "humanizer" tools treat this as a vocabulary problem. Humanizer treats it as a **structure-first** problem — which is why the scan order matters: structural tells before vocab, vocab before positive checks, positive checks before context.

The detection patterns are synthesized from public AI-writing research (Carnegie Mellon, Wikipedia editor guidance, Buffer's 52M-post LinkedIn analysis, plus several open-source taxonomies — see `SKILL.md` §9).

---

## Quick start

### Claude Code

```bash
git clone https://github.com/<you>/humanizer.git
mkdir -p ~/.claude/skills/humanizer
cp humanizer/SKILL.md ~/.claude/skills/humanizer/SKILL.md
```

Then in Claude Code:

```
/humanizer

(or: humanize this draft, scrub AI tells, final review)
```

For a project-scoped install, drop `SKILL.md` into `.claude/skills/humanizer/` in any repo.

### Other agents (Cursor, Continue, Aider, etc.)

Most agent harnesses accept markdown context files. Either:
- Paste the contents of `SKILL.md` into your agent's system prompt or rules file, or
- Reference the file path in whatever your tool calls "agent context" / "project rules."

### Raw Anthropic / OpenAI API

Use `SKILL.md` as the system prompt. The skill is self-contained — it doesn't depend on any tools beyond standard text I/O.

```python
import anthropic, pathlib

system = pathlib.Path("humanizer/SKILL.md").read_text()
draft  = pathlib.Path("draft.md").read_text()

client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    system=system,
    messages=[{"role": "user", "content": draft}],
)
print(msg.content[0].text)
```

See [`docs/interoperability.md`](docs/interoperability.md) for more harness examples.

---

## First-run setup (optional but recommended)

Humanizer works with zero configuration. To make it sharper for your voice or your brand:

```
humanizer setup
```

The skill walks you through a 7-question interview — your channels, sample writing, quirks to preserve, hard nos, punctuation preferences, domain vocabulary — and produces a populated voice profile file you can keep editing.

You can also skip the interview and copy [`examples/author-voice.example.md`](examples/author-voice.example.md) or [`examples/brand-voice.example.md`](examples/brand-voice.example.md), then fill in the blanks.

---

## What's in the box

| File | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | The skill itself — the only file you strictly need. |
| [`examples/author-voice.example.md`](examples/author-voice.example.md) | Template for a personal voice profile. |
| [`examples/brand-voice.example.md`](examples/brand-voice.example.md) | Template for a brand/organizational voice profile. |
| [`examples/before-after-email.md`](examples/before-after-email.md) | Worked example — sales email. |
| [`examples/before-after-linkedin.md`](examples/before-after-linkedin.md) | Worked example — LinkedIn post. |
| [`examples/before-after-blog.md`](examples/before-after-blog.md) | Worked example — blog intro. |
| [`docs/voice-profiles.md`](docs/voice-profiles.md) | How to write a voice profile that actually changes the output. |
| [`docs/integration.md`](docs/integration.md) | Patterns for chaining Humanizer with other writing/review agents. |
| [`docs/interoperability.md`](docs/interoperability.md) | Using Humanizer outside Claude Code (Cursor, Continue, raw API, CI). |
| [`install.sh`](install.sh) | One-line installer for Claude Code. |

---

## How it differs from generic "AI humanizer" tools

Most tools take AI-generated text and run it through paraphrasing models. They lower detector scores; they don't make the writing better.

Humanizer is the opposite shape:

- **Structural before vocabulary.** Most of the AI-tell signal is in *how* the sentences are arranged, not which words are picked. Swapping "leverage" for "use" is necessary but rarely sufficient.
- **Voice-preserving.** The skill takes a voice profile (yours or your brand's) and refuses to flatten it. Short sentences, "And"/"But" starts, deliberate fragments — all preserved when the profile says so.
- **Honest about hollow drafts.** A draft that passes every AI-tells check but says nothing specific gets flagged `[HOLLOW]` rather than silently approved. The model won't manufacture facts to fill the gap.
- **Audited by itself.** After the rewrite, the skill asks itself *"what makes this still obviously AI generated?"* and revises again. This second pass catches more than any single sweep.
- **Auditable output.** You see what was flagged, what changed, and what the model thinks is still off. No black-box paraphrase.

---

## Roadmap

- A small CLI wrapper so you can pipe text through Humanizer outside any agent harness (`cat draft.md | humanizer`).
- Optional GitHub Action that runs Humanizer on `.md` files in PRs and posts the diff as a review comment.
- Drop-in Slack / Linear bot for teams that want shared voice enforcement.

Pull requests welcome. The pattern catalog in `SKILL.md` §3 is the most valuable part of this repo — additions there (with examples) are the highest-leverage contribution.

---

## License

MIT. See [`LICENSE`](LICENSE). Use it, fork it, ship it inside paid products, modify the patterns, ignore the patterns. The only ask is that you don't claim the synthesized pattern catalog is your original research without crediting the underlying sources listed in `SKILL.md` §9.

---

## Credits

The pattern catalog is synthesized from work by Carnegie Mellon's AI-writing study (2025), Wikipedia's "Signs of AI Writing" editor community, Buffer's 52M-post LinkedIn analysis, and several open-source projects credited in `SKILL.md` §9.

If you ship something interesting on top of this, open an issue or a PR — I'd like to see it.
