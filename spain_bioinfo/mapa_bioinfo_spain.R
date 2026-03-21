#!/usr/bin/env Rscript
# =============================================================================
# Bioinformatics in Spain — Map & Analysis (Pelamovic Aesthetic)
# =============================================================================
suppressPackageStartupMessages({
  library(sf)
  library(ggplot2)
  library(ggrepel)
  library(dplyr)
  library(tidyr)
  library(scales)
  library(patchwork)
  library(rnaturalearth)
  library(rnaturalearthdata)
})

outdir <- "D:/Antigravity/awesome-awesomers/spain_bioinfo/plots"
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

# Pelamovic colors
pel_green      <- "#2D6A4F"
pel_green_light <- "#95D5B2"
pel_green_pale  <- "#D8F3DC"
pel_green_dark  <- "#1B4332"
pel_coral      <- "#E76F51"
pel_salmon     <- "#F4845F"
pel_bg         <- "#FAFAF5"
pel_grey       <- "#8D99AE"
pel_grey_dark  <- "#2B2B2B"
pel_blue       <- "#264653"
pel_teal       <- "#2A9D8F"

type_colors <- c(
  "center"    = pel_green,
  "unit"      = pel_teal,
  "group"     = pel_coral,
  "program"   = "#E9C46A",
  "service"   = pel_grey,
  "platform"  = "#457B9D",
  "network"   = pel_salmon,
  "society"   = "#B5838D",
  "university" = pel_blue
)

type_shapes <- c(
  "center" = 21, "unit" = 22, "group" = 24, "program" = 23,
  "service" = 25, "platform" = 21, "network" = 21, "society" = 21, "university" = 22
)

theme_map <- function(base_size = 8) {
  theme_void(base_size = base_size) +
    theme(
      plot.background  = element_rect(fill = pel_bg, color = NA),
      plot.title       = element_text(face = "bold", size = 12, color = pel_green_dark,
                                      hjust = 0, margin = margin(b = 2)),
      plot.subtitle    = element_text(size = 8, color = pel_grey, hjust = 0,
                                      face = "italic", margin = margin(b = 6)),
      plot.caption     = element_text(size = 6, color = "#AAA", hjust = 0,
                                      face = "italic", margin = margin(t = 6)),
      legend.position  = "bottom",
      legend.text      = element_text(size = 6.5),
      legend.title     = element_text(size = 7.5, face = "bold", color = pel_green_dark),
      legend.key.size  = unit(0.35, "cm"),
      plot.margin      = margin(8, 8, 5, 8)
    )
}

