# Awesome Awesomers — Figure Captions (Pelamovic Edition)

**Aesthetic**: Botanical green `#2D6A4F`, coral accents `#E76F51`, cream background `#FAFAF5`
**Stack**: R 4.4.3 | ggplot2 + ggrepel + ggraph + ggstatsplot + patchwork
**Data**: GitHub API scrape, 2026-03-17

---

## Fig01: Awesomers by category

**Caption**: Figure 1. Distribution of 39 GitHub-profiled awesomers across scientific and technical categories. AI/ML dominates (n=20, 51%), followed by Bioinformatics (n=13, 33%). Horizontal bar chart, botanical green fill. Data: GitHub API, 2026-03-17.

| Field | Value |
|---|---|
| Input | df1 (39 awesomers: Name, Category, GitHub, Followers, Repos, TotalStars) |
| Geometry | geom_col (horizontal bar) |
| Aesthetics | x = count, y = Category (reordered by n) |
| Statistics | count() aggregation by Category |
| Output | `Fig01_categories.png / .pdf` |
| Data rows | 3 |
| CSV | `companion/Fig01_data.csv` |
| Card | `companion/Fig01_card.png` |

---

## Fig02: Awesomer Score Ranking

**Caption**: Figure 2. Composite awesomer score ranking (n=39). Score = 0.40*log10(followers) + 0.35*log10(total_stars) + 0.25*log10(repos). Cleveland dot plot with coral ring highlighting top 5. Karpathy leads (6.41), followed by Raschka (5.62) and Labonne (5.18). Data: GitHub API, 2026-03-17.

| Field | Value |
|---|---|
| Input | df1 with derived score column |
| Geometry | geom_segment + geom_point (Cleveland lollipop) |
| Aesthetics | x = score, y = Name (reordered), fill = Category |
| Statistics | Weighted log composite: 0.40*log_f + 0.35*log_s + 0.25*log_r |
| Output | `Fig02_score_ranking.png / .pdf` |
| Data rows | 39 |
| CSV | `companion/Fig02_data.csv` |
| Card | `companion/Fig02_card.png` |

---

## Fig03: Developer Influence Landscape

**Caption**: Figure 3. Scatter plot of personal followers vs. aggregated project stars (both log10-transformed). Bubble size encodes number of repositories. Points above the diagonal indicate project-driven influence (project outgrew creator). ggrepel used for non-overlapping labels. Data: GitHub API, 2026-03-17.

| Field | Value |
|---|---|
| Input | df1 with log_f, log_s, Repos |
| Geometry | geom_point (shape=21) + geom_text_repel + geom_abline |
| Aesthetics | x = log10(Followers), y = log10(TotalStars), size = Repos, fill = Category |
| Statistics | log10 transformation; diagonal reference line (slope=1) |
| Output | `Fig03_landscape.png / .pdf` |
| Data rows | 39 |
| CSV | `companion/Fig03_data.csv` |
| Card | `companion/Fig03_card.png` |

---

## Fig04: Awesomers Network

**Caption**: Figure 4. Force-directed network graph (Fruchterman-Reingold layout). Nodes = awesomers, edges = shared category membership. Node size = followers, fill = category. Labels shown for >3k followers only. Built with igraph + ggraph. n=39 nodes, edges from category co-membership.

| Field | Value |
|---|---|
| Input | df1 (GitHub, Category, Followers) -> igraph graph |
| Geometry | ggraph: geom_edge_link + geom_node_point + geom_node_text |
| Aesthetics | fill = Category, size = Followers |
| Statistics | graph_from_data_frame(); layout = 'fr' (Fruchterman-Reingold) |
| Output | `Fig04_network.png / .pdf` |
| Data rows | 39 |
| CSV | `companion/Fig04_data.csv` |
| Card | `companion/Fig04_card.png` |

---

## Fig05: Influence efficiency

**Caption**: Figure 5. Followers-per-repository ratio for top 25 awesomers. Higher values indicate greater follower engagement per published repository. Norvig (2432) and Karpathy (2349) lead, suggesting quality-over-quantity strategies. Cleveland dot plot.

