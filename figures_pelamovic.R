#!/usr/bin/env Rscript
# =============================================================================
# Awesome Awesomers — Pelamovic Aesthetic Edition
# =============================================================================
# Visual identity: botanical green #2D6A4F, coral accents #E76F51,
# thin strokes, rounded elements, maximum space usage, Nature-style
# =============================================================================
suppressPackageStartupMessages({
  library(tidyplots)
  library(ggplot2)
  library(ggrepel)
  library(dplyr)
  library(tidyr)
  library(scales)
  library(patchwork)
  library(igraph)
  library(ggraph)
})
has_ggstatsplot <- requireNamespace("ggstatsplot", quietly = TRUE)
if (has_ggstatsplot) library(ggstatsplot)

outdir <- "D:/Antigravity/awesome-awesomers/plots/pelamovic"
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

# =============================================================================
# PELAMOVIC PALETTE
# =============================================================================
# Primary
pel_green      <- "#2D6A4F"
pel_green_light <- "#95D5B2"
pel_green_pale  <- "#D8F3DC"
pel_green_dark  <- "#1B4332"
# Accents
pel_coral      <- "#E76F51"
pel_salmon     <- "#F4845F"
pel_peach      <- "#FFDAB9"
# Neutrals
pel_grey       <- "#8D99AE"
pel_grey_light <- "#CED4DA"
pel_grey_dark  <- "#2B2B2B"
pel_bg         <- "#FAFAF5"
pel_white      <- "#FFFFFF"

# Category palette (Pelamovic-ized)
cat_pal <- c(
  "AI/ML"           = pel_coral,
  "Bioinfo."        = pel_green,
  "Data Sci."       = "#52796F",
  "Meta"            = "#B5838D",
  "Python"          = "#457B9D",
  "Go"              = pel_green_light,
  "DevOps"          = pel_grey,
  "Frontend"        = "#A8DADC",
  "AI/LLM"          = pel_salmon,
  "Security"        = "#6D6875",
  "Education"       = "#52796F",
  "Architecture"    = "#BC6C25",
  "ML"              = pel_coral,
  "DL"              = "#D62828",
  "Tools"           = "#8D99AE",
  "Mobile"          = "#2A9D8F",
  "Career"          = "#B5838D",
  "Data"            = "#264653",
  "Bioinformatics"  = pel_green,
  "Leadership"      = "#BC6C25",
  "Design"          = "#A8DADC",
  "Java"            = "#E9C46A",
  ".NET"            = pel_grey,
  "Node.js"         = "#52796F",
  "Rust"            = "#BC6C25",
  "C++"             = "#6D6875",
  "PHP"             = "#457B9D"
)

# Ordered domain palette for Phase 2
dom_pal <- c(pel_green, pel_coral, pel_salmon, "#457B9D", "#52796F",
             pel_grey, "#A8DADC", "#2A9D8F", "#BC6C25", "#264653",
             "#B5838D", "#6D6875", "#E9C46A", "#D62828", pel_green_light,
             pel_green_dark)

# =============================================================================
# THEME PELAMOVIC — Publication, tight, botanical
# =============================================================================
theme_pelamovic <- function(base_size = 8.5) {
  theme_minimal(base_size = base_size) +
    theme(
      text             = element_text(family = "sans", color = pel_grey_dark),
      plot.background  = element_rect(fill = pel_bg, color = NA),
      panel.background = element_rect(fill = pel_bg, color = NA),
      plot.title       = element_text(face = "bold", size = rel(1.35), hjust = 0,
                                      color = pel_green_dark, margin = margin(b = 1)),
      plot.subtitle    = element_text(size = rel(0.82), color = pel_grey,
                                      hjust = 0, face = "italic", margin = margin(b = 5)),
      plot.caption     = element_text(size = rel(0.65), color = "#AAAAAA",
                                      hjust = 0, face = "italic", margin = margin(t = 4)),
      plot.tag         = element_text(face = "bold", size = 11, color = pel_green_dark),
      axis.title       = element_text(size = rel(0.95), color = pel_grey_dark),
      axis.text        = element_text(size = rel(0.8), color = "#666666"),
      axis.line        = element_line(color = pel_grey_light, linewidth = 0.3),
      panel.grid.major = element_line(color = "#EDEDED", linewidth = 0.25),
      panel.grid.minor = element_blank(),
      legend.background = element_rect(fill = pel_bg, color = NA),
      legend.position  = "bottom",
      legend.key.size  = unit(0.3, "cm"),
      legend.text      = element_text(size = rel(0.7)),
      legend.title     = element_text(size = rel(0.8), face = "bold", color = pel_green_dark),
      strip.text       = element_text(face = "bold", size = rel(0.9), color = pel_green_dark),
      plot.margin      = margin(8, 10, 5, 8)
    )
}

