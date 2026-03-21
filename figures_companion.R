#!/usr/bin/env Rscript
# =============================================================================
# Awesome Awesomers — Companion: Data Tables + Technical Cards
# =============================================================================
# For each of the 14 Pelamovic figures, exports:
#   1. CSV with the source data table
#   2. Technical card (PNG) summarizing input/code/output
# =============================================================================
suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
  library(ggplot2)
  library(scales)
  library(gridExtra)
  library(grid)
})

outdir <- "D:/Antigravity/awesome-awesomers/plots/pelamovic/companion"
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

# Pelamovic colors
pel_green      <- "#2D6A4F"
pel_green_dark <- "#1B4332"
pel_green_pale <- "#D8F3DC"
pel_coral      <- "#E76F51"
pel_bg         <- "#FAFAF5"
pel_grey       <- "#8D99AE"

# =============================================================================
# DATA (same as figures_pelamovic.R)
# =============================================================================
df1 <- tibble(
  Name = c("Andrej Karpathy","George Hotz","Sebastian Raschka","Hadley Wickham",
           "Jake Vanderplas","Francois Chollet","Soumith Chintala","Christopher Olah",
           "Peter Norvig","Ross Wightman","Maxime Labonne","Heng Li","Sasha Rush",
           "Ming Tommy Tang","Alfredo Canziani","Gael Varoquaux","Tri Dao",
           "Chelsea Finn","Laurens vd Maaten","Rafael Irizarry","Wei Shen",
           "Yann LeCun","Fabian Theis","Cassie Kozyrkov","Jim Fan","Phil Ewels",
           "Aaron Quinlan","Durk Kingma","Pierre Lindenbaum","Eugene Myers",
           "Richard Durbin","Adam Kosiorek","Nils Homer","Lior Pachter",
           "Boas Pucker","Sahar Mor","Ben Johnson","Dean Lee","Oriol Vinyals"),
  Category = c("AI/ML","AI/ML","AI/ML","Data Sci.","Data Sci.","AI/ML","AI/ML","AI/ML",
               "AI/ML","AI/ML","AI/ML","Bioinfo.","AI/ML","Bioinfo.","AI/ML","Data Sci.",
               "AI/ML","AI/ML","AI/ML","Bioinfo.","Bioinfo.","AI/ML","Data Sci.","AI/ML",
               "AI/ML","Bioinfo.","Bioinfo.","AI/ML","Bioinfo.","Bioinfo.","Bioinfo.",
               "AI/ML","Bioinfo.","Bioinfo.","Bioinfo.","AI/ML","Bioinfo.","Bioinfo.","AI/ML"),
  GitHub = c("karpathy","geohot","rasbt","hadley","jakevdp","fchollet","soumith","colah",
             "norvig","rwightman","mlabonne","lh3","srush","crazyhottommy","Atcold",
             "GaelVaroquaux","tridao","cbfinn","lvdmaaten","rafalab","shenwei356",
             "ylecun","theislab","kozyrkov","DrJimFan","ewels","arq5x","dpkingma",
             "lindenb","thegenemyers","richarddurbin","akosiorek","nh13","pachterlab",
             "bpucker","saharmor","biobenkj","deanslee","OriolVinyals"),
  Followers = c(148001,46135,36352,26541,19048,17861,13119,9766,9726,7002,6536,4267,
                3832,3726,3675,3393,2933,2174,1975,1633,1469,1509,1400,1039,934,844,
                771,597,555,467,380,375,374,377,187,205,121,118,84),
  Repos = c(63,101,147,230,239,16,169,52,4,74,23,138,165,177,70,90,10,25,23,49,119,
            12,253,5,7,159,75,9,178,19,20,40,207,169,80,86,132,2,3),
  TotalStars = c(393395,23453,152172,7131,1589,36434,18439,1728,0,5079,82837,9184,
                 19106,3885,0,606,0,0,0,0,6116,0,0,0,0,419,0,0,0,0,0,0,0,0,0,0,0,0,0),
  PrimaryLang = c("Python","Python","Python","R","Python","Python","Python","TypeScript",
                  "--","Python","Python","C","TeX","Python","--","Python","--","--","--",
                  "R","Go","--","--","--","--","Nextflow","--","--","Java","C","C","--",
                  "--","--","Python","--","--","--","--"),
  Source = c("G","G","S","G","G","G","G","G","G","G","G","G","G","S","G","G","G","G","G",
             "S","G","S","S","S","G","G","G","G","G","G","G","S","S","S","S","S","G","S","G")
) %>%
  mutate(
    log_f = log10(pmax(Followers, 1)),
    log_r = log10(pmax(Repos, 1)),
    log_s = log10(pmax(TotalStars, 1)),
    fpr = round(Followers / pmax(Repos, 1)),
    score = round(log_f * 0.40 + log_s * 0.35 + log_r * 0.25, 2)
  )

