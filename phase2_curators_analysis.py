"""
Awesome Awesomers — Phase 2 CORRECTED
=====================================
Focus: Curators (people behind awesome-* repos), not repos themselves
Data model: SAME as Phase 1 (people-centric, not repo-centric)
Paleta: FUTURAMA
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
# DATA: Curators of awesome-* repositories (21 people, >1k star repos)
# ============================================================================
raw = [
    # name, github, followers, repos, total_stars, category, top_awesome_repo, top_stars, primary_lang, source
    ("Sindre Sorhus", "sindresorhus", 77926, 1133, 576262, "Meta/Curator", "awesome", 446321, "JS", "S"),
    ("Vinta Chen", "vinta", 9112, 28, 294451, "Python/Data", "awesome-python", 287627, "Python", "S"),
    ("Avelino", "avelino", 6268, 241, 168666, "Go/Backend", "awesome-go", 167575, "Go", "S"),
    ("Shubham Saboo", "Shubhamsaboo", 7612, 164, 103434, "AI/LLM", "awesome-llm-apps", 102569, "Python", "S"),
    ("Ashish P. Singh", "ashishps1", 12684, 42, 88775, "Architecture", "awesome-system-design", 35215, "Markdown", "S"),
    ("Frank Fiegel", "punkpeye", 1721, 4826, 12, "AI/LLM", "awesome-mcp-servers", 83354, "Python", "S"),
    ("Kenny Wong", "jaywcjlove", 9005, 211, 0, "Tools/Mac", "awesome-mac", 100350, "JS", "S"),
    ("Joseph Misiti", "josephmisiti", 4430, 291, 72346, "ML/AI", "awesome-machine-learning", 72015, "Python", "S"),
    ("Shmavon Gazanchyan", "MunGell", 2302, 137, 0, "Education", "awesome-for-beginners", 83600, "Markdown", "S"),
    ("J. Le Coupanec", "LeCoupa", 2774, 20, 0, "Frontend", "awesome-cheatsheets", 45493, "JS", "G"),
    ("PatrickJS", "PatrickJS", 3507, 961, 0, "Frontend", "awesome-cursorrules", 38529, "Markdown", "G"),
    ("Alexander Bayandin", "bayandin", 720, 27, 0, "Meta/Curator", "awesome-awesomeness", 33283, "Markdown", "S"),
    ("Dima Kuchin", "kuchin", 635, 13, 0, "Leadership", "awesome-cto", 34521, "Markdown", "S"),
    ("Chris Christofidis", "ChristosChristofidis", 1351, 140, 28047, "DL/AI", "awesome-deep-learning", 27711, "Markdown", "S"),
    ("Terry T. Um", "terryum", 1486, 7, 0, "DL/AI", "awesome-deep-learning-papers", 26095, "Markdown", "S"),
    ("Daniel Cook", "danielecook", 415, 76, 4259, "Bioinformatics", "Awesome-Bioinformatics", 3900, "Markdown", "G"),
    ("Gokcen Eraslan", "gokceneraslan", 483, 101, 0, "Bioinformatics", "awesome-deepbio", 1968, "Markdown", "G"),
    ("Lukas Masuch", "lukasmasuch", 1361, 72, 0, "ML/Data", "best-of-ml-python", 23320, "Python", "G"),
    ("Patrick Hall", "jphall663", 743, 39, 0, "ML/Interpretability", "awesome-ml-interpretability", 3997, "Python", "G"),
    ("Lukasz Madon", "lukasz-madon", 667, 59, 0, "Career/Remote", "awesome-remote-job", 44102, "Markdown", "G"),
    ("Julien Bisconti", "veggiemonk", 680, 182, 0, "DevOps", "awesome-docker", 35692, "Markdown", "G"),
]

cols = ["Name", "GitHub", "Followers", "Repos", "TotalStars", "Category",
        "TopAwesomeRepo", "TopStars", "PrimaryLang", "Source"]
df = pd.DataFrame(raw, columns=cols)

# Derived metrics (SAME as Phase 1)
df["log_f"] = np.log10(df["Followers"].clip(lower=1))
df["log_r"] = np.log10(df["Repos"].clip(lower=1))
df["log_s"] = np.log10(df["TotalStars"].clip(lower=1))
df["spr"] = (df["TotalStars"] / df["Repos"].clip(lower=1)).round(0)  # stars per repo
df["fpr"] = (df["Followers"] / df["Repos"].clip(lower=1)).round(0)   # followers per repo
df["score"] = (df["log_f"]*0.40 + df["log_s"]*0.35 + df["log_r"]*0.25).round(2)

print(f"Loaded {len(df)} curators | {df['Followers'].sum():,} followers | {df['TotalStars'].sum():,} awesome stars")

# ============================================================================
# PALETA FUTURAMA
# ============================================================================
FUTURAMA = {
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

# Category colors
C = {
    "AI/LLM": FUTURAMA["orange"],
    "Meta/Curator": FUTURAMA["orange"],
    "Bioinformatics": FUTURAMA["teal"],
    "DL/AI": FUTURAMA["red"],
    "ML/AI": FUTURAMA["red"],
    "ML/Data": FUTURAMA["red"],
    "Python/Data": FUTURAMA["purple"],
    "Data": FUTURAMA["purple"],
    "Backend": FUTURAMA["teal"],
    "Go/Backend": FUTURAMA["teal"],
    "Frontend": FUTURAMA["cyan"],
    "DevOps": FUTURAMA["gray_teal"],
    "Architecture": FUTURAMA["pink"],
    "Leadership": FUTURAMA["light"],
    "Tools/Mac": FUTURAMA["red_orange"],
    "Education": FUTURAMA["cyan"],
    "Career/Remote": FUTURAMA["light"],
    "ML/Interpretability": FUTURAMA["purple"],
}
C_source = {
    "S": FUTURAMA["teal"],
    "G": FUTURAMA["orange"],
}

# ============================================================================
# GLOBAL STYLE (same as Phase 1)
# ============================================================================
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": FUTURAMA["dark"],
    "axes.labelcolor": FUTURAMA["dark"],
    "axes.linewidth": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": FUTURAMA["dark"],
    "ytick.color": FUTURAMA["dark"],
    "xtick.major.width": 0.45,
    "ytick.major.size": 2.5,
    "ytick.direction": "out",
    "text.color": FUTURAMA["dark"],
    "font.family": "Arial",
    "font.size": 8,
})

OUT = "D:/Antigravity/awesome-awesomers/plots"
os.makedirs(OUT, exist_ok=True)

# ============================================================================
# FIG 1: OVERVIEW (4 paneles)
# ============================================================================
print("Generating Fig 1: Overview...")

fig = plt.figure(figsize=(11, 8))
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3, left=0.08, right=0.97, top=0.94, bottom=0.08)

# Panel A: Score ranking (lollipop)
ax_a = fig.add_subplot(gs[0, 0])
df_sorted_score = df.sort_values("score")
y_pos = np.arange(len(df_sorted_score))
colors_a = [C.get(cat, FUTURAMA["dark"]) for cat in df_sorted_score["Category"]]

ax_a.scatter(df_sorted_score["score"], y_pos, s=100, color=colors_a, zorder=3, edgecolor=FUTURAMA["dark"], linewidth=0.5)
for i, (idx, row) in enumerate(df_sorted_score.iterrows()):
    ax_a.plot([0, row["score"]], [i, i], color=colors_a[i], linewidth=1, alpha=0.4, zorder=1)

ax_a.set_yticks(y_pos)
ax_a.set_yticklabels([n.split()[0] for n in df_sorted_score["Name"]], fontsize=5)
ax_a.set_xlabel("Score", fontsize=7)
ax_a.set_xlim(0, df["score"].max() * 1.1)
ax_a.set_title("a) Curator Score Ranking", fontsize=8, fontweight="bold", loc="left", pad=5)
ax_a.grid(True, alpha=0.2, axis="x", linestyle=":", linewidth=0.5)
ax_a.spines["left"].set_visible(False)
ax_a.set_yticks([])
for i, (idx, row) in enumerate(df_sorted_score.iterrows()):
    ax_a.text(-0.5, i, row["Name"].split()[0], fontsize=4.5, ha="right", va="center")

# Panel B: Donut (Source)
ax_b = fig.add_subplot(gs[0, 1])
source_counts = df["Source"].value_counts()
colors_b = [C_source[s] for s in source_counts.index]
wedges, texts, autotexts = ax_b.pie(source_counts.values, labels=source_counts.index, colors=colors_b,
                                      autopct="%1.0f%%", startangle=90, textprops={"fontsize": 7})
for autotext in autotexts:
    autotext.set_color("white")
    autotext.set_fontweight("bold")
ax_b.set_title("b) Source: Seed vs Graph", fontsize=8, fontweight="bold", loc="left", pad=5)

# Panel C: Stars per repo distribution
ax_c = fig.add_subplot(gs[1, 0])
cats = df["Category"].value_counts().head(6).index
for i, cat in enumerate(cats):
    cat_spr = df[df["Category"] == cat]["spr"].values
    ax_c.scatter([i] * len(cat_spr), cat_spr, alpha=0.4, s=25,
                color=C.get(cat, FUTURAMA["dark"]))

ax_c.set_xticks(range(len(cats)))
ax_c.set_xticklabels(cats, rotation=45, ha="right", fontsize=6)
ax_c.set_ylabel("Stars per Repo", fontsize=7)
ax_c.set_yscale("log")
ax_c.set_title("c) Productivity (Stars/Repo)", fontsize=8, fontweight="bold", loc="left", pad=5)
ax_c.grid(True, alpha=0.2, axis="y", linestyle=":", linewidth=0.5)

# Panel D: Languages
ax_d = fig.add_subplot(gs[1, 1])
lang_counts = df["PrimaryLang"].value_counts().sort_values(ascending=True)
colors_d = FUTURAMA["orange"] if lang_counts.index[0] in ["Python"] else FUTURAMA["teal"]
ax_d.barh(range(len(lang_counts)), lang_counts.values, color=[FUTURAMA["orange"], FUTURAMA["teal"], FUTURAMA["cyan"]][:len(lang_counts)],
         edgecolor=FUTURAMA["dark"], linewidth=0.5, height=0.7)
ax_d.set_yticks(range(len(lang_counts)))
ax_d.set_yticklabels(lang_counts.index, fontsize=7)
ax_d.set_xlabel("Count", fontsize=7)
ax_d.set_title("d) Primary Languages", fontsize=8, fontweight="bold", loc="left", pad=5)

fig.suptitle("Awesome Repo Curators: Overview (n=21, 4.2M awesome stars)",
             fontsize=9, fontweight="bold", y=0.99)
plt.savefig(f"{OUT}/P2_Fig1_overview_curators_futurama.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig(f"{OUT}/P2_Fig1_overview_curators_futurama.pdf", bbox_inches="tight", facecolor="white")
plt.close()

# ============================================================================
# FIG 2: SCORE RANKING + DECOMPOSITION
# ============================================================================
print("Generating Fig 2: Score Ranking...")

fig = plt.figure(figsize=(11, 6))
gs = GridSpec(1, 2, figure=fig, wspace=0.35, left=0.08, right=0.97, top=0.92, bottom=0.15)

# Panel A: Cleveland dots (score components)
ax_a = fig.add_subplot(gs[0, 0])
df_sorted = df.sort_values("score")
y_pos = np.arange(len(df_sorted))

# Stacked contribution
followers_contrib = df_sorted["log_f"] * 0.40
stars_contrib = df_sorted["log_s"] * 0.35
repos_contrib = df_sorted["log_r"] * 0.25

x_followers = followers_contrib
x_stars = x_followers + stars_contrib
x_repos = x_stars + repos_contrib

ax_a.barh(y_pos, followers_contrib, label="Followers (40%)", color=FUTURAMA["orange"], height=0.65)
ax_a.barh(y_pos, stars_contrib, left=x_followers, label="Stars (35%)", color=FUTURAMA["cyan"], height=0.65)
ax_a.barh(y_pos, repos_contrib, left=x_stars, label="Repos (25%)", color=FUTURAMA["teal"], height=0.65)

ax_a.set_yticks(y_pos)
names_short = [n.split()[0][:8] for n in df_sorted["Name"]]
ax_a.set_yticklabels(names_short, fontsize=5.5)
ax_a.set_xlabel("Score Decomposition", fontsize=7)
ax_a.legend(fontsize=5.5, loc="lower right", framealpha=0.95)
ax_a.set_title("a) Score Components (Stacked)", fontsize=8, fontweight="bold", loc="left", pad=5)
ax_a.spines["left"].set_visible(False)

# Panel B: Log-log scatter (followers vs stars)
ax_b = fig.add_subplot(gs[0, 1])
for cat in df["Category"].unique():
    mask = df["Category"] == cat
    ax_b.scatter(df[mask]["log_f"], df[mask]["log_s"], s=80, alpha=0.7,
                color=C.get(cat, FUTURAMA["dark"]), label=cat, edgecolor=FUTURAMA["dark"], linewidth=0.5)

# Fit a line
z = np.polyfit(df["log_f"], df["log_s"], 1)
p = np.poly1d(z)
ax_b.plot(df["log_f"].sort_values(), p(df["log_f"].sort_values()), "k--", alpha=0.3, linewidth=1)

ax_b.set_xlabel("Log Followers", fontsize=7)
ax_b.set_ylabel("Log Awesome Stars", fontsize=7)
ax_b.set_title("b) Influence vs Impact", fontsize=8, fontweight="bold", loc="left", pad=5)
ax_b.legend(fontsize=4.5, loc="lower right", ncol=2, framealpha=0.95)
ax_b.grid(True, alpha=0.2, linestyle=":", linewidth=0.5)

fig.suptitle("Curator Score Decomposition & Correlations", fontsize=9, fontweight="bold", y=0.98)
plt.savefig(f"{OUT}/P2_Fig2_score_curators_futurama.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig(f"{OUT}/P2_Fig2_score_curators_futurama.pdf", bbox_inches="tight", facecolor="white")
plt.close()

# ============================================================================
# FIG 3: LANDSCAPE (Repos vs Stars scatter)
# ============================================================================
print("Generating Fig 3: Landscape...")

fig, ax = plt.subplots(figsize=(10, 7))

for cat in df["Category"].unique():
    mask = df["Category"] == cat
    ax.scatter(df[mask]["Repos"], df[mask]["TotalStars"], s=100, alpha=0.7,
              color=C.get(cat, FUTURAMA["dark"]), label=cat, edgecolor=FUTURAMA["dark"], linewidth=0.6)

# Annotate top outliers
top_outliers = df.nlargest(3, "TotalStars")
for idx, row in top_outliers.iterrows():
    ax.annotate(row["Name"].split()[0], (row["Repos"], row["TotalStars"]),
               fontsize=5, alpha=0.7, xytext=(5, 5), textcoords="offset points")

ax.set_xlabel("Number of Repos (log)", fontsize=8)
ax.set_ylabel("Total Awesome Stars (log)", fontsize=8)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_title("Repository Landscape: Breadth vs Depth", fontsize=9, fontweight="bold", pad=10)
ax.legend(fontsize=6, loc="lower right", ncol=2, framealpha=0.95)
ax.grid(True, alpha=0.2, which="both", linestyle=":", linewidth=0.5)

plt.tight_layout()
plt.savefig(f"{OUT}/P2_Fig3_landscape_curators_futurama.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig(f"{OUT}/P2_Fig3_landscape_curators_futurama.pdf", bbox_inches="tight", facecolor="white")
plt.close()

# ============================================================================
# FIG 4: NETWORK (curator connections by category)
# ============================================================================
print("Generating Fig 4: Network...")

fig, ax = plt.subplots(figsize=(9, 8))

# Create graph
G = nx.Graph()
for idx, row in df.iterrows():
    G.add_node(row["GitHub"], category=row["Category"], score=row["score"])

# Connect curators in same category (simplified)
for cat in df["Category"].unique():
    cat_members = df[df["Category"] == cat]["GitHub"].tolist()
    for i, m1 in enumerate(cat_members):
        for m2 in cat_members[i+1:]:
            G.add_edge(m1, m2, weight=0.5)

# Layout
pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

# Draw
for node in G.nodes():
    cat = G.nodes[node].get("category", "Unknown")
    score = G.nodes[node].get("score", 0)
    size = 300 + score * 200
    nx.draw_networkx_nodes(G, pos, nodelist=[node], node_size=size,
                          node_color=[C.get(cat, FUTURAMA["dark"])],
                          edgecolors=FUTURAMA["dark"], linewidths=0.8,
                          ax=ax, alpha=0.8)

# Edges
nx.draw_networkx_edges(G, pos, alpha=0.1, width=0.5, ax=ax)

# Labels (abbreviated)
labels = {node: node.split("_")[0][:6] for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=4, font_color=FUTURAMA["dark"], ax=ax)

ax.set_title("Curator Network (node size = score, edges = same category)", fontsize=9, fontweight="bold", pad=10)
ax.axis("off")

plt.tight_layout()
plt.savefig(f"{OUT}/P2_Fig4_network_curators_futurama.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig(f"{OUT}/P2_Fig4_network_curators_futurama.pdf", bbox_inches="tight", facecolor="white")
plt.close()

# ============================================================================
# FIG 5: EFFICIENCY & PRODUCTIVITY
# ============================================================================
print("Generating Fig 5: Efficiency...")

fig = plt.figure(figsize=(11, 6))
gs = GridSpec(1, 2, figure=fig, wspace=0.35, left=0.08, right=0.97, top=0.92, bottom=0.15)

# Panel A: Followers per repo
ax_a = fig.add_subplot(gs[0, 0])
df_eff = df.sort_values("fpr", ascending=True)
y_pos = np.arange(len(df_eff))
colors_a = [C.get(cat, FUTURAMA["dark"]) for cat in df_eff["Category"]]

ax_a.barh(y_pos, df_eff["fpr"], color=colors_a, edgecolor=FUTURAMA["dark"], linewidth=0.5, height=0.65)
ax_a.set_yticks(y_pos)
ax_a.set_yticklabels([n.split()[0][:8] for n in df_eff["Name"]], fontsize=5.5)
ax_a.set_xlabel("Followers per Repo", fontsize=7)
ax_a.set_xscale("log")
ax_a.set_title("a) Engagement Efficiency", fontsize=8, fontweight="bold", loc="left", pad=5)
ax_a.spines["left"].set_visible(False)

# Panel B: Stars per repo (productivity)
ax_b = fig.add_subplot(gs[0, 1])
df_prod = df.sort_values("spr", ascending=True)
y_pos = np.arange(len(df_prod))
colors_b = [C.get(cat, FUTURAMA["dark"]) for cat in df_prod["Category"]]

ax_b.barh(y_pos, df_prod["spr"], color=colors_b, edgecolor=FUTURAMA["dark"], linewidth=0.5, height=0.65)
ax_b.set_yticks(y_pos)
ax_b.set_yticklabels([n.split()[0][:8] for n in df_prod["Name"]], fontsize=5.5)
ax_b.set_xlabel("Awesome Stars per Repo", fontsize=7)
ax_b.set_xscale("log")
ax_b.set_title("b) Curation Quality (Stars/Repo)", fontsize=8, fontweight="bold", loc="left", pad=5)
ax_b.spines["left"].set_visible(False)

fig.suptitle("Curator Efficiency Metrics", fontsize=9, fontweight="bold", y=0.98)
plt.savefig(f"{OUT}/P2_Fig5_efficiency_curators_futurama.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig(f"{OUT}/P2_Fig5_efficiency_curators_futurama.pdf", bbox_inches="tight", facecolor="white")
plt.close()

# ============================================================================
# FIG 6: CATEGORY DEEP DIVE (top 3)
# ============================================================================
print("Generating Fig 6: Category Deep Dive...")

fig = plt.figure(figsize=(12, 6))
gs = GridSpec(1, 3, figure=fig, wspace=0.3, left=0.06, right=0.98, top=0.92, bottom=0.15)

top_cats = df["Category"].value_counts().head(3).index
for panel_idx, cat in enumerate(top_cats):
    ax = fig.add_subplot(gs[0, panel_idx])
    cat_df = df[df["Category"] == cat].sort_values("score", ascending=True)

    y_pos = np.arange(len(cat_df))
    color_cat = C.get(cat, FUTURAMA["dark"])

    ax.barh(y_pos, cat_df["score"], color=color_cat, edgecolor=FUTURAMA["dark"], linewidth=0.5, height=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(cat_df["Name"], fontsize=5.5)
    ax.set_xlabel("Score", fontsize=7)
    ax.set_title(f"{chr(97+panel_idx)}) {cat} (n={len(cat_df)})", fontsize=8, fontweight="bold", loc="left", pad=5)
    ax.spines["left"].set_visible(False)

fig.suptitle("Top 3 Categories: Curator Scores", fontsize=9, fontweight="bold", y=0.98)
plt.savefig(f"{OUT}/P2_Fig6_deepdive_curators_futurama.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig(f"{OUT}/P2_Fig6_deepdive_curators_futurama.pdf", bbox_inches="tight", facecolor="white")
plt.close()

# ============================================================================
# FIG 7: HEATMAP (all curators × metrics)
# ============================================================================
print("Generating Fig 7: Heatmap...")

fig, ax = plt.subplots(figsize=(10, 8))

# Normalize metrics
df_norm = df.copy()
for col in ["log_f", "log_r", "log_s"]:
    df_norm[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min()) * 100

# Heatmap data (sorted by score)
heatmap_data = df_norm.sort_values("score", ascending=False)[["log_f", "log_r", "log_s"]].values.T
curator_labels = df_norm.sort_values("score", ascending=False)["Name"].values

im = ax.imshow(heatmap_data, cmap="YlOrRd", aspect="auto", vmin=0, vmax=100)

ax.set_xticks(range(len(curator_labels)))
ax.set_xticklabels(curator_labels, rotation=45, ha="right", fontsize=5.5)
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(["Followers", "Repos", "Stars"], fontsize=7)

# Colorbar
cbar = plt.colorbar(im, ax=ax, orientation="vertical", pad=0.02, shrink=0.8)
cbar.set_label("Normalized Score", fontsize=6)
cbar.ax.tick_params(labelsize=5)

# Add text annotations
for i in range(len(heatmap_data)):
    for j in range(len(curator_labels)):
        text = ax.text(j, i, f"{int(heatmap_data[i, j])}", ha="center", va="center",
                      color="white" if heatmap_data[i, j] > 50 else "black", fontsize=4)

ax.set_title("Curator Metrics Heatmap (Normalized 0-100)", fontsize=9, fontweight="bold", pad=10)

plt.tight_layout()
plt.savefig(f"{OUT}/P2_Fig7_heatmap_curators_futurama.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig(f"{OUT}/P2_Fig7_heatmap_curators_futurama.pdf", bbox_inches="tight", facecolor="white")
plt.close()

# ============================================================================
# FIG 8: CATEGORY × LANGUAGE BREAKDOWN
# ============================================================================
print("Generating Fig 8: Category × Language...")

fig = plt.figure(figsize=(11, 6))
gs = GridSpec(1, 2, figure=fig, wspace=0.35, left=0.08, right=0.97, top=0.92, bottom=0.15)

# Panel A: Total stars by category
ax_a = fig.add_subplot(gs[0, 0])
cat_stats = df.groupby("Category")["TotalStars"].sum().sort_values(ascending=True)
colors_a = [C.get(c, FUTURAMA["dark"]) for c in cat_stats.index]
ax_a.barh(range(len(cat_stats)), cat_stats.values, color=colors_a, edgecolor=FUTURAMA["dark"], linewidth=0.5, height=0.65)
ax_a.set_yticks(range(len(cat_stats)))
ax_a.set_yticklabels(cat_stats.index, fontsize=6)
ax_a.set_xlabel("Total Awesome Stars", fontsize=7)
ax_a.set_xscale("log")
ax_a.set_title("a) Category Impact (Total Stars)", fontsize=8, fontweight="bold", loc="left", pad=5)
ax_a.spines["left"].set_visible(False)

# Panel B: Languages (stack)
ax_b = fig.add_subplot(gs[0, 1])
lang_counts = df["PrimaryLang"].value_counts().sort_values(ascending=False)
colors_b = [FUTURAMA["orange"], FUTURAMA["teal"], FUTURAMA["cyan"], FUTURAMA["purple"]][:len(lang_counts)]
ax_b.bar(range(len(lang_counts)), lang_counts.values, color=colors_b, edgecolor=FUTURAMA["dark"], linewidth=0.5, width=0.6)
ax_b.set_xticks(range(len(lang_counts)))
ax_b.set_xticklabels(lang_counts.index, fontsize=6, rotation=45, ha="right")
ax_b.set_ylabel("Curator Count", fontsize=7)
ax_b.set_title("b) Primary Languages", fontsize=8, fontweight="bold", loc="left", pad=5)

fig.suptitle("Category Impact & Language Distribution", fontsize=9, fontweight="bold", y=0.98)
plt.savefig(f"{OUT}/P2_Fig8_languages_curators_futurama.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig(f"{OUT}/P2_Fig8_languages_curators_futurama.pdf", bbox_inches="tight", facecolor="white")
plt.close()

print("\n" + "="*70)
print("PHASE 2 CORRECTED: ALL 8 FIGURES GENERATED")
print("="*70)
print("* Focus: 21 Awesome Repo CURATORS (not repos)")
print("* Data model: Identical to Phase 1 (people-centric)")
print("* Metrics: score, followers, repos, stars, efficiency")
print("* Paleta: FUTURAMA")
print("* All files: 300 dpi PNG + vectorial PDF")
print("="*70)