theme_pelamovic <- function(base_size = 8.5) {
  theme_minimal(base_size = base_size) +
    theme(
      text             = element_text(family = "sans", color = pel_grey_dark),
      plot.background  = element_rect(fill = pel_bg, color = NA),
      panel.background = element_rect(fill = pel_bg, color = NA),
      plot.title       = element_text(face = "bold", size = rel(1.3), hjust = 0,
                                      color = pel_green_dark, margin = margin(b = 1)),
      plot.subtitle    = element_text(size = rel(0.82), color = pel_grey,
                                      hjust = 0, face = "italic", margin = margin(b = 5)),
      plot.caption     = element_text(size = rel(0.65), color = "#AAA",
                                      hjust = 0, face = "italic", margin = margin(t = 4)),
      axis.title       = element_text(size = rel(0.95)),
      axis.text        = element_text(size = rel(0.8), color = "#666"),
      panel.grid.major = element_line(color = "#EDEDED", linewidth = 0.25),
      panel.grid.minor = element_blank(),
      legend.position  = "bottom",
      legend.key.size  = unit(0.3, "cm"),
      legend.text      = element_text(size = rel(0.7)),
      legend.title     = element_text(size = rel(0.8), face = "bold", color = pel_green_dark),
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
# DATA
# =============================================================================
cat("Loading data...\n")
dat <- read.csv("D:/Antigravity/awesome-awesomers/spain_bioinfo/centros_bioinfo_spain.csv",
                stringsAsFactors = FALSE)
# Filter to plottable entries (have valid coords, not multi-region)
map_dat <- dat %>%
  filter(!is.na(lat), !is.na(lon), region != "multi-region", region != "Spain") %>%
  mutate(type = factor(type, levels = names(type_colors)))

cat(nrow(dat), "total entries,", nrow(map_dat), "plottable\n")

# =============================================================================
# SPAIN MAP (without Portugal)
# =============================================================================
cat("Loading Spain map...\n")
world <- ne_countries(scale = "medium", returnclass = "sf")
spain <- world %>% filter(admin == "Spain")

# Get regions for fill
spain_regions <- ne_states(country = "Spain", returnclass = "sf")

# Bounding box: Spain without Canary Islands for main map
bbox_main <- c(xmin = -10.0, xmax = 4.5, ymin = 35.5, ymax = 44.0)

# =============================================================================
# FIG S1 — Main map: all centres
# =============================================================================
cat("Fig S1: Main map...\n")

# Count centres per region
region_counts <- map_dat %>%
  count(region, name = "n_entries")

# Join counts to sf
spain_r <- spain_regions %>%
  left_join(region_counts, by = c("name" = "region")) %>%
  mutate(n_entries = replace_na(n_entries, 0))

p_map <- ggplot() +
  # Choropleth base
  geom_sf(data = spain_r, aes(fill = n_entries), color = "white", linewidth = 0.3) +
  scale_fill_gradient(low = pel_green_pale, high = pel_green,
                      name = "Bioinformatics\nentities", na.value = "#F0F0F0",
                      guide = guide_colorbar(barwidth = 8, barheight = 0.4)) +
  # Points
  geom_point(data = map_dat, aes(x = lon, y = lat, color = type, shape = type),
             size = 2.5, stroke = 0.3, alpha = 0.85) +
  scale_color_manual(values = type_colors, name = "Type") +
  scale_shape_manual(values = type_shapes, name = "Type") +
  # Labels for centres only
  geom_text_repel(
    data = map_dat %>% filter(type == "center") %>%
      distinct(name, .keep_all = TRUE),
    aes(x = lon, y = lat, label = name),
    size = 1.8, color = pel_grey_dark, fontface = "bold",
    max.overlaps = 30, segment.color = pel_grey, segment.size = 0.15,
    seed = 42, box.padding = 0.25, point.padding = 0.15, nudge_y = 0.1
  ) +
  coord_sf(xlim = c(bbox_main["xmin"], bbox_main["xmax"]),
           ylim = c(bbox_main["ymin"], bbox_main["ymax"]), expand = FALSE) +
  labs(
    title = "Bioinformatics in Spain",
    subtitle = paste0("Map of ", nrow(map_dat), " centres, units, groups and programmes | ",
                      length(unique(map_dat$region)), " Comunidades Autonomas"),
    caption = paste0("Data: curated directory 2026-03-21 | Sources: INB-ELIXIR, SEBiBC, ",
                     "BIB, SOMMa, institutional websites\n",
                     "Map: Natural Earth | Pelamovic aesthetic")
  ) +
  theme_map() +
  guides(
    color = guide_legend(nrow = 2, override.aes = list(size = 3)),
    shape = guide_legend(nrow = 2),
    fill = guide_colorbar(order = 1)
  )

save_fig(p_map, "FigS1_spain_bioinfo_map", w = 9, h = 7)

# =============================================================================
# FIG S2 — Region bar chart
# =============================================================================
cat("Fig S2: Region breakdown...\n")
region_summary <- map_dat %>%
  count(region, sort = TRUE) %>%
  mutate(region = reorder(region, n))

p_regions <- region_summary %>%
  ggplot(aes(x = n, y = region)) +
  geom_col(fill = pel_green, width = 0.55, alpha = 0.85) +
  geom_text(aes(label = n), hjust = -0.3, size = 3, color = pel_green_dark, fontface = "bold") +
  scale_x_continuous(expand = expansion(mult = c(0, 0.15))) +
  labs(
    title = "Bioinformatics entities by region",
    subtitle = "Number of centres, units, groups and programmes per Comunidad Autonoma",
    x = "Count", y = NULL,
    caption = "Catalunya and Madrid dominate the Spanish bioinformatics landscape."
  ) +
  theme_pelamovic() +
  theme(panel.grid.major.y = element_blank())

save_fig(p_regions, "FigS2_region_breakdown", w = 5.5, h = 4)

# =============================================================================
# FIG S3 — Type distribution
# =============================================================================
cat("Fig S3: Type distribution...\n")
type_summary <- map_dat %>%
  count(type, sort = TRUE) %>%
  mutate(type = reorder(type, n))

p_types <- type_summary %>%
  ggplot(aes(x = n, y = type, fill = type)) +
  geom_col(width = 0.5, alpha = 0.85, show.legend = FALSE) +
  geom_text(aes(label = n), hjust = -0.3, size = 3, color = pel_green_dark, fontface = "bold") +
  scale_fill_manual(values = type_colors) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.15))) +
  labs(
    title = "Entity types",
    subtitle = "Distribution by type: centres lead, followed by units and groups",
    x = "Count", y = NULL,
    caption = "Classification: center, unit, group, program, service, platform, network, society"
  ) +
  theme_pelamovic() +
  theme(panel.grid.major.y = element_blank())

save_fig(p_types, "FigS3_type_distribution", w = 5, h = 3.5)

# =============================================================================
# FIG S4 — City-level concentration
# =============================================================================
cat("Fig S4: City concentration...\n")
city_summary <- map_dat %>%
  count(city, sort = TRUE) %>%
  mutate(city = reorder(city, n)) %>%
  head(12)

