#!/usr/bin/env Rscript
# =============================================================================
# Awesome Awesomers — Tidyplots + ggplot2 + ggrepel + ggstatsplot
# Publication-quality (Nature/Cell Reports aesthetic)
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

# Try loading ggstatsplot (may not be installed)
has_ggstatsplot <- requireNamespace("ggstatsplot", quietly = TRUE)
if (has_ggstatsplot) library(ggstatsplot)

outdir <- "D:/Antigravity/awesome-awesomers/plots/tidyplots"
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

# =============================================================================
# PALETTES — ggsci Simpsons inspired (user preference)
# =============================================================================
pal_simpsons <- c("#FED439","#709AE1","#8A9197","#D2AF81","#FD7446",
                  "#D5E4A2","#197EC0","#F05C3B","#46732E","#71D0F5",
                  "#370335","#075149","#C80813","#91331F","#1A9993","#FD8CC1")
pal_accent  <- "#FD7446"
pal_accent2 <- "#709AE1"
pal_dark    <- "#2b2b2b"
pal_grey    <- "#8A9197"

# Category palette
cat_colors <- c(
  "AI/ML" = "#FD7446", "Bioinfo." = "#197EC0", "Data Sci." = "#46732E",
  "Meta" = "#FED439", "Python" = "#709AE1", "Go" = "#71D0F5",
  "DevOps" = "#8A9197", "Frontend" = "#D5E4A2", "AI/LLM" = "#F05C3B",
  "Security" = "#370335", "Education" = "#075149", "Architecture" = "#C80813",
  "ML" = "#FD7446", "DL" = "#91331F", "Tools" = "#D2AF81",
  "Mobile" = "#1A9993", "Career" = "#FD8CC1", "Data" = "#197EC0",
  "Bioinformatics" = "#197EC0", "Leadership" = "#D2AF81",
  "Design" = "#D5E4A2", "Java" = "#FED439", ".NET" = "#8A9197",
  "Node.js" = "#46732E", "Rust" = "#C80813", "C++" = "#370335",
  "PHP" = "#075149"
)

# =============================================================================
# THEME — Publication quality, tight, Nature-style
# =============================================================================
theme_pub <- function(base_size = 8) {
  theme_minimal(base_size = base_size) +
    theme(
      text = element_text(family = "sans", color = pal_dark),
      plot.title = element_text(face = "bold", size = rel(1.3), hjust = 0, margin = margin(b = 2)),
      plot.subtitle = element_text(size = rel(0.85), color = "#777", hjust = 0, margin = margin(b = 4)),
      plot.caption = element_text(size = rel(0.7), color = "#999", hjust = 0, face = "italic"),
      axis.title = element_text(size = rel(1.0)),
      axis.text = element_text(size = rel(0.85), color = "#444"),
      panel.grid.major = element_line(color = "#e8e8e8", linewidth = 0.3),
      panel.grid.minor = element_blank(),
      legend.position = "bottom",
      legend.key.size = unit(0.35, "cm"),
      legend.text = element_text(size = rel(0.75)),
      legend.title = element_text(size = rel(0.85), face = "bold"),
      plot.margin = margin(6, 8, 4, 6),
      strip.text = element_text(face = "bold", size = rel(0.9))
    )
}

save_fig <- function(p, name, w = 7.2, h = 5) {
  ggsave(file.path(outdir, paste0(name, ".png")), p, width = w, height = h, dpi = 300, bg = "white")
  ggsave(file.path(outdir, paste0(name, ".pdf")), p, width = w, height = h, bg = "white")
  cat("[OK]", name, "\n")
}

