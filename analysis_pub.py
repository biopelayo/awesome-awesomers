"""
Awesome Awesomers — Publication-Quality Analysis
=================================================
Nature / Cell Reports aesthetic. Network analysis + EDA.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as pe
from matplotlib.patches import Patch, FancyBboxPatch
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec
import numpy as np
import networkx as nx
from scipy import stats as sp_stats
import warnings
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════════════
data = [
    # AI / ML Leaders
    ("Andrej Karpathy", "AI/ML Leaders", "karpathy", 147980, 63, "G", "Former OpenAI / Tesla AI Director"),
    ("George Hotz", "AI/ML Leaders", "geohot", 46136, 101, "G", "Founder tinygrad / comma.ai"),
    ("Francois Chollet", "AI/ML Leaders", "fchollet", 17860, 16, "G", "Creator of Keras"),
    ("Soumith Chintala", "AI/ML Leaders", "soumith", 13119, 169, "G", "Co-creator PyTorch"),
    ("Peter Norvig", "AI/ML Leaders", "norvig", 9726, 4, "G", "Director of Research, Google"),
    ("Yann LeCun", "AI/ML Leaders", "ylecun", 1509, 12, "S", "VP & Chief AI Scientist, Meta"),
    ("Cassie Kozyrkov", "AI/ML Leaders", "kozyrkov", 1039, 5, "S", "CEO, ex-Google"),
    ("Aravind Srinivas", "AI/ML Leaders", "aravindsrinivas", 229, 34, "S", "Founder & CEO Perplexity"),
    ("Andrew Ng", "AI/ML Leaders", "AndrewNg", 98, 20, "S", "DeepLearning.AI, Stanford"),
    ("Demis Hassabis", "AI/ML Leaders", None, None, None, "S", "CEO Google DeepMind"),
    ("Fei-Fei Li", "AI/ML Leaders", None, None, None, "S", "Co-Director Stanford HAI"),
    ("Mustafa Suleyman", "AI/ML Leaders", None, None, None, "S", "CEO Microsoft AI"),
    ("Yossi Matias", "AI/ML Leaders", None, None, None, "S", "VP Google Research"),
    ("Xiaole Shirley Liu", "AI/ML Leaders", None, None, None, "S", "GV20 Therapeutics"),
    ("Lior Pachter", "AI/ML Leaders", "pachterlab", 377, 169, "S", "Caltech, kallisto"),
    ("Santiago Carmona", "AI/ML Leaders", None, None, None, "S", "Comp. biology, CHUV/UNIL"),

    # AI / ML Researchers & Engineers
    ("Sebastian Raschka", "AI/ML Research", "rasbt", 36345, 147, "S", "AI Research Engineer, LLMs"),
    ("Christopher Olah", "AI/ML Research", "colah", 9766, 52, "G", "Interpretability, Anthropic"),
    ("Ross Wightman", "AI/ML Research", "rwightman", 7002, 74, "G", "Computer Vision, HuggingFace"),
    ("Maxime Labonne", "AI/ML Research", "mlabonne", 6536, 23, "G", "Head Post-Training, Liquid AI"),
    ("Sasha Rush", "AI/ML Research", "srush", 3832, 165, "G", "Cornell Tech / HuggingFace"),
    ("Alfredo Canziani", "AI/ML Research", "Atcold", 3675, 70, "G", "Asst. Prof. CS, NYU"),
    ("Tri Dao", "AI/ML Research", "tridao", 2933, 10, "G", "Princeton, FlashAttention"),
    ("Chelsea Finn", "AI/ML Research", "cbfinn", 2174, 25, "G", "Asst. Prof. Stanford CS"),
    ("Laurens van der Maaten", "AI/ML Research", "lvdmaaten", 1975, 23, "G", "Creator of t-SNE"),
    ("Jim Fan", "AI/ML Research", "DrJimFan", 934, 7, "G", "NVIDIA AI Research"),
    ("Durk Kingma", "AI/ML Research", "dpkingma", 597, 9, "G", "Creator VAE, Adam optimizer"),
    ("Adam Kosiorek", "AI/ML Research", "akosiorek", 375, 40, "S", "Research Scientist, DeepMind"),
    ("Sahar Mor", "AI/ML Research", "saharmor", 205, 86, "S", "AI researcher, aitidbits"),
    ("Oriol Vinyals", "AI/ML Research", "OriolVinyals", 84, 3, "G", "VP Research, DeepMind"),
    ("Marily Nika", "AI/ML Research", None, None, None, "S", "Gen AI Product, Google"),
    ("Diego Granados", "AI/ML Research", None, None, None, "S", "AI Product Manager, Google"),
    ("Sasha Dagayev", "AI/ML Research", None, None, None, "S", "Head of AI"),
    ("Lior Alexander", "AI/ML Research", None, None, None, "S", "CEO AlphaSignal"),
    ("Leo Kadieff", "AI/ML Research", None, None, None, "S", "Sr. Creative Technologist"),

    # AI Educators
    ("Ben Pierron", "AI Educators", None, None, None, "S", "Co-founder Reino IA"),
    ("Altiam Kabir", "AI Educators", None, None, None, "S", "AI Educator, 800K+"),
    ("Sai Charan", "AI Educators", None, None, None, "S", "LLMs, RAG educator"),
    ("Hamna Aslam Kahn", "AI Educators", None, None, None, "S", "AI newsletter, 1M+"),
    ("Khizer Abbas", "AI Educators", None, None, None, "S", "Newsletter AI, 2M+"),
    ("Tianyu Xu", "AI Educators", None, None, None, "S", "Gen AI Educator"),
    ("Sumanth P", "AI Educators", None, None, None, "S", "ML Developer Advocate"),
    ("Luiza Jarovsky", "AI Educators", None, None, None, "S", "AI, Tech & Privacy Academy"),

    # Bioinformatics
    ("Heng Li", "Bioinformatics", "lh3", 4267, 138, "G", "BWA, minimap2, samtools"),
    ("Ming Tommy Tang", "Bioinformatics", "crazyhottommy", 3726, 177, "S", "Dir. Bioinfo, AstraZeneca"),
    ("Rafael Irizarry", "Bioinformatics", "rafalab", 1633, 49, "S", "Chair Data Sci, Dana-Farber"),
    ("Wei Shen", "Bioinformatics", "shenwei356", 1469, 119, "G", "Bioinfo tools developer"),
    ("Phil Ewels", "Bioinformatics", "ewels", 844, 159, "G", "PM Seqera, MultiQC, nf-core"),
    ("Aaron Quinlan", "Bioinformatics", "arq5x", 771, 75, "G", "Prof. Human Genetics, bedtools"),
    ("Pierre Lindenbaum", "Bioinformatics", "lindenb", 555, 178, "G", "Bioinfo, Inst. du Thorax"),
    ("Eugene Myers", "Bioinformatics", "thegenemyers", 467, 19, "G", "Inventor of BLAST"),
    ("Richard Durbin", "Bioinformatics", "richarddurbin", 380, 20, "G", "Sanger Inst, samtools"),
    ("Nils Homer", "Bioinformatics", "nh13", 374, 207, "S", "Founder Fulcrum Genomics"),
    ("Boas Pucker", "Bioinformatics", "bpucker", 187, 80, "S", "Prof. Plant Genomics"),
    ("Ben Johnson", "Bioinformatics", "biobenkj", 121, 132, "G", "Sr. Research, Van Andel"),
    ("Dean Lee", "Bioinformatics", "deanslee", 118, 2, "S", "Comp. bio educator"),
    ("Zuguang Gu", "Bioinformatics", "jokergoo", 0, 97, "G", "ComplexHeatmap author"),
    ("Ana Hernandez Plaza", "Bioinformatics", None, None, None, "S", "Bioinformatica, INIA"),
    ("Alejandro Lozano", "Bioinformatics", None, None, None, "S", "PhD Stanford, open bio AI"),
    ("Vidith Phillips", "Bioinformatics", "VidithPhillips", 0, 10, "S", "Imaging AI, St Jude"),

    # Data Science
    ("Hadley Wickham", "Data Science", "hadley", 26541, 230, "G", "Chief Scientist Posit, ggplot2"),
    ("Jake Vanderplas", "Data Science", "jakevdp", 19048, 239, "G", "Python ML & Data Science"),
    ("Gael Varoquaux", "Data Science", "GaelVaroquaux", 3393, 90, "G", "Inria, scikit-learn"),
    ("Fabian Theis", "Data Science", "theislab", 1399, 253, "S", "Dir. Comp. Health, Helmholtz"),

    # Pharma / Science Policy
    ("Thibault Geoui", "Pharma/Policy", None, None, None, "S", "Science CDO"),
    ("Simon Uribe", "Pharma/Policy", None, None, None, "S", "Head Clinical Informatics"),
    ("Nerea Eloy Gimenez", "Pharma/Policy", None, None, None, "S", "Marketing Rare Diseases"),
    ("Juan Cruz Cigudosa", "Pharma/Policy", None, None, None, "S", "Secretario Estado Ciencia ES"),
    ("Anna Medvedeva", "Pharma/Policy", None, None, None, "S", "Functional Medicine MD"),

    # Other
    ("Manuel Sopena", "Other", "ManuelSopenaBallesteros", 0, 0, "S", "Sr. System Engineer, CSCS"),
    ("Andrew Sandford", "Other", None, None, None, "S", "--"),
    ("Layal Al Kibbi", "Other", None, None, None, "S", "Content & Social Media"),
    ("Liubov Timofeeva", "Other", None, None, None, "S", "Brand Strategy"),
    ("Bhav Malik", "Other", None, None, None, "S", "Business Intelligence"),
    ("Mariana Fano", "Other", None, None, None, "S", "Bellas Artes"),
    ("Beatriz Paneda", "Other", None, None, None, "S", "Historiadora, Lund Univ."),
]

cols = ["Name", "Category", "GitHub", "Followers", "Repos", "Source", "Role"]
df = pd.DataFrame(data, columns=cols)

# Derived metrics
gh = df.dropna(subset=["Followers", "Repos"]).copy()
gh = gh[gh["Followers"] > 0].copy()
gh["log_followers"] = np.log10(gh["Followers"].clip(lower=1))
gh["log_repos"] = np.log10(gh["Repos"].clip(lower=1))
gh["influence_score"] = (gh["log_followers"] * 0.7 + gh["log_repos"] * 0.3).round(2)
gh["followers_per_repo"] = (gh["Followers"] / gh["Repos"].clip(lower=1)).round(0)

OUT = "D:/Antigravity/awesome-awesomers/plots"
import os; os.makedirs(OUT, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════════
# NATURE / CELL REPORTS STYLE
# ═══════════════════════════════════════════════════════════════════════════════
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#222222",
    "axes.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": "#555555",
    "ytick.color": "#555555",
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
    "text.color": "#222222",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.labelsize": 9.5,
    "legend.fontsize": 8,
    "legend.frameon": False,
    "grid.color": "#e0e0e0",
    "grid.linewidth": 0.4,
    "grid.alpha": 0.7,
    "figure.dpi": 200,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
})

# Nature-inspired palette (muted, professional)
NATURE_PAL = {
    "AI/ML Leaders":  "#E64B35",   # Nature red
    "AI/ML Research":  "#4DBBD5",  # Cyan
    "AI Educators":    "#00A087",  # Teal
    "Bioinformatics":  "#3C5488",  # Dark blue
    "Data Science":    "#F39B7F",  # Salmon
    "Pharma/Policy":   "#8491B4",  # Slate
    "Other":           "#B09C85",  # Warm grey
}
CAT_ORDER = list(NATURE_PAL.keys())

def nature_label(ax, label, x=-0.02, y=1.06, fontsize=14):
    """Add panel label like Nature figures (a, b, c...)"""
    ax.text(x, y, label, transform=ax.transAxes,
            fontsize=fontsize, fontweight="bold", va="top", ha="right",
            fontfamily="Arial")


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — Multi-panel overview (2x2)
# ═══════════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(10, 8.5))
gs = GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.35)

# ── Panel a: Category composition (horizontal lollipop) ──
ax_a = fig.add_subplot(gs[0, 0])
nature_label(ax_a, "a")

cat_counts = df["Category"].value_counts().reindex(CAT_ORDER)
y_pos = np.arange(len(cat_counts))
colors_a = [NATURE_PAL[c] for c in cat_counts.index]

ax_a.hlines(y_pos, 0, cat_counts.values, color=colors_a, linewidth=2, zorder=2)
ax_a.scatter(cat_counts.values, y_pos, c=colors_a, s=60, zorder=3, edgecolors="white", linewidth=0.8)

for i, (v, c) in enumerate(zip(cat_counts.values, cat_counts.index)):
    ax_a.text(v + 0.4, i, f"n={v}", va="center", fontsize=7.5, color="#555555")

ax_a.set_yticks(y_pos)
ax_a.set_yticklabels(cat_counts.index, fontsize=8)
ax_a.set_xlabel("Number of individuals")
ax_a.set_title("Composition by domain", fontweight="bold", pad=8)
ax_a.invert_yaxis()
ax_a.set_xlim(0, cat_counts.max() + 4)

# ── Panel b: Source composition (donut + stacked) ──
ax_b = fig.add_subplot(gs[0, 1])
nature_label(ax_b, "b")

# Donut chart
source_c = df["Source"].value_counts()
wedges, texts, autotexts = ax_b.pie(
    source_c, labels=None,
    autopct=lambda p: f"{p:.0f}%",
    colors=["#3C5488", "#E64B35"],
    startangle=90,
    wedgeprops=dict(width=0.45, edgecolor="white", linewidth=1.5),
    pctdistance=0.76,
    textprops={"fontsize": 9, "color": "#333"}
)
ax_b.legend(["Seed (LinkedIn/Web)", "Graph expansion (GitHub)"],
            loc="lower center", bbox_to_anchor=(0.5, -0.08), fontsize=7.5, ncol=1)
ax_b.set_title("Discovery source", fontweight="bold", pad=8)

# ── Panel c: GitHub digital footprint (violin-like strip) ──
ax_c = fig.add_subplot(gs[1, 0])
nature_label(ax_c, "c")

cats_with_gh = [c for c in CAT_ORDER if c in gh["Category"].values]
positions = []
for i, cat in enumerate(cats_with_gh):
    sub = gh[gh["Category"] == cat]["log_followers"]
    jitter = np.random.default_rng(42).normal(0, 0.08, len(sub))
    ax_c.scatter(sub, np.full(len(sub), i) + jitter,
                 c=NATURE_PAL[cat], s=35, alpha=0.8,
                 edgecolors="white", linewidth=0.4, zorder=3)
    # Add median line
    med = sub.median()
    ax_c.plot([med, med], [i - 0.25, i + 0.25], color=NATURE_PAL[cat],
              linewidth=2.5, zorder=4, solid_capstyle="round")
    positions.append(i)

ax_c.set_yticks(positions)
ax_c.set_yticklabels(cats_with_gh, fontsize=7.5)
ax_c.set_xlabel("log₁₀(GitHub followers)")
ax_c.set_title("Follower distribution by domain", fontweight="bold", pad=8)
ax_c.invert_yaxis()
ax_c.grid(axis="x", linestyle="--", alpha=0.4)

# ── Panel d: Seed vs Graph per category (stacked percent) ──
ax_d = fig.add_subplot(gs[1, 1])
nature_label(ax_d, "d")

pivot = df.groupby(["Category", "Source"]).size().unstack(fill_value=0).reindex(CAT_ORDER)
pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

y_pos_d = np.arange(len(pivot_pct))
seed_vals = pivot_pct.get("S", pd.Series(0, index=pivot_pct.index)).values
graph_vals = pivot_pct.get("G", pd.Series(0, index=pivot_pct.index)).values

ax_d.barh(y_pos_d, seed_vals, height=0.6, color="#3C5488", label="Seed", edgecolor="white", linewidth=0.5)
ax_d.barh(y_pos_d, graph_vals, height=0.6, left=seed_vals, color="#E64B35", label="Graph", edgecolor="white", linewidth=0.5)

ax_d.set_yticks(y_pos_d)
ax_d.set_yticklabels(pivot_pct.index, fontsize=7.5)
ax_d.set_xlabel("Proportion (%)")
ax_d.set_title("Discovery method by domain", fontweight="bold", pad=8)
ax_d.invert_yaxis()
ax_d.legend(loc="lower right", fontsize=7.5)
ax_d.set_xlim(0, 105)

fig.suptitle("Awesome Awesomers — Landscape Overview", fontsize=13, fontweight="bold", y=1.01)
plt.savefig(f"{OUT}/fig1_overview.png")
plt.savefig(f"{OUT}/fig1_overview.pdf")
plt.close()
print("[OK] Figure 1: Multi-panel overview")


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Influence landscape (scatter + marginals)
# ═══════════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(8, 7.5))
gs2 = GridSpec(2, 2, figure=fig, width_ratios=[4, 1], height_ratios=[1, 4],
               hspace=0.05, wspace=0.05)

ax_main = fig.add_subplot(gs2[1, 0])
ax_top = fig.add_subplot(gs2[0, 0], sharex=ax_main)
ax_right = fig.add_subplot(gs2[1, 1], sharey=ax_main)

# Main scatter
for cat in CAT_ORDER:
    sub = gh[gh["Category"] == cat]
    if len(sub) == 0:
        continue
    ax_main.scatter(sub["log_repos"], sub["log_followers"],
                    c=NATURE_PAL[cat], label=cat, s=sub["influence_score"] * 18,
                    alpha=0.85, edgecolors="#333333", linewidth=0.3, zorder=3)

# Label top individuals
from adjustText import adjust_text
top_label = gh.nlargest(15, "Followers")
texts = []
for _, row in top_label.iterrows():
    short = row["Name"].split()[-1]
    if row["Name"] == "Ming Tommy Tang":
        short = "Tang"
    elif row["Name"] == "Laurens van der Maaten":
        short = "vd Maaten"
    t = ax_main.text(row["log_repos"], row["log_followers"], short,
                     fontsize=6.5, color="#333", alpha=0.9, style="italic")
    texts.append(t)
adjust_text(texts, ax=ax_main, arrowprops=dict(arrowstyle="-", color="#aaa", lw=0.4))

# Regression line
slope, intercept, r, p, se = sp_stats.linregress(gh["log_repos"], gh["log_followers"])
x_line = np.linspace(gh["log_repos"].min(), gh["log_repos"].max(), 100)
ax_main.plot(x_line, slope * x_line + intercept, "--", color="#999999", linewidth=1, alpha=0.7, zorder=1)
ax_main.text(0.02, 0.97, f"r = {r:.2f}, p = {p:.1e}",
             transform=ax_main.transAxes, fontsize=7.5, va="top", color="#666666")

ax_main.set_xlabel("log₁₀(public repositories)")
ax_main.set_ylabel("log₁₀(GitHub followers)")
ax_main.grid(True, linestyle="--", alpha=0.3)
ax_main.legend(loc="lower right", fontsize=6.5, markerscale=0.7, handletextpad=0.3)

# Top marginal histogram
ax_top.hist(gh["log_repos"], bins=15, color="#888888", edgecolor="white", linewidth=0.5, alpha=0.6)
ax_top.set_ylabel("Count", fontsize=7)
ax_top.tick_params(labelbottom=False)
ax_top.spines["bottom"].set_visible(False)
nature_label(ax_top, "a", x=-0.02, y=1.15)

# Right marginal histogram
ax_right.hist(gh["log_followers"], bins=15, orientation="horizontal",
              color="#888888", edgecolor="white", linewidth=0.5, alpha=0.6)
ax_right.set_xlabel("Count", fontsize=7)
ax_right.tick_params(labelleft=False)
ax_right.spines["left"].set_visible(False)

fig.suptitle("Influence Landscape — Repositories vs. Followers", fontsize=12, fontweight="bold", y=0.98)
plt.savefig(f"{OUT}/fig2_influence_landscape.png")
plt.savefig(f"{OUT}/fig2_influence_landscape.pdf")
plt.close()
print("[OK] Figure 2: Influence landscape with marginals")


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — Network graph (who-follows-whom)
# ═══════════════════════════════════════════════════════════════════════════════
# Known following edges (from graph expansion data in README)
edges = [
    # rasbt follows:
    ("rasbt", "karpathy"), ("rasbt", "Atcold"), ("rasbt", "biobenkj"),
    ("rasbt", "colah"), ("rasbt", "fchollet"), ("rasbt", "norvig"),
    ("rasbt", "rwightman"), ("rasbt", "mlabonne"), ("rasbt", "srush"),
    ("rasbt", "tridao"), ("rasbt", "cbfinn"), ("rasbt", "lvdmaaten"),
    ("rasbt", "DrJimFan"), ("rasbt", "dpkingma"), ("rasbt", "hadley"),
    ("rasbt", "jakevdp"), ("rasbt", "GaelVaroquaux"),
    # aravindsrinivas follows:
    ("aravindsrinivas", "karpathy"), ("aravindsrinivas", "Atcold"),
    ("aravindsrinivas", "OriolVinyals"), ("aravindsrinivas", "soumith"),
    ("aravindsrinivas", "geohot"),
    # crazyhottommy follows:
    ("crazyhottommy", "lh3"), ("crazyhottommy", "biobenkj"),
    ("crazyhottommy", "shenwei356"), ("crazyhottommy", "lindenb"),
    ("crazyhottommy", "ewels"), ("crazyhottommy", "arq5x"),
    ("crazyhottommy", "thegenemyers"), ("crazyhottommy", "richarddurbin"),
    ("crazyhottommy", "jokergoo"), ("crazyhottommy", "hadley"),
    # nh13 follows:
    ("nh13", "lh3"), ("nh13", "shenwei356"), ("nh13", "lindenb"),
    ("nh13", "ewels"), ("nh13", "arq5x"),
    # Pelayo (seed hub)
    ("biopelayo", "rasbt"), ("biopelayo", "crazyhottommy"),
    ("biopelayo", "aravindsrinivas"), ("biopelayo", "nh13"),
    ("biopelayo", "akosiorek"), ("biopelayo", "saharmor"),
    ("biopelayo", "ylecun"), ("biopelayo", "kozyrkov"),
    ("biopelayo", "AndrewNg"), ("biopelayo", "rafalab"),
    ("biopelayo", "bpucker"), ("biopelayo", "deanslee"),
    ("biopelayo", "VidithPhillips"), ("biopelayo", "pachterlab"),
]

G = nx.DiGraph()
G.add_edges_from(edges)

# Map GitHub usernames to categories
user_cat = dict(zip(gh["GitHub"], gh["Category"]))
user_cat["biopelayo"] = "Curator"
NATURE_PAL_NET = {**NATURE_PAL, "Curator": "#FFD700"}

# Node attributes
in_deg = dict(G.in_degree())
node_sizes = {n: max(80, in_deg.get(n, 0) * 120 + 80) for n in G.nodes()}

fig, ax = plt.subplots(figsize=(10, 9))
nature_label(ax, "", x=-0.01, y=1.03)

# Layout — spring with seed for reproducibility
pos = nx.spring_layout(G, k=1.8, iterations=80, seed=42)

# Draw edges
nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#cccccc", width=0.6,
                       arrows=True, arrowsize=8, arrowstyle="-|>",
                       connectionstyle="arc3,rad=0.1", alpha=0.5)

# Draw nodes by category
for cat, color in NATURE_PAL_NET.items():
    nodes = [n for n in G.nodes() if user_cat.get(n) == cat]
    if not nodes:
        continue
    sizes = [node_sizes[n] for n in nodes]
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=color,
                           node_size=sizes, edgecolors="#333333",
                           linewidths=0.5, alpha=0.9, ax=ax)

# Labels — only for hub nodes (in-degree >= 2 or is biopelayo)
hub_labels = {n: n for n in G.nodes() if in_deg.get(n, 0) >= 2 or n == "biopelayo"}
nx.draw_networkx_labels(G, pos, hub_labels, font_size=7, font_color="#222222",
                        font_weight="bold", ax=ax)

# Minor labels for others
minor_labels = {n: n for n in G.nodes() if n not in hub_labels}
nx.draw_networkx_labels(G, pos, minor_labels, font_size=5.5, font_color="#777777", ax=ax)

# Legend
legend_elements = [Patch(facecolor=c, edgecolor="#333", label=l) for l, c in NATURE_PAL_NET.items()
                   if any(user_cat.get(n) == l for n in G.nodes())]
ax.legend(handles=legend_elements, loc="upper left", fontsize=7.5, title="Domain",
          title_fontsize=8)

ax.set_title("Following Network — Graph Expansion from Seed Awesomers",
             fontsize=12, fontweight="bold", pad=15)
ax.axis("off")

plt.savefig(f"{OUT}/fig3_network.png")
plt.savefig(f"{OUT}/fig3_network.pdf")
plt.close()
print("[OK] Figure 3: Network graph")


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 — Awesomer Score ranking (Cleveland dot plot)
# ═══════════════════════════════════════════════════════════════════════════════
ranked = gh.nlargest(30, "influence_score").sort_values("influence_score", ascending=True).copy()

fig, ax = plt.subplots(figsize=(7, 9))
nature_label(ax, "", x=-0.01, y=1.02)

y_pos = np.arange(len(ranked))
colors = [NATURE_PAL.get(c, "#888") for c in ranked["Category"]]

# Lollipop
ax.hlines(y_pos, 0, ranked["influence_score"], color="#dddddd", linewidth=1, zorder=1)
scatter = ax.scatter(ranked["influence_score"], y_pos, c=colors, s=70, zorder=3,
                     edgecolors="#333333", linewidth=0.5)

# Names and scores
for i, (_, row) in enumerate(ranked.iterrows()):
    ax.text(-0.15, i, row["Name"], va="center", ha="right", fontsize=7.5, color="#333")
    ax.text(row["influence_score"] + 0.08, i,
            f'{row["influence_score"]:.1f}',
            va="center", fontsize=6.5, color="#888888")

ax.set_yticks([])
ax.set_xlabel("Awesomer Influence Score\n(0.7 × log₁₀ followers + 0.3 × log₁₀ repos)")
ax.set_title("Top 30 — Awesomer Influence Score", fontsize=12, fontweight="bold", pad=12)
ax.set_xlim(-0.2, ranked["influence_score"].max() + 0.6)
ax.grid(axis="x", linestyle="--", alpha=0.3)

# Category legend
legend_el = [Line2D([0], [0], marker="o", color="w", markerfacecolor=c,
                    markersize=7, markeredgecolor="#333", markeredgewidth=0.5, label=l)
             for l, c in NATURE_PAL.items() if l in ranked["Category"].values]
ax.legend(handles=legend_el, loc="lower right", fontsize=7, title="Domain", title_fontsize=7.5)

plt.savefig(f"{OUT}/fig4_influence_ranking.png")
plt.savefig(f"{OUT}/fig4_influence_ranking.pdf")
plt.close()
print("[OK] Figure 4: Influence score ranking")


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 5 — Bioinformatics deep-dive (3 panels)
# ═══════════════════════════════════════════════════════════════════════════════
bio = gh[gh["Category"] == "Bioinformatics"].copy()
bio = bio.sort_values("Followers", ascending=True)

fig = plt.figure(figsize=(12, 5))
gs5 = GridSpec(1, 3, figure=fig, wspace=0.4)

# ── Panel a: Followers bar ──
ax5a = fig.add_subplot(gs5[0, 0])
nature_label(ax5a, "a")

bar_colors = ["#E64B35" if s == "S" else "#3C5488" for s in bio["Source"]]
ax5a.barh(np.arange(len(bio)), bio["Followers"], color=bar_colors, height=0.7,
          edgecolor="white", linewidth=0.5)
ax5a.set_yticks(np.arange(len(bio)))
ax5a.set_yticklabels(bio["Name"], fontsize=7)
ax5a.set_xlabel("GitHub followers")
ax5a.set_title("Followers", fontweight="bold", pad=8)
for i, v in enumerate(bio["Followers"]):
    if v > 0:
        ax5a.text(v + 30, i, f"{int(v):,}", va="center", fontsize=6.5, color="#888")
ax5a.legend([Patch(fc="#E64B35"), Patch(fc="#3C5488")], ["Seed", "Graph"],
            fontsize=7, loc="lower right")

# ── Panel b: Repos bar ──
ax5b = fig.add_subplot(gs5[0, 1])
nature_label(ax5b, "b")

ax5b.barh(np.arange(len(bio)), bio["Repos"], color="#3C5488", height=0.7,
          edgecolor="white", linewidth=0.5, alpha=0.7)
ax5b.set_yticks(np.arange(len(bio)))
ax5b.set_yticklabels(bio["Name"], fontsize=7)
ax5b.set_xlabel("Public repositories")
ax5b.set_title("Productivity", fontweight="bold", pad=8)

# ── Panel c: Followers per repo (efficiency) ──
ax5c = fig.add_subplot(gs5[0, 2])
nature_label(ax5c, "c")

bio_eff = bio.copy()
bio_eff["eff"] = (bio_eff["Followers"] / bio_eff["Repos"].clip(lower=1)).round(1)
bio_eff = bio_eff.sort_values("eff", ascending=True)

ax5c.barh(np.arange(len(bio_eff)), bio_eff["eff"], color="#00A087", height=0.7,
          edgecolor="white", linewidth=0.5)
ax5c.set_yticks(np.arange(len(bio_eff)))
ax5c.set_yticklabels(bio_eff["Name"], fontsize=7)
ax5c.set_xlabel("Followers per repository")
ax5c.set_title("Efficiency", fontweight="bold", pad=8)

fig.suptitle("Bioinformatics Awesomers — Deep Dive", fontsize=12, fontweight="bold", y=1.02)
plt.savefig(f"{OUT}/fig5_bioinformatics.png")
plt.savefig(f"{OUT}/fig5_bioinformatics.pdf")
plt.close()
print("[OK] Figure 5: Bioinformatics deep-dive")


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 6 — Heatmap: GitHub presence × category metrics
# ═══════════════════════════════════════════════════════════════════════════════
import matplotlib.colors as mcolors

metrics_df = df.groupby("Category").agg(
    n=("Name", "count"),
    github_pct=("GitHub", lambda x: x.notna().mean() * 100),
    median_followers=("Followers", "median"),
    median_repos=("Repos", "median"),
    max_followers=("Followers", "max"),
    total_repos=("Repos", "sum"),
).reindex(CAT_ORDER)

# Normalize for heatmap (0-1 per column)
norm_df = metrics_df.copy()
for col in norm_df.columns:
    cmin, cmax = norm_df[col].min(), norm_df[col].max()
    if cmax > cmin:
        norm_df[col] = (norm_df[col] - cmin) / (cmax - cmin)
    else:
        norm_df[col] = 0

fig, ax = plt.subplots(figsize=(8, 5))
nature_label(ax, "", x=-0.01, y=1.05)

# Custom colormap (white -> Nature blue)
cmap = mcolors.LinearSegmentedColormap.from_list("nature_blue",
    ["#ffffff", "#b3cde3", "#3C5488"], N=256)

im = ax.imshow(norm_df.values, aspect="auto", cmap=cmap, vmin=0, vmax=1)

# Annotate with actual values
col_labels = ["n", "GitHub %", "Med.\nfollowers", "Med.\nrepos", "Max\nfollowers", "Total\nrepos"]
for i in range(len(metrics_df)):
    for j in range(len(metrics_df.columns)):
        val = metrics_df.iloc[i, j]
        if pd.isna(val):
            txt = "—"
        elif j == 1:  # percentage
            txt = f"{val:.0f}%"
        elif val >= 1000:
            txt = f"{val/1000:.1f}k"
        else:
            txt = f"{val:.0f}"
        text_col = "white" if norm_df.iloc[i, j] > 0.65 else "#333333"
        ax.text(j, i, txt, ha="center", va="center", fontsize=8, color=text_col, fontweight="bold")

ax.set_xticks(np.arange(len(col_labels)))
ax.set_xticklabels(col_labels, fontsize=8)
ax.set_yticks(np.arange(len(metrics_df)))
ax.set_yticklabels(metrics_df.index, fontsize=8)
ax.set_title("Domain Characterization Matrix", fontsize=12, fontweight="bold", pad=12)

# Colorbar
cbar = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.04)
cbar.set_label("Relative intensity", fontsize=8)
cbar.ax.tick_params(labelsize=7)

plt.savefig(f"{OUT}/fig6_heatmap.png")
plt.savefig(f"{OUT}/fig6_heatmap.pdf")
plt.close()
print("[OK] Figure 6: Domain heatmap")


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 7 — Composite: Awesomer archetype quadrants
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 7))

# Quadrant thresholds
med_repos = gh["log_repos"].median()
med_follow = gh["log_followers"].median()

# Background quadrant shading
ax.axhline(med_follow, color="#cccccc", linewidth=0.8, linestyle="-", zorder=0)
ax.axvline(med_repos, color="#cccccc", linewidth=0.8, linestyle="-", zorder=0)

# Quadrant labels
quad_style = dict(fontsize=8, color="#aaaaaa", fontstyle="italic", alpha=0.8)
ax.text(0.25, 0.97, "FOCUSED EXPERT\nfew repos, high influence", transform=ax.transAxes,
        ha="center", va="top", **quad_style)
ax.text(0.78, 0.97, "PROLIFIC LEADER\nmany repos, high influence", transform=ax.transAxes,
        ha="center", va="top", **quad_style)
ax.text(0.25, 0.04, "EMERGING\nfew repos, building audience", transform=ax.transAxes,
        ha="center", va="bottom", **quad_style)
ax.text(0.78, 0.04, "PROLIFIC BUILDER\nmany repos, growing audience", transform=ax.transAxes,
        ha="center", va="bottom", **quad_style)

for cat in CAT_ORDER:
    sub = gh[gh["Category"] == cat]
    if len(sub) == 0:
        continue
    ax.scatter(sub["log_repos"], sub["log_followers"],
               c=NATURE_PAL[cat], label=cat, s=55, alpha=0.85,
               edgecolors="#333333", linewidth=0.4, zorder=3)

# Label the 20 most influential
top20 = gh.nlargest(20, "influence_score")
texts2 = []
for _, row in top20.iterrows():
    short = row["Name"].split()[-1]
    if "Tommy" in row["Name"]:
        short = "Tang"
    elif "van der" in row["Name"]:
        short = "vd Maaten"
    t = ax.text(row["log_repos"], row["log_followers"], short,
                fontsize=6, color="#444", style="italic")
    texts2.append(t)
adjust_text(texts2, ax=ax, arrowprops=dict(arrowstyle="-", color="#bbb", lw=0.3))

ax.set_xlabel("log₁₀(public repositories)")
ax.set_ylabel("log₁₀(GitHub followers)")
ax.set_title("Awesomer Archetype Quadrants", fontsize=12, fontweight="bold", pad=12)
ax.legend(loc="upper left", fontsize=6.5, markerscale=0.8)
ax.grid(True, linestyle="--", alpha=0.2)

plt.savefig(f"{OUT}/fig7_quadrants.png")
plt.savefig(f"{OUT}/fig7_quadrants.pdf")
plt.close()
print("[OK] Figure 7: Archetype quadrants")


# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY TABLES (printed)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("SUMMARY TABLES")
print("=" * 80)

print("\nTable 1: Domain metrics")
print(metrics_df.to_string())

print("\nTable 2: Top 15 by Awesomer Score")
top15 = gh.nlargest(15, "influence_score")[["Name", "Category", "GitHub", "Followers", "Repos", "influence_score", "Source"]]
print(top15.to_string(index=False))

print("\nTable 3: Network centrality (in-degree)")
in_deg_sorted = sorted(in_deg.items(), key=lambda x: x[1], reverse=True)[:15]
for user, deg in in_deg_sorted:
    cat = user_cat.get(user, "?")
    print(f"  {user:25s}  in-degree={deg:2d}  domain={cat}")

print(f"\nTotal awesomers: {len(df)}")
print(f"With GitHub: {df['GitHub'].notna().sum()} | Without: {df['GitHub'].isna().sum()}")
print(f"Seed: {(df['Source']=='S').sum()} | Graph: {(df['Source']=='G').sum()}")
print(f"\nAll figures saved to: {OUT}/")
print("Formats: PNG (300 dpi) + PDF (vector)")
