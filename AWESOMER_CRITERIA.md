# Awesome Awesomers — Formal Criteria

## Definition

An **Awesomer** is a developer, researcher, or thought leader whose open-source presence
demonstrates sustained impact on the community through code, curation, or education.

## Inclusion Criteria (meet ≥2 of 4)

| Criterion | Threshold | Rationale |
|-----------|-----------|-----------|
| **C1. Followers** | ≥200 GitHub followers | Signals peer recognition |
| **C2. Curation** | Maintains ≥1 awesome-* list OR >50 starred repos | Active knowledge curator |
| **C3. Productivity** | ≥50 public repos OR ≥10 with >10 stars | Sustained output |
| **C4. Impact** | ≥1k total stars OR ≥1 repo with >500 stars | Community adoption |

## Composite Score

```
Score = 0.40 × log₁₀(followers) + 0.35 × log₁₀(total_stars) + 0.25 × log₁₀(repos)
```

- **Tier 1 (Elite):** Score ≥ 4.0 — e.g., Karpathy, Raschka, Hadley
- **Tier 2 (Established):** Score 3.0–3.99 — e.g., Heng Li, Sasha Rush, Tommy Tang
- **Tier 3 (Rising):** Score 2.0–2.99 — e.g., Boas Pucker, Dean Lee
- **Unranked:** Score < 2.0 — below threshold, monitor

## Discovery Pipeline

```
Seed (biopelayo web + LinkedIn) → GitHub following graph → Profile enrichment → Score → Rank
```

1. **Seed**: 10 people from biopelayo.github.io
2. **Graph expansion**: Follow edges from seed × 2 hops (crazyhottommy → 43 follows, rasbt → 40 follows)
3. **Enrichment**: GitHub API (followers, repos, stars, languages, activity)
4. **Scoring**: Apply composite formula
5. **Tiering**: Assign tier based on score

## Current Census

| Phase | Source | Candidates | After filtering |
|-------|--------|------------|-----------------|
| Phase 1 | Seed + graph | 39 | 39 (all ≥ Tier 3) |
| Phase 2 | awesome-* repos | 27 curators | 27 (all ≥ Tier 2) |
| Expansion | crazyhottommy follows | 43 new | ~30 (≥ C1 threshold) |
| Expansion | rasbt follows | 40 new | ~25 (≥ C1 threshold) |
| **Total unique** | | **~95** | **~80** |

## Domain Distribution

- AI/ML: ~45%
- Bioinformatics: ~25%
- Data Science: ~15%
- Other (DevOps, Frontend, etc.): ~15%

## Platform Coverage

| Platform | Status |
|----------|--------|
| GitHub | ✅ Full API access |
| GitLab | ❌ 403 (auth required) |
| Bitbucket | ❌ 404 (auth required) |
| LinkedIn | ⚠️ Via Chrome extension only |

---
*Generated 2026-03-20 by Sistema Pelamovic*
