# Humanizer

> A drop-in writing skill that scrubs AI tells out of your drafts before they ship.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate](https://github.com/milock/humanizer/actions/workflows/validate.yml/badge.svg)](https://github.com/milock/humanizer/actions/workflows/validate.yml)
[![Anthropic Skills compliant](https://img.shields.io/badge/Anthropic_Skills-compliant-7E3FF2)](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills)
[![Status: stable](https://img.shields.io/badge/status-stable-brightgreen.svg)](CHANGELOG.md)

Humanizer is a portable writing skill — a single markdown file you can install into Claude Code, paste into Cursor, or use as a system prompt with the Anthropic, OpenAI, or any other API. It catches the structural and vocabulary patterns that make AI-generated writing read as obviously AI-generated, then rewrites the offending spans without flattening the writer's voice.

It's not a stylechecker. It's a final pre-delivery pass that runs before you click send.

---

## Pipeline at a glance

```
                        ┌─────────────────────────────────────────┐
                        │           Input draft + context         │
                        └────────────────────┬────────────────────┘
                                             │
                  ┌──────────────────────────┴──────────────────────────┐
                  │ Step 0: Auto-detect channel (email, Slack, blog, …) │
                  └──────────────────────────┬──────────────────────────┘
                                             │
                  ┌──────────────────────────┴──────────────────────────┐
                  │ Step 1: Voice calibration (optional, profile-based) │
                  └──────────────────────────┬──────────────────────────┘
                                             │
                  ┌──────────────────────────┴──────────────────────────┐
                  │ Step 2: Pattern scan                                │
                  │   structural → vocab → positive → context           │
                  │   (16 named patterns, 3 vocab tiers, 5 punctuation  │
                  │    budgets, banned-opener list)                     │
                  └──────────────────────────┬──────────────────────────┘
                                             │
                  ┌──────────────────────────┴──────────────────────────┐
                  │ Step 3: Severity gate (patch vs. full rewrite,      │
                  │         clean-but-hollow check)                     │
                  └──────────────────────────┬──────────────────────────┘
                                             │
                  ┌──────────────────────────┴──────────────────────────┐
                  │ Step 4: Rewrite at chosen depth                     │
                  └──────────────────────────┬──────────────────────────┘
                                             │
                  ┌──────────────────────────┴──────────────────────────┐
                  │ Step 5: Self-audit                                  │
                  │   "What makes this still obviously AI generated?"   │
                  │   Revise again if the answer isn't "nothing."       │
                  └──────────────────────────┬──────────────────────────┘
                                             │
                  ┌──────────────────────────┴──────────────────────────┐
                  │ Step 6: Emit Final Version + structured report      │
                  │   Issues Found / What Changed / Self-Audit /        │
                  │   Final Version / Humanizer Report                  │
                  └─────────────────────────────────────────────────────┘
```

---

## Severity at a glance

| Severity | What it catches | Example |
|---|---|---|
| **CRITICAL** | Credibility killers — fabricated stats, fake attributions, chatbot artifacts, sycophancy, knowledge-cutoff disclaimers | "Studies show that 73% of teams…" with no citation |
| **HIGH** | Structural AI tells — dramatic reframes, manufactured punchlines, runway sentences, performative directness, anaphora, copula avoidance, etc. | "This isn't an X problem. This is a Y problem." |
| **MEDIUM** | Stylistic drag — compulsive tricolons, premature lists, em dash overuse, fake humility closers, rhetorical throat-clearing | "Calm. Specific. Human." |
| **LOW** | Watch-list — only flagged when stacked with other tells | One sentence fragment in a paragraph |

Full catalog with before/after examples in [`references/patterns.md`](references/patterns.md).

---

## Quick start

### Claude Code (recommended)

```bash
git clone https://github.com/milock/humanizer.git
cd humanizer && ./install.sh
```

Then in Claude Code, type `/humanizer` or say "humanize this draft," "scrub AI tells," "final review."

For project-scoped install (just this repo), use `./install.sh --project`.

### Cursor / Continue / Aider / other harnesses

Either paste the contents of [`SKILL.md`](SKILL.md) into your tool's rules/system-prompt file, or reference the file path. Detailed harness-specific instructions in [`docs/interoperability.md`](docs/interoperability.md).

### Raw Anthropic / OpenAI API

Use `SKILL.md` as the system prompt:

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

---

## First-run setup (optional)

Humanizer works with zero configuration. To make it sharper for your voice or your brand:

```
humanizer setup
```

The skill walks you through a 7-question interview — your channels, sample writing, quirks to preserve, hard nos, punctuation preferences, domain vocabulary — and produces a populated voice profile file you can keep editing.

You can also skip the interview and copy [`examples/author-voice.example.md`](examples/author-voice.example.md) or [`examples/brand-voice.example.md`](examples/brand-voice.example.md), then fill in the blanks.

Detailed guidance in [`docs/voice-profiles.md`](docs/voice-profiles.md).

---

## What's in the box

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | The skill core — workflow, output format, setup mode, guardrails. ~340 lines. |
| [`references/patterns.md`](references/patterns.md) | Full AI-tell catalog (16 structural patterns, 3-tier vocab, punctuation budgets, banned openers). Loaded on demand. |
| [`references/channels.md`](references/channels.md) | Channel detection cues, strictness matrix, hollow failure modes, voice carve-outs. |
| [`examples/author-voice.example.md`](examples/author-voice.example.md) | Template for a personal voice profile. |
| [`examples/brand-voice.example.md`](examples/brand-voice.example.md) | Template for an organizational/brand voice profile. |
| [`examples/before-after-email.md`](examples/before-after-email.md) | Worked example — sales email with 4 AI tells. |
| [`examples/before-after-linkedin.md`](examples/before-after-linkedin.md) | Worked example — personal LinkedIn post with 6 structural patterns and zero Tier-1 vocab. |
| [`examples/before-after-blog.md`](examples/before-after-blog.md) | Worked example — generic SaaS blog intro, full rewrite. |
| [`docs/voice-profiles.md`](docs/voice-profiles.md) | What actually changes the output (and what doesn't) when you write a profile. |
| [`docs/integration.md`](docs/integration.md) | Patterns for chaining Humanizer with other writing/review agents and CI. |
| [`docs/interoperability.md`](docs/interoperability.md) | Using Humanizer outside Claude Code (Cursor, Continue, raw API, Slack bots, GitHub Actions). |
| [`scripts/validate_skill.py`](scripts/validate_skill.py) | CI validator — checks frontmatter against the Anthropic Skills spec. |
| [`install.sh`](install.sh) | One-line installer for Claude Code (user-wide or project-scoped). |

---

## How Humanizer differs from generic "AI humanizer" tools

Most browser-based humanizer SaaS products take AI-generated text and run it through paraphrasing models. They lower detector scores; they don't make the writing better.

Humanizer is the opposite shape:

- **Structural before vocabulary.** Most of the AI-tell signal is in *how* the sentences are arranged, not which words are picked. Swapping "leverage" for "use" is necessary but rarely sufficient. Humanizer scans 16 named structural patterns first.
- **Voice-preserving by default.** The skill takes a voice profile (yours or your brand's) and refuses to flatten it. Short sentences, "And"/"But" starts, deliberate fragments — all preserved when the profile says so.
- **Honest about hollow drafts.** A draft that passes every AI-tells check but says nothing specific gets flagged `[HOLLOW]` rather than silently approved. The model won't manufacture facts to fill the gap.
- **Self-audited.** After the rewrite, the skill asks itself *"what makes this still obviously AI generated?"* and revises again. This second pass catches more than any single sweep.
- **Auditable output.** You see what was flagged, what changed, and what the model thinks is still off. No black-box paraphrase.
- **Not a detector-evasion tool.** Humanizer is for shipping copy you wrote with AI assistance, not laundering text past Turnitin. The framing matters: better drafts, not lower detection scores.

---

## Roadmap

- A small CLI wrapper so you can pipe text through Humanizer outside an agent harness (`cat draft.md | humanize`)
- Optional GitHub Action that runs Humanizer on `.md` files in PRs and posts the diff as a review comment
- Drop-in Slack / Linear bot for teams that want shared voice enforcement
- Per-domain pattern overlays (technical writing, academic register, sales copy)

PRs welcome. The pattern catalog in [`references/patterns.md`](references/patterns.md) is the most valuable surface — additions there (with examples) are the highest-leverage contribution. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## License & credits

MIT — see [`LICENSE`](LICENSE).

The pattern catalog is synthesized from public AI-writing research and several open-source projects. Full credits in [`ATTRIBUTION.md`](ATTRIBUTION.md).