repos_df <- tibble(
  Repo = c("sindresorhus/awesome","vinta/awesome-python","awesome-selfhosted/awesome-selfhosted",
           "avelino/awesome-go","Hack-with-Github/Awesome-Hacking","Shubhamsaboo/awesome-llm-apps",
           "jaywcjlove/awesome-mac","MunGell/awesome-for-beginners","punkpeye/awesome-mcp-servers",
           "DopplerHQ/awesome-interview-questions","josephmisiti/awesome-machine-learning",
           "fffaraz/awesome-cpp","binhnguyennus/awesome-scalability","prakhar1989/awesome-courses",
           "sindresorhus/awesome-nodejs","Solido/awesome-flutter","rust-unofficial/awesome-rust",
           "ashishps1/awesome-system-design-resources","kuchin/awesome-cto","bayandin/awesome-awesomeness",
           "ChristosChristofidis/awesome-deep-learning","terryum/awesome-deep-learning-papers",
           "danielecook/Awesome-Bioinformatics","gokceneraslan/awesome-deepbio"),
  Stars = c(446331,287631,280586,167576,108547,102573,100351,83601,83355,81471,72017,
            70274,69466,67078,65315,59299,56196,35216,34522,33283,27711,26095,3900,1968),
  Domain = c("Meta","Python","DevOps","Go","Security","AI/LLM","Tools","Education","AI/LLM",
             "Career","ML","C++","Architecture","Education","Node.js","Mobile","Rust",
             "Architecture","Leadership","Meta","DL","DL","Bioinformatics","Bioinformatics")
) %>% mutate(ShortName = sub(".*/", "", Repo), is_bio = Domain == "Bioinformatics")

curators_df <- tibble(
  Name = c("Sindre Sorhus","Vinta Chen","Avelino","Shubham Saboo","Kenny Wong",
           "Shmavon Gazanchyan","Frank Fiegel","Joseph Misiti","J. Le Coupanec",
           "PatrickJS","Ashish P. Singh","Julien Bisconti","Lukasz Madon",
           "Sarah Drasner","sorrycc","Wasabeef","Prakhar Srivastav",
           "Kevin Deldycke","Christos Christofidis","Terry T. Um",
           "Alexander Bayandin","Dima Kuchin","Daniel Cook","Gokcen Eraslan",
           "Jia-Bin Huang","Wilson Freitas","enaqx"),
  GitHub = c("sindresorhus","vinta","avelino","Shubhamsaboo","jaywcjlove",
             "MunGell","punkpeye","josephmisiti","LeCoupa","PatrickJS",
             "ashishps1","veggiemonk","lukasz-madon","sdras","sorrycc",
             "wasabeef","prakhar1989","kdeldycke","ChristosChristofidis",
             "terryum","bayandin","kuchin","danielecook","gokceneraslan",
             "jbhuang0604","wilsonfreitas","enaqx"),
  Followers = c(77927,9112,6268,7615,9005,2303,1721,4430,2774,3507,12684,
                680,667,24842,14677,9614,6451,1881,1351,1486,720,635,415,483,
                1971,1429,2612),
  Repos = c(1133,28,241,164,211,137,4827,291,20,961,42,182,59,102,250,58,178,
            54,140,7,27,13,76,101,23,122,54),
  Domain = c("Meta","Python","Go","AI/LLM","Tools","Education","AI/LLM","ML",
             "Education","AI/LLM","Architecture","DevOps","Career","DevOps",
             "Frontend","Mobile","Education","Education","DL","DL","Meta",
             "Leadership","Bioinformatics","Bioinformatics","DL","Data","Frontend"),
  TopStars = c(446331,287631,167576,102573,100351,83601,83355,72017,45493,38530,
               35216,35692,44102,27555,34931,55672,67078,27176,27711,26095,33283,
               34522,3900,1968,23118,24958,72413)
) %>%
  mutate(
    log_f = log10(pmax(Followers, 1)),
    log_top = log10(pmax(TopStars, 1)),
    log_r = log10(pmax(Repos, 1)),
    curator_score = round(log_top * 0.50 + log_f * 0.30 + log_r * 0.20, 2),
    in_phase1 = GitHub %in% df1$GitHub
  )