# =============================================================================
# DATA — Phase 1: Awesomers
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
  TopRepo = c("nanoGPT","fromthetransistor","LLMs-from-scratch","adv-r","JSAnimation",
              "stable-diff-tf","mini-sglang","lucid","--","timm","--","minimap2",
              "awesome-o1","genomics-resources","--","--","--","--","--","--","--","--",
              "--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--"),
  TopStars = c(55059,6456,88460,2454,240,324,3,9,0,59,0,2143,1213,1373,0,0,0,0,0,0,0,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
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

# =============================================================================
# DATA — Phase 2: Awesome repos
# =============================================================================
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

# =============================================================================
# DATA — Phase 2: Curators
# =============================================================================
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
  TopAwesome = c("awesome","awesome-python","awesome-go","awesome-llm-apps","awesome-mac",
                 "awesome-for-beginners","awesome-mcp-servers","awesome-machine-learning",
                 "awesome-cheatsheets","awesome-cursorrules","awesome-system-design",
                 "awesome-docker","awesome-remote-job","awesome-actions","awesome-javascript",
                 "awesome-android-ui","awesome-courses","awesome-falsehood",
                 "awesome-deep-learning","awesome-deep-learning-papers","awesome-awesomeness",
                 "awesome-cto","Awesome-Bioinformatics","awesome-deepbio",
                 "awesome-computer-vision","awesome-quant","awesome-react"),
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
# FIG 1 — Overview: Category distribution + Source (tidyplots)
# =============================================================================
cat("Generating Fig 1...\n")
p1a <- df1 %>%
  count(Category, sort = TRUE) %>%
  mutate(Category = reorder(Category, n)) %>%
  tidyplot(x = n, y = Category) %>%
  add_barstack_absolute(width = 0.6) %>%
  adjust_colors(new_colors = pal_accent) %>%
  adjust_title("Awesomers by category") %>%
  adjust_x_axis(title = "Count (n)") %>%
  adjust_y_axis(title = "") %>%
  adjust_caption("n = 39 GitHub profiles scraped 2026-03-17")

p1b <- df1 %>%
  count(Source) %>%
  mutate(Source = ifelse(Source == "G", "GitHub graph", "Seed (manual)")) %>%
  tidyplot(x = Source, y = n) %>%
  add_barstack_absolute(width = 0.5) %>%
  adjust_colors(new_colors = c(pal_accent, pal_accent2)) %>%
  adjust_title("Discovery source") %>%
  adjust_x_axis(title = "") %>%
  adjust_y_axis(title = "Count") %>%
  adjust_caption("G = graph expansion, S = seed list")

save_fig(p1a, "Fig01a_categories_tidy", w = 4, h = 3.5)
save_fig(p1b, "Fig01b_source_tidy", w = 3.5, h = 3.5)

# =============================================================================
# FIG 2 — Score ranking (Cleveland dot plot, ggplot2 + ggrepel)
# =============================================================================
cat("Generating Fig 2...\n")
p2 <- df1 %>%
  mutate(Name = reorder(Name, score)) %>%
  ggplot(aes(x = score, y = Name)) +
  geom_segment(aes(xend = 0, yend = Name), color = "#e0e0e0", linewidth = 0.5) +
  geom_point(aes(color = Category), size = 2.5, alpha = 0.9) +
  geom_text(aes(label = sprintf("%.1f", score)), hjust = -0.4, size = 2, color = "#888") +
  scale_color_manual(values = cat_colors) +
  labs(
    title = "Awesomer Score Ranking",
    subtitle = "Composite: 0.40 log(followers) + 0.35 log(total_stars) + 0.25 log(repos)",
    x = "Awesomer Score", y = NULL,
    caption = "Data: GitHub API scrape 2026-03-17 | Score = weighted log-metric composite"
  ) +
  theme_pub() +
  theme(
    axis.text.y = element_text(size = 5.5),
    legend.position = "right",
    legend.key.size = unit(0.3, "cm")
  )

save_fig(p2, "Fig02_score_ranking", w = 7, h = 7)

# =============================================================================
# FIG 3 — Followers vs Stars landscape (ggplot2 + ggrepel)
# =============================================================================
cat("Generating Fig 3...\n")
p3 <- df1 %>%
  ggplot(aes(x = log_f, y = log_s, color = Category, size = Repos)) +
  geom_point(alpha = 0.8) +
  geom_text_repel(
    aes(label = GitHub), size = 2.2, max.overlaps = 25,
    segment.color = "#ccc", segment.size = 0.2, seed = 42
  ) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "#ddd", linewidth = 0.5) +
  annotate("text", x = 2.2, y = 5.3, label = "Stars > Followers\n(project outgrew creator)",
           size = 2, color = "#bbb", fontface = "italic") +
  scale_color_manual(values = cat_colors) +
  scale_size_continuous(range = c(1, 6), breaks = c(10, 50, 150, 250)) +
  labs(
    title = "Developer Influence Landscape",
    subtitle = "Followers vs. total aggregated stars (log scale) | Size = number of repos",
    x = expression(log[10](Followers)), y = expression(log[10](Total~Stars)),
    caption = "Diagonal: equal followers and stars. Points above = project-driven influence."
  ) +
  theme_pub() +
  theme(legend.position = "right")

save_fig(p3, "Fig03_landscape", w = 7.5, h = 5.5)

