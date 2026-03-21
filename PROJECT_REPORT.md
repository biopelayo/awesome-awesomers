# Awesome Awesomers — Project Report
> Generated 2026-03-20 | Sistema Pelamovic

## 1. Objective

Build a curated, data-driven meta-awesome-list profiling the **people** behind
the awesome movement on GitHub — developers, researchers, and thought leaders
across AI, bioinformatics, and computational science.

## 2. Methodology

### 2.1 Discovery Pipeline

```
Seed → Graph Expansion → Profile Enrichment → Scoring → Tiering
```

| Step | Method | Yield |
|------|--------|-------|
| Seed | biopelayo.github.io (10 refs) + LinkedIn | 47 candidates |
| Graph hop 1 | `crazyhottommy/following` (43 edges) | +32 new |
| Graph hop 2 | `rasbt/following` (40 edges) | +25 new |
| Phase 2 scrape | Top awesome-* repos (>30k stars) | +27 curators |
| **Total unique** | | **~95 candidates** |

### 2.2 Data Sources

- **GitHub REST API** via `gh` CLI — profiles, repos, stars, followers, following
- **biopelayo.github.io** — seed references (WebFetch)
- **GitLab/Bitbucket** — attempted, blocked by auth (403/404)
- **LinkedIn** — blocked without Chrome extension auth

### 2.3 Scoring

```
Influence Score = 0.40 × log₁₀(followers) + 0.35 × log₁₀(total_stars) + 0.25 × log₁₀(repos)
Curator Score  = 0.50 × log₁₀(top_repo_stars) + 0.30 × log₁₀(followers) + 0.20 × log₁₀(repos)
```

## 3. Results

### 3.1 Phase 1: Awesomers (People)

- **39 profiled** across 4 categories
- Domain split: AI/ML 59%, Bioinformatics 28%, Data Science 13%
- Top 5 by score: Karpathy (5.28), Raschka (4.83), Hadley (4.27), Hotz (4.24), Vanderplas (4.08)
- Primary languages: Python (59%), R (10%), C (8%)
- Discovery: 69% via graph expansion, 31% seed

### 3.2 Phase 2: Awesome Repo Ecosystem

- **65 repos** scraped (threshold >1k stars general, >50 bio)
- **27 curators** profiled
- Stars range: 54 (bioinfo format list) to 446k (sindresorhus/awesome)
- Power-law distribution confirmed (Zipf exponent ~0.8)
- Top curator: Sindre Sorhus (score 5.48, 576k total stars)

### 3.3 Graph Expansion

- `crazyhottommy` → 43 following (bioinformatics hub)
  - Notable discoveries: Brent Pedersen (1.4k followers), Brad Chapman (976), Vince Buffalo (930), Olga Botvinnik (828)
- `rasbt` → 40 following (AI/ML hub)
  - Notable: Wes McKinney (16k), Andreas Mueller (11k), Olivier Grisel (4.9k), Niels Rogge (4.3k)

### 3.4 Bioinformatics Ecosystem

- Top awesome-bioinformatics: Daniel Cook (3.9k stars)
- Major bioinformatics awesomers by followers:
  1. Heng Li — 4,267 (minimap2, bwa-mem2)
  2. Tommy Tang — 3,732 (genomics resources)
  3. Rafael Irizarry — 1,633 (R/bioc education)
  4. Brent Pedersen — 1,425 (mosdepth, smoove)
  5. Wei Shen — 1,469 (seqkit, csvtk)

## 4. Deliverables

### 4.1 Figures (44 total)

11 publication-quality figures × 4 palettes (Simpsons, Futurama, JAMA, Lancet):

| Fig | Content | Panels |
|-----|---------|--------|
| 1 | Phase 1 Overview | Category, Source, Language, Followers strip |
| 2 | Score Ranking | Cleveland dot + decomposition |
| 3 | Landscape | Repos vs followers scatter + marginals |
| 4 | Social Network | Directed graph + betweenness centrality |
| 5 | Activity & Efficiency | Timeline + quadrants |
| 6 | Bioinformatics Deep-dive | Followers, repos, stars/repo |
| 7 | Multi-metric Heatmap | Top 20 normalized matrix |
| 8 | P2 Top Repos | Top 30 awesome-* + domain dist. |
| 9 | P2 Curator Ranking | Score + personal vs project influence |
| 10 | P2 Power Law | Rank-stars + bioinformatics zoom |
| 11 | P2 Cross-reference | Phase 1 × Phase 2 network |

All at 300 DPI (PNG + PDF vector), with panel labels (a, b, c...), subtitles, and figure captions.

### 4.2 Documents

| File | Purpose |
|------|---------|
| `README.md` | Main awesome list (repo-ready) |
| `AWESOMER_CRITERIA.md` | Formal inclusion criteria + tiers |
| `FIGURE_CAPTIONS.md` | Detailed figure descriptions |
| `PROJECT_REPORT.md` | This report |

### 4.3 Scripts

| Script | Purpose |
|--------|---------|
| `figures_master.py` | All 11 figures × 4 palettes |
| `phase2_awesome_repos.py` | Phase 2 data + figures |
| `analysis_enriched.py` | Enriched analysis |
| `generate_research_paper.py` | Paper generation |

## 5. Pending / Future Work

- [ ] LinkedIn scraping via Chrome extension (full contact network)
- [ ] GitLab/Bitbucket with proper auth tokens
- [ ] Temporal analysis (activity trends over months)
- [ ] Citation cross-reference (OpenAlex integration, cf. BioAwesomers project)
- [ ] Automated weekly refresh via scheduled task
- [ ] Push to `github.com/biopelayo/awesome-awesomers`

## 6. Limitations

1. **GitHub-centric** — GitLab/Bitbucket/SourceHut not covered
2. **Snapshot data** — scraped 2026-03-17/20, will decay
3. **English bias** — discovery pipeline biased toward English-language profiles
4. **Graph depth** — only 2 hops from seed; deeper exploration may reveal more
5. **Score simplicity** — log-weighted composite may not capture all dimensions of "awesomeness"

---
*Awesome Awesomers is a project of the Sistema Pelamovic ecosystem.*
*Author: Pelayo González de Lena Rodríguez (@biopelayo)*