save_fig <- function(p, name, w = 7.2, h = 5) {
  ggsave(file.path(outdir, paste0(name, ".png")), p, width = w, height = h,
         dpi = 300, bg = pel_bg)
  ggsave(file.path(outdir, paste0(name, ".pdf")), p, width = w, height = h,
         bg = pel_bg)
  cat("[OK]", name, "\n")
}

# =============================================================================
# DATA (identical to previous script)
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
    spr = round(TotalStars / pmax(Repos, 1)),
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
) %>%
  mutate(
    ShortName = sub(".*/", "", Repo),
    log_stars = log10(pmax(Stars, 1)),
    is_bio = Domain == "Bioinformatics",
    Rank = row_number(desc(Stars))
  )

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
# FIG 1 — Category overview (ggplot2, Pelamovic bars)
# =============================================================================
cat("Fig 1...\n")
p1 <- df1 %>%
  count(Category, sort = TRUE) %>%
  mutate(Category = reorder(Category, n)) %>%
  ggplot(aes(x = n, y = Category)) +
  geom_col(fill = pel_green, width = 0.55, alpha = 0.85) +
  geom_text(aes(label = n), hjust = -0.3, size = 2.8, color = pel_green_dark, fontface = "bold") +
  labs(
    title = "Awesomers by category",
    subtitle = "Distribution of 39 profiled developers across domains",
    x = "Count", y = NULL,
    caption = "Data: GitHub API | 2026-03-17 | n = 39 profiles"
  ) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.15))) +
  theme_pelamovic() +
  theme(panel.grid.major.y = element_blank())

save_fig(p1, "Fig01_categories", w = 4.5, h = 3.8)

# =============================================================================
# FIG 2 — Score ranking (Cleveland dot, Pelamovic green + coral highlights)
# =============================================================================
cat("Fig 2...\n")
top_n_highlight <- 5
p2 <- df1 %>%
  mutate(
    Name = reorder(Name, score),
    is_top = rank(-score) <= top_n_highlight
  ) %>%
  ggplot(aes(x = score, y = Name)) +
  geom_segment(aes(xend = 0, yend = Name), color = pel_grey_light, linewidth = 0.35) +
  geom_point(aes(fill = Category), shape = 21, size = 2.8, stroke = 0.3,
             color = pel_white, alpha = 0.9) +
  geom_text(aes(label = sprintf("%.1f", score)), hjust = -0.5, size = 2, color = "#999") +
  # Highlight top 5
  geom_point(data = . %>% filter(is_top), aes(fill = Category),
             shape = 21, size = 3.5, stroke = 0.6, color = pel_coral) +
  scale_fill_manual(values = cat_pal) +
  labs(
    title = "Awesomer Score Ranking",
    subtitle = "Composite: 0.40 log(followers) + 0.35 log(stars) + 0.25 log(repos)",
    x = "Awesomer Score", y = NULL,
    caption = "Top 5 highlighted with coral ring | Score = weighted log-metric composite"
  ) +
  theme_pelamovic() +
  theme(
    axis.text.y = element_text(size = 5.5, color = "#555"),
    panel.grid.major.y = element_blank(),
    legend.position = "right",
    legend.key.size = unit(0.25, "cm")
  )

save_fig(p2, "Fig02_score_ranking", w = 7, h = 7.5)