# =============================================================================
# FIG 4 — Network graph (ggraph + igraph)
# =============================================================================
cat("Generating Fig 4...\n")
# Category-based edges only (no external "biopelayo" node)
edges <- tibble(from = character(), to = character())
for (cat in unique(df1$Category)) {
  members <- df1 %>% filter(Category == cat) %>% pull(GitHub)
  if (length(members) > 1) {
    combos <- combn(members, 2)
    edges <- bind_rows(edges, tibble(from = combos[1,], to = combos[2,]))
  }
}

g <- graph_from_data_frame(edges, directed = FALSE, vertices = df1 %>% select(name = GitHub, Category, Followers, score))
g <- simplify(g)

set.seed(42)
p4 <- ggraph(g, layout = "fr") +
  geom_edge_link(alpha = 0.08, color = "#ccc") +
  geom_node_point(aes(color = Category, size = Followers), alpha = 0.85) +
  geom_node_text(
    aes(label = ifelse(Followers > 3000, name, "")),
    size = 2, repel = TRUE, max.overlaps = 20
  ) +
  scale_color_manual(values = cat_colors) +
  scale_size_continuous(range = c(1.5, 10), labels = label_comma(), guide = "none") +
  labs(
    title = "Awesomers Network",
    subtitle = "Force-directed layout | Edges = shared category + GitHub follows",
    caption = "Node size = followers. Only labels for >3k followers shown."
  ) +
  theme_void(base_size = 8) +
  theme(
    plot.title = element_text(face = "bold", size = 11, hjust = 0),
    plot.subtitle = element_text(size = 7, color = "#777", hjust = 0),
    plot.caption = element_text(size = 5.5, color = "#999", face = "italic", hjust = 0),
    legend.position = "bottom",
    legend.text = element_text(size = 6),
    legend.key.size = unit(0.3, "cm")
  )

save_fig(p4, "Fig04_network", w = 7.5, h = 6)

# =============================================================================
# FIG 5 — Activity & efficiency (tidyplots)
# =============================================================================
cat("Generating Fig 5...\n")
p5 <- df1 %>%
  mutate(Name = reorder(Name, fpr)) %>%
  tidyplot(x = fpr, y = Name) %>%
  add_barstack_absolute(width = 0.6) %>%
  adjust_colors(new_colors = pal_accent2) %>%
  adjust_title("Followers per Repo (efficiency)") %>%
  adjust_x_axis(title = "Followers / Repos") %>%
  adjust_y_axis(title = "") %>%
  adjust_caption("Higher = more followers per repository published")

save_fig(p5, "Fig05_efficiency_tidy", w = 5, h = 7)

# =============================================================================
# FIG 6 — Bioinformatics focus (ggplot2)
# =============================================================================
cat("Generating Fig 6...\n")
bio <- df1 %>% filter(Category == "Bioinfo.")

p6 <- bio %>%
  mutate(Name = reorder(Name, Followers)) %>%
  ggplot(aes(x = Followers, y = Name)) +
  geom_segment(aes(xend = 0, yend = Name), color = "#e8e8e8", linewidth = 0.5) +
  geom_point(color = "#197EC0", size = 3) +
  geom_text(aes(label = GitHub), hjust = -0.15, size = 2.3, color = "#555", fontface = "italic") +
  scale_x_continuous(labels = label_comma()) +
  labs(
    title = "Bioinformatics Awesomers",
    subtitle = "GitHub followers | Bioinfo. category only",
    x = "Followers", y = NULL,
    caption = "Heng Li, Tommy Tang, Phil Ewels, Wei Shen lead the bioinformatics cohort."
  ) +
  theme_pub()

save_fig(p6, "Fig06_bioinformatics", w = 5.5, h = 4.5)

# =============================================================================
# FIG 7 — Heatmap: Category x Language (ggplot2 tile)
# =============================================================================
cat("Generating Fig 7...\n")
hl <- df1 %>%
  filter(PrimaryLang != "--") %>%
  count(Category, PrimaryLang) %>%
  complete(Category, PrimaryLang, fill = list(n = 0))

p7 <- hl %>%
  ggplot(aes(x = PrimaryLang, y = Category, fill = n)) +
  geom_tile(color = "white", linewidth = 0.5) +
  geom_text(aes(label = ifelse(n > 0, n, "")), size = 3, fontface = "bold") +
  scale_fill_gradient(low = "#f0f0f0", high = pal_accent, name = "n") +
  labs(
    title = "Category x Language Heatmap",
    subtitle = "Number of awesomers per category-language pair",
    x = NULL, y = NULL,
    caption = "Only awesomers with a known primary language shown."
  ) +
  theme_pub() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    panel.grid = element_blank()
  )