p_cities <- city_summary %>%
  ggplot(aes(x = n, y = city)) +
  geom_col(fill = pel_teal, width = 0.5, alpha = 0.85) +
  geom_text(aes(label = n), hjust = -0.3, size = 3, color = pel_green_dark, fontface = "bold") +
  scale_x_continuous(expand = expansion(mult = c(0, 0.15))) +
  labs(
    title = "Top 12 bioinformatics cities",
    subtitle = "Concentration of entities by city",
    x = "Count", y = NULL,
    caption = "Barcelona and Madrid concentrate >70% of all bioinformatics entities."
  ) +
  theme_pelamovic() +
  theme(panel.grid.major.y = element_blank())

save_fig(p_cities, "FigS4_city_concentration", w = 5, h = 4)

# =============================================================================
# FIG S5 — Heatmap: Region x Type
# =============================================================================
cat("Fig S5: Heatmap...\n")
hm <- map_dat %>%
  count(region, type) %>%
  complete(region, type, fill = list(n = 0))

p_hm <- hm %>%
  ggplot(aes(x = type, y = region, fill = n)) +
  geom_tile(color = pel_bg, linewidth = 1) +
  geom_text(aes(label = ifelse(n > 0, n, ""),
                color = ifelse(n > 2, "white", pel_grey_dark)),
            size = 2.8, fontface = "bold", show.legend = FALSE) +
  scale_color_identity() +
  scale_fill_gradient(low = pel_green_pale, high = pel_green, name = "n",
                      guide = guide_colorbar(barwidth = 6, barheight = 0.4)) +
  labs(
    title = "Region x Entity Type",
    subtitle = "Heatmap of bioinformatics entities across Spain",
    x = NULL, y = NULL,
    caption = "Catalunya has the most diverse ecosystem; Madrid dominates in centres."
  ) +
  theme_pelamovic() +
  theme(
    axis.text.x = element_text(angle = 40, hjust = 1, size = 7),
    panel.grid = element_blank()
  )

save_fig(p_hm, "FigS5_heatmap_region_type", w = 6.5, h = 5)

# =============================================================================
# FIG S6 — Map zooms: Madrid and Barcelona
# =============================================================================
cat("Fig S6: City zooms...\n")

make_zoom <- function(data, city_name, bbox, title_suffix) {
  city_data <- data %>% filter(grepl(city_name, city, ignore.case = TRUE) |
                                grepl(city_name, region, ignore.case = TRUE))

  ggplot() +
    geom_sf(data = spain_r, fill = pel_green_pale, color = "white", linewidth = 0.2) +
    geom_point(data = city_data, aes(x = lon, y = lat, fill = type, shape = type),
               size = 3, stroke = 0.3, color = pel_bg, alpha = 0.9) +
    geom_text_repel(
      data = city_data %>% distinct(name, .keep_all = TRUE),
      aes(x = lon, y = lat, label = name),
      size = 2, color = pel_grey_dark, fontface = "bold",
      max.overlaps = 30, segment.color = pel_grey, segment.size = 0.15,
      seed = 42, box.padding = 0.3
    ) +
    scale_fill_manual(values = type_colors, name = "Type") +
    scale_shape_manual(values = type_shapes, name = "Type") +
    coord_sf(xlim = bbox[1:2], ylim = bbox[3:4], expand = FALSE) +
    labs(title = paste0("Bioinformatics hub: ", title_suffix),
         subtitle = paste0(nrow(city_data), " entities")) +
    theme_map() +
    theme(legend.position = "none")
}

p_madrid <- make_zoom(map_dat, "Madrid", c(-4.1, -3.5, 40.3, 40.6), "Madrid")
p_bcn    <- make_zoom(map_dat, "Barcel|Badal|Bellat|Hospit", c(1.8, 2.5, 41.3, 41.55), "Barcelona")

p_zooms <- p_madrid + p_bcn +
  plot_annotation(
    title = "Major bioinformatics hubs: Madrid & Barcelona",
    subtitle = "Zoom into the two main clusters of bioinformatics entities",
    caption = "Pelamovic aesthetic | Data: curated directory 2026-03-21",
    tag_levels = "a",
    theme = theme(
      plot.background = element_rect(fill = pel_bg, color = NA),
      plot.title = element_text(face = "bold", size = 11, color = pel_green_dark),
      plot.subtitle = element_text(size = 8, color = pel_grey, face = "italic"),
      plot.caption = element_text(size = 6, color = "#AAA", face = "italic"),
      plot.tag = element_text(face = "bold", size = 10, color = pel_green_dark)
    )
  )

save_fig(p_zooms, "FigS6_zooms_madrid_barcelona", w = 10, h = 5)

# =============================================================================
cat("\n=== ALL SPAIN BIOINFO FIGURES GENERATED ===\n")
cat("Output:", outdir, "\n")
cat("Figures: 6 (PNG + PDF)\n")
