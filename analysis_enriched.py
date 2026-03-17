"""
Awesome Awesomers -- Enriched Analysis v2
==========================================
Publication-quality. Enriched with total stars, top repos, languages, activity.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec
import matplotlib.colors as mcolors
import numpy as np
import networkx as nx
from scipy import stats as sp_stats
from adjustText import adjust_text
from datetime import datetime
import warnings, os
warnings.filterwarnings("ignore")

# ============================================================================
# ENRICHED DATA
# ============================================================================
data = [
    # name, category, github, followers, repos, following, total_stars, top_repo, top_stars, primary_lang, last_push, source, created
    ("Andrej Karpathy","AI/ML Leaders","karpathy",148001,63,8,393395,"nanoGPT",55059,"Python","2026-03-16","G","2010-04"),
    ("George Hotz","AI/ML Leaders","geohot",46135,101,0,23453,"fromthetransistor",6456,"Python","2026-02-25","G","2009-04"),
    ("Sebastian Raschka","AI/ML Research","rasbt",36352,147,41,152172,"LLMs-from-scratch",88460,"Python","2026-03-17","S","2013-10"),
    ("Hadley Wickham","Data Science","hadley",26541,230,0,7131,"adv-r",2454,"R","2026-03-17","G","2008-04"),
    ("Jake Vanderplas","Data Science","jakevdp",19048,239,6,1589,"JSAnimation",240,"Python","2026-03-17","G","2011-05"),
    ("Francois Chollet","AI/ML Leaders","fchollet",17861,16,0,36434,"stable-diffusion-tensorflow",324,"Python","2025-09-18","G","2011-04"),
    ("Soumith Chintala","AI/ML Leaders","soumith",13119,169,419,18439,"mini-sglang",3,"Python","2025-12-18","G","2012-01"),
    ("Christopher Olah","AI/ML Research","colah",9766,52,7,1728,"lucid",9,"TypeScript","2024-04-16","G","2009-03"),
    ("Peter Norvig","AI/ML Leaders","norvig",9726,4,14,0,"--",0,"--","2026-03-17","G","2013-05"),
    ("Ross Wightman","AI/ML Research","rwightman",7002,74,40,5079,"timm",59,"Python","2025-09-09","G","2013-10"),
    ("Maxime Labonne","AI/ML Research","mlabonne",6536,23,25,82837,"--",0,"Python","2026-03-09","G","2021-03"),
    ("Heng Li","Bioinformatics","lh3",4267,138,8,9184,"minimap2",2143,"C","2026-03-15","G","2010-11"),
    ("Sasha Rush","AI/ML Research","srush",3832,165,14,19106,"awesome-o1",1213,"TeX","2026-01-01","G","2008-11"),
    ("Ming Tommy Tang","Bioinformatics","crazyhottommy",3726,177,43,3885,"getting-started-with-genomics-tools-and-resources",1373,"Python","2026-03-15","S","2013-04"),
    ("Alfredo Canziani","AI/ML Research","Atcold",3675,70,4,0,"--",0,"--","2026-03-16","G","2012-08"),
    ("Gael Varoquaux","Data Science","GaelVaroquaux",3393,90,5,606,"--",0,"Python","2026-03-13","G","2010-02"),
    ("Tri Dao","AI/ML Research","tridao",2933,10,3,0,"--",0,"--","2026-02-11","G","2013-10"),
    ("Chelsea Finn","AI/ML Research","cbfinn",2174,25,0,0,"--",0,"--","2011-12-10","G","2011-12"),
    ("Laurens van der Maaten","AI/ML Research","lvdmaaten",1975,23,4,0,"--",0,"--","--","G","2011-11"),
    ("Rafael Irizarry","Bioinformatics","rafalab",1633,49,0,0,"--",0,"R","--","S","--"),
    ("Wei Shen","Bioinformatics","shenwei356",1469,119,290,6116,"--",0,"Go","2026-03-13","G","2012-10"),
    ("Yann LeCun","AI/ML Leaders","ylecun",1509,12,0,0,"--",0,"--","--","S","--"),
    ("Fabian Theis","Data Science","theislab",1400,253,0,0,"--",0,"--","2026-03-17","S","2016-09"),
    ("Cassie Kozyrkov","AI/ML Leaders","kozyrkov",1039,5,0,0,"--",0,"--","--","S","--"),
    ("Jim Fan","AI/ML Research","DrJimFan",934,7,43,0,"--",0,"--","--","G","2012-12"),
    ("Phil Ewels","Bioinformatics","ewels",844,159,31,419,"--",0,"Nextflow","2026-03-17","G","2010-11"),
    ("Aaron Quinlan","Bioinformatics","arq5x",771,75,71,0,"--",0,"--","2026-02-22","G","2009-04"),
    ("Durk Kingma","AI/ML Research","dpkingma",597,9,4,0,"--",0,"--","--","G","2012-09"),
    ("Pierre Lindenbaum","Bioinformatics","lindenb",555,178,81,0,"--",0,"Java","2026-03-14","G","2008-11"),
    ("Eugene Myers","Bioinformatics","thegenemyers",467,19,0,0,"--",0,"C","--","G","2014-03"),
    ("Richard Durbin","Bioinformatics","richarddurbin",380,20,3,0,"--",0,"C","--","G","2013-01"),
    ("Adam Kosiorek","AI/ML Research","akosiorek",375,40,0,0,"--",0,"--","--","S","--"),
    ("Nils Homer","Bioinformatics","nh13",374,207,16,0,"--",0,"--","2026-03-17","S","2011-06"),
    ("Lior Pachter","AI/ML Leaders","pachterlab",377,169,0,0,"--",0,"--","--","S","--"),
    ("Boas Pucker","Bioinformatics","bpucker",187,80,0,0,"--",0,"Python","--","S","--"),
    ("Sahar Mor","AI/ML Research","saharmor",205,86,0,0,"--",0,"--","--","S","--"),
    ("Ben Johnson","Bioinformatics","biobenkj",121,132,0,0,"--",0,"--","--","G","--"),
    ("Dean Lee","Bioinformatics","deanslee",118,2,0,0,"--",0,"--","--","S","--"),
    ("Oriol Vinyals","AI/ML Research","OriolVinyals",84,3,0,0,"--",0,"--","--","G","--"),
]

cols = ["Name","Category","GitHub","Followers","Repos","Following","TotalStars",
        "TopRepo","TopStars","PrimaryLang","LastPush","Source","Created"]
df = pd.DataFrame(data, columns=cols)

# -- Derived metrics --
df["log_followers"] = np.log10(df["Followers"].clip(lower=1))
df["log_repos"] = np.log10(df["Repos"].clip(lower=1))
df["log_stars"] = np.log10(df["TotalStars"].clip(lower=1))
df["stars_per_repo"] = (df["TotalStars"] / df["Repos"].clip(lower=1)).round(0)
df["followers_per_repo"] = (df["Followers"] / df["Repos"].clip(lower=1)).round(0)

# Composite Awesomer Score v2 (followers 40%, total_stars 35%, repos 25%)
df["score_v2"] = (
    df["log_followers"] * 0.40 +
    df["log_stars"] * 0.35 +
    df["log_repos"] * 0.25
).round(2)

# Activity: days since last push
today = datetime(2026, 3, 17)
def days_since(push_str):
    if push_str == "--" or pd.isna(push_str):
        return np.nan
    try:
        d = datetime.strptime(push_str[:10], "%Y-%m-%d")
        return (today - d).days
    except:
        return np.nan

df["days_inactive"] = df["LastPush"].apply(days_since)
df["active"] = df["days_inactive"].apply(lambda x: "Active" if pd.notna(x) and x <= 90 else ("Dormant" if pd.notna(x) else "Unknown"))

OUT = "D:/Antigravity/awesome-awesomers/plots"
os.makedirs(OUT, exist_ok=True)

# ============================================================================
# STYLE -- Nature / Cell Reports
# ============================================================================
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
    "figure.dpi": 200,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

PAL = {
    "AI/ML Leaders": "#E64B35",
    "AI/ML Research": "#4DBBD5",
    "Bioinformatics": "#3C5488",
    "Data Science": "#F39B7F",
}

def panel_label(ax, label, x=-0.02, y=1.06):
    ax.text(x, y, label, transform=ax.transAxes, fontsize=13, fontweight="bold", va="top", ha="right")


# ============================================================================
# FIGURE 1 -- Enriched Influence Score v2 (Top 30 Cleveland dot)
# ============================================================================
top30 = df.nlargest(30, "score_v2").sort_values("score_v2", ascending=True).copy()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 9), gridspec_kw={"width_ratios": [3, 2], "wspace": 0.45})
panel_label(ax1, "a")
panel_label(ax2, "b")

# Panel a: Score ranking
y = np.arange(len(top30))
colors = [PAL.get(c, "#888") for c in top30["Category"]]
ax1.hlines(y, 0, top30["score_v2"], color="#e0e0e0", linewidth=0.8, zorder=1)
ax1.scatter(top30["score_v2"], y, c=colors, s=60, zorder=3, edgecolors="#333", linewidth=0.4)

for i, (_, row) in enumerate(top30.iterrows()):
    ax1.text(-0.08, i, row["Name"], va="center", ha="right", fontsize=7.5)
    ax1.text(row["score_v2"] + 0.05, i, f'{row["score_v2"]:.1f}', va="center", fontsize=6.5, color="#888")

ax1.set_xlabel("Awesomer Score v2\n(0.4 log followers + 0.35 log stars + 0.25 log repos)")
ax1.set_title("Top 30 -- Composite Influence Score", fontweight="bold", pad=10)
ax1.set_yticks([])
ax1.set_xlim(-0.2, top30["score_v2"].max() + 0.5)
ax1.grid(axis="x", linestyle="--", alpha=0.3)

legend_el = [Line2D([0],[0],marker="o",color="w",markerfacecolor=c,markersize=7,
                    markeredgecolor="#333",markeredgewidth=0.4,label=l)
             for l,c in PAL.items() if l in top30["Category"].values]
ax1.legend(handles=legend_el, loc="lower right", fontsize=7, title="Domain", title_fontsize=7.5)

# Panel b: Score decomposition (stacked horizontal bar)
top15 = top30.tail(15).copy()  # top 15 for decomposition
y2 = np.arange(len(top15))
comp_follow = top15["log_followers"] * 0.40
comp_stars = top15["log_stars"] * 0.35
comp_repos = top15["log_repos"] * 0.25

ax2.barh(y2, comp_follow, height=0.6, color="#E64B35", label="Followers (40%)", edgecolor="white", linewidth=0.5)
ax2.barh(y2, comp_stars, height=0.6, left=comp_follow, color="#4DBBD5", label="Stars (35%)", edgecolor="white", linewidth=0.5)
ax2.barh(y2, comp_repos, height=0.6, left=comp_follow + comp_stars, color="#3C5488", label="Repos (25%)", edgecolor="white", linewidth=0.5)

ax2.set_yticks(y2)
ax2.set_yticklabels(top15["Name"], fontsize=7.5)
ax2.set_xlabel("Score components")
ax2.set_title("Score Decomposition (Top 15)", fontweight="bold", pad=10)
ax2.legend(loc="lower right", fontsize=7)

fig.suptitle("Awesome Awesomers -- Enriched Influence Analysis", fontsize=13, fontweight="bold", y=1.01)
plt.savefig(f"{OUT}/fig_e1_score_v2.png")
plt.savefig(f"{OUT}/fig_e1_score_v2.pdf")
plt.close()
print("[OK] Figure E1: Enriched score v2")


# ============================================================================
# FIGURE 2 -- Stars landscape (scatter with bubble size = total stars)
# ============================================================================
has_stars = df[df["TotalStars"] > 0].copy()

fig = plt.figure(figsize=(10, 8))
gs = GridSpec(2, 2, figure=fig, width_ratios=[4,1], height_ratios=[1,4], hspace=0.05, wspace=0.05)

ax_main = fig.add_subplot(gs[1,0])
ax_top = fig.add_subplot(gs[0,0], sharex=ax_main)
ax_right = fig.add_subplot(gs[1,1], sharey=ax_main)

for cat in PAL:
    sub = has_stars[has_stars["Category"] == cat]
    if len(sub) == 0:
        continue
    sizes = np.clip(sub["log_stars"] * 30, 30, 300)
    ax_main.scatter(sub["log_repos"], sub["log_followers"], c=PAL[cat], label=cat,
                    s=sizes, alpha=0.8, edgecolors="#333", linewidth=0.3, zorder=3)

# Labels
texts = []
for _, row in has_stars.nlargest(15, "score_v2").iterrows():
    short = row["Name"].split()[-1]
    if "Tommy" in row["Name"]: short = "Tang"
    elif "van der" in row["Name"]: short = "vd Maaten"
    t = ax_main.text(row["log_repos"], row["log_followers"], short,
                     fontsize=6.5, color="#333", style="italic")
    texts.append(t)
adjust_text(texts, ax=ax_main, arrowprops=dict(arrowstyle="-", color="#bbb", lw=0.3))

# Regression
slope, intercept, r, p, se = sp_stats.linregress(has_stars["log_repos"], has_stars["log_followers"])
x_line = np.linspace(has_stars["log_repos"].min(), has_stars["log_repos"].max(), 100)
ax_main.plot(x_line, slope*x_line + intercept, "--", color="#999", lw=1, alpha=0.6)
ax_main.text(0.02, 0.97, f"r = {r:.2f}", transform=ax_main.transAxes, fontsize=8, va="top", color="#666")

ax_main.set_xlabel("log10(public repos)")
ax_main.set_ylabel("log10(GitHub followers)")
ax_main.grid(True, linestyle="--", alpha=0.25)
ax_main.legend(loc="lower right", fontsize=7, markerscale=0.6)

# Marginals
ax_top.hist(has_stars["log_repos"], bins=12, color="#aaa", edgecolor="white", lw=0.5, alpha=0.6)
ax_top.tick_params(labelbottom=False)
ax_top.spines["bottom"].set_visible(False)
ax_top.set_ylabel("n", fontsize=7)
panel_label(ax_top, "a", x=-0.02, y=1.15)

ax_right.hist(has_stars["log_followers"], bins=12, orientation="horizontal", color="#aaa", edgecolor="white", lw=0.5, alpha=0.6)
ax_right.tick_params(labelleft=False)
ax_right.spines["left"].set_visible(False)
ax_right.set_xlabel("n", fontsize=7)

# Size legend
for s_val, s_label in [(2, "100"), (4, "10k"), (5, "100k")]:
    ax_main.scatter([], [], s=s_val*30, c="white", edgecolors="#333", linewidth=0.5, label=f"{s_label} stars")

fig.suptitle("Influence Landscape -- Bubble Size = Total Stars Received", fontsize=12, fontweight="bold", y=0.98)
plt.savefig(f"{OUT}/fig_e2_stars_landscape.png")
plt.savefig(f"{OUT}/fig_e2_stars_landscape.pdf")
plt.close()
print("[OK] Figure E2: Stars landscape")


# ============================================================================
# FIGURE 3 -- Network graph (enriched with node size = score)
# ============================================================================
edges = [
    ("rasbt","karpathy"),("rasbt","Atcold"),("rasbt","biobenkj"),
    ("rasbt","colah"),("rasbt","fchollet"),("rasbt","norvig"),
    ("rasbt","rwightman"),("rasbt","mlabonne"),("rasbt","srush"),
    ("rasbt","tridao"),("rasbt","cbfinn"),("rasbt","lvdmaaten"),
    ("rasbt","DrJimFan"),("rasbt","dpkingma"),("rasbt","hadley"),
    ("rasbt","jakevdp"),("rasbt","GaelVaroquaux"),
    ("aravindsrinivas","karpathy"),("aravindsrinivas","Atcold"),
    ("aravindsrinivas","OriolVinyals"),("aravindsrinivas","soumith"),
    ("aravindsrinivas","geohot"),
    ("crazyhottommy","lh3"),("crazyhottommy","biobenkj"),
    ("crazyhottommy","shenwei356"),("crazyhottommy","lindenb"),
    ("crazyhottommy","ewels"),("crazyhottommy","arq5x"),
    ("crazyhottommy","thegenemyers"),("crazyhottommy","richarddurbin"),
    ("crazyhottommy","jokergoo"),("crazyhottommy","hadley"),
    ("nh13","lh3"),("nh13","shenwei356"),("nh13","lindenb"),
    ("nh13","ewels"),("nh13","arq5x"),
    ("biopelayo","rasbt"),("biopelayo","crazyhottommy"),
    ("biopelayo","aravindsrinivas"),("biopelayo","nh13"),
    ("biopelayo","akosiorek"),("biopelayo","saharmor"),
    ("biopelayo","ylecun"),("biopelayo","kozyrkov"),
    ("biopelayo","AndrewNg"),("biopelayo","rafalab"),
    ("biopelayo","bpucker"),("biopelayo","deanslee"),
    ("biopelayo","VidithPhillips"),("biopelayo","pachterlab"),
]

Gn = nx.DiGraph()
Gn.add_edges_from(edges)

user_cat = dict(zip(df["GitHub"], df["Category"]))
user_cat["biopelayo"] = "Curator"
user_score = dict(zip(df["GitHub"], df["score_v2"]))
PAL_NET = {**PAL, "Curator": "#FFD700"}

in_deg = dict(Gn.in_degree())
out_deg = dict(Gn.out_degree())
betw = nx.betweenness_centrality(Gn)

fig, (ax_net, ax_centr) = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={"width_ratios": [3, 2], "wspace": 0.3})
panel_label(ax_net, "a")
panel_label(ax_centr, "b")

pos = nx.spring_layout(Gn, k=2.0, iterations=100, seed=42)

# Edges with alpha based on target in-degree
for u, v in Gn.edges():
    alpha = 0.15 + 0.15 * in_deg.get(v, 0)
    ax_net.annotate("", xy=pos[v], xytext=pos[u],
                    arrowprops=dict(arrowstyle="-|>", color="#bbbbbb",
                                   lw=0.5, alpha=min(alpha, 0.7),
                                   connectionstyle="arc3,rad=0.1"))

for cat, color in PAL_NET.items():
    nodes = [n for n in Gn.nodes() if user_cat.get(n) == cat]
    if not nodes:
        continue
    sizes = [max(80, user_score.get(n, 1.5) * 80) for n in nodes]
    nx.draw_networkx_nodes(Gn, pos, nodelist=nodes, node_color=color,
                           node_size=sizes, edgecolors="#333", linewidths=0.5, alpha=0.9, ax=ax_net)

hub_labels = {n: n for n in Gn.nodes() if in_deg.get(n,0) >= 2 or n == "biopelayo"}
nx.draw_networkx_labels(Gn, pos, hub_labels, font_size=7, font_weight="bold", ax=ax_net)
minor_labels = {n: n for n in Gn.nodes() if n not in hub_labels}
nx.draw_networkx_labels(Gn, pos, minor_labels, font_size=5.5, font_color="#777", ax=ax_net)

leg_el = [Patch(facecolor=c, edgecolor="#333", label=l) for l,c in PAL_NET.items()
          if any(user_cat.get(n)==l for n in Gn.nodes())]
ax_net.legend(handles=leg_el, loc="upper left", fontsize=7, title="Domain", title_fontsize=7.5)
ax_net.set_title("Following Network", fontweight="bold", pad=10)
ax_net.axis("off")

# Panel b: Centrality analysis
centr_data = []
for n in Gn.nodes():
    centr_data.append({
        "user": n, "in_degree": in_deg[n], "out_degree": out_deg[n],
        "betweenness": betw[n], "category": user_cat.get(n, "?")
    })
cdf = pd.DataFrame(centr_data).sort_values("betweenness", ascending=True).tail(15)

y_c = np.arange(len(cdf))
colors_c = [PAL_NET.get(c, "#888") for c in cdf["category"]]
ax_centr.barh(y_c, cdf["betweenness"], height=0.6, color=colors_c, edgecolor="white", linewidth=0.5)
ax_centr.set_yticks(y_c)
ax_centr.set_yticklabels(cdf["user"], fontsize=7.5)
ax_centr.set_xlabel("Betweenness centrality")
ax_centr.set_title("Network Brokers (Top 15)", fontweight="bold", pad=10)

# Annotate in/out degree
for i, (_, row) in enumerate(cdf.iterrows()):
    ax_centr.text(row["betweenness"] + 0.005, i,
                  f'in={row["in_degree"]} out={row["out_degree"]}',
                  va="center", fontsize=6, color="#888")

fig.suptitle("Awesome Awesomers -- Social Graph Analysis", fontsize=13, fontweight="bold", y=1.01)
plt.savefig(f"{OUT}/fig_e3_network_enriched.png")
plt.savefig(f"{OUT}/fig_e3_network_enriched.pdf")
plt.close()
print("[OK] Figure E3: Enriched network")


# ============================================================================
# FIGURE 4 -- Activity heatmap + archetype quadrants
# ============================================================================
fig = plt.figure(figsize=(13, 6))
gs4 = GridSpec(1, 2, figure=fig, wspace=0.35)

# Panel a: Activity vs Followers
ax4a = fig.add_subplot(gs4[0, 0])
panel_label(ax4a, "a")

active_df = df[df["days_inactive"].notna()].copy()
for cat in PAL:
    sub = active_df[active_df["Category"] == cat]
    if len(sub) == 0: continue
    ax4a.scatter(sub["days_inactive"], sub["log_followers"], c=PAL[cat], label=cat,
                 s=55, alpha=0.85, edgecolors="#333", linewidth=0.3, zorder=3)

# Activity zones
ax4a.axvspan(0, 90, alpha=0.05, color="#56d364", zorder=0)
ax4a.axvspan(90, 365, alpha=0.05, color="#ffa657", zorder=0)
ax4a.axvspan(365, active_df["days_inactive"].max() + 50, alpha=0.05, color="#f85149", zorder=0)
ax4a.text(30, ax4a.get_ylim()[0] if ax4a.get_ylim()[0] > 0 else 1.8, "Active", fontsize=7, color="#56d364", ha="center", alpha=0.8)
ax4a.text(200, ax4a.get_ylim()[0] if ax4a.get_ylim()[0] > 0 else 1.8, "Moderate", fontsize=7, color="#ffa657", ha="center", alpha=0.8)

texts_a = []
for _, row in active_df.nlargest(10, "Followers").iterrows():
    short = row["Name"].split()[-1]
    if "Tommy" in row["Name"]: short = "Tang"
    t = ax4a.text(row["days_inactive"], row["log_followers"], short, fontsize=6, color="#444", style="italic")
    texts_a.append(t)
adjust_text(texts_a, ax=ax4a, arrowprops=dict(arrowstyle="-", color="#ccc", lw=0.3))

ax4a.set_xlabel("Days since last push")
ax4a.set_ylabel("log10(GitHub followers)")
ax4a.set_title("Activity vs. Influence", fontweight="bold", pad=10)
ax4a.legend(loc="upper right", fontsize=6.5)
ax4a.grid(True, linestyle="--", alpha=0.2)

# Panel b: Stars per repo vs followers (efficiency quadrants)
ax4b = fig.add_subplot(gs4[0, 1])
panel_label(ax4b, "b")

eff_df = df[(df["TotalStars"] > 0) & (df["Repos"] > 0)].copy()
eff_df["log_spr"] = np.log10(eff_df["stars_per_repo"].clip(lower=1))

med_spr = eff_df["log_spr"].median()
med_foll = eff_df["log_followers"].median()

ax4b.axhline(med_foll, color="#ddd", lw=0.8, zorder=0)
ax4b.axvline(med_spr, color="#ddd", lw=0.8, zorder=0)

quad_style = dict(fontsize=7, color="#bbb", fontstyle="italic")
ax4b.text(0.15, 0.96, "CULT FOLLOWING\nfew stars/repo, many followers", transform=ax4b.transAxes, ha="center", va="top", **quad_style)
ax4b.text(0.85, 0.96, "SUPERSTAR\nhigh stars/repo + followers", transform=ax4b.transAxes, ha="center", va="top", **quad_style)
ax4b.text(0.15, 0.04, "EMERGING", transform=ax4b.transAxes, ha="center", va="bottom", **quad_style)
ax4b.text(0.85, 0.04, "STAR MAGNET\nhigh stars/repo, growing", transform=ax4b.transAxes, ha="center", va="bottom", **quad_style)

for cat in PAL:
    sub = eff_df[eff_df["Category"] == cat]
    if len(sub) == 0: continue
    ax4b.scatter(sub["log_spr"], sub["log_followers"], c=PAL[cat], label=cat,
                 s=55, alpha=0.85, edgecolors="#333", linewidth=0.3, zorder=3)

texts_b = []
for _, row in eff_df.nlargest(12, "score_v2").iterrows():
    short = row["Name"].split()[-1]
    if "Tommy" in row["Name"]: short = "Tang"
    elif "van der" in row["Name"]: short = "vd Maaten"
    t = ax4b.text(row["log_spr"], row["log_followers"], short, fontsize=6, color="#444", style="italic")
    texts_b.append(t)
adjust_text(texts_b, ax=ax4b, arrowprops=dict(arrowstyle="-", color="#ccc", lw=0.3))

ax4b.set_xlabel("log10(stars per repo)")
ax4b.set_ylabel("log10(GitHub followers)")
ax4b.set_title("Efficiency Quadrants -- Stars per Repo", fontweight="bold", pad=10)
ax4b.legend(loc="lower right", fontsize=6.5)
ax4b.grid(True, linestyle="--", alpha=0.2)

fig.suptitle("Awesome Awesomers -- Activity & Efficiency", fontsize=13, fontweight="bold", y=1.01)
plt.savefig(f"{OUT}/fig_e4_activity_efficiency.png")
plt.savefig(f"{OUT}/fig_e4_activity_efficiency.pdf")
plt.close()
print("[OK] Figure E4: Activity & efficiency")


# ============================================================================
# FIGURE 5 -- Language ecosystem + Bioinformatics deep dive
# ============================================================================
fig = plt.figure(figsize=(13, 5.5))
gs5 = GridSpec(1, 3, figure=fig, wspace=0.4, width_ratios=[1.2, 1.5, 1.5])

# Panel a: Primary languages
ax5a = fig.add_subplot(gs5[0, 0])
panel_label(ax5a, "a")

langs = df[df["PrimaryLang"] != "--"]["PrimaryLang"].value_counts()
lang_colors = {"Python": "#3572A5", "C": "#555555", "R": "#198CE7", "Go": "#00ADD8",
               "Nextflow": "#3AC486", "TypeScript": "#3178C6", "TeX": "#008040", "Java": "#B07219"}
colors_l = [lang_colors.get(l, "#888") for l in langs.index]

ax5a.barh(np.arange(len(langs)), langs.values, color=colors_l, height=0.6, edgecolor="white", linewidth=0.5)
ax5a.set_yticks(np.arange(len(langs)))
ax5a.set_yticklabels(langs.index, fontsize=8)
ax5a.set_xlabel("Number of awesomers")
ax5a.set_title("Primary Languages", fontweight="bold", pad=8)
ax5a.invert_yaxis()

# Panel b: Bioinformatics detail
ax5b = fig.add_subplot(gs5[0, 1])
panel_label(ax5b, "b")

bio = df[df["Category"] == "Bioinformatics"].sort_values("score_v2", ascending=True).copy()
y_bio = np.arange(len(bio))
bar_c = ["#E64B35" if s == "S" else "#3C5488" for s in bio["Source"]]

ax5b.barh(y_bio, bio["Followers"], color=bar_c, height=0.65, edgecolor="white", linewidth=0.5)
ax5b.set_yticks(y_bio)
ax5b.set_yticklabels(bio["Name"], fontsize=7)
ax5b.set_xlabel("GitHub followers")
ax5b.set_title("Bioinformatics -- Followers", fontweight="bold", pad=8)

for i, v in enumerate(bio["Followers"]):
    ax5b.text(v + 20, i, f"{int(v):,}", va="center", fontsize=6, color="#888")

ax5b.legend([Patch(fc="#E64B35"), Patch(fc="#3C5488")], ["Seed", "Graph"], fontsize=7, loc="lower right")

# Panel c: Stars per repo (efficiency)
ax5c = fig.add_subplot(gs5[0, 2])
panel_label(ax5c, "c")

bio_stars = df[(df["Category"] == "Bioinformatics") & (df["TotalStars"] > 0)].copy()
bio_stars = bio_stars.sort_values("stars_per_repo", ascending=True)
y_bs = np.arange(len(bio_stars))

ax5c.barh(y_bs, bio_stars["stars_per_repo"], color="#00A087", height=0.65, edgecolor="white", linewidth=0.5)
ax5c.set_yticks(y_bs)
ax5c.set_yticklabels(bio_stars["Name"], fontsize=7)
ax5c.set_xlabel("Stars per repository")
ax5c.set_title("Bioinformatics -- Star Efficiency", fontweight="bold", pad=8)

fig.suptitle("Ecosystem & Domain Analysis", fontsize=13, fontweight="bold", y=1.02)
plt.savefig(f"{OUT}/fig_e5_ecosystem.png")
plt.savefig(f"{OUT}/fig_e5_ecosystem.pdf")
plt.close()
print("[OK] Figure E5: Ecosystem & domain")


# ============================================================================
# FIGURE 6 -- Comprehensive heatmap (all metrics)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

top20_hm = df.nlargest(20, "score_v2").copy()
hm_cols = ["Followers", "TotalStars", "Repos", "stars_per_repo", "followers_per_repo", "score_v2"]
hm_labels = ["Followers", "Total Stars", "Repos", "Stars/Repo", "Followers/Repo", "Score v2"]

hm_data = top20_hm[hm_cols].copy()
# Normalize per column
hm_norm = hm_data.copy()
for col in hm_norm.columns:
    mn, mx = hm_norm[col].min(), hm_norm[col].max()
    if mx > mn:
        hm_norm[col] = (hm_norm[col] - mn) / (mx - mn)
    else:
        hm_norm[col] = 0

cmap = mcolors.LinearSegmentedColormap.from_list("nature", ["#ffffff", "#b3cde3", "#3C5488"], N=256)
im = ax.imshow(hm_norm.values, aspect="auto", cmap=cmap, vmin=0, vmax=1)

for i in range(len(hm_data)):
    for j in range(len(hm_cols)):
        val = hm_data.iloc[i, j]
        if val >= 10000:
            txt = f"{val/1000:.0f}k"
        elif val >= 1000:
            txt = f"{val/1000:.1f}k"
        else:
            txt = f"{val:.0f}" if val == int(val) else f"{val:.1f}"
        tc = "white" if hm_norm.iloc[i, j] > 0.6 else "#333"
        ax.text(j, i, txt, ha="center", va="center", fontsize=7, color=tc, fontweight="bold")

ax.set_xticks(np.arange(len(hm_labels)))
ax.set_xticklabels(hm_labels, fontsize=8, rotation=20, ha="right")
ax.set_yticks(np.arange(len(top20_hm)))
ax.set_yticklabels(top20_hm["Name"], fontsize=7.5)

# Category color strips on the left
for i, cat in enumerate(top20_hm["Category"]):
    ax.add_patch(plt.Rectangle((-0.7, i-0.4), 0.3, 0.8, color=PAL.get(cat, "#888"), clip_on=False))

cbar = plt.colorbar(im, ax=ax, fraction=0.02, pad=0.04)
cbar.set_label("Relative intensity", fontsize=8)
cbar.ax.tick_params(labelsize=7)

ax.set_title("Top 20 Awesomers -- Multi-Metric Profile", fontsize=12, fontweight="bold", pad=12)
plt.savefig(f"{OUT}/fig_e6_heatmap_full.png")
plt.savefig(f"{OUT}/fig_e6_heatmap_full.pdf")
plt.close()
print("[OK] Figure E6: Full heatmap")


# ============================================================================
# PRINT TABLES & CRITERIA
# ============================================================================
print("\n" + "="*80)
print("ENRICHED SUMMARY")
print("="*80)

print("\nTable 1: Top 20 by Awesomer Score v2")
t1 = df.nlargest(20, "score_v2")[["Name","Category","Followers","TotalStars","Repos","score_v2","active"]]
print(t1.to_string(index=False))

print("\nTable 2: Network centrality (betweenness)")
for n, b in sorted(betw.items(), key=lambda x: -x[1])[:10]:
    cat = user_cat.get(n, "?")
    print(f"  {n:25s}  betweenness={b:.3f}  in={in_deg[n]}  out={out_deg[n]}  domain={cat}")

print("\n" + "="*80)
print("PROPOSED AWESOMER CRITERIA")
print("="*80)
print("""
Based on the enriched analysis, we propose 5 tiers:

TIER 1 -- LEGENDARY (Score >= 3.5)
  Criteria: >10k followers OR >100k total stars OR created foundational tools
  Examples: Karpathy, Raschka, Wickham, Hotz

TIER 2 -- ESTABLISHED (Score 2.8-3.5)
  Criteria: >2k followers AND >1k total stars AND active (push < 90d)
  Examples: Heng Li, Tang, Olah, Rush, Labonne

TIER 3 -- RISING (Score 2.3-2.8)
  Criteria: >500 followers OR >500 total stars, active contributor
  Examples: Ewels, Quinlan, Shen, Lindenbaum

TIER 4 -- SPECIALIST (Score < 2.3 but domain expert)
  Criteria: Recognized in their niche, active repos, curated content
  Examples: Homer, Pucker, Kosiorek

TIER 5 -- SEED (no GitHub or minimal presence)
  Criteria: Identified via LinkedIn/network, influence via non-code channels
  Examples: Educators, Policy makers, Pharma leaders
""")

print(f"\nTotal enriched profiles: {len(df)}")
print(f"With star data: {(df['TotalStars']>0).sum()}")
print(f"Active (push <90d): {(df['active']=='Active').sum()}")
print(f"All figures saved to: {OUT}/")
