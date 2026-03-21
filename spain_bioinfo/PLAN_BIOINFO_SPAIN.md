# Plan de Ataque: Bioinformatics Map of Spain
## Repo independiente: `biopelayo/bioinfo-spain`

---

## 1. ESTADO ACTUAL (v3, 2026-03-21)

| Metrica | Valor |
|---------|-------|
| Entidades | 133 |
| CCAA cubiertas | 17/17 |
| PIs nombrados | 24 |
| Figuras | 7 (Pelamovic aesthetic) |
| Fuentes usadas | MPP Report (236pp), INB-ELIXIR (27 nodes), ISCIII (35 IIS) |

### Archivos base a copiar al nuevo repo
```
spain_bioinfo/centros_bioinfo_spain_v3.csv    # 133 entidades con geocoordenadas
spain_bioinfo/build_v3.py                      # Script de construccion del CSV
spain_bioinfo/mapa_bioinfo_spain_v2.R          # Script R de mapas (sf + ggplot2)
spain_bioinfo/MPP_fulltext.txt                 # Texto completo del PDF (559k chars)
spain_bioinfo/plots/                           # 7 figuras PNG+PDF
```

---

## 2. ARQUITECTURA DEL NUEVO REPO

```
bioinfo-spain/
├── README.md                    # Descripcion, badges, preview del mapa
├── METHODOLOGY.md               # Fuentes, criterios, reproducibilidad
├── data/
│   ├── raw/
│   │   ├── MPP_fulltext.txt     # Texto extraido del PDF Roche
│   │   ├── inb_elixir_nodes.json
│   │   ├── iis_isciii.json
│   │   └── scraped/             # JSONs de scraping por fuente
│   ├── processed/
│   │   ├── entities.csv         # Tabla maestra de entidades
│   │   ├── researchers.csv      # Tabla de investigadores (100+)
│   │   ├── spinoffs.csv         # Empresas y spin-offs
│   │   └── programs.csv         # Masters, doctorados, formacion
│   └── geo/
│       └── spain_ccaa.geojson   # Shapefile simplificado
├── scripts/
│   ├── 01_scrape_inb_elixir.py
│   ├── 02_scrape_sebibc.py
│   ├── 03_scrape_bib.py
│   ├── 04_scrape_somma.py
│   ├── 05_scrape_github_pis.py
│   ├── 06_scrape_openalex.py
│   ├── 07_scrape_orcid.py
│   ├── 08_build_entities.py
│   ├── 09_build_researchers.py
│   └── 10_geocode.py
├── figures/
│   ├── pelamovic/               # Figuras publication-quality
│   ├── companion/               # CSVs + cards por figura
│   └── figures_spain.R          # Script R maestro
├── report/
│   ├── bioinfo_spain_report.tex # LaTeX report
│   └── bioinfo_spain_report.pdf
└── .claude/
    └── CLAUDE.md                # Instrucciones para Claude Code
```

---

## 3. FUENTES DE DATOS SISTEMATICAS

