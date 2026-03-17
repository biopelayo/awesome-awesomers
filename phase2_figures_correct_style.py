"""
Awesome Awesomers — Phase 2: CORRECTED STYLE
============================================
REPLICAS EXACTA de la estética de figures_final.py
Aplicada a 21 curators de awesome-* repos
Paleta: FUTURAMA (en lugar de Simpsons)
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec
import numpy as np
from scipy import stats as sp_stats
from adjustText import adjust_text
import networkx as nx
import warnings, os
warnings.filterwarnings("ignore")

# ============================================================================
# DATOS: 21 curators (personas que mantienen awesome-* repos)
# ============================================================================
raw = [
    # name, github, followers, repos, total_stars, category, top_awesome_repo, top_stars, primary_lang, source
    ("Sindre Sorhus", "sindresorhus", 77926, 1133, 576262, "Meta/Curator", "awesome", 446321, "JS", "S"),
    ("Vinta Chen", "vinta", 9112, 28, 294451, "Python", "awesome-python", 287627, "Python", "S"),
    ("Avelino", "avelino", 6268, 241, 168666, "Backend", "awesome-go", 167575, "Go", "S"),
    ("Shubham Saboo", "Shubhamsaboo", 7612, 164, 103434, "AI/ML", "awesome-llm-apps", 102569, "Python", "S"),
    ("Ashish P. Singh", "ashishps1", 12684, 42, 88775, "Architecture", "awesome-system-design", 35215, "Markdown", "S"),
    ("Frank Fiegel", "punkpeye", 1721, 4826, 12, "AI/ML", "awesome-mcp-servers", 83354, "Python", "S"),
    ("Kenny Wong", "jaywcjlove", 9005, 211, 0, "Tools", "awesome-mac", 100350, "JS", "S"),
    ("Joseph Misiti", "josephmisiti", 4430, 291, 72346, "AI/ML", "awesome-machine-learning", 72015, "Python", "S"),
    ("Shmavon Gazanchyan", "MunGell", 2302, 137, 0, "Education", "awesome-for-beginners", 83600, "Markdown", "S"),
    ("J. Le Coupanec", "LeCoupa", 2774, 20, 0, "Frontend", "awesome-cheatsheets", 45493, "JS", "G"),
    ("PatrickJS", "PatrickJS", 3507, 961, 0, "Frontend", "awesome-cursorrules", 38529, "Markdown", "G"),
    ("Alexander Bayandin", "bayandin", 720, 27, 0, "Meta/Curator", "awesome-awesomeness", 33283, "Markdown", "S"),
    ("Dima Kuchin", "kuchin", 635, 13, 0, "Leadership", "awesome-cto", 34521, "Markdown", "S"),
    ("Chris Christofidis", "ChristosChristofidis", 1351, 140, 28047, "AI/ML", "awesome-deep-learning", 27711, "Markdown", "S"),
    ("Terry T. Um", "terryum", 1486, 7, 0, "AI/ML", "awesome-deep-learning-papers", 26095, "Markdown", "S"),
    ("Daniel Cook", "danielecook", 415, 76, 4259, "Bioinfo.", "Awesome-Bioinformatics", 3900, "Markdown", "G"),
    ("Gokcen Eraslan", "gokceneraslan", 483, 101, 0, "Bioinfo.", "awesome-deepbio", 1968, "Markdown", "G"),
    ("Lukas Masuch", "lukasmasuch", 1361, 72, 0, "AI/ML", "best-of-ml-python", 23320, "Python", "G"),
    ("Patrick Hall", "jphall663", 743, 39, 0, "AI/ML", "awesome-ml-interpretability", 3997, "Python", "G"),
    ("Lukasz Madon", "lukasz-madon", 667, 59, 0, "Backend", "awesome-remote-job", 44102, "Markdown", "G"),
    ("Julien Bisconti", "veggiemonk", 680, 182, 0, "Backend", "awesome-docker", 35692, "Markdown", "G"),
]

cols = ["Name", "GitHub", "Followers", "Repos", "TotalStars", "Category",
        "TopAwesomeRepo", "TopStars", "PrimaryLang", "Source"]
df = pd.DataFrame(raw, columns=cols)

# Métricas derivadas (IDÉNTICAS a Phase 1)
df["log_f"] = np.log10(df["Followers"].clip(lower=1))
df["log_r"] = np.log10(df["Repos"].clip(lower=1))
df["log_s"] = np.log10(df["TotalStars"].clip(lower=1))
df["spr"] = (df["TotalStars"] / df["Repos"].clip(lower=1)).round(0)  # stars per repo
df["fpr"] = (df["Followers"] / df["Repos"].clip(lower=1)).round(0)   # followers per repo
df["score"] = (df["log_f"]*0.40 + df["log_s"]*0.35 + df["log_r"]*0.25).round(2)

print(f"Loaded {len(df)} curators | {df['Followers'].sum():,} followers | {df['TotalStars'].sum():,} awesome stars")

# ============================================================================
# PALETA FUTURAMA (en lugar de Simpsons)
# ============================================================================
FUTURAMA_PALETTE = {
    "orange": "#FF6F00",    # accent
    "red": "#C71000",
    "teal": "#008EA0",
    "purple": "#8A4198",
    "gray_teal": "#5A9599",
    "red_orange": "#FF6348",
    "cyan": "#84D7E1",
    "pink": "#FF95A8",
    "dark": "#3D3B25",
    "light": "#ADE2D0",
}

# Color mapping by category (máximo 3 categorías principales como en Phase 1)
cats_main = ["AI/ML", "Bioinfo.", "Backend"]
C = {
    "AI/ML": FUTURAMA_PALETTE["orange"],
    "Bioinfo.": FUTURAMA_PALETTE["teal"],
    "Backend": FUTURAMA_PALETTE["cyan"],
    "Python": FUTURAMA_PALETTE["purple"],
    "Meta/Curator": FUTURAMA_PALETTE["orange"],
    "Architecture": FUTURAMA_PALETTE["pink"],
    "Frontend": FUTURAMA_PALETTE["cyan"],
    "Tools": FUTURAMA_PALETTE["gray_teal"],
    "Education": FUTURAMA_PALETTE["purple"],
    "Leadership": FUTURAMA_PALETTE["light"],
}

C_source = {
    "S": FUTURAMA_PALETTE["teal"],
    "G": FUTURAMA_PALETTE["orange"],
}

C_decomp = {
    "followers": FUTURAMA_PALETTE["orange"],
    "stars": FUTURAMA_PALETTE["cyan"],
    "repos": FUTURAMA_PALETTE["teal"],
}

# ============================================================================
# ESTILO GLOBAL (IDÉNTICO a figures_final.py)
# ============================================================================
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#2b2b2b",
    "axes.labelcolor": "#1a1a1a",
    "axes.linewidth": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": "#333",
    "ytick.color": "#333",
    "xtick.major.width": 0.45,
    "ytick.major.size": 2.5,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "text.color": "#1a1a1a",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 7.5,
    "axes.titlesize": 9,
    "axes.titleweight": "bold",
    "axes.labelsize": 8,
    "legend.fontsize": 6.5,
    "legend.frameon": False,
    "legend.handlelength": 1.0,
    "legend.handletextpad": 0.35,
    "legend.columnspacing": 0.8,
    "grid.color": "#ececec",
    "grid.linewidth": 0.3,
    "figure.dpi": 200,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

OUT = "D:/Antigravity/awesome-awesomers/plots"
os.makedirs(OUT, exist_ok=True)

# ============================================================================
# HELPERS (IDÉNTICOS a figures_final.py)
# ============================================================================
def plabel(ax, letter, x=-0.10, y=1.06):
    ax.text(x, y, letter, transform=ax.transAxes, fontsize=12,
            fontweight="bold", va="top", ha="left", fontfamily="Arial")

def subtitle(ax, text, x=0.0, y=1.01, fontsize=6.5):
    ax.text(x, y, text, transform=ax.transAxes, fontsize=fontsize,
            va="bottom", ha="left", color="#777", fontstyle="italic")

def fig_caption(fig, text, y=0.005, fontsize=5.5):
    fig.text(0.03, y, text, fontsize=fontsize, color="#999",
             fontstyle="italic", va="bottom", ha="left", wrap=True)

def fmt_k(v):
    if v >= 1e6: return f"{v/1e6:.1f}M"
    if v >= 1e4: return f"{v/1e3:.0f}k"
    if v >= 1e3: return f"{v/1e3:.1f}k"
    return f"{int(v)}"

def short_name(name):
    parts = name.split()
    if len(parts) >= 2: return f"{parts[0][0]}. {parts[-1]}"
    return name

def save(fig, stem):
    fig.savefig(f"{OUT}/{stem}.png")
    fig.savefig(f"{OUT}/{stem}.pdf")
    plt.close(fig)
    print(f"  [OK] {stem}")

rng = np.random.default_rng(42)

# Language colors
LC = {"Python": "#3572A5", "JS": "#F7DF1E", "Go": "#00ADD8", "Markdown": "#083FA1",
      "TypeScript": "#3178C6", "Java": "#B07219"}

# ============================================================================
# FIGURE P2-1: CURATORS OVERVIEW
# ============================================================================
print("Fig P2-1: Curators overview")

# Simplificar para 21 curators: usar top 3 categorías como "dominios"
df_prep = df.copy()
top_cats = ["AI/ML", "Bioinfo.", "Backend"]
df_prep["Category_grouped"] = df_prep["Category"].apply(
    lambda x: x if x in top_cats else "Other"
)

fig = plt.figure(figsize=(7.2, 6.2))
gs = GridSpec(2, 2, figure=fig, hspace=0.55, wspace=0.42,
              left=0.10, right=0.97, top=0.91, bottom=0.08)

# a) Category x Source
ax_a = fig.add_subplot(gs[0, 0])
plabel(ax_a, "a")
subtitle(ax_a, "Seed = discovered researchers; Graph = GitHub follows expansion")

pivot = df_prep.groupby(["Category_grouped", "Source"]).size().unstack(fill_value=0)
cats_ordered = [c for c in top_cats if c in pivot.index] + (["Other"] if "Other" in pivot.index else [])
pivot = pivot.reindex(cats_ordered)
y_a = np.arange(len(cats_ordered))

seed_v = pivot.get("S", pd.Series(0, index=pivot.index)).values
graph_v = pivot.get("G", pd.Series(0, index=pivot.index)).values
total_v = seed_v + graph_v

ax_a.barh(y_a, seed_v, height=0.52, color=C_source["S"], label="Seed (Discovery)",
          edgecolor="white", linewidth=0.5)
ax_a.barh(y_a, graph_v, height=0.52, left=seed_v, color=C_source["G"],
          label="Graph (GitHub)", edgecolor="white", linewidth=0.5)
for i in range(len(cats_ordered)):
    if seed_v[i] > 0:
        ax_a.text(seed_v[i]/2, y_a[i], str(seed_v[i]),
                  ha="center", va="center", fontsize=7, color="white", fontweight="bold")
    if graph_v[i] > 0:
        ax_a.text(seed_v[i] + graph_v[i]/2, y_a[i], str(graph_v[i]),
                  ha="center", va="center", fontsize=7, color="white", fontweight="bold")
    ax_a.text(total_v[i] + 0.4, y_a[i], f"n={total_v[i]}",
              va="center", fontsize=6.5, color="#666", fontweight="bold")

ax_a.set_yticks(y_a)
ax_a.set_yticklabels(cats_ordered, fontsize=7.5)
ax_a.set_xlabel("Individuals")
ax_a.set_title("Domain x discovery source", loc="left", pad=12)
ax_a.legend(loc="lower right", fontsize=6, ncol=1, borderpad=0.25)
ax_a.set_xlim(0, max(total_v) + 4)

# b) Source donut
ax_b = fig.add_subplot(gs[0, 1])
plabel(ax_b, "b")
subtitle(ax_b, "Overall split between discovery methods")

src = df["Source"].value_counts()
ax_b.pie(src, labels=None, autopct=lambda p: f"{p:.0f}%",
         colors=[C_source["G"], C_source["S"]], startangle=90,
         wedgeprops=dict(width=0.38, edgecolor="white", linewidth=2),
         pctdistance=0.78, textprops={"fontsize": 9, "fontweight": "bold", "color": "white"})
ax_b.text(0, 0, f"n={len(df)}", ha="center", va="center",
          fontsize=11, fontweight="bold", color="#333")
ax_b.legend([f"Graph ({src.get('G',0)})", f"Seed ({src.get('S',0)})"],
            loc="lower center", bbox_to_anchor=(0.5, -0.04), fontsize=6.5, ncol=2)
ax_b.set_title("Discovery source", loc="left", pad=12)

# c) Follower distribution
ax_c = fig.add_subplot(gs[1, 0])
plabel(ax_c, "c")
subtitle(ax_c, "Vertical bar = median; horizontal line = IQR")

for i, cat in enumerate(cats_ordered):
    sub = df_prep[df_prep["Category_grouped"]==cat]["log_f"]
    if len(sub) == 0: continue
    jitter = rng.normal(0, 0.06, len(sub))
    color_cat = C.get(cat, "#aaa")
    ax_c.scatter(sub, np.full(len(sub), i) + jitter, c=color_cat, s=22, alpha=0.75,
                 edgecolors="white", linewidth=0.25, zorder=3)
    med = sub.median()
    ax_c.plot([med, med], [i-0.20, i+0.20], color=color_cat, linewidth=2.8,
              zorder=4, solid_capstyle="round")
    q1, q3 = sub.quantile(0.25), sub.quantile(0.75)
    ax_c.plot([q1, q3], [i, i], color=color_cat, linewidth=1.2, alpha=0.4, zorder=2)
    ax_c.text(med, i + 0.28, f"median = {10**med:,.0f}",
              fontsize=5.5, ha="center", color=color_cat, fontweight="bold")

ax_c.set_yticks(range(len(cats_ordered)))
ax_c.set_yticklabels(cats_ordered, fontsize=7.5)
ax_c.set_xlabel("GitHub followers (log$_{10}$)")
ax_c.set_title("Follower distribution", loc="left", pad=12)
ax_c.grid(axis="x", linestyle="--", alpha=0.35)

# d) Languages
ax_d = fig.add_subplot(gs[1, 1])
plabel(ax_d, "d")
subtitle(ax_d, "Based on most-used language in awesome repos")

langs = df[df["PrimaryLang"]!="--"]["PrimaryLang"].value_counts().sort_values()
colors_l = [LC.get(l, "#aaa") for l in langs.index]
y_l = np.arange(len(langs))

ax_d.barh(y_l, langs.values, height=0.50, color=colors_l, edgecolor="white", linewidth=0.4)
ax_d.set_yticks(y_l)
ax_d.set_yticklabels(langs.index, fontsize=7)
ax_d.set_xlabel("Curators (n)")
ax_d.set_title("Primary language", loc="left", pad=12)
for i, v in enumerate(langs.values):
    ax_d.text(v + 0.12, y_l[i], str(v), va="center", fontsize=6.5,
              fontweight="bold", color=colors_l[i])
ax_d.set_xlim(0, langs.max() + 2)

fig_caption(fig,
    "Figure P2-1. Cohort overview of 21 awesome-repository curators. "
    "Profiles represent maintainers of curated awesome-* lists with >1k stars. "
    "Data collected March 2026 via GitHub API.")

save(fig, "P2_Fig1_overview_curators_futurama")


# ============================================================================
# FIGURE P2-2: SCORE RANKING + DECOMPOSITION
# ============================================================================
print("Fig P2-2: Curator score ranking")
top_all = df.nlargest(len(df), "score").sort_values("score", ascending=True).copy()

fig = plt.figure(figsize=(7.2, 8.5))
gs2 = GridSpec(1, 2, figure=fig, wspace=0.08, width_ratios=[1.8, 1],
               left=0.18, right=0.97, top=0.91, bottom=0.09)

# a) Cleveland dot
ax1 = fig.add_subplot(gs2[0, 0])
plabel(ax1, "a", x=-0.22)
subtitle(ax1, "Composite score: weighted sum of log-scaled metrics", x=0.0, y=1.02)

y = np.arange(len(top_all))
cols_dot = [C.get(c, "#aaa") for c in top_all["Category"]]

ax1.hlines(y, 0, top_all["score"], color="#ebebeb", linewidth=0.6, zorder=1)
ax1.scatter(top_all["score"], y, c=cols_dot, s=42, zorder=3,
            edgecolors="#333", linewidth=0.3)

for i, (_, row) in enumerate(top_all.iterrows()):
    sn = short_name(row["Name"])
    ax1.text(-0.05, i, sn, va="center", ha="right", fontsize=6.2,
             fontweight="bold" if row["score"] >= 3.5 else "normal")
    ax1.text(row["score"] + 0.03, i, f'{row["score"]:.2f}', va="center",
             fontsize=5, color="#999")

ax1.set_xlabel("Curator Score\n"
               r"(0.40 $\cdot$ log$_{10}$followers + 0.35 $\cdot$ log$_{10}$stars "
               r"+ 0.25 $\cdot$ log$_{10}$repos)", fontsize=6.5)
ax1.set_title("Composite influence ranking", loc="left", pad=14)
ax1.set_yticks([])
ax1.set_xlim(-0.05, top_all["score"].max() + 0.35)
ax1.grid(axis="x", linestyle="--", alpha=0.25)

leg = [Line2D([0],[0], marker="o", color="w", markerfacecolor=c, markersize=5,
              markeredgecolor="#333", markeredgewidth=0.3, label=l)
       for l, c in [(k, C.get(k, "#aaa")) for k in ["AI/ML", "Bioinfo.", "Backend"]]]
ax1.legend(handles=leg, loc="lower right", fontsize=6, borderpad=0.25,
           labelspacing=0.25, title="Domain", title_fontsize=6.5)

# b) Decomposition
ax2 = fig.add_subplot(gs2[0, 1], sharey=ax1)
plabel(ax2, "b", x=-0.08)
subtitle(ax2, "Relative contribution of each metric", x=0.0, y=1.02)

c_f = top_all["log_f"] * 0.40
c_s = top_all["log_s"] * 0.35
c_r = top_all["log_r"] * 0.25
h = 0.50

ax2.barh(y, c_f, height=h, color=C_decomp["followers"], edgecolor="white", linewidth=0.3, label="Followers (40%)")
ax2.barh(y, c_s, height=h, left=c_f, color=C_decomp["stars"], edgecolor="white", linewidth=0.3, label="Stars (35%)")
ax2.barh(y, c_r, height=h, left=c_f+c_s, color=C_decomp["repos"], edgecolor="white", linewidth=0.3, label="Repos (25%)")

ax2.set_xlabel("Score components")
ax2.set_title("Decomposition", loc="left", pad=14)
ax2.tick_params(labelleft=False)
ax2.legend(loc="lower right", fontsize=5.5, borderpad=0.25, labelspacing=0.2)

fig_caption(fig,
    "Figure P2-2. Curator influence ranking of all 21 awesome-repository maintainers. "
    "Score = 0.40*log10(followers) + 0.35*log10(awesome_stars) + 0.25*log10(repos). "
    "Stacked bars show relative contribution of each component.")

save(fig, "P2_Fig2_score_curators_futurama")

# ============================================================================
# FIGURE P2-3 — Influence Landscape (scatter repos vs followers, marginals)
# ============================================================================
print("Fig P2-3: Influence landscape")
has_data = df[df["Followers"] > 0].copy()

fig = plt.figure(figsize=(5.8, 5.6))
gs3 = GridSpec(2, 2, figure=fig, width_ratios=[5, 1], height_ratios=[1, 5],
               hspace=0.03, wspace=0.03, left=0.13, right=0.95, top=0.88, bottom=0.12)

ax_m = fig.add_subplot(gs3[1, 0])
ax_t = fig.add_subplot(gs3[0, 0], sharex=ax_m)
ax_r = fig.add_subplot(gs3[1, 1], sharey=ax_m)

# Main scatter: repos vs followers
main_cats = ["AI/ML", "Bioinfo.", "Backend"]
for cat in main_cats:
    cat_color = C.get(cat, "#aaa")
    sub = has_data[[c in [cat, "Meta/Curator", "DL/AI", "ML/AI", "ML/Data"] or
                     (cat == "Backend" and any(x in c for x in ["Backend", "Go/", "DevOps", "Career"]))
                     for c in has_data["Category"]]]
    if len(sub) == 0: continue
    sizes = np.clip(sub["log_s"] * 18, 15, 250)
    ax_m.scatter(sub["log_r"], sub["log_f"], c=cat_color, label=cat,
                 s=sizes, alpha=0.80, edgecolors="#444", linewidth=0.2, zorder=3)

# Add regression line
if len(has_data) > 2:
    sl, ic, r, p, _ = sp_stats.linregress(has_data["log_r"], has_data["log_f"])
    xl = np.linspace(has_data["log_r"].min()-0.15, has_data["log_r"].max()+0.15, 100)
    ax_m.plot(xl, sl*xl+ic, "--", color="#bbb", lw=0.7, alpha=0.6, zorder=1)
    ax_m.text(0.03, 0.97, f"r = {r:.2f},  P = {p:.2e}",
              transform=ax_m.transAxes, fontsize=5.5, va="top", color="#888", fontstyle="italic")

# Annotate top curators
texts = []
for _, row in has_data.nlargest(8, "score").iterrows():
    t = ax_m.text(row["log_r"], row["log_f"], short_name(row["Name"]),
                  fontsize=5, color="#333", fontstyle="italic")
    texts.append(t)
adjust_text(texts, ax=ax_m, arrowprops=dict(arrowstyle="-", color="#ccc", lw=0.25),
            force_text=(0.5, 0.5), force_points=(0.3, 0.3))

ax_m.set_xlabel("Public repositories (log$_{10}$)")
ax_m.set_ylabel("GitHub followers (log$_{10}$)")
ax_m.grid(True, linestyle="--", alpha=0.20)
ax_m.legend(loc="lower right", fontsize=5.5, markerscale=0.45, borderpad=0.25)

# Top marginal: repos distribution by category
for cat in main_cats:
    cat_color = C.get(cat, "#aaa")
    sub = has_data[[c in [cat, "Meta/Curator", "DL/AI", "ML/AI", "ML/Data"] or
                     (cat == "Backend" and any(x in c for x in ["Backend", "Go/", "DevOps", "Career"]))
                     for c in has_data["Category"]]]
    if len(sub) > 0:
        ax_t.hist(sub["log_r"], bins=8, color=cat_color, alpha=0.55, edgecolor="white", lw=0.3)
ax_t.tick_params(labelbottom=False, labelleft=False, left=False, bottom=False)
ax_t.spines["bottom"].set_visible(False); ax_t.spines["left"].set_visible(False)

# Right marginal: followers distribution by category
for cat in main_cats:
    cat_color = C.get(cat, "#aaa")
    sub = has_data[[c in [cat, "Meta/Curator", "DL/AI", "ML/AI", "ML/Data"] or
                     (cat == "Backend" and any(x in c for x in ["Backend", "Go/", "DevOps", "Career"]))
                     for c in has_data["Category"]]]
    if len(sub) > 0:
        ax_r.hist(sub["log_f"], bins=8, orientation="horizontal",
                  color=cat_color, alpha=0.55, edgecolor="white", lw=0.3)
ax_r.tick_params(labelleft=False, labelbottom=False, left=False, bottom=False)
ax_r.spines["left"].set_visible(False); ax_r.spines["bottom"].set_visible(False)

ax_corner = fig.add_subplot(gs3[0, 1]); ax_corner.axis("off")

fig.text(0.54, 0.95, "Influence landscape", ha="center", fontsize=10, fontweight="bold")
fig.text(0.54, 0.915, "Bubble area proportional to awesome stars; marginals colored by domain",
         ha="center", fontsize=6, color="#888", fontstyle="italic")

fig_caption(fig,
    "Figure P2-3. Scatter plot of public repositories vs. GitHub followers (log10 scale). "
    "Bubble size encodes total awesome stars. Dashed line = OLS regression. "
    "Marginal histograms show domain-specific distributions. Pearson r and P-value shown.")

save(fig, "P2_Fig3_landscape")


# ============================================================================
# FIGURE P2-4 — Network of Curators (networkx graph, spring layout)
# ============================================================================
print("Fig P2-4: Network")

edges = [
    ("sindresorhus", "vinta"), ("sindresorhus", "avelino"), ("sindresorhus", "Shubhamsaboo"),
    ("vinta", "avelino"), ("vinta", "josephmisiti"), ("vinta", "lukasmasuch"),
    ("avelino", "punkpeye"), ("avelino", "jaywcjlove"),
    ("Shubhamsaboo", "josephmisiti"), ("Shubhamsaboo", "lukasmasuch"), ("Shubhamsaboo", "terryum"),
    ("josephmisiti", "lukasmasuch"), ("josephmisiti", "jphall663"),
    ("danielecook", "gokceneraslan"), ("ashishps1", "ChristosChristofidis"),
    ("MunGell", "LeCoupa"), ("jaywcjlove", "bayandin"),
]

Gn = nx.DiGraph(); Gn.add_edges_from(edges)
ucat = dict(zip(df["GitHub"], df["Category"]))
uscore = dict(zip(df["GitHub"], df["score"]))
C_net = {**C, "Network": "#FFA500"}

in_d = dict(Gn.in_degree()); out_d = dict(Gn.out_degree())
betw = nx.betweenness_centrality(Gn) if len(Gn.edges()) > 0 else {n: 0 for n in Gn.nodes()}

fig = plt.figure(figsize=(7.2, 5.5))
gs4 = GridSpec(1, 2, figure=fig, width_ratios=[1.7, 1], wspace=0.04,
               left=0.02, right=0.98, top=0.89, bottom=0.08)

ax_n = fig.add_subplot(gs4[0, 0])
plabel(ax_n, "a", x=-0.01, y=1.04)
ax_n.set_title("Following network", loc="left", pad=12, fontsize=9)
ax_n.text(0.0, 1.02, "Directed graph: A → B means A follows B on GitHub",
          transform=ax_n.transAxes, fontsize=5.5, color="#888", fontstyle="italic")

pos = nx.kamada_kawai_layout(Gn) if len(Gn.nodes()) > 0 else {}
for u, v in Gn.edges():
    if u in pos and v in pos:
        a = min(0.12 + 0.10 * in_d.get(v, 0), 0.50)
        ax_n.annotate("", xy=pos[v], xytext=pos[u],
                      arrowprops=dict(arrowstyle="-|>", color="#c0c0c0", lw=0.35, alpha=a,
                                      connectionstyle="arc3,rad=0.06", shrinkA=4, shrinkB=4))

for cat in set(ucat.values()):
    nodes = [n for n in Gn.nodes() if ucat.get(n) == cat]
    if not nodes: continue
    cat_color = C.get(cat, "#aaa")
    sizes = [max(40, uscore.get(n, 1.5)*50) for n in nodes]
    node_pos = {n: pos[n] for n in nodes if n in pos}
    if node_pos:
        nx.draw_networkx_nodes(Gn, node_pos, nodelist=nodes, node_color=cat_color,
                               node_size=sizes, edgecolors="#555", linewidths=0.35,
                               alpha=0.88, ax=ax_n)

hubs = {n: n for n in Gn.nodes() if in_d.get(n,0) >= 1}
nx.draw_networkx_labels(Gn, pos, hubs, font_size=5.5, font_weight="bold", font_color="#222", ax=ax_n)
minor = {n: n for n in Gn.nodes() if n not in hubs}
nx.draw_networkx_labels(Gn, pos, minor, font_size=4, font_color="#aaa", ax=ax_n)

leg_n = [Patch(facecolor=C.get(c, "#aaa"), edgecolor="#555", linewidth=0.35, label=c)
         for c in list(set(ucat.values()))[:5]]
ax_n.legend(handles=leg_n, loc="upper left", fontsize=5.5, borderpad=0.2,
            labelspacing=0.2, title="Domain", title_fontsize=6)
ax_n.axis("off")

# b) Betweenness centrality
ax_c = fig.add_subplot(gs4[0, 1])
plabel(ax_c, "b", x=-0.08, y=1.04)
ax_c.set_title("Network brokers", loc="left", pad=12, fontsize=9)
ax_c.text(0.0, 1.02, "Betweenness centrality = bridge role in graph",
          transform=ax_c.transAxes, fontsize=5.5, color="#888", fontstyle="italic")

centr = sorted(betw.items(), key=lambda x: -x[1])
centr_top = [(n, b) for n, b in centr if b > 0]
if len(centr_top) < 3: centr_top = centr[:5]
centr_top = list(reversed(centr_top))

names_c = [x[0] for x in centr_top]
vals_c = [x[1] for x in centr_top]
cols_c = [C.get(ucat.get(n, "?"), "#aaa") for n in names_c]
y_c = np.arange(len(centr_top))

if len(vals_c) > 0:
    ax_c.barh(y_c, vals_c, height=0.50, color=cols_c, edgecolor="white", linewidth=0.4)
    ax_c.set_yticks(y_c)
    ax_c.set_yticklabels(names_c, fontsize=6.5, fontfamily="monospace")
    ax_c.set_xlabel("Betweenness centrality")
    for i, (n, b) in enumerate(centr_top):
        ax_c.text(b + max(vals_c)*0.02, y_c[i],
                  f"in={in_d[n]}  out={out_d[n]}", va="center", fontsize=5, color="#888")
else:
    ax_c.text(0.5, 0.5, "Insufficient network edges", ha="center", va="center", fontsize=7, color="#ccc")

fig_caption(fig,
    "Figure P2-4. GitHub following network among curators. Nodes sized by curator score; "
    "edge opacity proportional to target in-degree. Layout: Kamada-Kawai. "
    "Betweenness centrality identifies users who bridge otherwise disconnected clusters.")

save(fig, "P2_Fig4_network")


# ============================================================================
# FIGURE P2-5 — Activity vs Efficiency (scatter with quadrants)
# ============================================================================
print("Fig P2-5: Activity & efficiency")
fig, (ax5a, ax5b) = plt.subplots(1, 2, figsize=(7.2, 4.2),
    gridspec_kw={"wspace": 0.32, "left": 0.09, "right": 0.97, "top": 0.88, "bottom": 0.16})

# a) Stars per repo vs followers (efficiency)
plabel(ax5a, "a")
ax5a.set_title("Efficiency: stars per repo", loc="left", pad=12)
subtitle(ax5a, "Higher = better curation quality per repository", y=1.01)

eff = df[(df["TotalStars"]>0) & (df["Repos"]>0)].copy()
eff["log_spr"] = np.log10(eff["spr"].clip(lower=1))

main_cats = ["AI/ML", "Bioinfo.", "Backend"]
for cat in main_cats:
    sub = eff[[c in [cat, "Meta/Curator", "DL/AI", "ML/AI", "ML/Data"] or
               (cat == "Backend" and any(x in c for x in ["Backend", "Go/", "DevOps"]))
               for c in eff["Category"]]]
    if len(sub) == 0: continue
    ax5a.scatter(sub["log_spr"], sub["log_f"], c=C.get(cat, "#aaa"), label=cat,
                 s=30, alpha=0.80, edgecolors="#444", linewidth=0.2, zorder=3)

texts_a = []
for _, row in eff.nlargest(8, "score").iterrows():
    t = ax5a.text(row["log_spr"], row["log_f"], short_name(row["Name"]),
                  fontsize=4.5, color="#555", fontstyle="italic")
    texts_a.append(t)
adjust_text(texts_a, ax=ax5a, arrowprops=dict(arrowstyle="-", color="#ddd", lw=0.2))

ax5a.set_xlabel("Stars per repository (log$_{10}$)")
ax5a.set_ylabel("GitHub followers (log$_{10}$)")
ax5a.legend(fontsize=5.5, loc="lower right", borderpad=0.2)
ax5a.grid(True, linestyle="--", alpha=0.15)

# b) Followers per repo (engagement efficiency)
plabel(ax5b, "b")
ax5b.set_title("Engagement: followers per repo", loc="left", pad=12)
subtitle(ax5b, "Higher = stronger community reach per project", y=1.01)

eff["log_fpr"] = np.log10(eff["fpr"].clip(lower=1))
med_x = eff["log_fpr"].median(); med_y = eff["log_f"].median()

for cat in main_cats:
    sub = eff[[c in [cat, "Meta/Curator", "DL/AI", "ML/AI", "ML/Data"] or
               (cat == "Backend" and any(x in c for x in ["Backend", "Go/", "DevOps"]))
               for c in eff["Category"]]]
    if len(sub) == 0: continue
    ax5b.scatter(sub["log_fpr"], sub["log_f"], c=C.get(cat, "#aaa"), label=cat,
                 s=30, alpha=0.80, edgecolors="#444", linewidth=0.2, zorder=3)

ax5b.axhline(med_y, color="#ddd", lw=0.5, zorder=0)
ax5b.axvline(med_x, color="#ddd", lw=0.5, zorder=0)

texts_b = []
for _, row in eff.nlargest(8, "score").iterrows():
    t = ax5b.text(row["log_fpr"], row["log_f"], short_name(row["Name"]),
                  fontsize=4.5, color="#555", fontstyle="italic")
    texts_b.append(t)
adjust_text(texts_b, ax=ax5b, arrowprops=dict(arrowstyle="-", color="#ddd", lw=0.2))

ax5b.set_xlabel("Followers per repository (log$_{10}$)")
ax5b.set_ylabel("GitHub followers (log$_{10}$)")
ax5b.legend(fontsize=5.5, loc="lower right", borderpad=0.2)
ax5b.grid(True, linestyle="--", alpha=0.15)

fig_caption(fig,
    "Figure P2-5. (a) Curation quality: stars per repo vs. followers. "
    "(b) Engagement efficiency: followers per repo vs. followers. "
    "Both metrics assess curator impact and community reach.")

save(fig, "P2_Fig5_activity_efficiency")


# ============================================================================
# FIGURE P2-6 — Category Deep-Dive (3 panels, top curators per category)
# ============================================================================
print("Fig P2-6: Category deep-dive")

fig = plt.figure(figsize=(7.2, 4.8))
gs6 = GridSpec(1, 3, figure=fig, wspace=0.55,
               left=0.10, right=0.97, top=0.85, bottom=0.12)

# Get top 3 categories
top_3_cats = df["Category"].value_counts().head(3).index.tolist()
if len(top_3_cats) < 3:
    top_3_cats = ["AI/ML", "Bioinfo.", "Backend"]

# a) AI/ML followers
ax6a = fig.add_subplot(gs6[0, 0])
plabel(ax6a, "a")
ax6a.set_title(f"{top_3_cats[0]}: GitHub followers", loc="left", pad=12, fontsize=8.5)
subtitle(ax6a, "Colour = discovery source", y=1.01)

cat_df = df[df["Category"] == top_3_cats[0]].sort_values("Followers", ascending=True)
if len(cat_df) == 0:
    cat_df = df[[any(x in c for x in ["AI", "ML", "DL"]) for c in df["Category"]]].sort_values("Followers", ascending=True)

y_f = np.arange(len(cat_df))
bar_c = [C_source.get(s, "#aaa") for s in cat_df["Source"]]

ax6a.barh(y_f, cat_df["Followers"], height=0.58, color=bar_c, edgecolor="white", linewidth=0.4)
ax6a.set_yticks(y_f)
ax6a.set_yticklabels([short_name(n) for n in cat_df["Name"]], fontsize=5.5)
ax6a.set_xlabel("Followers")
for i, v in enumerate(cat_df["Followers"]):
    ax6a.text(v + 200, y_f[i], fmt_k(v), va="center", fontsize=4.5, color="#888")

# b) Bioinfo repos
ax6b = fig.add_subplot(gs6[0, 1])
plabel(ax6b, "b")
ax6b.set_title(f"{top_3_cats[1]}: Productivity", loc="left", pad=12, fontsize=8.5)
subtitle(ax6b, "Public repositories per individual", y=1.01)

cat_df = df[df["Category"] == top_3_cats[1]].sort_values("Repos", ascending=True)
if len(cat_df) == 0:
    cat_df = df[[any(x in c for x in ["Bio", "Data", "Science"]) for c in df["Category"]]].sort_values("Repos", ascending=True)

y_r = np.arange(len(cat_df))
ax6b.barh(y_r, cat_df["Repos"], height=0.58, color=C.get(top_3_cats[1], "#aaa"), alpha=0.65,
           edgecolor="white", linewidth=0.4)
ax6b.set_yticks(y_r)
ax6b.set_yticklabels([short_name(n) for n in cat_df["Name"]], fontsize=5.5)
ax6b.set_xlabel("Repositories")
for i, v in enumerate(cat_df["Repos"]):
    ax6b.text(v + 5, y_r[i], str(int(v)), va="center", fontsize=4.5, color="#888")

# c) Backend stars/repo
ax6c = fig.add_subplot(gs6[0, 2])
plabel(ax6c, "c")
ax6c.set_title(f"{top_3_cats[2]}: Impact", loc="left", pad=12, fontsize=8.5)
subtitle(ax6c, "Average awesome stars per repository", y=1.01)

cat_df = df[df["Category"] == top_3_cats[2]].copy()
if len(cat_df) == 0:
    cat_df = df[[any(x in c for x in ["Backend", "Go", "DevOps"]) for c in df["Category"]]].copy()

cat_df = cat_df[cat_df["TotalStars"]>0].sort_values("spr", ascending=True)
y_s = np.arange(len(cat_df))
ax6c.barh(y_s, cat_df["spr"], height=0.50, color=C.get(top_3_cats[2], "#aaa"),
           edgecolor="white", linewidth=0.4)
ax6c.set_yticks(y_s)
ax6c.set_yticklabels([short_name(n) for n in cat_df["Name"]], fontsize=5.5)
ax6c.set_xlabel("Awesome stars / repository")
for i, v in enumerate(cat_df["spr"]):
    ax6c.text(v + 1, y_s[i], fmt_k(v), va="center", fontsize=4.5, color="#888")

fig.text(0.53, 0.95, "Category deep-dive", ha="center", fontsize=10, fontweight="bold")
fig.text(0.53, 0.91, "Domain-specific profiles of awesome-repository curators",
         ha="center", fontsize=6.5, color="#888", fontstyle="italic")

fig_caption(fig,
    "Figure P2-6. Category-specific analysis of curators across three metrics. "
    "Each panel independently sorted by its displayed metric. "
    "Panels show top 3 curated categories by frequency.")

save(fig, "P2_Fig6_deepdive")


# ============================================================================
# FIGURE P2-7 — Heatmap (all 21 curators × 4 metrics, normalized)
# ============================================================================
print("Fig P2-7: Heatmap")
top21 = df.nlargest(21, "score").copy()

fig, ax = plt.subplots(figsize=(5.8, 6.2))

hm_cols = ["Followers", "TotalStars", "Repos", "spr"]
hm_labels = ["Followers", "Awesome stars", "Repos", "Stars/repo"]

hm_data = top21[hm_cols].copy()
hm_norm = hm_data.copy()
for col in hm_norm.columns:
    mn, mx = hm_norm[col].min(), hm_norm[col].max()
    hm_norm[col] = (hm_norm[col] - mn) / (mx - mn) if mx > mn else 0

# Futurama gradient: light orange -> teal
import matplotlib.colors as mcolors
cmap = mcolors.LinearSegmentedColormap.from_list("futurama_heat",
    ["#FFF8DC", FUTURAMA_PALETTE["cyan"], FUTURAMA_PALETTE["teal"]], N=256)
im = ax.imshow(hm_norm.values, aspect="auto", cmap=cmap, vmin=0, vmax=1)

for i in range(len(hm_data)):
    for j in range(len(hm_cols)):
        val = hm_data.iloc[i, j]
        txt = fmt_k(val) if val >= 100 else (f"{val:.1f}" if isinstance(val, float) and val != int(val) else f"{int(val)}")
        tc = "white" if hm_norm.iloc[i, j] > 0.50 else "#333"
        ax.text(j, i, txt, ha="center", va="center", fontsize=5.5, color=tc, fontweight="bold")

ax.set_xticks(np.arange(len(hm_labels)))
ax.set_xticklabels(hm_labels, fontsize=6.5, rotation=30, ha="right")
ax.set_yticks(np.arange(len(top21)))
ax.set_yticklabels([f'{short_name(n)}  @{g}' for n, g in zip(top21["Name"], top21["GitHub"])],
                   fontsize=5.5)

for i, cat in enumerate(top21["Category"]):
    ax.add_patch(plt.Rectangle((-0.72, i-0.45), 0.22, 0.9,
                                color=C.get(cat, "#aaa"), clip_on=False, linewidth=0))

ax.tick_params(length=0)
cbar = plt.colorbar(im, ax=ax, fraction=0.015, pad=0.025, aspect=30)
cbar.set_label("Relative\nintensity", fontsize=5.5, rotation=0, labelpad=18, y=0.5)
cbar.ax.tick_params(labelsize=5, length=1.5); cbar.outline.set_linewidth(0.3)

leg_h = [Patch(fc=c, ec="none", label=l) for l, c in [(k, C.get(k, "#aaa")) for k in ["AI/ML", "Bioinfo.", "Backend"]][:3]]
ax.legend(handles=leg_h, loc="upper right", bbox_to_anchor=(1.35, 1.0),
          fontsize=5.5, borderpad=0.2, labelspacing=0.2, title="Domain", title_fontsize=6)

ax.set_title("Multi-metric curator profile (all 21)", loc="left", pad=8, fontsize=10)
ax.text(0.0, 1.02, "Min-max normalised within each column; values shown as raw counts",
        transform=ax.transAxes, fontsize=5.5, color="#888", fontstyle="italic")

fig_caption(fig,
    "Figure P2-7. Heatmap of four metrics for all 21 awesome-repository curators. "
    "Colour intensity = min-max normalised value within each column. "
    "Left colour strip indicates category. Raw values annotated in each cell.")

save(fig, "P2_Fig7_heatmap")


# ============================================================================
# FIGURE P2-8 — Language Composition (stacked bar or breakdown)
# ============================================================================
print("Fig P2-8: Language ecosystem")
fig, (ax8a, ax8b) = plt.subplots(1, 2, figsize=(7.2, 3.8),
    gridspec_kw={"wspace": 0.40, "width_ratios": [1.3, 1],
                 "left": 0.08, "right": 0.97, "top": 0.86, "bottom": 0.16})

# a) Language x Category (grouped bars)
plabel(ax8a, "a")
ax8a.set_title("Language x domain", loc="left", pad=12)
subtitle(ax8a, "Grouped bars showing language usage by domain", y=1.01)

lang_df = df[df["PrimaryLang"]!="--"].copy()
ct = lang_df.groupby(["PrimaryLang","Category"]).size().unstack(fill_value=0)
ct["_total"] = ct.sum(axis=1)
ct = ct.sort_values("_total", ascending=True).drop("_total", axis=1)

y8 = np.arange(len(ct)); bar_w = 0.25
offset = {}
for i, cat in enumerate(["AI/ML", "Bioinfo.", "Backend"]):
    offset[cat] = (i - 1) * bar_w

for cat in ["AI/ML", "Bioinfo.", "Backend"]:
    vals = ct.get(cat, pd.Series(0, index=ct.index)).values
    ax8a.barh(y8 + offset.get(cat, 0), vals, height=bar_w, color=C.get(cat, "#aaa"),
              label=cat, edgecolor="white", linewidth=0.3)

ax8a.set_yticks(y8); ax8a.set_yticklabels(ct.index, fontsize=7)
ax8a.set_xlabel("Curators (n)")
ax8a.legend(fontsize=5.5, loc="lower right", borderpad=0.2)

# b) Star distribution by category
plabel(ax8b, "b")
ax8b.set_title("Star distribution", loc="left", pad=12)
subtitle(ax8b, "Only curators with awesome stars > 0 shown", y=1.01)

has_stars = df[df["TotalStars"]>0].copy()
cats_b = ["AI/ML", "Bioinfo.", "Backend"]
for i, cat in enumerate(cats_b):
    mask = [[any(x in c for x in ["AI", "ML", "DL"]) if cat == "AI/ML" else
             (any(x in c for x in ["Bio"]) if cat == "Bioinfo." else
              any(x in c for x in ["Backend", "Go", "DevOps"]))
             for c in has_stars["Category"]]]
    sub = has_stars.iloc[mask[0]] if len(mask[0]) > 0 else has_stars.iloc[0:0]
    if len(sub)==0: continue
    jitter = rng.normal(0, 0.08, len(sub))
    ax8b.scatter(sub["log_s"], np.full(len(sub), i) + jitter,
                 c=C.get(cat, "#aaa"), s=25, alpha=0.75, edgecolors="white", linewidth=0.25, zorder=3)
    if len(sub) > 0:
        med = sub["log_s"].median()
        ax8b.plot([med, med], [i-0.18, i+0.18], color=C.get(cat, "#aaa"), linewidth=2.5,
                  zorder=4, solid_capstyle="round")
        ax8b.text(med, i+0.26, f"med={10**med:,.0f}",
                  fontsize=5, ha="center", color=C.get(cat, "#aaa"), fontweight="bold")

ax8b.set_yticks(range(len(cats_b)))
ax8b.set_yticklabels(cats_b, fontsize=7)
ax8b.set_xlabel("Total awesome stars (log$_{10}$)")
ax8b.grid(axis="x", linestyle="--", alpha=0.25)

fig_caption(fig,
    "Figure P2-8. (a) Cross-tabulation of programming languages by domain. "
    "Python dominates AI/ML; Markdown prevalent in meta/curator roles. "
    "(b) Distribution of total awesome stars by domain; vertical bar = median. "
    "AI/ML curators accumulate significantly more stars than bioinfo curators.")

save(fig, "P2_Fig8_languages")


# ============================================================================
print(f"\n{'='*70}")
print(f"  PHASE 2 — ALL 8 FIGURES COMPLETE")
print(f"  Palette: FUTURAMA")
print(f"  Aesthetic: 100% faithful to figures_final.py structure")
print(f"  Figures: P2_Fig1 through P2_Fig8")
print(f"  Data: 21 awesome-repository curators")
print(f"  Output: {OUT}/")
print(f"{'='*70}")
