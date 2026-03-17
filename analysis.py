"""
Awesome Awesomers — Analysis & Visualization
=============================================
Generates tables and plots from the curated awesomers dataset.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os

# ── Data ────────────────────────────────────────────────────────────────────
data = [
    # AI / ML Leaders
    ("Andrej Karpathy", "AI / ML Leaders", "karpathy", 147980, 63, "G"),
    ("George Hotz", "AI / ML Leaders", "geohot", 46136, 101, "G"),
    ("Francois Chollet", "AI / ML Leaders", "fchollet", 17860, 16, "G"),
    ("Soumith Chintala", "AI / ML Leaders", "soumith", 13119, 169, "G"),
    ("Peter Norvig", "AI / ML Leaders", "norvig", 9726, 4, "G"),
    ("Yann LeCun", "AI / ML Leaders", "ylecun", 1509, 12, "S"),
    ("Cassie Kozyrkov", "AI / ML Leaders", "kozyrkov", 1039, 5, "S"),
    ("Aravind Srinivas", "AI / ML Leaders", "aravindsrinivas", 229, 34, "S"),
    ("Andrew Ng", "AI / ML Leaders", "AndrewNg", 98, 20, "S"),
    ("Demis Hassabis", "AI / ML Leaders", None, None, None, "S"),
    ("Fei-Fei Li", "AI / ML Leaders", None, None, None, "S"),
    ("Mustafa Suleyman", "AI / ML Leaders", None, None, None, "S"),
    ("Yossi Matias", "AI / ML Leaders", None, None, None, "S"),
    ("Xiaole Shirley Liu", "AI / ML Leaders", None, None, None, "S"),
    ("Lior Pachter", "AI / ML Leaders", "pachterlab", 377, 169, "S"),
    ("Santiago Carmona", "AI / ML Leaders", None, None, None, "S"),

    # AI / ML Researchers & Engineers
    ("Sebastian Raschka", "AI / ML Researchers", "rasbt", 36345, 147, "S"),
    ("Christopher Olah", "AI / ML Researchers", "colah", 9766, 52, "G"),
    ("Ross Wightman", "AI / ML Researchers", "rwightman", 7002, 74, "G"),
    ("Maxime Labonne", "AI / ML Researchers", "mlabonne", 6536, 23, "G"),
    ("Sasha Rush", "AI / ML Researchers", "srush", 3832, 165, "G"),
    ("Alfredo Canziani", "AI / ML Researchers", "Atcold", 3675, 70, "G"),
    ("Tri Dao", "AI / ML Researchers", "tridao", 2933, 10, "G"),
    ("Chelsea Finn", "AI / ML Researchers", "cbfinn", 2174, 25, "G"),
    ("Laurens van der Maaten", "AI / ML Researchers", "lvdmaaten", 1975, 23, "G"),
    ("Jim Fan", "AI / ML Researchers", "DrJimFan", 934, 7, "G"),
    ("Durk Kingma", "AI / ML Researchers", "dpkingma", 597, 9, "G"),
    ("Adam Kosiorek", "AI / ML Researchers", "akosiorek", 375, 40, "S"),
    ("Sahar Mor", "AI / ML Researchers", "saharmor", 205, 86, "S"),
    ("Oriol Vinyals", "AI / ML Researchers", "OriolVinyals", 84, 3, "G"),
    ("Marily Nika", "AI / ML Researchers", None, None, None, "S"),
    ("Diego Granados", "AI / ML Researchers", None, None, None, "S"),
    ("Sasha Dagayev", "AI / ML Researchers", None, None, None, "S"),
    ("Lior Alexander", "AI / ML Researchers", None, None, None, "S"),
    ("Leo Kadieff", "AI / ML Researchers", None, None, None, "S"),

    # AI Educators
    ("Ben Pierron", "AI Educators", None, None, None, "S"),
    ("Altiam Kabir", "AI Educators", None, None, None, "S"),
    ("Sai Charan", "AI Educators", None, None, None, "S"),
    ("Hamna Aslam Kahn", "AI Educators", None, None, None, "S"),
    ("Khizer Abbas", "AI Educators", None, None, None, "S"),
    ("Tianyu Xu", "AI Educators", None, None, None, "S"),
    ("Sumanth P", "AI Educators", None, None, None, "S"),
    ("Luiza Jarovsky", "AI Educators", None, None, None, "S"),

    # Bioinformatics
    ("Heng Li", "Bioinformatics", "lh3", 4267, 138, "G"),
    ("Ming Tommy Tang", "Bioinformatics", "crazyhottommy", 3726, 177, "S"),
    ("Rafael Irizarry", "Bioinformatics", "rafalab", 1633, 49, "S"),
    ("Wei Shen", "Bioinformatics", "shenwei356", 1469, 119, "G"),
    ("Phil Ewels", "Bioinformatics", "ewels", 844, 159, "G"),
    ("Aaron Quinlan", "Bioinformatics", "arq5x", 771, 75, "G"),
    ("Pierre Lindenbaum", "Bioinformatics", "lindenb", 555, 178, "G"),
    ("Eugene Myers", "Bioinformatics", "thegenemyers", 467, 19, "G"),
    ("Richard Durbin", "Bioinformatics", "richarddurbin", 380, 20, "G"),
    ("Nils Homer", "Bioinformatics", "nh13", 374, 207, "S"),
    ("Boas Pucker", "Bioinformatics", "bpucker", 187, 80, "S"),
    ("Ben Johnson", "Bioinformatics", "biobenkj", 121, 132, "G"),
    ("Dean Lee", "Bioinformatics", "deanslee", 118, 2, "S"),
    ("Zuguang Gu", "Bioinformatics", "jokergoo", 0, 97, "G"),
    ("Ana Hernandez Plaza", "Bioinformatics", None, None, None, "S"),
    ("Alejandro Lozano", "Bioinformatics", None, None, None, "S"),
    ("Vidith Phillips", "Bioinformatics", "VidithPhillips", 0, 10, "S"),

    # Data Science
    ("Hadley Wickham", "Data Science", "hadley", 26541, 230, "G"),
    ("Jake Vanderplas", "Data Science", "jakevdp", 19048, 239, "G"),
    ("Gael Varoquaux", "Data Science", "GaelVaroquaux", 3393, 90, "G"),
    ("Fabian Theis", "Data Science", "theislab", 1399, 253, "S"),

    # Pharma / Science Policy
    ("Thibault Geoui", "Pharma / Science", None, None, None, "S"),
    ("Simon Uribe", "Pharma / Science", None, None, None, "S"),
    ("Nerea Eloy Gimenez", "Pharma / Science", None, None, None, "S"),
    ("Juan Cruz Cigudosa", "Pharma / Science", None, None, None, "S"),
    ("Anna Medvedeva", "Pharma / Science", None, None, None, "S"),

    # Other
    ("Manuel Sopena", "Other", "ManuelSopenaBallesteros", 0, 0, "S"),
    ("Andrew Sandford", "Other", None, None, None, "S"),
    ("Layal Al Kibbi", "Other", None, None, None, "S"),
    ("Liubov Timofeeva", "Other", None, None, None, "S"),
    ("Bhav Malik", "Other", None, None, None, "S"),
    ("Mariana Fano", "Other", None, None, None, "S"),
    ("Beatriz Paneda", "Other", None, None, None, "S"),
]

df = pd.DataFrame(data, columns=["Name", "Category", "GitHub", "Followers", "Repos", "Source"])

OUT = "D:/Antigravity/awesome-awesomers/plots"
os.makedirs(OUT, exist_ok=True)

# ── Style ───────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#0d1117",
    "axes.facecolor": "#0d1117",
    "axes.edgecolor": "#30363d",
    "axes.labelcolor": "#c9d1d9",
    "xtick.color": "#8b949e",
    "ytick.color": "#8b949e",
    "text.color": "#c9d1d9",
    "font.family": "sans-serif",
    "font.size": 11,
    "grid.color": "#21262d",
    "grid.alpha": 0.7,
})

PALETTE = {
    "AI / ML Leaders": "#f78166",
    "AI / ML Researchers": "#d2a8ff",
    "AI Educators": "#79c0ff",
    "Bioinformatics": "#56d364",
    "Data Science": "#ffa657",
    "Pharma / Science": "#ff7b72",
    "Other": "#8b949e",
}

# ══════════════════════════════════════════════════════════════════════════════
# PLOT 1 — Category distribution
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))
cat_counts = df["Category"].value_counts()
colors = [PALETTE.get(c, "#8b949e") for c in cat_counts.index]
bars = ax.barh(cat_counts.index, cat_counts.values, color=colors, edgecolor="#30363d", linewidth=0.5)
ax.set_xlabel("Number of Awesomers")
ax.set_title("Awesome Awesomers — Distribution by Category", fontsize=14, fontweight="bold", pad=15)
ax.invert_yaxis()
for bar, val in zip(bars, cat_counts.values):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, str(val),
            va="center", ha="left", fontsize=11, color="#c9d1d9")
ax.set_xlim(0, cat_counts.max() + 3)
ax.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{OUT}/01_category_distribution.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Plot 1: Category distribution")

# ══════════════════════════════════════════════════════════════════════════════
# PLOT 2 — Seed vs Graph expansion
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Pie chart
source_counts = df["Source"].value_counts()
axes[0].pie(source_counts, labels=["Seed (LinkedIn/Web)", "Graph (GitHub)"],
            autopct="%1.0f%%", colors=["#79c0ff", "#56d364"],
            textprops={"color": "#c9d1d9", "fontsize": 12},
            wedgeprops={"edgecolor": "#0d1117", "linewidth": 2})
axes[0].set_title("Source of Discovery", fontsize=13, fontweight="bold")

# Stacked bar per category
pivot = df.groupby(["Category", "Source"]).size().unstack(fill_value=0)
pivot = pivot.reindex(cat_counts.index)
pivot.plot(kind="barh", stacked=True, ax=axes[1],
           color={"S": "#79c0ff", "G": "#56d364"},
           edgecolor="#30363d", linewidth=0.5)
axes[1].set_xlabel("Count")
axes[1].set_title("Seed vs Graph per Category", fontsize=13, fontweight="bold")
axes[1].legend(["Seed", "Graph"], loc="lower right", facecolor="#161b22", edgecolor="#30363d")
axes[1].invert_yaxis()
axes[1].grid(axis="x", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.savefig(f"{OUT}/02_seed_vs_graph.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Plot 2: Seed vs Graph")

# ══════════════════════════════════════════════════════════════════════════════
# PLOT 3 — Top 20 by GitHub followers (log scale)
# ══════════════════════════════════════════════════════════════════════════════
gh = df.dropna(subset=["Followers"]).nlargest(20, "Followers").copy()
gh = gh.iloc[::-1]  # reverse for horizontal bar

fig, ax = plt.subplots(figsize=(11, 8))
colors = [PALETTE.get(c, "#8b949e") for c in gh["Category"]]
bars = ax.barh(gh["Name"], gh["Followers"], color=colors, edgecolor="#30363d", linewidth=0.5)
ax.set_xscale("log")
ax.set_xlabel("GitHub Followers (log scale)")
ax.set_title("Top 20 Awesomers by GitHub Followers", fontsize=14, fontweight="bold", pad=15)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.grid(axis="x", linestyle="--", alpha=0.3)

# Add follower count labels
for bar, val in zip(bars, gh["Followers"]):
    ax.text(val * 1.15, bar.get_y() + bar.get_height()/2, f"{int(val):,}",
            va="center", ha="left", fontsize=9, color="#8b949e")

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=c, edgecolor="#30363d", label=l) for l, c in PALETTE.items() if l in gh["Category"].values]
ax.legend(handles=legend_elements, loc="lower right", facecolor="#161b22", edgecolor="#30363d", fontsize=9)

plt.tight_layout()
plt.savefig(f"{OUT}/03_top20_followers.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Plot 3: Top 20 followers")

# ══════════════════════════════════════════════════════════════════════════════
# PLOT 4 — Repos vs Followers scatter
# ══════════════════════════════════════════════════════════════════════════════
gh_all = df.dropna(subset=["Followers", "Repos"]).copy()
gh_all = gh_all[gh_all["Followers"] > 0]

fig, ax = plt.subplots(figsize=(11, 8))
for cat in gh_all["Category"].unique():
    subset = gh_all[gh_all["Category"] == cat]
    ax.scatter(subset["Repos"], subset["Followers"],
               c=PALETTE.get(cat, "#8b949e"), label=cat,
               s=80, alpha=0.85, edgecolors="#30363d", linewidth=0.5, zorder=3)

# Label notable points
notable = gh_all.nlargest(12, "Followers")
for _, row in notable.iterrows():
    ax.annotate(row["Name"].split()[-1],
                (row["Repos"], row["Followers"]),
                textcoords="offset points", xytext=(8, 5),
                fontsize=8, color="#8b949e", alpha=0.9)

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Public Repos (log)")
ax.set_ylabel("GitHub Followers (log)")
ax.set_title("Repos vs Followers — Awesomer Landscape", fontsize=14, fontweight="bold", pad=15)
ax.legend(loc="upper left", facecolor="#161b22", edgecolor="#30363d", fontsize=9)
ax.grid(True, linestyle="--", alpha=0.3)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

plt.tight_layout()
plt.savefig(f"{OUT}/04_repos_vs_followers.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Plot 4: Repos vs Followers")

# ══════════════════════════════════════════════════════════════════════════════
# PLOT 5 — GitHub presence heatmap by category
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
stats = df.groupby("Category").agg(
    total=("Name", "count"),
    has_github=("GitHub", lambda x: x.notna().sum()),
    avg_followers=("Followers", "mean"),
    avg_repos=("Repos", "mean"),
    max_followers=("Followers", "max"),
).reindex(cat_counts.index)
stats["github_pct"] = (stats["has_github"] / stats["total"] * 100).round(0)

# Table-style bar chart
x = np.arange(len(stats))
width = 0.35
bars1 = ax.bar(x - width/2, stats["total"], width, label="Total", color="#79c0ff", edgecolor="#30363d")
bars2 = ax.bar(x + width/2, stats["has_github"], width, label="Has GitHub", color="#56d364", edgecolor="#30363d")
ax.set_xticks(x)
ax.set_xticklabels(stats.index, rotation=30, ha="right", fontsize=9)
ax.set_ylabel("Count")
ax.set_title("GitHub Presence by Category", fontsize=14, fontweight="bold", pad=15)
ax.legend(facecolor="#161b22", edgecolor="#30363d")
ax.grid(axis="y", linestyle="--", alpha=0.3)

# Add percentage labels
for i, (b1, b2, pct) in enumerate(zip(bars1, bars2, stats["github_pct"])):
    ax.text(b2.get_x() + b2.get_width()/2, b2.get_height() + 0.3,
            f"{int(pct)}%", ha="center", va="bottom", fontsize=9, color="#56d364")

plt.tight_layout()
plt.savefig(f"{OUT}/05_github_presence.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Plot 5: GitHub presence")

# ══════════════════════════════════════════════════════════════════════════════
# PLOT 6 — Bioinformatics focus: followers ranking
# ══════════════════════════════════════════════════════════════════════════════
bio = df[df["Category"] == "Bioinformatics"].dropna(subset=["Followers"]).copy()
bio = bio.sort_values("Followers", ascending=True)

fig, ax = plt.subplots(figsize=(10, 7))
bars = ax.barh(bio["Name"], bio["Followers"], color="#56d364", edgecolor="#30363d", linewidth=0.5)
ax.set_xlabel("GitHub Followers")
ax.set_title("Bioinformatics Awesomers — GitHub Followers", fontsize=14, fontweight="bold", pad=15)
ax.grid(axis="x", linestyle="--", alpha=0.3)
for bar, val in zip(bars, bio["Followers"]):
    label = f"{int(val):,}" if val > 0 else "0"
    ax.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2, label,
            va="center", ha="left", fontsize=10, color="#8b949e")
ax.set_xlim(0, bio["Followers"].max() * 1.15)

plt.tight_layout()
plt.savefig(f"{OUT}/06_bioinformatics_ranking.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Plot 6: Bioinformatics ranking")

# ══════════════════════════════════════════════════════════════════════════════
# Print summary tables
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*80)
print("SUMMARY TABLES")
print("="*80)

print("\n📊 Table 1: Category Overview")
print(stats[["total", "has_github", "github_pct", "avg_followers", "max_followers"]].to_string())

print("\n📊 Table 2: Top 15 by GitHub Followers")
top15 = df.dropna(subset=["Followers"]).nlargest(15, "Followers")[["Name", "Category", "GitHub", "Followers", "Repos", "Source"]]
print(top15.to_string(index=False))

print("\n📊 Table 3: Top 10 by Repos")
top10r = df.dropna(subset=["Repos"]).nlargest(10, "Repos")[["Name", "Category", "GitHub", "Repos", "Followers"]]
print(top10r.to_string(index=False))

print("\n📊 Table 4: Bioinformatics Leaderboard")
bio_table = df[df["Category"] == "Bioinformatics"].dropna(subset=["Followers"]).sort_values("Followers", ascending=False)
print(bio_table[["Name", "GitHub", "Followers", "Repos", "Source"]].to_string(index=False))

print(f"\n✅ All 6 plots saved to: {OUT}/")
print(f"📈 Total awesomers: {len(df)}")
print(f"   Seed: {(df['Source']=='S').sum()} | Graph: {(df['Source']=='G').sum()}")
print(f"   With GitHub: {df['GitHub'].notna().sum()} | Without: {df['GitHub'].isna().sum()}")
