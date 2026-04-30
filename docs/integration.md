# Integration Patterns

Humanizer is designed to be the **last** pass on a draft, not the only one. The most useful pipelines chain it after a drafting step and (optionally) before a publish step.

This doc covers the common patterns.

---

## Pattern 1: Drafting agent → Humanizer (the default)

```
[ writing/drafting agent ]  →  [ humanizer ]  →  final draft
```

Use when you have a content-generation step (a writer agent, a marketing-content skill, a one-shot prompt). The drafting step produces the first draft; Humanizer scrubs it before delivery.

**How to wire it (Claude Code):**

In a writing agent's instructions, end with:

```
After producing the draft, invoke the humanizer skill on the output.
Pass the brand voice profile path if this is client-facing,
or the author voice profile if it's first-person.
Return the Final Version section to the user.
```

That's it. The agent drafts; the skill audits and rewrites; the user sees the audited version.

**Why it works:** Drafting agents and humanizing agents have different goals. A drafting agent is rewarded for filling a blank page; it's prone to all the AI tells Humanizer catches. Splitting the two responsibilities lets each do its job.

---

## Pattern 2: Detect-only mode in CI

```
PR with .md files  →  GitHub Action  →  humanizer in detect mode  →  PR comment
```

Use when you have a content repo (docs, marketing, blog) and want a non-blocking signal on AI-tells in PRs.

**Sketch:**

```yaml
# .github/workflows/humanizer.yml
name: Humanizer
on:
  pull_request:
    paths: ['**/*.md', '**/*.mdx']

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run humanizer (detect mode) on changed files
        run: |
          # Pseudo — adapt to your CI runner of choice.
          # The skill is just a markdown file; you call any LLM API
          # with SKILL.md as the system prompt and the diff'd content as input.
          # Detect mode returns Issues Found + Assessment, which you post as a PR comment.
```

You can either:
- Keep the audit advisory (post a comment, don't block)
- Make it blocking on `[CRITICAL]` issues only (chatbot artifacts, fake stats, fabricated attributions — all true credibility killers)

Don't make `[HIGH]` issues blocking unless your content team has agreed — those are judgment calls.

---

## Pattern 3: Multi-reviewer pipeline (advanced)

```
draft  →  humanizer (rewrite)  →  brand reviewer  →  fact-checker  →  publish
```

For long-form, high-stakes content (case studies, sales collateral, executive comms). Humanizer runs first because:

- It's purely structural/stylistic — no domain knowledge required
- Its output is parseable, so downstream agents can read what changed
- Brand reviewers and fact-checkers can focus on substance once the AI tells are gone

**Tip:** if a downstream brand reviewer keeps re-flagging things Humanizer didn't catch, those patterns belong in your brand voice profile (or in a PR to this repo's pattern catalog).

---

## Pattern 4: Single-shot for one-off drafts

```
paste draft  →  humanizer  →  done
```

For everything else. The skill works fine on a paste-and-go basis — no setup, no chaining. This is the most common usage.

The interactive version (`humanize this`, with the draft pasted) is fine for emails, Slack messages, LinkedIn posts. The path-based version (`humanize ./draft.md`) is more useful for blog drafts and case studies because you can re-run cleanly.

---

## Avoiding common mistakes

### Don't run Humanizer twice in a row

The first pass catches structural and vocab tells. The second pass starts to flatten voice — short sentences get smoothed, intentional fragments get fixed, the prose loses snap. Trust the self-audit step (§5 of the skill); it's already a second pass.

### Don't use Humanizer as a content reviewer

It scrubs AI tells. It does not check whether your facts are right, whether the strategic framing is correct, or whether the ask is buried. Pair it with a separate review step for those — see Pattern 3 above. The `[HOLLOW]` flag is the only "is this saying something" signal Humanizer provides.

### Don't blindly accept the rewrite

The output is structured for review precisely because it's not always right. The Issues Found section explains what was flagged; the Self-Audit section names anything still off. Read both. Override with "stet" or "keep it" when the skill is wrong — it'll stop flagging that span.

### Don't load both author and brand profiles for the same draft

Pick one based on the channel:
- First-person, internal, casual → author profile
- Client-facing, organizational → brand profile

Loading both gives the skill conflicting signals (one says "preserve sentence fragments," the other says "strict in long-form").

---

## Calling Humanizer from code

If you want to run the skill outside an agent harness (e.g., in a script, a Slack bot, a Vercel function), it's just a system prompt + a user message:

```python
import anthropic, pathlib

client = anthropic.Anthropic()
system = pathlib.Path("humanizer/SKILL.md").read_text()

# Optionally append a voice profile to the system prompt.
voice = pathlib.Path("voice/author.md").read_text()
system_with_voice = system + "\n\n## Active voice profile\n\n" + voice

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    system=system_with_voice,
    messages=[
        {"role": "user", "content": "Humanize the following draft:\n\n" + draft_text}
    ],
)

print(response.content[0].text)
```

The output follows the format documented in `SKILL.md` "Output Format." Parse it by section header (`## Issues Found`, `## Final Version`, etc.) — the format is intentionally stable for downstream consumers.

---

## Slack / chat integration

A common ask: "I want to drop a draft into Slack and get the humanized version back."

Sketch:
1. Slash command (`/humanize <text>` or message to a bot user)
2. Webhook fires a Vercel/Lambda function with the draft
3. Function calls the Anthropic API with `SKILL.md` as system prompt
4. Response posts back to the thread

Keep the response in detect mode if the channel is high-traffic — long rewrites flood threads. Save full rewrites for DM or paste-back contexts.