save_fig(p7, "Fig07_heatmap", w = 5, h = 4)

# =============================================================================
# FIG 8 — Phase 2: Top awesome-* repos (tidyplots)
# =============================================================================
cat("Generating Fig 8...\n")
p8 <- repos_df %>%
  filter(!is_bio) %>%
  slice_max(Stars, n = 20) %>%
  mutate(ShortName = reorder(ShortName, Stars)) %>%
  tidyplot(x = Stars, y = ShortName, color = Domain) %>%
  add_barstack_absolute(width = 0.6) %>%
  adjust_colors(new_colors = pal_simpsons) %>%
  adjust_title("Top 20 awesome-* repositories") %>%
  adjust_x_axis(title = "GitHub Stars") %>%
  adjust_y_axis(title = "") %>%
  adjust_caption("Source: GitHub API, 2026-03-17 | Bioinformatics repos excluded (see Fig 10)")

save_fig(p8, "Fig08_P2_repos_tidy", w = 6, h = 6)

# =============================================================================
# FIG 9 — Phase 2: Curator ranking (ggplot2 + ggrepel)
# =============================================================================
cat("Generating Fig 9...\n")
p9 <- curators_df %>%
  mutate(Name = reorder(Name, curator_score)) %>%
  ggplot(aes(x = curator_score, y = Name)) +
  geom_segment(aes(xend = 0, yend = Name), color = "#e0e0e0", linewidth = 0.5) +
  geom_point(aes(color = Domain), size = 2.5, alpha = 0.9) +
  geom_text(aes(label = sprintf("%.1f", curator_score)), hjust = -0.3, size = 2, color = "#888") +
  scale_color_manual(values = cat_colors) +
  labs(
    title = "Awesome Curator Score",
    subtitle = "0.50 log(top_repo_stars) + 0.30 log(followers) + 0.20 log(repos)",
    x = "Curator Score", y = NULL,
    caption = "Curator score weights project impact (stars) over personal following."
  ) +
  theme_pub() +
  theme(axis.text.y = element_text(size = 5.5))

save_fig(p9, "Fig09_P2_curators", w = 6.5, h = 7)

# =============================================================================
# FIG 10 — Power law + bioinformatics zoom (ggplot2)
# =============================================================================
cat("Generating Fig 10...\n")
p10a <- repos_df %>%
  ggplot(aes(x = Rank, y = Stars, color = is_bio)) +
  geom_point(aes(size = ifelse(is_bio, 3, 1.5)), alpha = 0.8) +
  geom_text_repel(
    data = repos_df %>% filter(Rank <= 3 | is_bio),
    aes(label = ShortName), size = 2.2, seed = 42, max.overlaps = 15,
    segment.color = "#ccc", segment.size = 0.2
  ) +
  scale_y_log10(labels = label_comma()) +
  scale_color_manual(values = c("FALSE" = pal_accent, "TRUE" = "#197EC0"),
                     labels = c("General", "Bioinformatics")) +
  scale_size_identity() +
  labs(
    title = "Stars follow a power law",
    subtitle = "Rank-size plot of awesome-* repos | Log y-axis",
    x = "Rank", y = "Stars (log scale)", color = NULL,
    caption = "Bioinformatics repos highlighted. Top 3 repos hold >1M stars combined."
  ) +
  theme_pub()

bio_repos <- repos_df %>% filter(is_bio) %>% mutate(ShortName = reorder(ShortName, Stars))
p10b <- bio_repos %>%
  ggplot(aes(x = Stars, y = ShortName)) +
  geom_col(fill = "#197EC0", width = 0.5) +
  geom_text(aes(label = scales::comma(Stars)), hjust = -0.1, size = 2.5, color = "#555") +
  geom_vline(xintercept = 1000, linetype = "dashed", color = pal_accent, linewidth = 0.4) +
  annotate("text", x = 1200, y = 1.2, label = "quality\nthreshold", size = 2, color = pal_accent) +
  labs(
    title = "Bioinformatics awesome-* repos",
    subtitle = "Only 2 repos exceed 1k stars threshold",
    x = "Stars", y = NULL,
    caption = "danielecook/Awesome-Bioinformatics is the dominant list."
  ) +
  theme_pub()

p10 <- p10a + p10b + plot_layout(widths = c(1.5, 1)) +
  plot_annotation(tag_levels = "a", theme = theme(plot.tag = element_text(face = "bold", size = 10)))

save_fig(p10, "Fig10_P2_powerlaw", w = 9, h = 4.5)