### 3.1 Fuentes ya explotadas (v3)
- [x] MPP Report Fundacion Roche (236 pp, 2019)
- [x] INB-ELIXIR-ES nodes (27 grupos, https://inb-elixir.es/about-inb/inb-nodes)
- [x] ISCIII IIS acreditados (35, https://www.sanidad.gob.es/estadEstudios/sanidadDatos/tablas/tabla29_2.htm)

### 3.2 Fuentes pendientes de scraping

#### Institucionales
- [ ] **SOMMa** (https://somma.es/centres/) — Centros Severo Ochoa y Maria de Maeztu. Scrape todos los centros con "bioinformatics" o "genomics" en descripcion.
- [ ] **BIB Bioinformatics Barcelona** (https://bioinformaticsbarcelona.org/strategic-research/) — Lista completa de grupos, empresas y partners en Catalunya.
- [ ] **SEBiBC** (https://www.sebibc.es) — Miembros, socios protectores, actas de congresos con nombres de PIs.
- [ ] **CSIC directorio** (https://www.csic.es/en/investigation/research-groups) — Filtrar por "bioinformatics", "genomics", "computational biology" en grupos CSIC.
- [ ] **CIBERER, CIBERONC, CIBERINFEC** (redes CIBER ISCIII) — Grupos de bioinformatica dentro de cada CIBER.
- [ ] **Red Andaluza de Bioinformatica (ReBiAn)** — Grupos Khaos, BitLab, etc.
- [ ] **Fundacion Progreso y Salud** (https://www.clinbioinfosspa.es) — Plataforma de Medicina Computacional, OpenCGA, Clinical Bioinformatics.

#### Academicas
- [ ] **OpenAlex** (API) — Buscar autores con affiliation "Spain" + concept "bioinformatics" OR "computational biology". Top 200 por citaciones.
- [ ] **ORCID** (API) — Buscar perfiles con keyword "bioinformatics" + country "ES".
- [ ] **Google Scholar** — Perfiles de los PIs ya identificados para h-index y citaciones.
- [ ] **Semantic Scholar** (API) — Complementar con metricas de publicacion.

#### GitHub/Code
- [ ] **GitHub API** — `gh search users` con location "Spain" + bio containing "bioinformatics" OR "computational biology" OR "genomics". Top 200 por followers.
- [ ] **GitHub repos** — Repos de los centros (BSC, CRG, CNIO, IRB, etc.) para contar herramientas publicadas.

#### LinkedIn
- [ ] **LinkedIn** (via Chrome extension) — Follows de biopelayo + busqueda "bioinformatics Spain".

#### Empresas/Spin-offs
- [ ] **Catalonia Bio & HealthTech** — Directorio de empresas miembro.
- [ ] **Bioval** (Valencia) — Directorio empresas biotech.
- [ ] **ASEBIO** (https://asebio.com) — Asociacion Espanola de Bioempresas, directorio completo.
- [ ] **Scrape spin-offs** mencionados en el PDF: qGenomics, Xenopat, Health in Code, DREAMgenics, Genometra, Biotechvana, AB Biotics, DBGen, CIMA Lab Diagnostics, Owl Metabolomics, Protein Alternatives, Lorgen, Genoma4u, ONCOgenics, Healthsens, CELLBIOCAN.

---

## 4. ESQUEMA DE DATOS

### 4.1 entities.csv (entidades)
```
id, type, name, acronym, parent_institution, city, region, lat, lon,
severo_ochoa, maria_maeztu, iis_acreditado, inb_elixir_node,
main_area, description, url, year_founded
```

### 4.2 researchers.csv (investigadores)
```
id, name, orcid, github, google_scholar_id, twitter,
institution, city, region, position,
h_index, citations, papers_count,
main_area, top_keywords,
github_followers, github_repos, github_stars
```

### 4.3 spinoffs.csv (empresas)
```
id, name, parent_institution, city, region, lat, lon,
founded_year, sector, description, url
```

---

## 5. PIPELINE DE SCRAPING

### Paso 1: Instituciones (scraping web)
```bash
python scripts/01_scrape_inb_elixir.py   # 27 nodes -> JSON
python scripts/02_scrape_sebibc.py       # Miembros SEBiBC -> JSON
python scripts/03_scrape_bib.py          # BIB Catalunya -> JSON
python scripts/04_scrape_somma.py        # SOMMa centres -> JSON
```

### Paso 2: Investigadores (APIs academicas)
```bash
python scripts/05_scrape_github_pis.py   # GitHub: location Spain + bio bioinfo
python scripts/06_scrape_openalex.py     # OpenAlex: top cited Spanish bioinformaticians
python scripts/07_scrape_orcid.py        # ORCID: keyword bioinformatics + country ES
```

### Paso 3: Integracion y geocodificacion
```bash
python scripts/08_build_entities.py      # Merge all JSONs -> entities.csv
python scripts/09_build_researchers.py   # Merge academic APIs -> researchers.csv
python scripts/10_geocode.py             # Geocode missing coords (Nominatim)
```

### Paso 4: Figuras
```bash
Rscript figures/figures_spain.R          # Genera todas las figuras Pelamovic
```

---

## 6. FIGURAS OBJETIVO (12 figuras publication-quality)

| Fig | Titulo | Tipo |
|-----|--------|------|
| 1 | Mapa de Espana: todas las entidades | Choropleth + puntos |
| 2 | Zoom Barcelona hub | Mapa detalle |
| 3 | Zoom Madrid hub | Mapa detalle |
| 4 | CCAA breakdown | Barras horizontales |
| 5 | Tipo de entidad | Barras + colores |
| 6 | Top 20 ciudades | Lollipop chart |
| 7 | Heatmap Region x Tipo | Tile plot |
| 8 | Network: centros-PIs-areas | ggraph |
| 9 | PIs ranking por h-index | Cleveland dot |
| 10 | PIs: followers GitHub vs citaciones | Scatter + ggrepel |
| 11 | Spin-offs por CCAA y sector | Stacked bar |
| 12 | Timeline: fundacion de centros | Gantt-like |

---

## 7. CRITERIOS DE INCLUSION

### Entidad
- Debe tener actividad demostrable en bioinformatica, biologia computacional, genomica computacional, o infraestructura HPC para ciencias de la vida.
- Se incluyen: centros de investigacion, unidades core, grupos de investigacion, plataformas, universidades (con programa de bioinfo), empresas/spin-offs, redes, sociedades.
- Se excluyen: hospitales sin unidad de genetica/genomica propia, biobancos sin componente bioinformatico.

### Investigador (para llegar a 100+)
- Afiliacion actual o reciente en institucion espanola.
- Al menos 1 de: >10 papers en bioinformatica/comp.bio., perfil GitHub con repos de bioinfo, PI de grupo/unidad de bioinfo, docente en master de bioinfo.
- Seed: 24 PIs de INB-ELIXIR + PIs de centros SOMMa + top OpenAlex + top GitHub Spain.

---

## 8. PROMPT DE INICIO DE SESION

Copiar y pegar esto al iniciar una nueva sesion de Claude Code:

```
Estoy trabajando en el proyecto bioinfo-spain, un directorio y mapa
de bioinformatica en Espana. El repo esta en D:/Antigravity/awesome-awesomers/spain_bioinfo/
(pendiente de mover a su propio repo biopelayo/bioinfo-spain).

Estado actual: v3 con 133 entidades, 17 CCAA, 24 PIs.
Plan completo: spain_bioinfo/PLAN_BIOINFO_SPAIN.md

Fuentes principales:
- MPP Report (236pp, texto en spain_bioinfo/MPP_fulltext.txt)
- INB-ELIXIR-ES (27 nodes con PIs)
- ISCIII IIS (35 acreditados)
- SOMMa/Severo Ochoa centres

Estetica: Pelamovic (verde botanico #2D6A4F, coral #E76F51, fondo blanco).
Stack: R (sf + ggplot2 + ggrepel + ggraph + patchwork), Python (scraping).

Objetivo inmediato: [lo que quieras hacer en esa sesion]

Lee la memoria del proyecto: memory/project_bioinfo_spain_map.md
Lee el plan: spain_bioinfo/PLAN_BIOINFO_SPAIN.md
```

---

## 9. PRIORIDADES (orden sugerido)

1. **Crear repo independiente** `biopelayo/bioinfo-spain` y migrar datos
2. **Scrape OpenAlex** para llegar a 100+ investigadores con metricas
3. **Scrape GitHub** para perfiles de bioinformaticos espanoles
4. **Ampliar spin-offs** con ASEBIO + Catalonia Bio + Bioval
5. **Ampliar Andalucia** (FPS/OpenCGA, ReBiAn, mas centros)
6. **Ampliar Galicia** (FPGMX/Xenoma en detalle, Health in Code)
7. **Ampliar Pais Vasco** (Bioaraba, BIOEF, spin-offs)
8. **Generar report LaTeX** con todas las figuras y analisis
9. **Mapa interactivo** (leaflet en R o plotly) para el README del repo

---

## 10. METRICAS OBJETIVO FINAL

| Metrica | v3 actual | Objetivo |
|---------|-----------|----------|
| Entidades | 133 | 250+ |
| CCAA | 17 | 17 (completas) |
| PIs nombrados | 24 | 100+ |
| Spin-offs | 0 | 30+ |
| Programas educativos | 0 | 15+ |
| Figuras | 7 | 12+ |
| Fuentes de datos | 3 | 10+ |

---

*Plan generado 2026-03-21 | Sistema Pelamovic | Claude Opus 4.6*