# =============================================================================
# FIG 3 — Landscape: Followers vs Stars (scatter + ggrepel)
# =============================================================================
cat("Fig 3...\n")
p3 <- df1 %>%
  ggplot(aes(x = log_f, y = log_s)) +
  # Reference diagonal
  geom_abline(slope = 1, intercept = 0, linetype = "dashed",
              color = pel_green_pale, linewidth = 0.5) +
  # Points
  geom_point(aes(fill = Category, size = Repos), shape = 21,
             stroke = 0.3, color = pel_white, alpha = 0.8) +
  geom_text_repel(
    aes(label = GitHub), size = 2, color = "#777", fontface = "italic",
    max.overlaps = 25, segment.color = pel_grey_light, segment.size = 0.15,
    seed = 42, box.padding = 0.3
  ) +
  # Annotation
  annotate("label", x = 2.3, y = 5.2, fill = pel_green_pale, color = pel_green_dark,
           label = "Stars > Followers\n(project outgrew creator)",
           size = 2, fontface = "italic", label.size = 0.2, label.r = unit(0.15, "lines")) +
  scale_fill_manual(values = cat_pal) +
  scale_size_continuous(range = c(1.2, 7), breaks = c(10, 50, 150, 250),
                        name = "Repos") +
  labs(
    title = "Developer Influence Landscape",
    subtitle = "Personal followers vs. aggregated project stars (log scale) | Bubble size = repos",
    x = expression(log[10]~"(Followers)"), y = expression(log[10]~"(Total Stars)"),
    fill = "Category",
    caption = "Diagonal = equal followers and stars. Above = project-driven influence."
  ) +
  theme_pelamovic() +
  theme(legend.position = "right")

save_fig(p3, "Fig03_landscape", w = 8, h = 5.8)

# =============================================================================
# FIG 4 — Network (ggraph, Pelamovic botanical)
# =============================================================================
cat("Fig 4...\n")
edges <- tibble(from = character(), to = character())
for (cat in unique(df1$Category)) {
  members <- df1 %>% filter(Category == cat) %>% pull(GitHub)
  if (length(members) > 1) {
    combos <- combn(members, 2)
    edges <- bind_rows(edges, tibble(from = combos[1,], to = combos[2,]))
  }
}
g <- graph_from_data_frame(edges, directed = FALSE,
       vertices = df1 %>% select(name = GitHub, Category, Followers, score))
g <- simplify(g)

set.seed(42)
p4 <- ggraph(g, layout = "fr") +
  geom_edge_link(alpha = 0.06, color = pel_green_light, edge_width = 0.3) +
  geom_node_point(aes(fill = Category, size = Followers), shape = 21,
                  stroke = 0.3, color = pel_white, alpha = 0.85) +
  geom_node_text(
    aes(label = ifelse(Followers > 3000, name, "")),
    size = 2, repel = TRUE, max.overlaps = 20, color = pel_grey_dark,
    fontface = "bold"
  ) +
  scale_fill_manual(values = cat_pal) +
  scale_size_continuous(range = c(1.5, 12), labels = label_comma(), guide = "none") +
  labs(
    title = "Awesomers Network",
    subtitle = "Force-directed layout | Edges = shared category",
    fill = "Category",
    caption = "Node size = followers. Labels shown for >3k followers."
  ) +
  theme_void(base_size = 8) +
  theme(
    plot.background = element_rect(fill = pel_bg, color = NA),
    plot.title = element_text(face = "bold", size = 11, color = pel_green_dark, hjust = 0),
    plot.subtitle = element_text(size = 7, color = pel_grey, hjust = 0, face = "italic"),
    plot.caption = element_text(size = 5.5, color = "#AAA", face = "italic", hjust = 0),
    legend.position = "bottom",
    legend.text = element_text(size = 6),
    legend.key.size = unit(0.25, "cm"),
    legend.title = element_text(size = 7, face = "bold", color = pel_green_dark),
    plot.margin = margin(8, 8, 5, 8)
  )

save_fig(p4, "Fig04_network", w = 7.5, h = 6.5)

# =============================================================================
# FIG 5 — Efficiency: followers per repo (horizontal lollipop)
# =============================================================================
cat("Fig 5...\n")
p5 <- df1 %>%
  slice_max(fpr, n = 25) %>%
  mutate(Name = reorder(Name, fpr)) %>%
  ggplot(aes(x = fpr, y = Name)) +
  geom_segment(aes(xend = 0, yend = Name), color = pel_grey_light, linewidth = 0.3) +
  geom_point(fill = pel_green, shape = 21, size = 2.5, stroke = 0.3, color = pel_white) +
  geom_text(aes(label = comma(fpr)), hjust = -0.3, size = 2, color = "#999") +
  labs(
    title = "Influence efficiency",
    subtitle = "Followers per repository | Top 25 awesomers",
    x = "Followers / Repos", y = NULL,
    caption = "Higher = greater follower engagement per published repository."
  ) +
  scale_x_continuous(labels = label_comma(), expand = expansion(mult = c(0, 0.15))) +
  theme_pelamovic() +
  theme(panel.grid.major.y = element_blank())