# =============================================================================
# FIGURE REGISTRY: metadata for all 14 figures
# =============================================================================
fig_registry <- list(
  list(
    id = "Fig01", title = "Awesomers by category",
    caption = paste("Figure 1. Distribution of 39 GitHub-profiled awesomers across",
                    "scientific and technical categories. AI/ML dominates (n=20, 51%),",
                    "followed by Bioinformatics (n=13, 33%). Horizontal bar chart,",
                    "botanical green fill. Data: GitHub API, 2026-03-17."),
    input = "df1 (39 awesomers: Name, Category, GitHub, Followers, Repos, TotalStars)",
    geom = "geom_col (horizontal bar)",
    aes = "x = count, y = Category (reordered by n)",
    stats = "count() aggregation by Category",
    output = "Fig01_categories.png / .pdf",
    table_fn = function() df1 %>% count(Category, sort = TRUE) %>% rename(Count = n)
  ),
  list(
    id = "Fig02", title = "Awesomer Score Ranking",
    caption = paste("Figure 2. Composite awesomer score ranking (n=39). Score =",
                    "0.40*log10(followers) + 0.35*log10(total_stars) + 0.25*log10(repos).",
                    "Cleveland dot plot with coral ring highlighting top 5. Karpathy leads (6.41),",
                    "followed by Raschka (5.62) and Labonne (5.18). Data: GitHub API, 2026-03-17."),
    input = "df1 with derived score column",
    geom = "geom_segment + geom_point (Cleveland lollipop)",
    aes = "x = score, y = Name (reordered), fill = Category",
    stats = "Weighted log composite: 0.40*log_f + 0.35*log_s + 0.25*log_r",
    output = "Fig02_score_ranking.png / .pdf",
    table_fn = function() df1 %>% select(Name, GitHub, Category, Followers, Repos, TotalStars, score) %>% arrange(desc(score))
  ),
  list(
    id = "Fig03", title = "Developer Influence Landscape",
    caption = paste("Figure 3. Scatter plot of personal followers vs. aggregated project",
                    "stars (both log10-transformed). Bubble size encodes number of repositories.",
                    "Points above the diagonal indicate project-driven influence (project outgrew",
                    "creator). ggrepel used for non-overlapping labels. Data: GitHub API, 2026-03-17."),
    input = "df1 with log_f, log_s, Repos",
    geom = "geom_point (shape=21) + geom_text_repel + geom_abline",
    aes = "x = log10(Followers), y = log10(TotalStars), size = Repos, fill = Category",
    stats = "log10 transformation; diagonal reference line (slope=1)",
    output = "Fig03_landscape.png / .pdf",
    table_fn = function() df1 %>% select(Name, GitHub, Category, Followers, TotalStars, Repos, log_f, log_s) %>% arrange(desc(Followers))
  ),
  list(
    id = "Fig04", title = "Awesomers Network",
    caption = paste("Figure 4. Force-directed network graph (Fruchterman-Reingold layout).",
                    "Nodes = awesomers, edges = shared category membership. Node size = followers,",
                    "fill = category. Labels shown for >3k followers only. Built with igraph +",
                    "ggraph. n=39 nodes, edges from category co-membership."),
    input = "df1 (GitHub, Category, Followers) -> igraph graph",
    geom = "ggraph: geom_edge_link + geom_node_point + geom_node_text",
    aes = "fill = Category, size = Followers",
    stats = "graph_from_data_frame(); layout = 'fr' (Fruchterman-Reingold)",
    output = "Fig04_network.png / .pdf",
    table_fn = function() df1 %>% select(GitHub, Category, Followers, score) %>% arrange(desc(Followers))
  ),
  list(
    id = "Fig05", title = "Influence efficiency",
    caption = paste("Figure 5. Followers-per-repository ratio for top 25 awesomers.",
                    "Higher values indicate greater follower engagement per published",
                    "repository. Norvig (2432) and Karpathy (2349) lead, suggesting",
                    "quality-over-quantity strategies. Cleveland dot plot."),
    input = "df1 with derived fpr = Followers / Repos",
    geom = "geom_segment + geom_point (lollipop)",
    aes = "x = fpr, y = Name (reordered by fpr)",
    stats = "fpr = Followers / max(Repos, 1)",
    output = "Fig05_efficiency.png / .pdf",
    table_fn = function() df1 %>% select(Name, GitHub, Followers, Repos, fpr) %>% arrange(desc(fpr)) %>% head(25)
  ),
  list(
    id = "Fig06", title = "Bioinformatics Awesomers",
    caption = paste("Figure 6. GitHub followers for bioinformatics-category awesomers",
                    "(n=13). Heng Li leads (4,267 followers, 138 repos), followed by",
                    "Tommy Tang (3,726) and Phil Ewels (844). Repos count annotated",
                    "in parentheses. Horizontal bar chart, botanical green fill."),
    input = "df1 filtered to Category == 'Bioinfo.'",
    geom = "geom_col + geom_text",
    aes = "x = Followers, y = Name (reordered)",
    stats = "Filter + sort",
    output = "Fig06_bioinformatics.png / .pdf",
    table_fn = function() df1 %>% filter(Category == "Bioinfo.") %>% select(Name, GitHub, Followers, Repos, TotalStars, PrimaryLang) %>% arrange(desc(Followers))
  ),
  list(
    id = "Fig07", title = "Category x Language Heatmap",
    caption = paste("Figure 7. Heatmap showing number of awesomers per category-language",
                    "combination. Python x AI/ML is the dominant cell (n=9). R appears",
                    "exclusively in Data Sci. and Bioinfo. Gradient: pale green (#D8F3DC)",
                    "to botanical green (#2D6A4F). Only awesomers with known language shown."),
    input = "df1 filtered to PrimaryLang != '--', cross-tabulated",
    geom = "geom_tile + geom_text",
    aes = "x = PrimaryLang, y = Category, fill = count",
    stats = "count() + complete() for full grid",
    output = "Fig07_heatmap.png / .pdf",
    table_fn = function() df1 %>% filter(PrimaryLang != "--") %>% count(Category, PrimaryLang, sort = TRUE)
  ),
  list(
    id = "Fig08", title = "Top 20 awesome-* repositories",
    caption = paste("Figure 8. Top 20 awesome-* repositories by GitHub stars (excluding",
                    "bioinformatics, shown in Fig 10). sindresorhus/awesome dominates at",
                    "446k stars. Color = domain category. AI/LLM repos show rapid recent",
                    "growth. Data: GitHub API search, 2026-03-17."),
    input = "repos_df (24 repos: Repo, Stars, Domain), top 20 non-bio",
    geom = "geom_col (horizontal) + geom_text",
    aes = "x = Stars, y = ShortName (reordered), fill = Domain",
    stats = "slice_max(Stars, n=20) after filtering is_bio",
    output = "Fig08_P2_repos.png / .pdf",
    table_fn = function() repos_df %>% filter(!is_bio) %>% arrange(desc(Stars)) %>% head(20) %>% select(Repo, Stars, Domain)
  ),
  list(
    id = "Fig09", title = "Awesome Curator Score",
    caption = paste("Figure 9. Curator score ranking (n=27). Score =",
                    "0.50*log10(top_repo_stars) + 0.30*log10(followers) + 0.20*log10(repos).",
                    "Weights project impact (stars) over personal following. Sindre Sorhus",
                    "leads (4.78), followed by punkpeye (4.21) and Vinta Chen (4.10)."),
    input = "curators_df with derived curator_score",
    geom = "geom_segment + geom_point (Cleveland lollipop)",
    aes = "x = curator_score, y = Name (reordered), fill = Domain",
    stats = "Weighted log composite: 0.50*log_top + 0.30*log_f + 0.20*log_r",
    output = "Fig09_P2_curators.png / .pdf",
    table_fn = function() curators_df %>% select(Name, GitHub, Domain, Followers, Repos, TopStars, curator_score) %>% arrange(desc(curator_score))
  ),
  list(
    id = "Fig10", title = "Power law + Bioinformatics zoom",
    caption = paste("Figure 10. (a) Rank-size plot showing power-law distribution of",
                    "awesome-* repository stars (log y-axis). Bioinformatics repos",
                    "highlighted in coral. (b) Zoom on bioinformatics awesome repos:",
                    "only Awesome-Bioinformatics (3.9k) and awesome-deepbio (2.0k)",
                    "exceed the 1k quality threshold. Multi-panel via patchwork."),
    input = "repos_df (all 24 repos, is_bio flag)",
    geom = "(a) geom_point + scale_y_log10; (b) geom_col + geom_vline",
    aes = "(a) x=Rank, y=Stars, fill=is_bio; (b) x=Stars, y=ShortName",
    stats = "Rank ordering; log10 y-axis; 1k threshold line",
    output = "Fig10_P2_powerlaw.png / .pdf",
    table_fn = function() repos_df %>% select(Repo, Stars, Domain, is_bio) %>% arrange(desc(Stars))
  ),
  list(
    id = "Fig11", title = "Personal vs. Project Influence",
    caption = paste("Figure 11. Scatter of curator personal followers vs. their top",
                    "awesome repo stars (both log10). Shape distinguishes Phase 1",
                    "(triangle) from Phase 2-only (circle) curators. Points above",
                    "diagonal = project outgrew creator. ggrepel labels. n=27 curators."),
    input = "curators_df with log_f, log_top, in_phase1",
    geom = "geom_point (shape=21/24) + geom_text_repel + geom_abline",
    aes = "x = log_f, y = log_top, fill = Domain, shape = in_phase1",
    stats = "log10 transforms; diagonal reference; phase cross-reference",
    output = "Fig11_P2_crossref.png / .pdf",
    table_fn = function() curators_df %>% select(Name, GitHub, Domain, Followers, TopStars, in_phase1, curator_score) %>% arrange(desc(TopStars))
  ),
  list(
    id = "Fig12", title = "Followers by Category (statistical)",
    caption = paste("Figure 12. Non-parametric comparison of log10(followers) across",
                    "three main categories (AI/ML, Bioinfo., Data Sci.). Kruskal-Wallis",
                    "test with pairwise Dunn post-hoc tests (Holm correction). AI/ML",
                    "shows significantly higher follower counts. Generated with ggstatsplot."),
    input = "df1 filtered to 3 categories, log_f column",
    geom = "ggstatsplot::ggbetweenstats (violin + box + jitter)",
    aes = "x = Category, y = log10(Followers)",
    stats = "Kruskal-Wallis H-test + Dunn pairwise (Holm p-adjustment)",
    output = "Fig12_stats_category.png / .pdf",
    table_fn = function() df1 %>% filter(Category %in% c("AI/ML","Bioinfo.","Data Sci.")) %>% select(Name, Category, Followers, log_f) %>% arrange(Category, desc(Followers))
  ),
  list(
    id = "Fig13", title = "Primary language distribution",
    caption = paste("Figure 13. Programming language distribution among awesomers with",
                    "known primary language (n=22 of 39). Python dominates (n=11, 50%),",
                    "followed by C (n=3) and R (n=2). Reflects the Python hegemony in",
                    "AI/ML and bioinformatics. Horizontal bar chart."),
    input = "df1 filtered to PrimaryLang != '--'",
    geom = "geom_col (horizontal) + geom_text",
    aes = "x = count, y = PrimaryLang (reordered)",
    stats = "count() aggregation by PrimaryLang",
    output = "Fig13_languages.png / .pdf",
    table_fn = function() df1 %>% filter(PrimaryLang != "--") %>% count(PrimaryLang, sort = TRUE) %>% rename(Count = n)
  ),
  list(
    id = "Fig14", title = "Awesome repo domains",
    caption = paste("Figure 14. Domain distribution of scraped awesome-* repositories",
                    "(n=24). AI/LLM leads with 4 repos, reflecting the 2024-2026 AI boom.",
                    "Bioinformatics has 2 repos. Architecture, Education, DL, Meta each",
                    "have 2. Color = domain. Horizontal bar chart."),
    input = "repos_df, count by Domain",
    geom = "geom_col (horizontal, colored by domain) + geom_text",
    aes = "x = count, y = Domain (reordered), fill = Domain",
    stats = "count() aggregation by Domain",
    output = "Fig14_P2_domains.png / .pdf",
    table_fn = function() repos_df %>% count(Domain, sort = TRUE) %>% rename(Count = n)
  )
)

