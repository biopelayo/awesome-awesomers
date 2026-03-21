#!/usr/bin/env Rscript
# =============================================================================
# Bioinformatics in Spain v2 — White map, hub clustering, Pelamovic aesthetic
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
pel_bg         <- "#FFFFFF"  # WHITE background per user request
pel_grey       <- "#8D99AE"
pel_grey_dark  <- "#2B2B2B"
pel_teal       <- "#2A9D8F"
pel_blue       <- "#264653"

# Type colors
type_colors <- c(
  "center"  = pel_green,
  "unit"    = pel_teal,
  "group"   = pel_coral,
  "network" = pel_salmon,
  "society" = "#B5838D"
)

# Hub colors (by region cluster)
hub_colors <- c(
  "Catalunya"           = "#2A9D8F",
  "Comunidad de Madrid" = "#E76F51",
  "Andalucia"           = "#E9C46A",
  "Comunitat Valenciana" = "#457B9D",
  "Galicia"             = "#264653",
  "Pais Vasco"          = "#6D6875",
  "Aragon"              = "#BC6C25",
  "Asturias"            = "#52796F",
  "Navarra"             = "#D62828",
  "Cantabria"           = "#8D99AE",
  "Castilla y Leon"     = "#B5838D",
  "Illes Balears"       = "#F4845F",
  "Region de Murcia"    = "#A8DADC"
)

theme_map_white <- function(base_size = 8) {
  theme_void(base_size = base_size) +
    theme(
      plot.background  = element_rect(fill = pel_bg, color = NA),
      plot.title       = element_text(face = "bold", size = 12, color = pel_green_dark,
                                      hjust = 0, margin = margin(b = 2)),
      plot.subtitle    = element_text(size = 7.5, color = pel_grey, hjust = 0,
                                      face = "italic", margin = margin(b = 6)),
      plot.caption     = element_text(size = 5.5, color = "#BBB", hjust = 0,
                                      face = "italic", margin = margin(t = 6)),
      legend.position  = "bottom",
      legend.text      = element_text(size = 6),
      legend.title     = element_text(size = 7, face = "bold", color = pel_green_dark),
      legend.key.size  = unit(0.3, "cm"),
      plot.margin      = margin(6, 6, 4, 6)
    )
}