save_fig(p5, "Fig05_efficiency", w = 5.5, h = 6.5)

# =============================================================================
# FIG 6 — Bioinformatics deep-dive (paired bars: followers + repos)
# =============================================================================
cat("Fig 6...\n")
bio <- df1 %>%
  filter(Category == "Bioinfo.") %>%
  mutate(Name = reorder(Name, Followers))

p6 <- bio %>%
  ggplot(aes(x = Followers, y = Name)) +
  geom_col(fill = pel_green, width = 0.5, alpha = 0.85) +
  geom_text(aes(label = paste0(GitHub, " (", Repos, " repos)")),
            hjust = -0.05, size = 2, color = "#777", fontface = "italic") +
  scale_x_continuous(labels = label_comma(), expand = expansion(mult = c(0, 0.35))) +
  labs(
    title = "Bioinformatics Awesomers",
    subtitle = "GitHub followers | Bioinfo. category | repos count in parentheses",
    x = "Followers", y = NULL,
    caption = "Heng Li, Tommy Tang, Phil Ewels, Wei Shen lead the bioinformatics cohort."
  ) +
  theme_pelamovic() +
  theme(panel.grid.major.y = element_blank())

save_fig(p6, "Fig06_bioinformatics", w = 6, h = 4.5)

# =============================================================================
# FIG 7 — Heatmap: Category x Language
# =============================================================================
cat("Fig 7...\n")
hl <- df1 %>%
  filter(PrimaryLang != "--") %>%
  count(Category, PrimaryLang) %>%
  complete(Category, PrimaryLang, fill = list(n = 0))

p7 <- hl %>%
  ggplot(aes(x = PrimaryLang, y = Category, fill = n)) +
  geom_tile(color = pel_bg, linewidth = 1) +
  geom_text(aes(label = ifelse(n > 0, n, ""), color = ifelse(n > 2, "white", pel_grey_dark)),
            size = 3.2, fontface = "bold", show.legend = FALSE) +
  scale_color_identity() +
  scale_fill_gradient(low = pel_green_pale, high = pel_green, name = "n",
                      guide = guide_colorbar(barwidth = 6, barheight = 0.4)) +
  labs(
    title = "Category x Language",
    subtitle = "Number of awesomers per category-language combination",
    x = NULL, y = NULL,
    caption = "Only awesomers with a known primary programming language shown."
  ) +
  theme_pelamovic() +
  theme(
    axis.text.x = element_text(angle = 40, hjust = 1, size = 7),
    panel.grid = element_blank(),
    legend.position = "bottom"
  )

save_fig(p7, "Fig07_heatmap", w = 5.5, h = 4)

# =============================================================================
# FIG 8 — Phase 2: Top awesome repos (horizontal bars)
# =============================================================================
cat("Fig 8...\n")
p8 <- repos_df %>%
  filter(!is_bio) %>%
  slice_max(Stars, n = 20) %>%
  mutate(ShortName = reorder(ShortName, Stars)) %>%
  ggplot(aes(x = Stars, y = ShortName, fill = Domain)) +
  geom_col(width = 0.55, alpha = 0.85) +
  geom_text(aes(label = paste0(comma(Stars / 1000, accuracy = 0.1), "k")),
            hjust = -0.1, size = 2, color = "#999") +
  scale_fill_manual(values = cat_pal) +
  scale_x_continuous(labels = label_comma(), expand = expansion(mult = c(0, 0.12))) +
  labs(
    title = "Top 20 awesome-* repositories",
    subtitle = "GitHub stars | Bioinformatics repos excluded (see Fig 10)",
    x = "Stars", y = NULL, fill = "Domain",
    caption = "Source: GitHub API, 2026-03-17 | sindresorhus/awesome dominates at 446k stars."
  ) +
  theme_pelamovic() +
  theme(
    panel.grid.major.y = element_blank(),
    axis.text.y = element_text(size = 5.5, family = "mono"),
    legend.position = "right",
    legend.key.size = unit(0.25, "cm")
  )

save_fig(p8, "Fig08_P2_repos", w = 7, h = 6)