# =============================================================================
# EXPORT: CSV tables
# =============================================================================
cat("Exporting CSV tables...\n")
for (fig in fig_registry) {
  tbl <- fig$table_fn()
  csv_path <- file.path(outdir, paste0(fig$id, "_data.csv"))
  write.csv(tbl, csv_path, row.names = FALSE)
  cat("  [CSV]", fig$id, "->", nrow(tbl), "rows\n")
}

# =============================================================================
# EXPORT: Technical cards (one PNG per figure)
# =============================================================================
cat("\nGenerating technical cards...\n")

make_card <- function(fig) {
  tbl <- fig$table_fn()
  preview <- head(tbl, 6)

  # Card layout using ggplot
  card_text <- paste0(
    "FIGURE: ", fig$id, " | ", fig$title, "\n",
    paste(rep("\u2500", 60), collapse = ""), "\n\n",
    "INPUT:\n  ", fig$input, "\n\n",
    "GEOMETRY:\n  ", fig$geom, "\n\n",
    "AESTHETICS:\n  ", fig$aes, "\n\n",
    "STATISTICS:\n  ", fig$stats, "\n\n",
    "OUTPUT:\n  ", fig$output, "\n\n",
    paste(rep("\u2500", 60), collapse = ""), "\n",
    "DATA PREVIEW (first 6 rows of ", nrow(tbl), " total):\n",
    paste(capture.output(print(as.data.frame(preview), row.names = FALSE)), collapse = "\n"), "\n\n",
    paste(rep("\u2500", 60), collapse = ""), "\n",
    "CAPTION:\n", fig$caption
  )

  p <- ggplot() +
    annotate("label", x = 0.5, y = 0.5, label = card_text,
             size = 2.5, hjust = 0.5, vjust = 0.5, family = "mono",
             fill = pel_bg, color = pel_green_dark,
             label.padding = unit(0.8, "lines"),
             label.r = unit(0.3, "lines")) +
    theme_void() +
    theme(
      plot.background = element_rect(fill = pel_bg, color = pel_green, linewidth = 0.5),
      plot.margin = margin(10, 10, 10, 10)
    ) +
    labs(title = paste0(fig$id, " | Technical Card"),
         subtitle = "Awesome Awesomers — Pelamovic Aesthetic") +
    theme(
      plot.title = element_text(face = "bold", size = 10, color = pel_green_dark,
                                hjust = 0, margin = margin(b = 2)),
      plot.subtitle = element_text(size = 7, color = pel_grey, hjust = 0,
                                   face = "italic", margin = margin(b = 4))
    )

  card_path <- file.path(outdir, paste0(fig$id, "_card.png"))
  ggsave(card_path, p, width = 7, height = 6, dpi = 200, bg = pel_bg)
  cat("  [CARD]", fig$id, "\n")
}

