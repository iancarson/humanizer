---
name: humanizer
description: 'Final pre-delivery scrub for AI tells on every draft — external (blog, email, LinkedIn, case study, landing page, newsletter, sales collateral) and internal (Slack, agenda, memo, feedback note). Returns a corrected draft plus a diff of changes. Triggers on "humanize", "scrub AI tells", "final review", "check for AI tells", "de-robot". First-run onboarding via "humanizer setup" / "configure humanizer".'
argument-hint: "[setup | path-to-draft | paste content]"
---

# Humanizer

Final pre-delivery scrub for AI tells. Run on every draft longer than a single sentence, external or internal — emails, Slack threads, LinkedIn, blog posts, case studies, sales collateral, newsletters, meeting agendas with prose, feedback notes. Single-line replies are exempt.

A draft can use zero banned words and still read like a robot if it leans on dramatic reframes, staccato rhythm, and manufactured punchlines, which is why the scan runs structural before vocab before positive checks before context.

Severity maps to action:

| Severity | Meaning | Action |
|---|---|---|
| **CRITICAL (P0)** | Credibility killer. Reader loses trust. | Always fix. No exceptions. |
| **HIGH (P1)** | Clear AI tell. Reader notices. | Fix unless the pattern is intentional and earned. |
| **MEDIUM (P2)** | Stylistic drag. Accumulates. | Fix if 2+ in same piece, or if combined with other patterns. |
| **LOW** | Watch-list. Only flag in clusters. | Note if density is high; otherwise leave. |

---

## Setup (Optional)

This skill works out of the box. Two optional configurations make it sharper for a specific user or brand:

1. **Author voice profile** — a short markdown file (any path) describing the writer's natural voice: sentence-length distribution, word-choice register, paragraph-opener habits, recurring phrases, things to leave alone. Pass the path when invoking, or the skill can be configured to auto-load it for first-person drafts.
2. **Brand voice profile** — same shape, but for client-facing or organizational copy. Pass the path for blog/case-study/landing-page/marketing-email work.

Without either profile, the skill preserves the draft's existing voice and applies the universal rules below.

**Two ways to set up:**
- **Guided:** run `humanizer setup` (or say "set up humanizer" / "configure humanizer"). The skill walks you through a short interview and produces a populated voice profile. See **Setup Mode** below.
- **Manual:** copy `examples/author-voice.example.md` or `examples/brand-voice.example.md`, fill in your details, and pass the path when invoking the skill.

---

## Workflow

Six-step pipeline:

```
0. Auto-detect channel + voice target
1. Voice calibration (conditional)
2. Pattern scan (structural → vocab → positive → context)
3. Severity gate (patch vs. full rewrite; clean-but-hollow check)
4. Rewrite at chosen depth
5. Self-audit (mandatory long-form; conditional short-form)
6. Emit final draft + humanizer report
```

### Step 0 — Auto-detect channel

Infer channel silently from context: greeting/salutation, file path, word count, hashtags, code fences, voice cues. See **Channel Profiles** below. Default to `generic long-form` if ambiguous and note the assumption in the final report. Don't ask unless two or more channels are genuinely plausible.

### Step 1 — Voice calibration (conditional)

Skip by default. Run only when one of these is true:

1. The user pastes a writing sample and asks for voice-matched output.
2. An author voice profile is configured and the draft is first-person / personal.
3. A brand voice profile is configured and the draft is client-facing or organizational.
4. The draft was produced by an upstream drafting agent with its own voice rules; the humanizer runs as a final pass on that output and respects its register.

When calibrating from a sample, capture a six-line voice profile: sentence-length distribution, word-choice level, paragraph openers, punctuation habits, recurring phrases, transition style. Keep in working memory for Steps 4 and 5.

Never fabricate a voice profile. If no trigger fires, preserve the draft's existing voice rather than imposing one.

### Step 2 — Pattern scan

Fixed order — structural tells are load-bearing; vocab tells are surface:

1. **Dramatic reframe + punchline structures** (§3.1, §3.2) — the highest-signal tells
2. **Structural patterns** (§3.3 through §3.16)
3. **Vocabulary tiers** (§4)
4. **Positive checks** — is there a point of view, a concrete detail, an earned opener?
5. **Context checks** — punctuation budgets, disclaimer patterns, register-appropriate forms of address

Tally hits. Group vocab hits by category — category count feeds Step 3.

### Step 3 — Severity gate

**Patch vs. full rewrite.** Trigger full rewrite if all three are true (see §1):
- 5+ Tier 1/Tier 2 vocab hits
- 3+ distinct pattern categories triggered
- Uniform sentence length — three-plus consecutive sentences within 2 words of each other

Otherwise patch mode. Surgical edits only, leave the rest alone.

**Clean-but-hollow flag.** If the draft passes the scan but says nothing — no concrete claim, no specific example, no defensible point of view — flag it explicitly. A clean-style draft with no substance is still broken; the user needs to know before it ships.

### Step 4 — Rewrite

Produce the rewrite at the depth Step 3 chose. Preserve the writer's voice and argument. The humanizer removes tells; it does not impose a house style on a draft that already has one.

For **patch mode**, show only edited spans with minimal surrounding context. For **full rewrite**, produce the full replacement.

### Step 5 — Self-audit (mandatory second pass)

The load-bearing step of the pipeline. Do not skip on long-form.

**Mandatory for:** blog posts, case studies, sales collateral, newsletters, LinkedIn posts, any external email >4 sentences, any draft that triggered full rewrite in Step 3.

**Conditional for:** Slack messages, short internal emails, CTAs, subject lines — skip **only if** Step 2 flagged nothing. If anything was flagged, audit runs.

Two prompts, asked internally, answered in writing:

> **Prompt 1:** "What makes the below so obviously AI generated?"
> List every residual tell in the rewritten draft. Do not protect your own work. If none, say "None" with a one-sentence justification.

> **Prompt 2:** "Now make it not obviously AI generated."
> Revise against every tell surfaced in Prompt 1.

If Prompt 1 returns "None" and the justification holds, skip Prompt 2 and emit.

### Step 6 — Emit final + report

Use the Output Format below. Downstream agents that parse this skill's output rely on a stable shape — keep the section headers consistent.

---

## Output Format

Two modes. Default to **Rewrite**. Use **Detect** when the user says "scan," "check," "audit" without asking for a rewrite.

### Rewrite Mode (default)

```
## Issues Found

- **[CRITICAL]** "<verbatim offending text>" — <why it reads AI> → <fix direction>
- **[HIGH]** "<verbatim>" — <reason> → <fix>
- **[MEDIUM]** "<verbatim>" — <reason> → <fix>

(Group by severity. Quote offending text verbatim — vague paraphrases let bad lines slip back in.)

## Rewritten Draft

<full corrected draft — no preamble, no commentary, copy-paste ready>

## What Changed

- <1-line summary of major edit>
- <max 6 bullets; major edits only, not every word swap>

## Self-Audit

"What makes the above so obviously AI generated?"

- <residual tell #1>
- <residual tell #2>

(or: "None detected.")

## Final Version

<full post-audit revision — this is what the user copies>

(If Self-Audit found nothing, repeat the Rewritten Draft verbatim under this header so downstream parsers always find a Final Version section.)

## Humanizer Report

- **Channel detected:** <email | slack | linkedin | newsletter | case-study | blog | agenda | landing-page | generic long-form>
- **Voice loaded:** <none | author profile | brand profile | sample>
- **Rewrite depth:** <patch | full>
- **Clean-but-hollow:** <no | yes + what's missing>
- **Notes:** <punctuation swaps, register corrections, other context-layer fixes>
```

### Detect Mode

```
## Issues Found

- **[CRITICAL/HIGH/MEDIUM/LOW]** "<verbatim>" — <reason>

## Assessment

<2-3 sentences: overall AI-likeness + channel fit. Flag clean-but-hollow if applicable.>
```

### Setup Mode