| Field | Value |
|---|---|
| Input | df1 with derived fpr = Followers / Repos |
| Geometry | geom_segment + geom_point (lollipop) |
| Aesthetics | x = fpr, y = Name (reordered by fpr) |
| Statistics | fpr = Followers / max(Repos, 1) |
| Output | `Fig05_efficiency.png / .pdf` |
| Data rows | 25 |
| CSV | `companion/Fig05_data.csv` |
| Card | `companion/Fig05_card.png` |

---

## Fig06: Bioinformatics Awesomers

**Caption**: Figure 6. GitHub followers for bioinformatics-category awesomers (n=13). Heng Li leads (4,267 followers, 138 repos), followed by Tommy Tang (3,726) and Phil Ewels (844). Repos count annotated in parentheses. Horizontal bar chart, botanical green fill.

| Field | Value |
|---|---|
| Input | df1 filtered to Category == 'Bioinfo.' |
| Geometry | geom_col + geom_text |
| Aesthetics | x = Followers, y = Name (reordered) |
| Statistics | Filter + sort |
| Output | `Fig06_bioinformatics.png / .pdf` |
| Data rows | 14 |
| CSV | `companion/Fig06_data.csv` |
| Card | `companion/Fig06_card.png` |

---

## Fig07: Category x Language Heatmap