# =============================================================================
# FIG 11 — Cross-reference scatter: personal followers vs repo stars (ggplot2 + ggrepel)
# =============================================================================
cat("Generating Fig 11...\n")
p11 <- curators_df %>%
  ggplot(aes(x = log_f, y = log_top, color = Domain)) +
  geom_point(aes(shape = in_phase1), size = 3, alpha = 0.85) +
  geom_text_repel(aes(label = GitHub), size = 2, max.overlaps = 20,
                  segment.color = "#ccc", segment.size = 0.2, seed = 42) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "#ddd", linewidth = 0.5) +
  scale_color_manual(values = cat_colors) +
  scale_shape_manual(values = c("FALSE" = 16, "TRUE" = 17),
                     labels = c("Phase 2 only", "Also in Phase 1")) +
  annotate("text", x = 2.8, y = 5.5, label = "Repo outgrew creator",
           size = 2.2, color = "#bbb", fontface = "italic") +
  labs(
    title = "Personal vs. Project Influence",
    subtitle = "Curators: personal followers vs. their top awesome repo stars",
    x = expression(log[10](Followers)), y = expression(log[10](Top~repo~stars)),
    color = "Domain", shape = "Phase",
    caption = "Triangle = also identified in Phase 1. Above diagonal = project-driven influence."
  ) +
  theme_pub()

save_fig(p11, "Fig11_P2_crossref", w = 7, h = 5.5)

# =============================================================================
# FIG 12 — Statistical: Category comparison (ggstatsplot if available)
# =============================================================================
if (has_ggstatsplot) {
  cat("Generating Fig 12 (ggstatsplot)...\n")
  p12 <- ggbetweenstats(
    data = df1 %>% filter(Category %in% c("AI/ML", "Bioinfo.", "Data Sci.")),
    x = Category, y = log_f,
    type = "nonparametric",
    pairwise.comparisons = TRUE,
    pairwise.display = "all",
    p.adjust.method = "holm",
    title = "Followers by Category (Kruskal-Wallis)",
    subtitle = "Pairwise Dunn tests with Holm correction",
    xlab = "", ylab = expression(log[10](Followers)),
    caption = "Non-parametric comparison. AI/ML awesomers have significantly higher followings.",
    ggtheme = theme_pub()
  ) + scale_color_manual(values = c("AI/ML" = "#FD7446", "Bioinfo." = "#197EC0", "Data Sci." = "#46732E"))
  save_fig(p12, "Fig12_stats_category", w = 6, h = 5)
} else {
  cat("[SKIP] Fig 12: ggstatsplot not available\n")
}

# =============================================================================
# FIG 13 — Language distribution (tidyplots)
# =============================================================================
cat("Generating Fig 13...\n")
lang_counts <- df1 %>%
  filter(PrimaryLang != "--") %>%
  count(PrimaryLang, sort = TRUE) %>%
  mutate(PrimaryLang = reorder(PrimaryLang, n))

p13 <- lang_counts %>%
  tidyplot(x = n, y = PrimaryLang) %>%
  add_barstack_absolute(width = 0.55) %>%
  adjust_colors(new_colors = pal_accent2) %>%
  adjust_title("Primary language distribution") %>%
  adjust_x_axis(title = "Number of awesomers") %>%
  adjust_y_axis(title = "") %>%
  adjust_caption("Python dominates. R and C reflect bioinfo/data science niches.")

save_fig(p13, "Fig13_languages_tidy", w = 4, h = 3.5)

# =============================================================================
# FIG 14 — Domain breakdown for Phase 2 repos (tidyplots)
# =============================================================================
cat("Generating Fig 14...\n")
dom_counts <- repos_df %>%
  count(Domain, sort = TRUE) %>%
  mutate(Domain = reorder(Domain, n))

p14 <- dom_counts %>%
  tidyplot(x = n, y = Domain) %>%
  add_barstack_absolute(width = 0.55) %>%
  adjust_colors(new_colors = pal_simpsons[5]) %>%
  adjust_title("Awesome repo domains") %>%
  adjust_x_axis(title = "Number of repos") %>%
  adjust_y_axis(title = "") %>%
  adjust_caption("AI/LLM has overtaken traditional dev categories in awesome repo creation.")

save_fig(p14, "Fig14_P2_domains_tidy", w = 4.5, h = 4)

# =============================================================================
# DONE
# =============================================================================
cat("\n=== ALL FIGURES GENERATED ===\n")
cat("Output:", outdir, "\n")
cat("Total figures: 14 (PNG + PDF each)\n")