Triggered when the user says "humanizer setup", "configure humanizer", "set up my voice profile", "onboard me", or runs `humanizer setup` as an argument.

The goal is a populated voice profile (or two — author + brand) saved to a path the user controls. Don't overdesign the interview; capture what's load-bearing for AI-tells detection and stop.

**Interview flow** — ask questions one screen at a time. Wait for an answer before moving on. Skip any section the user says "skip" to. Aim for ≤7 minutes total.

```
Q1. Who's this profile for?
    a) Me, personally (I write in first person — emails, LinkedIn, Slack, internal notes)
    b) A brand or organization (we voice — blog, case studies, marketing copy)
    c) Both (I'll fill out two profiles back to back)

Q2. What do you actually write?
    Pick all that apply: email · Slack · LinkedIn · blog · case study · newsletter ·
    landing page · sales collateral · meeting agenda · feedback note · other (describe)

Q3. Paste 1–3 short samples of your natural writing.
    (Anything you've actually sent or published. 3–10 sentences each is plenty.
    The skill reads register, sentence-length distribution, paragraph openers,
    punctuation habits, recurring phrases — not topic.)

Q4. Quirks to preserve.
    Are there patterns that look AI-ish in isolation but are actually you/your brand?
    Examples: short fragments, "And/But" sentence starts, one-line paragraphs,
    specific terms of address (Dr., Professor), house spelling (gray vs grey),
    idioms, signature sign-offs.

Q5. Hard nos.
    Are there phrases, tropes, or framings you NEVER want to see?
    Examples: industry clichés, fear-mongering language, specific banned words
    beyond the universal Tier 1 list, idioms that don't fit your audience.

Q6. Punctuation preferences.
    a) Em dashes: allowed (default), reduced (max 1 / 500 words), or banned (use hyphen-spaces or commas)?
    b) Exclamation points: default (max 1 / 1,000 words), allowed in casual channels only, or never?
    c) Anything else? (e.g., Oxford comma always, no semicolons, etc.)

Q7. Domain vocabulary that should be exempt from filler-word checks.
    Industry terms where words like "significant," "critical," "comprehensive" are
    load-bearing rather than filler. Examples: clinical findings, legal/compliance
    language, financial reporting, regulatory references.

Q8. Where should the profile be saved?
    Suggest a default (~/.humanizer/author-voice.md or ./voice/author.md) — let the user
    override. Confirm before writing.
```

**Output:** a markdown file at the user-chosen path, populated using the templates in `examples/`. After saving, print:

```
Voice profile saved to <path>.

To use it:
  • Pass --voice <path> when invoking, OR
  • Set HUMANIZER_AUTHOR_VOICE=<path> in your shell, OR
  • Reference it in your project CLAUDE.md / equivalent agent config so the skill auto-loads it.

To edit later: open the file directly. To re-run setup: "humanizer setup --replace".
```