**Caption**: Figure 7. Heatmap showing number of awesomers per category-language combination. Python x AI/ML is the dominant cell (n=9). R appears exclusively in Data Sci. and Bioinfo. Gradient: pale green (#D8F3DC) to botanical green (#2D6A4F). Only awesomers with known language shown.

| Field | Value |
|---|---|
| Input | df1 filtered to PrimaryLang != '--', cross-tabulated |
| Geometry | geom_tile + geom_text |
| Aesthetics | x = PrimaryLang, y = Category, fill = count |
| Statistics | count() + complete() for full grid |
| Output | `Fig07_heatmap.png / .pdf` |
| Data rows | 11 |
| CSV | `companion/Fig07_data.csv` |
| Card | `companion/Fig07_card.png` |

---

## Fig08: Top 20 awesome-* repositories

**Caption**: Figure 8. Top 20 awesome-* repositories by GitHub stars (excluding bioinformatics, shown in Fig 10). sindresorhus/awesome dominates at 446k stars. Color = domain category. AI/LLM repos show rapid recent growth. Data: GitHub API search, 2026-03-17.

| Field | Value |
|---|---|
| Input | repos_df (24 repos: Repo, Stars, Domain), top 20 non-bio |
| Geometry | geom_col (horizontal) + geom_text |
| Aesthetics | x = Stars, y = ShortName (reordered), fill = Domain |
| Statistics | slice_max(Stars, n=20) after filtering is_bio |
| Output | `Fig08_P2_repos.png / .pdf` |
| Data rows | 20 |
| CSV | `companion/Fig08_data.csv` |
| Card | `companion/Fig08_card.png` |

---

## Fig09: Awesome Curator Score

**Caption**: Figure 9. Curator score ranking (n=27). Score = 0.50*log10(top_repo_stars) + 0.30*log10(followers) + 0.20*log10(repos). Weights project impact (stars) over personal following. Sindre Sorhus leads (4.78), followed by punkpeye (4.21) and Vinta Chen (4.10).

| Field | Value |
|---|---|
| Input | curators_df with derived curator_score |
| Geometry | geom_segment + geom_point (Cleveland lollipop) |
| Aesthetics | x = curator_score, y = Name (reordered), fill = Domain |
| Statistics | Weighted log composite: 0.50*log_top + 0.30*log_f + 0.20*log_r |
| Output | `Fig09_P2_curators.png / .pdf` |
| Data rows | 27 |
| CSV | `companion/Fig09_data.csv` |
| Card | `companion/Fig09_card.png` |

---

## Fig10: Power law + Bioinformatics zoom

**Caption**: Figure 10. (a) Rank-size plot showing power-law distribution of awesome-* repository stars (log y-axis). Bioinformatics repos highlighted in coral. (b) Zoom on bioinformatics awesome repos: only Awesome-Bioinformatics (3.9k) and awesome-deepbio (2.0k) exceed the 1k quality threshold. Multi-panel via patchwork.

| Field | Value |
|---|---|
| Input | repos_df (all 24 repos, is_bio flag) |
| Geometry | (a) geom_point + scale_y_log10; (b) geom_col + geom_vline |
| Aesthetics | (a) x=Rank, y=Stars, fill=is_bio; (b) x=Stars, y=ShortName |
| Statistics | Rank ordering; log10 y-axis; 1k threshold line |
| Output | `Fig10_P2_powerlaw.png / .pdf` |
| Data rows | 24 |
| CSV | `companion/Fig10_data.csv` |
| Card | `companion/Fig10_card.png` |

---

## Fig11: Personal vs. Project Influence

**Caption**: Figure 11. Scatter of curator personal followers vs. their top awesome repo stars (both log10). Shape distinguishes Phase 1 (triangle) from Phase 2-only (circle) curators. Points above diagonal = project outgrew creator. ggrepel labels. n=27 curators.

| Field | Value |
|---|---|
| Input | curators_df with log_f, log_top, in_phase1 |
| Geometry | geom_point (shape=21/24) + geom_text_repel + geom_abline |
| Aesthetics | x = log_f, y = log_top, fill = Domain, shape = in_phase1 |
| Statistics | log10 transforms; diagonal reference; phase cross-reference |
| Output | `Fig11_P2_crossref.png / .pdf` |
| Data rows | 27 |
| CSV | `companion/Fig11_data.csv` |
| Card | `companion/Fig11_card.png` |

---

## Fig12: Followers by Category (statistical)

**Caption**: Figure 12. Non-parametric comparison of log10(followers) across three main categories (AI/ML, Bioinfo., Data Sci.). Kruskal-Wallis test with pairwise Dunn post-hoc tests (Holm correction). AI/ML shows significantly higher follower counts. Generated with ggstatsplot.

| Field | Value |
|---|---|
| Input | df1 filtered to 3 categories, log_f column |
| Geometry | ggstatsplot::ggbetweenstats (violin + box + jitter) |
| Aesthetics | x = Category, y = log10(Followers) |
| Statistics | Kruskal-Wallis H-test + Dunn pairwise (Holm p-adjustment) |
| Output | `Fig12_stats_category.png / .pdf` |
| Data rows | 39 |
| CSV | `companion/Fig12_data.csv` |
| Card | `companion/Fig12_card.png` |

---

## Fig13: Primary language distribution

**Caption**: Figure 13. Programming language distribution among awesomers with known primary language (n=22 of 39). Python dominates (n=11, 50%), followed by C (n=3) and R (n=2). Reflects the Python hegemony in AI/ML and bioinformatics. Horizontal bar chart.

| Field | Value |
|---|---|
| Input | df1 filtered to PrimaryLang != '--' |
| Geometry | geom_col (horizontal) + geom_text |
| Aesthetics | x = count, y = PrimaryLang (reordered) |
| Statistics | count() aggregation by PrimaryLang |
| Output | `Fig13_languages.png / .pdf` |
| Data rows | 8 |
| CSV | `companion/Fig13_data.csv` |
| Card | `companion/Fig13_card.png` |

---

## Fig14: Awesome repo domains

**Caption**: Figure 14. Domain distribution of scraped awesome-* repositories (n=24). AI/LLM leads with 4 repos, reflecting the 2024-2026 AI boom. Bioinformatics has 2 repos. Architecture, Education, DL, Meta each have 2. Color = domain. Horizontal bar chart.

| Field | Value |
|---|---|
| Input | repos_df, count by Domain |
| Geometry | geom_col (horizontal, colored by domain) + geom_text |
| Aesthetics | x = count, y = Domain (reordered), fill = Domain |
| Statistics | count() aggregation by Domain |
| Output | `Fig14_P2_domains.png / .pdf` |
| Data rows | 18 |
| CSV | `companion/Fig14_data.csv` |
| Card | `companion/Fig14_card.png` |

---


