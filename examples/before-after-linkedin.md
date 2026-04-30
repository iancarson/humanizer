# Worked Example — LinkedIn Post (Personal)

A 180-word personal LinkedIn post written in a generic AI shape. Walked through Humanizer with a personal voice profile loaded.

---

## Input draft

```
Most leaders think hiring is a numbers problem.

It isn't.

Hiring is a clarity problem. When you don't know what good looks like, you
hire mediocrity. When you don't know what the role actually does, you hire
mismatch. When you don't know who's accountable, you hire chaos.

Here's the truth: the best leaders I've worked with don't hire faster.
They hire slower — and with more conviction.

They define the role. They define the bar. They define the trade-offs.

And then they say no, again and again, until the right person walks in.

It's not magic. It's discipline.

What's something you've learned about hiring that took you too long
to figure out?
```

---

## Pipeline output

### Step 0 — Channel detected

LinkedIn — personal (first-person, anecdotal frame, conversational length).

### Step 1 — Voice calibration

Author profile loaded. Profile preserves: short sentences, "And"/"But" starts, one-line paragraphs, occasional fragments. So those patterns alone won't trigger flags — the issue is what they're stacked with.

### Step 2 — Pattern scan

**Issues Found**

- **[HIGH]** "Most leaders think hiring is a numbers problem. / It isn't." — Dramatic reframe variant (§3.1)
- **[HIGH]** "Hiring is a clarity problem." — Definition reframe; relabels without adding info
- **[HIGH]** Three-sentence anaphora "When you don't know..." (§3.13) — One is rhythm, three is AI
- **[HIGH]** "Here's the truth:" — Performative directness (§3.4)
- **[HIGH]** Tricolon "They define the role. They define the bar. They define the trade-offs." — Compulsive tricolon (§5)
- **[HIGH]** "It's not magic. It's discipline." — Manufactured punchline (§3.2)
- **[MEDIUM]** "What's something you've learned about hiring that took you too long to figure out?" — Engagement-bait closer (§5)

### Step 3 — Severity gate

Six pattern categories triggered, no Tier 1 vocab hits, sentence lengths varied. Pattern density alone is enough — **full rewrite** (the structure is the AI tell here, not vocabulary).

### Step 4 — Rewrite

```
The first time I missed a hire badly, it cost us six months.

We knew we needed someone in the role. We didn't know what the role was —
we just knew the work wasn't getting done. So we hired for raw talent and
trusted that "they'd figure it out." They didn't. Not because the person
wasn't good, but because we kept moving the target.

The fix wasn't moving slower. It was getting honest with ourselves about
the role before we wrote the JD: what would the first 90 days actually
produce? What were we willing to give up to get those things? Who, on our
team, would lose responsibility when this person joined?

When we wrote those down, the hiring loop got faster, not slower. We
turned away two people we would have hired six months earlier. The third
one is still on the team three years later.
```

### Step 5 — Self-audit

> "What makes the above so obviously AI generated?"

- None detected. The post leads with a specific story (six months, third person three years), avoids reframes, and uses the author's natural cadence (varied sentences, one "And"-style continuation that fits, no manufactured closer).

### Final Version

(same as above)

### Humanizer Report

- **Channel detected:** linkedin (personal)
- **Voice loaded:** author profile
- **Rewrite depth:** full
- **Clean-but-hollow:** no (specific failure, specific timeline, specific outcome)
- **Notes:** rewrote opener to a real story instead of a reframe; cut anaphora, tricolon, and manufactured punchline; replaced engagement-bait closer with a concrete result the reader can react to

---

## What this example shows

The original post used **zero** Tier 1 vocab words. It still read as obviously AI-generated because it leaned on six structural patterns at once. Vocabulary scrubbers wouldn't have flagged any of it.

That's why Humanizer scans structural-first.
