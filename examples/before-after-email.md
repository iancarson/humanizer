# Worked Example — Sales Email

A short cold-outreach email that triggers four AI tells. Walked through the full Humanizer pipeline.

---

## Input draft

```
Subject: A quick thought on your onboarding workflow

Hi Sarah,

I hope this email finds you well! I noticed your team has been growing rapidly,
and I wanted to share a quick thought.

In today's competitive landscape, leveraging the right onboarding workflow
isn't just important — it's transformative. We've helped dozens of companies
streamline their processes, unlock better retention, and empower their teams
to focus on what really matters.

I'd love to learn more about your specific challenges and explore how we
might help. Would you be open to a brief 15-minute call next week?

Let me know if you'd like me to share some additional materials in the
meantime!

Best,
Alex
```

---

## Pipeline output

### Step 0 — Channel detected

Email (greeting + sign-off + 1:1 register).

### Step 1 — Voice calibration

No voice profile loaded. Preserving draft's existing register; flagging tells universal to AI-generated outreach.

### Step 2 — Pattern scan

**Issues Found**

- **[CRITICAL]** "I hope this email finds you well!" — Sycophancy / opening throat-clearing → cut
- **[CRITICAL]** "Let me know if you'd like me to share some additional materials in the meantime!" — Chatbot artifact + unearned exclamation → cut
- **[HIGH]** "In today's competitive landscape" — Banned opener (§7) → cut
- **[HIGH]** "isn't just important — it's transformative" — Dramatic reframe (§3.1) + Tier 1 vocab ("transformative")
- **[CRITICAL]** "leveraging" — Tier 1 vocab → "using" or specific verb
- **[CRITICAL]** "streamline" — Tier 1 vocab → "speed up" or specific outcome
- **[CRITICAL]** "unlock" — Tier 1 vocab → cut or replace with specific outcome
- **[CRITICAL]** "empower their teams" — Tier 1 vocab + vague claim
- **[HIGH]** "Helped dozens of companies streamline / unlock / empower" — Present participle stacking (§5)
- **[HIGH]** "what really matters" — Filler qualifier ("really") + meaningless phrase
- **[HOLLOW]** No specific reason for outreach, no specific result, no specific stake. Reads like a template.

### Step 3 — Severity gate

Six Tier 1 hits, four pattern categories, plus `[HOLLOW]` → **full rewrite**.

### Step 4 — Rewrite

```
Subject: Onboarding times at [Company]

Hi Sarah,

We worked with three SaaS teams in the last quarter that were growing the way
yours is, and the same pattern showed up: onboarding time per hire crept from
three days to six as the team passed thirty people. Each had a different fix.

If that pattern is on your radar at all, I'd be glad to share what worked for
the team that recovered the fastest — fifteen minutes, no slides.

Thanks,
Alex
```

### Step 5 — Self-audit

> "What makes the above so obviously AI generated?"

- "If that pattern is on your radar" reads slightly templated. Tighter: "If you're seeing this..."
- The fifteen-minutes-no-slides sign-off is fine for cold email but borderline cliché. Leave for now; flag if it shows up again.

Revision pass:

```
Subject: Onboarding times at [Company]

Hi Sarah,

We worked with three SaaS teams in the last quarter that were growing the way
yours is, and the same pattern showed up: onboarding time per hire crept from
three days to six as the team passed thirty people. Each had a different fix.

If you're seeing this, I'd be glad to share what worked for the team that
recovered the fastest. Fifteen minutes, no slides.

Thanks,
Alex
```

### Final Version

(same as above)

### Humanizer Report

- **Channel detected:** email
- **Voice loaded:** none
- **Rewrite depth:** full
- **Clean-but-hollow:** no (specific situation, specific stake, specific ask)
- **Notes:** swapped 6 Tier 1 words; cut sycophancy + chatbot artifact + banned opener; replaced participle stack with named result; added a real-world reason for outreach
