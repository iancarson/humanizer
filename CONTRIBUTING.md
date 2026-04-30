# Contributing to Humanizer

Thanks for considering it. This is a small, focused project — the most valuable contributions are sharper patterns and better worked examples, not framework code.

---

## What contributions are most useful

### High value

- **New AI-tell patterns** for `SKILL.md` §3 (HIGH) or §5 (MEDIUM), with a real before/after example. The pattern catalog is the heart of the project; additions there compound.
- **Worked examples** for channels not yet covered (case study, marketing email, customer-success update, technical doc, OKR write-up).
- **Harness integrations** — if you wire Humanizer into a tool not in [`docs/interoperability.md`](docs/interoperability.md), a short subsection added there is high leverage.
- **Bug reports** with a specific input that produced a flat / over-rewritten / mis-flagged output. Including the model and any voice profile loaded helps reproduce.

### Medium value

- **Refining tier-1/2/3 vocab lists.** If you have evidence (a study, a corpus analysis, your own A/B data) that a word should move tiers or be added/removed, open an issue with the evidence first.
- **Channel × Strictness matrix tweaks.** Same approach — specific channel, specific evidence.
- **Improving the setup-mode interview.** If a question is consistently confusing or producing low-quality answers, propose an alternative.

### Low value

- Pure formatting / wording changes to the docs without behavior change.
- Adding more banned words without evidence.
- "Make it strict by default" / "Make it lenient by default" preference changes — Humanizer's defaults are calibrated for the median user; preferences belong in your voice profile.

---

## How to propose a pattern

Open a PR that adds:

1. The pattern to `SKILL.md` §3 or §5 (matching the existing format — name, what it is, before/after).
2. One worked example in `examples/` showing the pattern in context (similar to the existing `before-after-*.md` files).
3. A short rationale in the PR description: where you've seen the pattern, why it's distinct from existing ones, what severity you suggest and why.

If the pattern overlaps with an existing one, propose merging or sharpening rather than adding a near-duplicate.

---

## Coding standards (such as they are)

There's no code yet. The project is markdown end-to-end. House style:

- **Headings.** Sentence case for H1/H2; title case for table headers.
- **Em dashes.** Use them in docs, not in `SKILL.md` examples (Humanizer's own §6 budget applies to itself).
- **Tone.** Match the existing register — direct, concrete, no marketing prose. The pitch in `README.md` should sell the project; everything else should explain it plainly.
- **Examples.** Use realistic but synthetic scenarios. No real people, no real customer names, no real revenue numbers. SaaS-flavored generic examples are fine.

---

## Testing your changes

There's no test runner. Testing is "load the modified `SKILL.md` into your harness, run it on three drafts you know well, see if the output got better or worse."

Before opening a PR for a pattern change:

1. Pick 2–3 drafts where the new pattern shows up.
2. Run the unmodified `SKILL.md` against them.
3. Run the modified `SKILL.md` against them.
4. Confirm the modified version catches the pattern without breaking other behavior.
5. Include the before/after in the PR description.

---

## Filing issues

A useful bug report:

- The input draft (or a redacted version)
- What channel you were trying to humanize for
- Voice profile loaded (or "none")
- Model and harness used (Claude Opus via Claude Code, etc.)
- Expected vs actual output
- Why you think it's wrong

A useful feature request:

- The specific scenario where the current skill falls short
- Why an existing mechanism (voice profile, stet protocol, channel matrix) doesn't already cover it
- A proposed change in concrete terms

---

## License

By contributing, you agree your contributions will be released under the MIT license (see [`LICENSE`](LICENSE)).