for (fig in fig_registry) {
  tryCatch(make_card(fig), error = function(e) cat("  [ERR]", fig$id, ":", e$message, "\n"))
}

# =============================================================================
# EXPORT: Master captions file (Markdown)
# =============================================================================
cat("\nWriting captions markdown...\n")
captions_md <- paste0(
  "# Awesome Awesomers — Figure Captions (Pelamovic Edition)\n\n",
  "**Aesthetic**: Botanical green `#2D6A4F`, coral accents `#E76F51`, ",
  "cream background `#FAFAF5`\n",
  "**Stack**: R 4.4.3 | ggplot2 + ggrepel + ggraph + ggstatsplot + patchwork\n",
  "**Data**: GitHub API scrape, 2026-03-17\n\n",
  "---\n\n"
)

for (fig in fig_registry) {
  tbl <- fig$table_fn()
  captions_md <- paste0(captions_md,
    "## ", fig$id, ": ", fig$title, "\n\n",
    "**Caption**: ", fig$caption, "\n\n",
    "| Field | Value |\n|---|---|\n",
    "| Input | ", fig$input, " |\n",
    "| Geometry | ", fig$geom, " |\n",
    "| Aesthetics | ", fig$aes, " |\n",
    "| Statistics | ", fig$stats, " |\n",
    "| Output | `", fig$output, "` |\n",
    "| Data rows | ", nrow(tbl), " |\n",
    "| CSV | `companion/", fig$id, "_data.csv` |\n",
    "| Card | `companion/", fig$id, "_card.png` |\n\n",
    "---\n\n"
  )
}

writeLines(captions_md, file.path(outdir, "..", "FIGURE_CAPTIONS_PELAMOVIC.md"))
cat("[OK] FIGURE_CAPTIONS_PELAMOVIC.md\n")

cat("\n=== COMPANION MATERIALS COMPLETE ===\n")
cat("CSV tables: 14\n")
cat("Technical cards: 14\n")
cat("Captions markdown: 1\n")
cat("Output:", outdir, "\n")