**Re-running setup.** If the profile already exists, default to `--update` (additive — the skill asks only the questions whose answers it can't infer from the existing file). The user must pass `--replace` to start over.

**Brand profile after author profile.** When Q1 = "Both", run the same interview a second time with brand-framing in the prompts (Q2 emphasizes client-facing channels; Q3 asks for published brand-voice samples; Q4 asks about house style guide; Q8 saves to `brand-voice.md`).

**What NOT to ask.** Don't ask the user to enumerate the Tier 1 vocab list, the structural patterns, or the punctuation budgets — those are universal and built in. Setup only captures what varies per user/brand.

### Clean-But-Hollow Flag

When the draft has no CRITICAL/HIGH issues but no concrete claims, numbers, named entities, or examples, add this to Issues Found:

`- **[HOLLOW]** Passes AI scan but lacks substance: <what's missing — specific number, named example, stake>.`

In Rewrite mode, the Final Version must add substance, not just polish. Never silently approve a hollow draft.

### Nothing Flagged

If the draft is clean: `## Issues Found` = `- None detected.`, Rewritten Draft = original, Self-Audit still runs, Final Version emitted verbatim. **Emit all section headers even on a clean pass** — downstream agents parse by header and will fail silently if the shape is inconsistent. Detect mode is the one exception; it does not emit `## Final Version`. Callers of Detect mode must check mode before parsing.

### Worked Mini-Example

**Input (Slack draft):** "Quick update — we're leveraging the new workflow to streamline onboarding and it's been transformative for the team."

**Output:**

```
## Issues Found

- **[CRITICAL]** "leveraging" — Tier 1 vocab → "using"
- **[CRITICAL]** "streamline" — Tier 1 vocab → "speed up" or cut
- **[CRITICAL]** "transformative" — Tier 1 vocab → replace with a concrete result
- **[HOLLOW]** Passes scan but no specifics: which workflow? how much faster?

## Rewritten Draft

Quick update: the new onboarding workflow is saving us about a day per new hire.

## What Changed

- Swapped three Tier 1 words for plain verbs
- Added concrete result (day per hire) to replace vague praise
- Replaced em dash with colon (cleaner for short Slack message)

## Self-Audit

"What makes the above so obviously AI generated?"

- None detected. "Quick update:" reads natural for Slack.

## Final Version

Quick update: the new onboarding workflow is saving us about a day per new hire.

## Humanizer Report

- Channel detected: slack
- Voice loaded: none
- Rewrite depth: patch
- Clean-but-hollow: no (added specifics)
- Notes: em dash → colon
```

---

## Channel Profiles

### Auto-Detect Cues

Strongest cue wins. If two cues point to different channels, ask rather than guess.

| Cue | Channel |
|---|---|
| `Hi [Name],` / `Hello,` / sign-off block / subject line | Email |
| `<@U…>` mentions, `:emoji:`, `#channel`, thread-style | Slack |
| <300 words + hashtags, or arrow chains | LinkedIn |
| First-person "I", personal anecdote | LinkedIn — personal |
| "We're building" / organizational cues without "I ran" | LinkedIn — organizational |
| Code fences, H2/H3 headers, >800 words, "we" voice | Blog post |
| Pull-quote blocks, before/after metrics, customer named | Case study |
| Editorial register, recurring section structure | Newsletter |
| Bulleted list + `@name` owner tags, no prose intro | Meeting agenda |
| Headline + subhead + <100 words + CTA language | Landing page / ad |
| `r/` prefix, "OP", anonymous first-person | Reddit reply |
| "Feedback:" / "When you did X, I noticed Y" | Feedback note |
| Marketing merge tags (`{{first_name}}`), promo CTA | Marketing email |

### Channel × Strictness Matrix

**S** = strict (flag), **R** = relaxed (house style — don't flag), **I** = inverted (required), **N** = normal.

| Channel | One-line paras | Staccato | "We" voice | First-person "I" | Voice profile to load |
|---|---|---|---|---|---|
| Newsletter (editorial) | R | R | N | R | brand or author |
| Blog post / case study | S | S | I | S | brand |
| Marketing email | N | N | I | S | brand |
| Email (1:1) | N | N | N | R | author |
| LinkedIn — personal | R | R | N | I | author |
| LinkedIn — organizational | R | R | N | R | brand |
| Slack (team or 1:1) | R | R | N | R | author |
| Meeting agenda | I (bullets) | N | N | N | none (format rules apply) |
| Feedback / coaching note | R | R | N | R | author |
| Landing page / ad | R | R | I | S | brand |
| Reddit reply | R | R | N | R (required) | none (anonymous register) |

### Per-Channel Hollow Failure Modes

A draft can pass the AI-tells scan and still fail. Flag `[HOLLOW]` if:

| Channel | Hollow failure mode |
|---|---|
| Blog / newsletter | No specific numbers, no named source, no operational detail — sounds smart, says nothing |
| Case study | No quantified before/after, no customer name, no direct quote |
| Email (1:1 or marketing) | Ask is buried past line 3, multiple asks stacked, or no ask when one is expected |
| LinkedIn — personal | Opinion without a concrete example or number — "take" without teeth |
| LinkedIn — organizational | Predicts audience pain instead of reporting what was observed; generic platitude |
| Slack — team | Over-explains context before the ask; ask buried |
| Slack — 1:1 (terse register) | More than 2 sentences of preamble before the point |
| Meeting agenda | Bullets without owners; talk tracks or time estimates present |
| Landing page / ad | No specific proof point (stat, customer, outcome) above the fold |
| Feedback note | Abstract ("be more proactive") without the specific behavior + moment |
| Reddit reply | Generic hot-take without a specific counter-point or personal experience; reads like it was written without reading the thread |

### When to Ask vs. Decide

**Auto-decide** when ≥2 cues agree. **Ask** when:
- Only one weak cue matches
- LinkedIn detected but voice ambiguous between personal and organizational
- Email detected but register unclear (marketing blast vs. 1:1)
- Slack detected but audience unclear (team channel vs. terse 1:1 — strictness differs)
- Draft <50 words with no format cues

Ask format: *"Looks like [channel A] or [channel B]. Which — and who's the audience?"* Never guess on audience; channel strictness pivots on it.

---

## 1. Full-Rewrite Threshold

Defined in Workflow Step 3. Short version: if 5+ Tier 1/Tier 2 vocab hits, 3+ distinct pattern categories, and uniform sentence length are all present, throw out the draft and rewrite from the outline rather than patching. Patching only smooths the surface — the skeleton is still AI-shaped.

---

## 2. CRITICAL Patterns (P0) — Credibility Killers

These lose the reader's trust in one sentence. Always fix. No judgment call.

| Pattern | What it is | Fix |
|---|---|---|
| **Fabricated stats / fake specificity** | Precise-sounding numbers with no real source ("studies show 73% of teams..."). | Cut, or replace with a real cited figure. Never approximate to sound authoritative. |
| **Fake attributions** | Quotes or claims attributed to an expert/study that doesn't exist or doesn't say that. | Verify the source says the exact thing. If not, cut. |
| **Knowledge-cutoff disclaimers** | "As of my last update..." / "I may not have the latest..." | Delete entirely. |
| **Chatbot artifacts** | "Let me know if you'd like me to expand...", "I hope this helps!", "Happy to revise." | Delete. Never ships in final copy. |
| **Sycophancy** | "Great question!", "That's a fantastic point..." | Delete. |

**BEFORE (fabricated stats):** "Studies show that 73% of B2B teams lose revenue to onboarding friction, with most seeing a 12% hit to deal velocity annually."
**AFTER:** "In the teams we've worked with, onboarding friction typically costs 3–8% of pipeline velocity — not catastrophic, but meaningful at scale." (Cites experience over invented precision.)

**BEFORE (chatbot artifact at end of email):** "Let me know if you'd like me to expand on any of this, or if you'd prefer I tighten it further!"
**AFTER:** (Delete entirely. Sign off cleanly with the writer's actual close.)

---

## 3. HIGH Patterns (P1) — Structural AI Tells

These are the high-signal structural tells. In order of severity:

### 3.1 Dramatic Reframe — the #1 AI tell
"That's not X. That's Y." — where Y adds no new information, just relabels X for effect.

- **BEFORE:** "This isn't a hiring problem. This is a process problem."
- **AFTER:** "The hiring gap is downstream of the process — fix the intake handoff and the headcount math changes."

Variant: **Definition reframes** — "It's an execution problem dressed up as a strategy problem." Same mechanic, same fix: say the actual thing.

### 3.2 Manufactured Punchline / Bumper-Sticker Closer
Section or piece ends on a tidy aphorism that sounds quotable but doesn't say anything. Includes **orphan closers** (one-line dramatic endings) and **section-ending zingers**.

- **BEFORE:** "Because in customer success, the details aren't details. They're everything."
- **AFTER:** "Miss the kickoff agenda and renewal probability drops 15 points. That's most of the variance between a 90% and 105% net retention number."

### 3.3 Staccato Overdose + Uniform Length
Every paragraph is 1–2 short sentences. Or three-plus consecutive sentences within 2 words of each other. Robotic cadence even if individual sentences are fine.

Rule of thumb: **no three consecutive same-length sentences**. Vary short/medium/long.

### 3.4 Performative Directness
"Here's the truth." / "Let's be real." / "The reality is..." — throat-clearing dressed as candor.

- **BEFORE:** "Here's the deal. Most vendors don't actually understand the workflow."
- **AFTER:** "Most vendors don't actually understand the workflow."

### 3.5 Dramatic Fragment Q&A
"Pricing? Undisclosed." / "The catch? There isn't one." Question-plus-fragment answer. Cut or convert to a full sentence.

### 3.6 Runway Sentences
Vague hype sentence that exists only to set up the real sentence that follows.

- **BEFORE:** "The stakes have never been higher. Companies are facing unprecedented pressure on margins."
- **AFTER:** "Companies are facing margin pressure — pricing power is flat while labor costs are up double digits since 2021."

### 3.7 Persuasive Authority Tropes
"The real question is...", "At its core...", "Fundamentally...", "What this really means is...". Authority-by-assertion with no earned authority behind it. Delete and state the thing.

### 3.8 Tailing Negations / Negative Parallelism
"No guessing. No wasted motion. No hand-offs that fall apart." Three-or-more negations tacked onto a claim. Reads like landing-page copy from any vendor.

- **BEFORE:** "We take over the migration. No handoffs. No dropped data. No surprises."
- **AFTER:** "We take over the migration on day one. The previous vendor's unfinished work is ours to close."

### 3.9 Elegant Variation / Synonym Cycling
The same thing named four different ways to avoid repetition — "the customer / the client / the partner / the organization". Readers notice. Pick one noun and repeat it.

### 3.10 Copula Avoidance
"Acme serves as the platform..." / "The product stands as a single source of truth..." Use *is/are*. "Acme is the platform." That's all the sentence needed.

### 3.11 Inspirational Pivot
Ends on uplift that wasn't earned by the preceding text. Usually starts with "But here's the thing..." or "The good news is...". Cut the pivot — if the argument earns an uplift, the reader reaches it on their own.

### 3.12 Vulnerability Performance
"I'll be honest..." / "Can I be real for a second?" / "Not gonna lie..." Performative candor as a credibility grab. Delete and say the honest thing directly.

### 3.13 Anaphora / Repetitive Negation
"Not the vendor. Not the timeline. Not the scope." Three-plus parallel openers with the same word. One is rhythm. Three is AI.

### 3.14 Universal Authority Without Source
"Industry experts agree...", "Studies show...", "It's well known that..." — no citation. Either add the source or cut the claim.

### 3.15 Fragmented Headers
Heading followed by a one-line restatement of the heading before the real content starts.

- **BEFORE:** `### The transition is fast` followed by "Our transitions are fast. Here's why:"
- **AFTER:** `### The transition is fast` followed by "Most customers are fully on the new system within three to six weeks..."

### 3.16 Credential-Stacking / Stat-Bomb / Tension-Colon Openers
Opening patterns to avoid:
- **Credential stack:** "As a marketing leader who's run campaigns for five years at three companies..."
- **Stat bomb:** "73% of teams lose revenue to churn. Most don't know it."
- **Tension colon:** "The dirty secret of the industry: vendors don't actually want you to leave."
- **Common-belief-then-counter:** "Everyone says switching vendors is risky. It isn't."

All of these signal "blog post written by AI." Open on a number tied to a specific situation, a named person or company, or a specific observation instead — "Lisa's team cut deployment time from four hours to twenty minutes" beats any of the four openers above.

---

## 4. Vocabulary — 3-Tier System

**Domain-terminology exemption:** Industry-specific metrics, technical codes, regulatory terms, and legal language are exempt from Tier 2/3 density checks. "Significant" in a clinical finding, "crucial" in a compliance clause, or "critical" in an incident report are precise, not filler. Apply the tiers to general prose only — not to technical claims, quoted regulations, or domain vocabulary the audience will read as load-bearing.

### Tier 1 — Always Replace (5–20x more common in AI than human writing)

delve, pivotal, multifaceted, myriad, plethora, robust, seamless, leverage, unlock, unleash, harness, empower, embark, realm, landscape (metaphorical), tapestry, beacon, illuminate, bolster, meticulous, elevate, streamline, groundbreaking, transformative, unprecedented, game-changer

No judgment call. Cut or swap every time.

### Tier 2 — Flag in Clusters (2+ in same paragraph)

foster, facilitate, nuanced, crucial, cornerstone, paramount, burgeoning, navigate (metaphorical), journey (metaphorical), vital, critical, holistic, cutting-edge, comprehensive, ecosystem

One of these in a paragraph: fine. Two or more: rewrite the paragraph — the AI tell is the density, not any single word.

### Tier 3 — Flag at Density (~3%+ of content words)

significant, innovative, effective, dynamic, scalable, compelling, exceptional, sophisticated, strategic, impactful, meaningful, valuable, essential, key (as adjective)

These are real English words. Only flag when the draft leans on them as a crutch — if three+ appear in 100 words, the draft has no specific nouns to stand on.

### Filler Qualifiers — Always Cut

arguably, notably, importantly, essentially, fundamentally, truly, really, very, simply, just (as softener), quite, rather, somewhat

Exceptions: "just" meaning "only/recently" ("we just launched"). "really" in quoted dialogue.

---

## 5. MEDIUM Patterns (P2) — Stylistic Drag

| Pattern | Fix |
|---|---|
| **Compulsive tricolons** | Three-item lists everywhere. Break pattern — use twos and fours. |
| **Present participle stacking** | "Helping teams, driving revenue, improving outcomes" → convert to verbs. |
| **Em dashes as default punctuation** | See §6 budget. |
| **Premature lists** | Bullets before the idea is developed in prose. Write prose first; bullet only if the list is truly list-shaped. |
| **Colon-heavy titles** | "The Onboarding Revolution: Why Teams Need a New Playbook". Pick one clause. |
| **Only 2nd/3rd person voice** | Vary — use "we" when it's a first-party claim. |
| **Puffing up importance** | "It's critical that..." / "Now more than ever..." Delete the puff. |
| **Generic/vanilla tone** | No specific numbers, names, or examples. Add one concrete detail per paragraph. |
| **Hyphenated word-pair over-consistency** | "data-driven, outcomes-focused, customer-centered" stacked. Pick one. |
| **Superficial -ing analyses** | "By focusing on X, teams can achieve Y" — vague cause-effect. Name the mechanism. |
| **Arrow chains** | "Research → draft → review → publish". Fine once; tic if repeated. |
| **Period-separated word emphasis** | "Calm. Specific. Human." Fine rarely; tic if used more than once per piece. |
| **One-line paragraphs throughout** | LinkedIn-style formatting. OK for LinkedIn; not for blog/email. |
| **Inline-header vertical lists / boldface overuse** | Every third phrase bolded. Bold only what a scanner truly needs. |
| **Fake humility / engagement-bait closers** | "What am I missing?" / "Am I wrong?" — only keep if the question is real. |
| **Rhetorical throat-clearing** | "Let's talk about...", "Now, about X..." Start on the thing. |
| **False ranges** | "From startups to enterprises, from solo founders to large companies" when the two ends aren't on a meaningful scale. Pick the specific audience. |

---

## 6. Quantified Punctuation Budgets

Hard caps per piece. Going over one is usually a sign of an unearned rhythm.

| Mark | Budget | Notes |
|---|---|---|
| Em dash (—) | **Max 1 per 500 words** | Some authors prefer zero — if a voice profile bans them, swap for hyphens with spaces or commas. |
| Exclamation point | **Max 1 per 1,000 words** | External content only. Avoid in 1:1 emails unless register is explicitly enthusiastic. |
| Ellipsis (…) | **Max 1 per piece** | Usually delete entirely. |
| Semicolon | **Max 2 per 500 words** | Rare in natural speech. |
| Rhetorical question | **Max 1 per 500 words** | More than that and the piece sounds like a monologue pretending to be a conversation. |

---

## 7. Banned Openers (Hard Cuts)

Never ship a piece that opens with:
- "In today's [anything] landscape/world/era..."
- "In an era of..."
- "Now more than ever..."
- "In the world of..."
- "When it comes to..."
- "Whether you're X or Y..."

If you find one, cut the opener and start on the second paragraph — 90% of the time it's the real opener.

---

## 8. Author Voice — Configurable Carve-Outs

Some patterns look AI-ish in isolation but are part of an author's actual voice. **When an author voice profile is loaded, do not flag these patterns unless combined with other tells:**

- **Short sentences (intentionally punchy).** Example: "We lost the deal. She knew before I did." Leave it if the author writes that way.
- **Occasional sentence fragments.** Example: "Tough call, but the right one." Leave it.
- **Starting sentences with "And" or "But."** Example: "And the results were better than we expected." / "But that's not the only issue." Leave them.
- **One-line paragraphs** in Slack, internal memos, and personal LinkedIn — not in client-facing brand voice. Example from a LinkedIn post: "It took us three tries to get the pricing right." — on its own line — is a natural cadence for many writers.
- **Hyphens with spaces** instead of em dashes, if the author or brand profile specifies it.
- **Specific terms of address or honorifics** the audience expects (titled professionals, formal salutations) — load these from the voice profile.

The test: would this pattern read as natural if the author spoke it out loud? If yes, leave it. If the piece is client-facing brand voice (blog post, case study, landing page), these carve-outs tighten — default to the Channel × Strictness Matrix above.

If no voice profile is loaded, treat the patterns above as low-priority — flag only when stacked with other tells.

---

## 9. Sources

Detection patterns synthesized from:
- Carnegie Mellon (2025) AI-writing word-frequency study
- Wikipedia "Signs of AI Writing" editor guidance
- Buffer 52M-post LinkedIn analysis (2025)
- blader/ai-detection open-source taxonomy
- conor-humanizer 3-tier vocabulary model
- jalaalrd/ai-writing-tells quantified budgets
- "The Humanizer" LinkedIn archetype catalog

---

## 10. Guardrails — When Flags Are Wrong

### Stet Protocol

Sometimes a flagged pattern is the right call for the piece — a tricolon that's actually earned, a short sentence doing real work, a stylistic choice that reads as the author's actual register. When the user says "keep it," "stet," "leave this," or "that's intentional":

1. Honor the override for this draft and any subsequent re-run.
2. Do not re-flag the same span in the Self-Audit pass.
3. Do not propagate the stet to other drafts — it's a one-piece decision, not a permanent rule change.
4. If the user overrides the same pattern three-plus times across different drafts, surface it at the end: "You've kept [pattern] in 3+ drafts. Want me to add it to §8 (voice carve-outs) for your profile?"

### What NOT to Do

- **Don't strip voice to hit the checklist.** Short sentences, fragments, and "And"/"But" starts can be intentional. The humanizer removes tells — it does not normalize every piece into beige corporate prose. If a short sentence is doing real work, leave it.
- **Don't add words for the sake of it.** If a sentence is tight and clear, don't lengthen it to avoid "staccato." The staccato tell is about uniformity across the whole piece, not individual short sentences.
- **Don't fabricate replacements.** If you're cutting a vague authority claim ("studies show..."), don't invent a source. Cut the claim or flag it with `[ADD SPECIFIC SOURCE OR CUT]` inline.
- **Don't rewrite past the user's intent.** If the piece is meant to be punchy (ad headline, stop-scroll caption, subject line), the structural rules loosen. Judgment over mechanical application.
- **Don't silently approve a hollow draft.** A draft that passes every tell but says nothing specific is still broken. Flag `[HOLLOW]` and let the user decide.
- **Don't decline the task; escalate instead.** If a full rewrite would require replacing >80% of the words, the draft is a ghost-write request, not a humanizing task. Return it with a note rather than fabricating new content.
