# Changelog

All notable changes to this project will be documented here. The format is loosely based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows semantic versioning.

## [1.0.0] — 2026-04-29

Initial public release.

### Added
- Six-step humanizer pipeline (auto-detect channel → optional voice calibration → pattern scan → severity gate → rewrite → self-audit → emit).
- Severity tiers (CRITICAL / HIGH / MEDIUM / LOW) with explicit action mapping.
- 16 structural pattern detectors (dramatic reframe, manufactured punchline, staccato overdose, performative directness, runway sentences, persuasive authority tropes, tailing negations, elegant variation, copula avoidance, inspirational pivot, vulnerability performance, anaphora, universal authority without source, fragmented headers, credential-stacking / stat-bomb / tension-colon openers).
- Three-tier vocabulary system (always-replace / cluster-flag / density-flag) with domain-terminology exemption.
- Quantified punctuation budgets (em dash, exclamation, ellipsis, semicolon, rhetorical question).
- Banned openers list (hard cuts).
- Channel × Strictness matrix for 11 common writing channels.
- Per-channel hollow-failure-mode catalog.
- Stable output format with parseable section headers (Issues Found / Rewritten Draft / What Changed / Self-Audit / Final Version / Humanizer Report).
- Detect-only mode for read-only audits.
- Clean-but-hollow flag for drafts that pass the scan but lack substance.
- **Setup mode** — guided 7-question interview that produces a populated voice profile.
- Author voice profile template.
- Brand voice profile template.
- Worked before/after examples for email, LinkedIn, and blog intros.
- Stet protocol for honoring user overrides.
- Integration patterns for upstream drafting agents.
- Interoperability docs for Claude Code, Cursor, raw API, and CI.
