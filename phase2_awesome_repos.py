"""
Awesome Awesomers -- Phase 2: Awesome Repo Ecosystem Analysis
==============================================================
Scrapes awesome-* repos, profiles their creators, cross-references
with Phase 1 awesomers, and generates publication-quality figures.
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
import networkx as nx
from adjustText import adjust_text
import warnings, os
warnings.filterwarnings("ignore")

# ============================================================================
# DATA: Top awesome-* repositories (>10k stars = quality threshold)
# ============================================================================
repos = [
    # repo_name, stars, owner, domain
    ("sindresorhus/awesome", 446321, "sindresorhus", "Meta"),
    ("vinta/awesome-python", 287627, "vinta", "Python"),
    ("awesome-selfhosted/awesome-selfhosted", 280577, "awesome-selfhosted", "DevOps"),
    ("avelino/awesome-go", 167575, "avelino", "Go"),
    ("f/prompts.chat", 153073, "f", "AI/LLM"),
    ("Hack-with-Github/Awesome-Hacking", 108545, "Hack-with-Github", "Security"),
    ("Shubhamsaboo/awesome-llm-apps", 102569, "Shubhamsaboo", "AI/LLM"),
    ("jaywcjlove/awesome-mac", 100350, "jaywcjlove", "Tools"),
    ("MunGell/awesome-for-beginners", 83600, "MunGell", "Education"),
    ("punkpeye/awesome-mcp-servers", 83354, "punkpeye", "AI/LLM"),
    ("DopplerHQ/awesome-interview-questions", 81471, "DopplerHQ", "Career"),
    ("fighting41love/funNLP", 79457, "fighting41love", "NLP"),
    ("FortAwesome/Font-Awesome", 76423, "FortAwesome", "Frontend"),
    ("vuejs/awesome-vue", 73619, "vuejs", "Frontend"),
    ("awesomedata/awesome-public-datasets", 73456, "awesomedata", "Data"),
    ("enaqx/awesome-react", 72411, "enaqx", "Frontend"),
    ("josephmisiti/awesome-machine-learning", 72015, "josephmisiti", "ML"),
    ("fffaraz/awesome-cpp", 70274, "fffaraz", "C++"),
    ("binhnguyennus/awesome-scalability", 69464, "binhnguyennus", "Architecture"),
    ("prakhar1989/awesome-courses", 67078, "prakhar1989", "Education"),
    ("sindresorhus/awesome-nodejs", 65315, "sindresorhus", "Node.js"),
    ("Solido/awesome-flutter", 59299, "Solido", "Mobile"),
    ("PlexPt/awesome-chatgpt-prompts-zh", 58751, "PlexPt", "AI/LLM"),
    ("rust-unofficial/awesome-rust", 56196, "rust-unofficial", "Rust"),
    ("ashishps1/awesome-system-design-resources", 35215, "ashishps1", "Architecture"),
    ("kuchin/awesome-cto", 34521, "kuchin", "Leadership"),
    ("bayandin/awesome-awesomeness", 33283, "bayandin", "Meta"),
    ("awesome-foss/awesome-sysadmin", 33238, "awesome-foss", "DevOps"),
    ("ChristosChristofidis/awesome-deep-learning", 27711, "ChristosChristofidis", "DL"),
    ("terryum/awesome-deep-learning-papers", 26095, "terryum", "DL"),
    ("danielecook/Awesome-Bioinformatics", 3900, "danielecook", "Bioinformatics"),
    ("gokceneraslan/awesome-deepbio", 1968, "gokceneraslan", "Bioinformatics"),
    ("OmicsML/awesome-deep-learning-single-cell-papers", 841, "OmicsML", "Bioinformatics"),
]

repos_df = pd.DataFrame(repos, columns=["Repo", "Stars", "Owner", "Domain"])

# ============================================================================
# DATA: Awesome curators (the people behind the repos)
# ============================================================================
curators = [
    # name, github, followers, repos, total_stars, bio, top_awesome_repo, top_stars
    ("Sindre Sorhus", "sindresorhus", 77926, 1133, 576262, "Full-Time Open-Sourcerer", "awesome", 446321),
    ("Vinta Chen", "vinta", 9112, 28, 294451, "Developer", "awesome-python", 287627),
    ("Avelino", "avelino", 6268, 241, 168666, "CTO buserbrasil", "awesome-go", 167575),
    ("Shubham Saboo", "Shubhamsaboo", 7612, 164, 103434, "Sr AI PM Google Cloud", "awesome-llm-apps", 102569),
    ("Ashish P. Singh", "ashishps1", 12684, 42, 88775, "AlgoMaster, ex-Amazon", "awesome-system-design", 35215),
    ("Frank Fiegel", "punkpeye", 1721, 4826, 12, "Engineer turned founder", "awesome-mcp-servers", 83354),
    ("Kenny Wong", "jaywcjlove", 9005, 211, 0, "Fullstack, Shanghai", "awesome-mac", 100350),
    ("Joseph Misiti", "josephmisiti", 4430, 291, 72346, "Co-founder PingIntel", "awesome-machine-learning", 72015),
    ("Shmavon Gazanchyan", "MunGell", 2302, 137, 0, "Developer", "awesome-for-beginners", 83600),
    ("J. Le Coupanec", "LeCoupa", 2774, 20, 0, "JS/TS Developer", "awesome-cheatsheets", 45493),
    ("PatrickJS", "PatrickJS", 3507, 961, 0, "Engineering Director", "awesome-cursorrules", 38529),
    ("Alexander Bayandin", "bayandin", 720, 27, 0, "Developer", "awesome-awesomeness", 33283),
    ("Dima Kuchin", "kuchin", 635, 13, 0, "Full Stack CTO", "awesome-cto", 34521),
    ("Chris Christofidis", "ChristosChristofidis", 1351, 140, 28047, "Developer", "awesome-deep-learning", 27711),
    ("Terry T. Um", "terryum", 1486, 7, 0, "AI & robotics researcher", "awesome-deep-learning-papers", 26095),
    ("Daniel Cook", "danielecook", 415, 76, 4259, "Bioinformatician", "Awesome-Bioinformatics", 3900),
    ("Gokcen Eraslan", "gokceneraslan", 483, 101, 0, "ML & genomics", "awesome-deepbio", 1968),
    ("Lukas Masuch", "lukasmasuch", 1361, 72, 0, "Developer", "best-of-ml-python", 23320),
    ("Patrick Hall", "jphall663", 743, 39, 0, "AI risk, GWU prof", "awesome-ml-interpretability", 3997),
    ("Lukasz Madon", "lukasz-madon", 667, 59, 0, "Python developer", "awesome-remote-job", 44102),
    ("Julien Bisconti", "veggiemonk", 680, 182, 0, "Developer", "awesome-docker", 35692),
]

cur_df = pd.DataFrame(curators, columns=["Name","GitHub","Followers","Repos","TotalStars",
                                          "Bio","TopAwesome","TopStars"])

# Derived
cur_df["log_f"] = np.log10(cur_df["Followers"].clip(lower=1))
cur_df["log_top"] = np.log10(cur_df["TopStars"].clip(lower=1))
cur_df["log_r"] = np.log10(cur_df["Repos"].clip(lower=1))
cur_df["curator_score"] = (cur_df["log_top"]*0.50 + cur_df["log_f"]*0.30 + cur_df["log_r"]*0.20).round(2)

# ============================================================================
# Phase 1 awesomers for cross-reference
# ============================================================================
p1_names = {
    "karpathy","rasbt","hadley","geohot","fchollet","soumith","colah","norvig",
    "rwightman","mlabonne","lh3","srush","crazyhottommy","Atcold","GaelVaroquaux",
    "tridao","cbfinn","lvdmaaten","rafalab","shenwei356","ylecun","theislab",
    "kozyrkov","DrJimFan","ewels","arq5x","dpkingma","lindenb","thegenemyers",
    "richarddurbin","akosiorek","nh13","pachterlab","bpucker","saharmor",
    "biobenkj","deanslee","OriolVinyals","jakevdp"
}

# Check overlap
overlap = set(cur_df["GitHub"]) & p1_names
cur_df["in_phase1"] = cur_df["GitHub"].isin(p1_names)

OUT = "D:/Antigravity/awesome-awesomers/plots"
os.makedirs(OUT, exist_ok=True)

# ============================================================================
# STYLE
# ============================================================================
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#2b2b2b",
    "axes.labelcolor": "#1a1a1a",
    "axes.linewidth": 0.7,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": "#444",
    "ytick.color": "#444",
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
    "text.color": "#1a1a1a",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial"],
    "font.size": 8,
    "axes.titlesize": 10,
    "axes.labelsize": 8.5,
    "legend.fontsize": 7,
    "legend.frameon": False,
    "grid.color": "#e8e8e8",
    "grid.linewidth": 0.35,
    "figure.dpi": 200,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.08,
})

# Domain palette
DOM_C = {
    "AI/LLM": "#E64B35", "ML": "#E64B35", "DL": "#E64B35", "NLP": "#E64B35",
    "Python": "#3572A5", "Go": "#00ADD8", "C++": "#f34b7d", "Rust": "#dea584",
    "Node.js": "#68A063", "Frontend": "#4DBBD5", "Mobile": "#00A087",
    "DevOps": "#8491B4", "Security": "#B09C85", "Architecture": "#F39B7F",
    "Data": "#3C5488", "Education": "#00A087", "Career": "#8491B4",
    "Tools": "#666", "Meta": "#FFD700", "Leadership": "#F39B7F",
    "Bioinformatics": "#3C5488",
}

def fmt_k(v):
    if v >= 1e6: return f"{v/1e6:.1f}M"
    if v >= 1000: return f"{v/1000:.0f}k" if v >= 10000 else f"{v/1000:.1f}k"
    return f"{int(v)}"

def short_name(n):
    parts = n.split()
    if len(parts) >= 2: return f"{parts[0][0]}. {parts[-1]}"
    return n

def plabel(ax, letter, x=-0.08, y=1.04):
    ax.text(x, y, letter, transform=ax.transAxes, fontsize=12,
            fontweight="bold", va="top", ha="left", fontfamily="Arial")


# ============================================================================
# FIGURE P2-1: Top awesome repos + domain breakdown
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 6),
    gridspec_kw={"width_ratios": [2, 1], "wspace": 0.45})

# Panel a: Top 25 repos
plabel(ax1, "a")
top25 = repos_df.nlargest(25, "Stars").sort_values("Stars", ascending=True).copy()
y = np.arange(len(top25))
colors = [DOM_C.get(d, "#aaa") for d in top25["Domain"]]

ax1.barh(y, top25["Stars"], height=0.62, color=colors, edgecolor="white", linewidth=0.4)
ax1.set_yticks(y)
labels = [r.split("/")[1][:28] for r in top25["Repo"]]
ax1.set_yticklabels(labels, fontsize=5.5, fontfamily="monospace")
ax1.set_xlabel("GitHub stars")
ax1.set_title("Top 25 awesome-* repositories", fontweight="bold", loc="left", pad=4)
ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: fmt_k(x)))

for i, v in enumerate(top25["Stars"]):
    ax1.text(v + 2000, i, fmt_k(v), va="center", fontsize=5, color="#888")

# Panel b: Domain breakdown
plabel(ax2, "b")
dom_counts = repos_df["Domain"].value_counts().sort_values()
y2 = np.arange(len(dom_counts))
colors2 = [DOM_C.get(d, "#aaa") for d in dom_counts.index]

ax2.barh(y2, dom_counts.values, height=0.55, color=colors2, edgecolor="white", linewidth=0.4)
ax2.set_yticks(y2)
ax2.set_yticklabels(dom_counts.index, fontsize=7)
ax2.set_xlabel("Repos (n)")
ax2.set_title("Domain distribution", fontweight="bold", loc="left", pad=4)

for i, v in enumerate(dom_counts.values):
    ax2.text(v + 0.1, i, str(v), va="center", fontsize=6.5, fontweight="bold", color=colors2[i])

plt.savefig(f"{OUT}/Fig_P2_1_repos.png")
plt.savefig(f"{OUT}/Fig_P2_1_repos.pdf")
plt.close()
print("[OK] P2 Fig 1: Top repos")


# ============================================================================
# FIGURE P2-2: Curator ranking + score decomposition
# ============================================================================
ranked = cur_df.sort_values("curator_score", ascending=True).copy()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 6.5),
    gridspec_kw={"width_ratios": [1.5, 1], "wspace": 0.50})

# Panel a: Curator score ranking
plabel(ax1, "a", x=-0.12)
y = np.arange(len(ranked))

ax1.hlines(y, 0, ranked["curator_score"], color="#e0e0e0", linewidth=0.7, zorder=1)
ax1.scatter(ranked["curator_score"], y, c="#E64B35", s=40, zorder=3,
            edgecolors="#333", linewidth=0.35)

for i, (_, row) in enumerate(ranked.iterrows()):
    label = f'{short_name(row["Name"])} ({row["GitHub"]})'
    ax1.text(-0.06, i, label, va="center", ha="right", fontsize=5.5)
    ax1.text(row["curator_score"] + 0.04, i, f'{row["curator_score"]:.1f}',
             va="center", fontsize=5, color="#888")

ax1.set_xlabel("Curator Score\n(0.5 log$_{10}$top_repo_stars + 0.3 log$_{10}$followers + 0.2 log$_{10}$repos)")
ax1.set_title("Awesome curators ranking", fontweight="bold", loc="left", pad=4)
ax1.set_yticks([])
ax1.set_xlim(-0.1, ranked["curator_score"].max() + 0.4)
ax1.grid(axis="x", linestyle="--", alpha=0.3)

# Panel b: Top repo stars vs personal followers
plabel(ax2, "b", x=-0.12)

ax2.scatter(cur_df["log_f"], cur_df["log_top"], c="#3C5488", s=40, alpha=0.85,
            edgecolors="#333", linewidth=0.3, zorder=3)

texts = []
for _, row in cur_df.iterrows():
    sn = row["GitHub"]
    if len(sn) > 12: sn = sn[:11] + "."
    t = ax2.text(row["log_f"], row["log_top"], sn, fontsize=5, color="#444", style="italic")
    texts.append(t)
adjust_text(texts, ax=ax2, arrowprops=dict(arrowstyle="-", color="#ccc", lw=0.25))

ax2.set_xlabel("Personal followers (log$_{10}$)")
ax2.set_ylabel("Top awesome repo stars (log$_{10}$)")
ax2.set_title("Personal vs. project influence", fontweight="bold", loc="left", pad=4)
ax2.grid(True, linestyle="--", alpha=0.25)

# Diagonal reference
lim = [min(ax2.get_xlim()[0], ax2.get_ylim()[0]), max(ax2.get_xlim()[1], ax2.get_ylim()[1])]
ax2.plot(lim, lim, "--", color="#ddd", lw=0.6, zorder=0)
ax2.text(0.05, 0.92, "Above line = repo\noutgrew creator", transform=ax2.transAxes,
         fontsize=5, color="#bbb", fontstyle="italic")

plt.savefig(f"{OUT}/Fig_P2_2_curators.png")
plt.savefig(f"{OUT}/Fig_P2_2_curators.pdf")
plt.close()
print("[OK] P2 Fig 2: Curator ranking")


# ============================================================================
# FIGURE P2-3: Stars power law + bioinformatics comparison
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 4.2),
    gridspec_kw={"wspace": 0.35})

# Panel a: Stars distribution (power law)
plabel(ax1, "a")
sorted_stars = repos_df["Stars"].sort_values(ascending=False).values
rank = np.arange(1, len(sorted_stars) + 1)

ax1.scatter(rank, sorted_stars, c="#E64B35", s=30, alpha=0.8, edgecolors="#333", linewidth=0.3, zorder=3)
ax1.set_yscale("log")
ax1.set_xlabel("Rank")
ax1.set_ylabel("Stars (log scale)")
ax1.set_title("Power law in awesome-* repos", fontweight="bold", loc="left", pad=4)
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: fmt_k(x)))
ax1.grid(True, linestyle="--", alpha=0.25)

# Annotate top 3 and bioinformatics
for i, row in repos_df.nlargest(3, "Stars").iterrows():
    r = np.where(sorted_stars == row["Stars"])[0][0] + 1
    ax1.annotate(row["Repo"].split("/")[1][:20], (r, row["Stars"]),
                 fontsize=5, color="#444", style="italic",
                 xytext=(5, 5), textcoords="offset points")

# Mark bioinformatics
bio_repos = repos_df[repos_df["Domain"] == "Bioinformatics"]
for _, row in bio_repos.iterrows():
    r = np.where(sorted_stars == row["Stars"])[0][0] + 1
    ax1.scatter(r, row["Stars"], c="#3C5488", s=50, zorder=4, edgecolors="#333", linewidth=0.5)
    ax1.annotate(row["Repo"].split("/")[1][:25], (r, row["Stars"]),
                 fontsize=5, color="#3C5488", fontweight="bold",
                 xytext=(5, -8), textcoords="offset points")

ax1.legend([Line2D([0],[0],marker="o",color="w",markerfacecolor="#E64B35",markersize=5),
            Line2D([0],[0],marker="o",color="w",markerfacecolor="#3C5488",markersize=5)],
           ["General", "Bioinformatics"], fontsize=6, loc="upper right")

# Panel b: Bioinformatics awesome repos zoom
plabel(ax2, "b")

bio_search = [
    ("Awesome-Bioinformatics", 3900, "danielecook"),
    ("awesome-deepbio", 1968, "gokceneraslan"),
    ("awesome-dl-single-cell", 841, "OmicsML"),
    ("awesome-bioinfo-benchmarks", 355, "j-andrews7"),
    ("awesome-bioinfo-education", 102, "lskatz"),
    ("awesome-bioinfo-formats", 54, "kmhernan"),
    ("awesome-bioinfo-jobs", 54, "lskatz"),
    ("awesome-bioinformatics", 45, "WooGenome"),
    ("awesome-awesomeness-bioinfo", 43, "Juke34"),
]
bio_df = pd.DataFrame(bio_search, columns=["Repo", "Stars", "Owner"])
bio_df = bio_df.sort_values("Stars", ascending=True)

y_b = np.arange(len(bio_df))
ax2.barh(y_b, bio_df["Stars"], height=0.55, color="#3C5488", edgecolor="white", linewidth=0.4)
ax2.set_yticks(y_b)
ax2.set_yticklabels(bio_df["Repo"], fontsize=5.5, fontfamily="monospace")
ax2.set_xlabel("Stars")
ax2.set_title("Bioinformatics awesome-* repos", fontweight="bold", loc="left", pad=4)

for i, (_, row) in enumerate(bio_df.iterrows()):
    ax2.text(row["Stars"] + 20, i, f'{fmt_k(row["Stars"])} ({row["Owner"]})',
             va="center", fontsize=5, color="#888")

ax2.axvline(1000, color="#E64B35", lw=0.6, ls="--", alpha=0.4)
ax2.text(1050, 0.5, "quality\nthreshold", fontsize=5, color="#E64B35", alpha=0.6, va="center")

plt.savefig(f"{OUT}/Fig_P2_3_powerlaw.png")
plt.savefig(f"{OUT}/Fig_P2_3_powerlaw.pdf")
plt.close()
print("[OK] P2 Fig 3: Power law + bio zoom")


# ============================================================================
# FIGURE P2-4: Cross-reference network (Phase 1 x Phase 2)
# ============================================================================
fig, ax = plt.subplots(figsize=(7.2, 5.5))

# Build bipartite graph: curators -> their awesome repos -> domain
G = nx.Graph()

for _, row in cur_df.iterrows():
    G.add_node(row["GitHub"], type="curator", score=row["curator_score"])
    repo_node = row["TopAwesome"]
    G.add_node(repo_node, type="repo", stars=row["TopStars"])
    G.add_edge(row["GitHub"], repo_node)

# Layout
pos = nx.spring_layout(G, k=2.5, iterations=80, seed=42)

# Draw edges
nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#ddd", width=0.5, alpha=0.5)

# Draw curator nodes
curator_nodes = [n for n, d in G.nodes(data=True) if d.get("type") == "curator"]
curator_sizes = [max(30, G.nodes[n].get("score", 2) * 25) for n in curator_nodes]
curator_colors = ["#FFD700" if n in p1_names else "#E64B35" for n in curator_nodes]

nx.draw_networkx_nodes(G, pos, nodelist=curator_nodes, node_color=curator_colors,
                       node_size=curator_sizes, edgecolors="#333", linewidths=0.4,
                       alpha=0.9, ax=ax)

# Draw repo nodes
repo_nodes = [n for n, d in G.nodes(data=True) if d.get("type") == "repo"]
repo_sizes = [max(20, np.log10(max(G.nodes[n].get("stars", 1), 1)) * 15) for n in repo_nodes]
nx.draw_networkx_nodes(G, pos, nodelist=repo_nodes, node_color="#3C5488",
                       node_size=repo_sizes, edgecolors="#333", linewidths=0.3,
                       alpha=0.6, ax=ax, node_shape="s")

# Labels
labels_cur = {n: n for n in curator_nodes if G.nodes[n].get("score", 0) > 3.5 or n in p1_names}
labels_repo = {n: n for n in repo_nodes if G.nodes[n].get("stars", 0) > 50000}
nx.draw_networkx_labels(G, pos, {**labels_cur, **labels_repo}, font_size=5.5,
                        font_weight="bold", font_color="#333", ax=ax)

# Minor labels
minor = {n: n for n in curator_nodes if n not in labels_cur}
nx.draw_networkx_labels(G, pos, minor, font_size=4, font_color="#999", ax=ax)

ax.legend([Line2D([0],[0],marker="o",color="w",markerfacecolor="#E64B35",markersize=6),
           Line2D([0],[0],marker="o",color="w",markerfacecolor="#FFD700",markersize=6),
           Line2D([0],[0],marker="s",color="w",markerfacecolor="#3C5488",markersize=5)],
          ["New curator (Phase 2)", "Also in Phase 1", "Awesome repo"],
          fontsize=6, loc="upper left")

ax.set_title("Curator-Repository Network", fontweight="bold", loc="left", pad=6, fontsize=10)
ax.axis("off")

plt.savefig(f"{OUT}/Fig_P2_4_cross_network.png")
plt.savefig(f"{OUT}/Fig_P2_4_cross_network.pdf")
plt.close()
print("[OK] P2 Fig 4: Cross-reference network")


# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("PHASE 2 SUMMARY")
print("=" * 80)

print(f"\nTotal awesome-* repos scraped: {len(repos_df)}")
print(f"Stars range: {fmt_k(repos_df['Stars'].min())} - {fmt_k(repos_df['Stars'].max())}")
print(f"Total curators profiled: {len(cur_df)}")
print(f"Overlap with Phase 1: {len(overlap)} ({overlap if overlap else 'none'})")

print("\nTop 10 Curators by Curator Score:")
t = cur_df.nlargest(10, "curator_score")[["Name","GitHub","Followers","TopAwesome","TopStars","curator_score"]]
print(t.to_string(index=False))

print("\nNew candidates for awesome-awesomers (not in Phase 1):")
new = cur_df[~cur_df["in_phase1"]].nlargest(10, "curator_score")
for _, row in new.iterrows():
    print(f"  {row['Name']:25s}  @{row['GitHub']:20s}  score={row['curator_score']:.1f}  "
          f"top_repo={row['TopAwesome']} ({fmt_k(row['TopStars'])} stars)")

print(f"\nBioinformatics awesome repos found: {len(bio_repos)}")
print("Quality threshold (>1k stars): Awesome-Bioinformatics (3.9k), awesome-deepbio (2.0k)")

print(f"\nAll Phase 2 figures saved to: {OUT}/")