# =============================================================================
# FIG 9 — Phase 2: Curator score (Cleveland dot)
# =============================================================================
cat("Fig 9...\n")
p9 <- curators_df %>%
  mutate(Name = reorder(Name, curator_score)) %>%
  ggplot(aes(x = curator_score, y = Name)) +
  geom_segment(aes(xend = 0, yend = Name), color = pel_grey_light, linewidth = 0.3) +
  geom_point(aes(fill = Domain), shape = 21, size = 2.8, stroke = 0.3, color = pel_white) +
  geom_text(aes(label = sprintf("%.1f", curator_score)), hjust = -0.4, size = 2, color = "#999") +
  scale_fill_manual(values = cat_pal) +
  labs(
    title = "Awesome Curator Score",
    subtitle = "0.50 log(top_repo_stars) + 0.30 log(followers) + 0.20 log(repos)",
    x = "Curator Score", y = NULL, fill = "Domain",
    caption = "Score weights project impact (stars) over personal following."
  ) +
  theme_pelamovic() +
  theme(
    axis.text.y = element_text(size = 5.5),
    panel.grid.major.y = element_blank(),
    legend.position = "right",
    legend.key.size = unit(0.25, "cm")
  )

save_fig(p9, "Fig09_P2_curators", w = 7, h = 7)

# =============================================================================
# FIG 10 — Power law + bioinformatics zoom (patchwork)
# =============================================================================
cat("Fig 10...\n")
p10a <- repos_df %>%
  ggplot(aes(x = Rank, y = Stars)) +
  geom_point(aes(fill = ifelse(is_bio, "Bioinformatics", "General")),
             shape = 21, size = ifelse(repos_df$is_bio, 3.5, 2),
             stroke = 0.3, color = pel_white, alpha = 0.85) +
  geom_text_repel(
    data = repos_df %>% filter(Rank <= 3 | is_bio),
    aes(label = ShortName), size = 2, color = "#777", fontface = "italic",
    seed = 42, max.overlaps = 15, segment.color = pel_grey_light, segment.size = 0.15
  ) +
  scale_y_log10(labels = label_comma()) +
  scale_fill_manual(values = c("General" = pel_green, "Bioinformatics" = pel_coral),
                    name = NULL) +
  labs(
    title = "Power law in awesome-* repos",
    subtitle = "Rank-size (log y) | Bio repos highlighted",
    x = "Rank", y = "Stars (log)"
  ) +
  theme_pelamovic() +
  theme(legend.position = c(0.75, 0.85), legend.background = element_blank())

bio_r <- repos_df %>% filter(is_bio) %>% mutate(ShortName = reorder(ShortName, Stars))
p10b <- bio_r %>%
  ggplot(aes(x = Stars, y = ShortName)) +
  geom_col(fill = pel_green, width = 0.45, alpha = 0.85) +
  geom_text(aes(label = comma(Stars)), hjust = -0.15, size = 2.5, color = "#777") +
  geom_vline(xintercept = 1000, linetype = "dashed", color = pel_coral, linewidth = 0.4) +
  annotate("label", x = 1500, y = 1.3, label = "1k threshold", size = 2,
           fill = pel_peach, color = pel_coral, label.size = 0.2,
           label.r = unit(0.15, "lines"), fontface = "italic") +
  scale_x_continuous(expand = expansion(mult = c(0, 0.25))) +
  labs(
    title = "Bioinformatics awesome repos",
    subtitle = "Only 2 exceed quality threshold",
    x = "Stars", y = NULL
  ) +
  theme_pelamovic() +
  theme(panel.grid.major.y = element_blank())

p10 <- p10a + p10b + plot_layout(widths = c(1.5, 1)) +
  plot_annotation(tag_levels = "a",
    theme = theme(
      plot.background = element_rect(fill = pel_bg, color = NA),
      plot.tag = element_text(face = "bold", size = 10, color = pel_green_dark)
    ))

save_fig(p10, "Fig10_P2_powerlaw", w = 9.5, h = 4.5)