theme_pub <- function(base_size = 8.5) {
  theme_minimal(base_size = base_size) +
    theme(
      text             = element_text(family = "sans", color = pel_grey_dark),
      plot.background  = element_rect(fill = pel_bg, color = NA),
      panel.background = element_rect(fill = pel_bg, color = NA),
      plot.title       = element_text(face = "bold", size = rel(1.3), hjust = 0,
                                      color = pel_green_dark, margin = margin(b = 1)),
      plot.subtitle    = element_text(size = rel(0.82), color = pel_grey,
                                      hjust = 0, face = "italic", margin = margin(b = 5)),
      plot.caption     = element_text(size = rel(0.65), color = "#BBB",
                                      hjust = 0, face = "italic", margin = margin(t = 4)),
      axis.title       = element_text(size = rel(0.95)),
      axis.text        = element_text(size = rel(0.8), color = "#666"),
      panel.grid.major = element_line(color = "#F0F0F0", linewidth = 0.25),
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
dat <- read.csv("D:/Antigravity/awesome-awesomers/spain_bioinfo/centros_bioinfo_spain_v3.csv",
                stringsAsFactors = FALSE)
map_dat <- dat %>%
  filter(!is.na(lat), !is.na(lon), !region %in% c("multi-region", "Spain")) %>%
  mutate(type = factor(type, levels = names(type_colors)))

cat(nrow(dat), "total entries,", nrow(map_dat), "plottable\n")

# Spain map
spain_regions <- ne_states(country = "Spain", returnclass = "sf")

# Region counts for choropleth
region_counts <- map_dat %>% count(region, name = "n_entities")
spain_r <- spain_regions %>%
  left_join(region_counts, by = c("name" = "region")) %>%
  mutate(n_entities = replace_na(n_entities, 0))

bbox_main <- c(xmin = -10.0, xmax = 4.5, ymin = 35.5, ymax = 44.0)

# =============================================================================
# FIG S1 — Main map: WHITE background, hubs by region colour
# =============================================================================
cat("Fig S1v2: Main map (white)...\n")

# Jitter overlapping points slightly
set.seed(42)
map_jitter <- map_dat %>%
  group_by(lat, lon) %>%
  mutate(
    n_overlap = n(),
    jitter_lon = lon + ifelse(n_overlap > 1, runif(n(), -0.12, 0.12), 0),
    jitter_lat = lat + ifelse(n_overlap > 1, runif(n(), -0.08, 0.08), 0)
  ) %>%
  ungroup()

# Labels: only show centres (deduplicated by city)
label_dat <- map_jitter %>%
  filter(type == "center") %>%
  group_by(city) %>%
  summarise(
    lon = mean(jitter_lon), lat = mean(jitter_lat),
    n = n(),
    label = ifelse(n > 3, paste0(first(city), " (", n, ")"), first(name)),
    region = first(region),
    .groups = "drop"
  )

p_map <- ggplot() +
  # White base with thin grey borders
  geom_sf(data = spain_r, fill = "white", color = "#E0E0E0", linewidth = 0.35) +
  # Light fill for regions with entities
  geom_sf(data = spain_r %>% filter(n_entities > 0),
          aes(fill = n_entities), color = "#D0D0D0", linewidth = 0.3, alpha = 0.4) +
  scale_fill_gradient(low = "#F5F5F5", high = pel_green_pale,
                      name = "Entities", na.value = "white",
                      guide = guide_colorbar(barwidth = 6, barheight = 0.35)) +
  # Points coloured by region (hub)
  geom_point(data = map_jitter,
             aes(x = jitter_lon, y = jitter_lat, color = region),
             size = 1.8, alpha = 0.8, stroke = 0.2) +
  scale_color_manual(values = hub_colors, name = "Hub") +
  # City labels
  geom_text_repel(
    data = label_dat,
    aes(x = lon, y = lat, label = label),
    size = 1.7, color = pel_grey_dark, fontface = "bold",
    max.overlaps = 40, segment.color = "#CCC", segment.size = 0.12,
    seed = 42, box.padding = 0.2, point.padding = 0.1
  ) +
  coord_sf(xlim = c(bbox_main["xmin"], bbox_main["xmax"]),
           ylim = c(bbox_main["ymin"], bbox_main["ymax"]), expand = FALSE) +
  labs(
    title = "Bioinformatics in Spain",
    subtitle = paste0(nrow(map_dat), " entities across ", length(unique(map_dat$region)),
                      " Comunidades Autonomas | Colour = regional hub"),
    caption = paste0("Sources: INB-ELIXIR-ES (27 nodes), ISCIII (35 IIS), SOMMa, BIB, SEBiBC, ",
                     "institutional websites | 2026-03-21")
  ) +
  theme_map_white() +
  guides(color = guide_legend(nrow = 2, override.aes = list(size = 2.5, alpha = 1)))

save_fig(p_map, "FigS1v2_spain_bioinfo_map", w = 9, h = 7)

# =============================================================================
# FIG S2v2 — Region breakdown (sorted, coloured by hub)
# =============================================================================
cat("Fig S2v2: Region breakdown...\n")
region_summary <- map_dat %>%
  count(region, sort = TRUE) %>%
  mutate(region = reorder(region, n))

p_regions <- region_summary %>%
  ggplot(aes(x = n, y = region, fill = region)) +
  geom_col(width = 0.55, alpha = 0.85, show.legend = FALSE) +
  geom_text(aes(label = n), hjust = -0.3, size = 3, color = pel_green_dark, fontface = "bold") +
  scale_fill_manual(values = hub_colors) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.15))) +
  labs(
    title = "Bioinformatics entities by CCAA",
    subtitle = paste0("n = ", nrow(map_dat), " | Catalunya and Madrid dominate"),
    x = "Count", y = NULL,
    caption = "Includes centres, units, groups, networks. IIS acreditados ISCIII included."
  ) +
  theme_pub() +
  theme(panel.grid.major.y = element_blank())

save_fig(p_regions, "FigS2v2_region_breakdown", w = 5.5, h = 4.5)

# =============================================================================
# FIG S3v2 — Type distribution (coloured by type)
# =============================================================================
cat("Fig S3v2: Type distribution...\n")
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
    subtitle = "Centres dominate, followed by research groups and core units",
    x = "Count", y = NULL
  ) +
  theme_pub() +
  theme(panel.grid.major.y = element_blank())

save_fig(p_types, "FigS3v2_type_distribution", w = 4.5, h = 3)

# =============================================================================
# FIG S4v2 — City concentration (top 12)
# =============================================================================
cat("Fig S4v2: City concentration...\n")
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
    title = "Top bioinformatics cities",
    subtitle = "Barcelona and Madrid concentrate >70% of entities",
    x = "Count", y = NULL,
    caption = "Badalona, Bellaterra, L'Hospitalet counted separately from Barcelona."
  ) +
  theme_pub() +
  theme(panel.grid.major.y = element_blank())

save_fig(p_cities, "FigS4v2_city_concentration", w = 5, h = 4)

# =============================================================================
# FIG S5v2 — PI network: named researchers
# =============================================================================
cat("Fig S5v2: Named PIs...\n")
pis <- map_dat %>%
  filter(!is.na(pi_lead), pi_lead != "") %>%
  select(pi_lead, name, city, region, type) %>%
  mutate(pi_lead = trimws(pi_lead))

# Some PIs have multiple names separated by ;
pi_long <- pis %>%
  separate_rows(pi_lead, sep = ";\\s*") %>%
  mutate(pi_lead = trimws(pi_lead)) %>%
  filter(pi_lead != "")

p_pis <- pi_long %>%
  mutate(pi_lead = factor(pi_lead, levels = rev(unique(pi_lead)))) %>%
  ggplot(aes(y = pi_lead, x = 1, color = region)) +
  geom_point(size = 3, alpha = 0.85) +
  geom_text(aes(label = paste0(name, " (", city, ")")),
            hjust = -0.05, size = 2, color = "#777") +
  scale_color_manual(values = hub_colors, name = "Hub") +
  scale_x_continuous(limits = c(0.8, 3.5)) +
  labs(
    title = "Named PIs in Spanish bioinformatics",
    subtitle = paste0(nrow(pi_long), " researchers identified across INB-ELIXIR nodes and centres"),
    y = NULL, x = NULL,
    caption = "Sources: INB-ELIXIR-ES node list, institutional websites."
  ) +
  theme_pub() +
  theme(
    axis.text.x = element_blank(),
    axis.ticks.x = element_blank(),
    panel.grid.major.x = element_blank(),
    panel.grid.major.y = element_line(color = "#F0F0F0", linewidth = 0.2)
  )

save_fig(p_pis, "FigS5v2_named_PIs", w = 7.5, h = 7)

# =============================================================================
# FIG S6v2 — Heatmap: Region x Type
# =============================================================================
cat("Fig S6v2: Heatmap...\n")
hm <- map_dat %>%
  count(region, type) %>%
  complete(region, type, fill = list(n = 0))

p_hm <- hm %>%
  ggplot(aes(x = type, y = region, fill = n)) +
  geom_tile(color = "white", linewidth = 1) +
  geom_text(aes(label = ifelse(n > 0, n, ""),
                color = ifelse(n > 3, "white", pel_grey_dark)),
            size = 2.8, fontface = "bold", show.legend = FALSE) +
  scale_color_identity() +
  scale_fill_gradient(low = "#F8F8F8", high = pel_green, name = "n",
                      guide = guide_colorbar(barwidth = 6, barheight = 0.35)) +
  labs(
    title = "Region x Entity Type",
    subtitle = "Catalunya dominates in centres, groups and units; Madrid strong in centres",
    x = NULL, y = NULL
  ) +
  theme_pub() +
  theme(
    axis.text.x = element_text(angle = 40, hjust = 1, size = 7),
    panel.grid = element_blank()
  )

save_fig(p_hm, "FigS6v2_heatmap_region_type", w = 5.5, h = 5)

# =============================================================================
# FIG S7 — Zooms: Barcelona + Madrid
# =============================================================================
cat("Fig S7: City zooms...\n")

make_zoom <- function(data, pattern, bbox, title) {
  city_data <- data %>% filter(grepl(pattern, city, ignore.case = TRUE))

  ggplot() +
    geom_sf(data = spain_r, fill = "white", color = "#E8E8E8", linewidth = 0.2) +
    geom_point(data = city_data,
               aes(x = jitter_lon, y = jitter_lat, color = type),
               size = 2.5, stroke = 0.3, alpha = 0.85) +
    geom_text_repel(
      data = city_data %>% distinct(name, .keep_all = TRUE) %>% filter(type %in% c("center", "group")),
      aes(x = jitter_lon, y = jitter_lat, label = name),
      size = 1.6, color = pel_grey_dark, fontface = "bold",
      max.overlaps = 35, segment.color = "#CCC", segment.size = 0.1,
      seed = 42, box.padding = 0.2
    ) +
    scale_color_manual(values = type_colors, name = "Type") +
    coord_sf(xlim = bbox[1:2], ylim = bbox[3:4], expand = FALSE) +
    labs(title = title, subtitle = paste0(nrow(city_data), " entities")) +
    theme_map_white() +
    theme(legend.position = "none")
}

p_bcn <- make_zoom(map_jitter, "Barcel|Badal|Bellat|Hospit|Sabadell",
                   c(1.7, 2.55, 41.3, 41.6), "Barcelona hub")
p_mad <- make_zoom(map_jitter, "Madrid",
                   c(-4.0, -3.5, 40.3, 40.6), "Madrid hub")

p_zooms <- p_bcn + p_mad +
  plot_annotation(
    title = "Major bioinformatics hubs",
    subtitle = "Zoom: Barcelona (left) and Madrid (right)",
    caption = "White background | Pelamovic aesthetic | Data: v2 directory 2026-03-21",
    tag_levels = "a",
    theme = theme(
      plot.background = element_rect(fill = pel_bg, color = NA),
      plot.title = element_text(face = "bold", size = 11, color = pel_green_dark),
      plot.subtitle = element_text(size = 7.5, color = pel_grey, face = "italic"),
      plot.caption = element_text(size = 5.5, color = "#BBB", face = "italic"),
      plot.tag = element_text(face = "bold", size = 10, color = pel_green_dark)
    )
  )

save_fig(p_zooms, "FigS7_zooms_hubs", w = 10, h = 5)

# =============================================================================
cat("\n=== ALL v2 FIGURES GENERATED ===\n")
cat("Output:", outdir, "\n")