# =============================================================================
# FIG 11 — Cross-reference: personal vs project influence
# =============================================================================
cat("Fig 11...\n")
p11 <- curators_df %>%
  ggplot(aes(x = log_f, y = log_top)) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed",
              color = pel_green_pale, linewidth = 0.5) +
  geom_point(aes(fill = Domain, shape = in_phase1), size = 3,
             stroke = 0.3, color = pel_white, alpha = 0.85) +
  geom_text_repel(aes(label = GitHub), size = 2, color = "#777", fontface = "italic",
                  max.overlaps = 20, segment.color = pel_grey_light,
                  segment.size = 0.15, seed = 42) +
  scale_fill_manual(values = cat_pal) +
  scale_shape_manual(values = c("FALSE" = 21, "TRUE" = 24),
                     labels = c("Phase 2 only", "Also in Phase 1"), name = "Phase") +
  annotate("label", x = 2.8, y = 5.5, label = "Repo outgrew\ncreator",
           size = 2, fill = pel_green_pale, color = pel_green_dark,
           label.size = 0.2, label.r = unit(0.15, "lines"), fontface = "italic") +
  labs(
    title = "Personal vs. Project Influence",
    subtitle = "Curators: followers vs. top awesome repo stars | Shape = phase overlap",
    x = expression(log[10]~"(Followers)"), y = expression(log[10]~"(Top repo stars)"),
    fill = "Domain",
    caption = "Above diagonal = project-driven. Triangle = also in Phase 1."
  ) +
  theme_pelamovic() +
  theme(legend.position = "right")

save_fig(p11, "Fig11_P2_crossref", w = 7.5, h = 5.5)

# =============================================================================
# FIG 12 — Statistical: Kruskal-Wallis (ggstatsplot, Pelamovic theme)
# =============================================================================
if (has_ggstatsplot) {
  cat("Fig 12...\n")
  p12 <- ggbetweenstats(
    data = df1 %>% filter(Category %in% c("AI/ML", "Bioinfo.", "Data Sci.")),
    x = Category, y = log_f,
    type = "nonparametric",
    pairwise.comparisons = TRUE,
    pairwise.display = "all",
    p.adjust.method = "holm",
    title = "Followers by Category",
    subtitle = "Kruskal-Wallis + pairwise Dunn tests (Holm correction)",
    xlab = "", ylab = expression(log[10]~"(Followers)"),
    caption = "AI/ML awesomers have significantly higher followings than Bioinfo./Data Sci.",
    ggtheme = theme_pelamovic()
  ) +
    scale_color_manual(values = c("AI/ML" = pel_coral, "Bioinfo." = pel_green,
                                  "Data Sci." = "#52796F"))
  save_fig(p12, "Fig12_stats_category", w = 6, h = 5)
} else {
  cat("[SKIP] Fig 12 (ggstatsplot not available)\n")
}

# =============================================================================
# FIG 13 — Languages (horizontal bar)
# =============================================================================
cat("Fig 13...\n")
p13 <- df1 %>%
  filter(PrimaryLang != "--") %>%
  count(PrimaryLang, sort = TRUE) %>%
  mutate(PrimaryLang = reorder(PrimaryLang, n)) %>%
  ggplot(aes(x = n, y = PrimaryLang)) +
  geom_col(fill = pel_green, width = 0.5, alpha = 0.85) +
  geom_text(aes(label = n), hjust = -0.4, size = 3, color = pel_green_dark, fontface = "bold") +
  scale_x_continuous(expand = expansion(mult = c(0, 0.15))) +
  labs(
    title = "Primary language distribution",
    subtitle = "Programming languages used by awesomers",
    x = "Number of awesomers", y = NULL,
    caption = "Python dominates. R and C reflect bioinfo/data science niches."
  ) +
  theme_pelamovic() +
  theme(panel.grid.major.y = element_blank())

save_fig(p13, "Fig13_languages", w = 4.5, h = 3.5)

# =============================================================================
# FIG 14 — Phase 2 domain breakdown
# =============================================================================
cat("Fig 14...\n")
p14 <- repos_df %>%
  count(Domain, sort = TRUE) %>%
  mutate(Domain = reorder(Domain, n)) %>%
  ggplot(aes(x = n, y = Domain, fill = Domain)) +
  geom_col(width = 0.5, alpha = 0.85, show.legend = FALSE) +
  geom_text(aes(label = n), hjust = -0.4, size = 2.8, color = pel_green_dark, fontface = "bold") +
  scale_fill_manual(values = cat_pal) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.15))) +
  labs(
    title = "Awesome repo domains",
    subtitle = "Distribution of scraped awesome-* repositories by domain",
    x = "Number of repos", y = NULL,
    caption = "AI/LLM has overtaken traditional dev categories in awesome repo creation."
  ) +
  theme_pelamovic() +
  theme(panel.grid.major.y = element_blank())

save_fig(p14, "Fig14_P2_domains", w = 5, h = 4.5)

# =============================================================================
cat("\n=== ALL PELAMOVIC FIGURES GENERATED ===\n")
cat("Output:", outdir, "\n")
