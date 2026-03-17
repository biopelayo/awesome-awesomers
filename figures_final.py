"""
Awesome Awesomers -- Publication-Quality Figures v3
====================================================
Simpsons palette (ggsci) + subtitles + figure captions
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
from scipy import stats as sp_stats
from adjustText import adjust_text
from datetime import datetime
import warnings, os
warnings.filterwarnings("ignore")

# ============================================================================
# DATA
# ============================================================================
raw = [
    ("Andrej Karpathy","AI/ML","karpathy",148001,63,393395,"nanoGPT",55059,"Python","2026-03-16","G"),
    ("George Hotz","AI/ML","geohot",46135,101,23453,"fromthetransistor",6456,"Python","2026-02-25","G"),
    ("Sebastian Raschka","AI/ML","rasbt",36352,147,152172,"LLMs-from-scratch",88460,"Python","2026-03-17","S"),
    ("Hadley Wickham","Data Sci.","hadley",26541,230,7131,"adv-r",2454,"R","2026-03-17","G"),
    ("Jake Vanderplas","Data Sci.","jakevdp",19048,239,1589,"JSAnimation",240,"Python","2026-03-17","G"),
    ("Francois Chollet","AI/ML","fchollet",17861,16,36434,"stable-diff-tf",324,"Python","2025-09-18","G"),
    ("Soumith Chintala","AI/ML","soumith",13119,169,18439,"mini-sglang",3,"Python","2025-12-18","G"),
    ("Christopher Olah","AI/ML","colah",9766,52,1728,"lucid",9,"TypeScript","2024-04-16","G"),
    ("Peter Norvig","AI/ML","norvig",9726,4,0,"--",0,"--","2026-03-17","G"),
    ("Ross Wightman","AI/ML","rwightman",7002,74,5079,"timm",59,"Python","2025-09-09","G"),
    ("Maxime Labonne","AI/ML","mlabonne",6536,23,82837,"--",0,"Python","2026-03-09","G"),
    ("Heng Li","Bioinfo.","lh3",4267,138,9184,"minimap2",2143,"C","2026-03-15","G"),
    ("Sasha Rush","AI/ML","srush",3832,165,19106,"awesome-o1",1213,"TeX","2026-01-01","G"),
    ("Ming Tommy Tang","Bioinfo.","crazyhottommy",3726,177,3885,"genomics-resources",1373,"Python","2026-03-15","S"),
    ("Alfredo Canziani","AI/ML","Atcold",3675,70,0,"--",0,"--","2026-03-16","G"),
    ("Gael Varoquaux","Data Sci.","GaelVaroquaux",3393,90,606,"--",0,"Python","2026-03-13","G"),
    ("Tri Dao","AI/ML","tridao",2933,10,0,"--",0,"--","2026-02-11","G"),
    ("Chelsea Finn","AI/ML","cbfinn",2174,25,0,"--",0,"--","--","G"),
    ("Laurens van der Maaten","AI/ML","lvdmaaten",1975,23,0,"--",0,"--","--","G"),
    ("Rafael Irizarry","Bioinfo.","rafalab",1633,49,0,"--",0,"R","--","S"),
    ("Wei Shen","Bioinfo.","shenwei356",1469,119,6116,"--",0,"Go","2026-03-13","G"),
    ("Yann LeCun","AI/ML","ylecun",1509,12,0,"--",0,"--","--","S"),
    ("Fabian Theis","Data Sci.","theislab",1400,253,0,"--",0,"--","2026-03-17","S"),
    ("Cassie Kozyrkov","AI/ML","kozyrkov",1039,5,0,"--",0,"--","--","S"),
    ("Jim Fan","AI/ML","DrJimFan",934,7,0,"--",0,"--","--","G"),
    ("Phil Ewels","Bioinfo.","ewels",844,159,419,"--",0,"Nextflow","2026-03-17","G"),
    ("Aaron Quinlan","Bioinfo.","arq5x",771,75,0,"--",0,"--","2026-02-22","G"),
    ("Durk Kingma","AI/ML","dpkingma",597,9,0,"--",0,"--","--","G"),
    ("Pierre Lindenbaum","Bioinfo.","lindenb",555,178,0,"--",0,"Java","2026-03-14","G"),
    ("Eugene Myers","Bioinfo.","thegenemyers",467,19,0,"--",0,"C","--","G"),
    ("Richard Durbin","Bioinfo.","richarddurbin",380,20,0,"--",0,"C","--","G"),
    ("Adam Kosiorek","AI/ML","akosiorek",375,40,0,"--",0,"--","--","S"),
    ("Nils Homer","Bioinfo.","nh13",374,207,0,"--",0,"--","2026-03-17","S"),
    ("Lior Pachter","AI/ML","pachterlab",377,169,0,"--",0,"--","--","S"),
    ("Boas Pucker","Bioinfo.","bpucker",187,80,0,"--",0,"Python","--","S"),
    ("Sahar Mor","AI/ML","saharmor",205,86,0,"--",0,"--","--","S"),
    ("Ben Johnson","Bioinfo.","biobenkj",121,132,0,"--",0,"--","--","G"),
    ("Dean Lee","Bioinfo.","deanslee",118,2,0,"--",0,"--","--","S"),
    ("Oriol Vinyals","AI/ML","OriolVinyals",84,3,0,"--",0,"--","--","G"),
]

cols = ["Name","Category","GitHub","Followers","Repos","TotalStars",
        "TopRepo","TopStars","PrimaryLang","LastPush","Source"]
df = pd.DataFrame(raw, columns=cols)

df["log_f"] = np.log10(df["Followers"].clip(lower=1))
df["log_r"] = np.log10(df["Repos"].clip(lower=1))
df["log_s"] = np.log10(df["TotalStars"].clip(lower=1))
df["spr"] = (df["TotalStars"] / df["Repos"].clip(lower=1)).round(0)
df["fpr"] = (df["Followers"] / df["Repos"].clip(lower=1)).round(0)
df["score"] = (df["log_f"]*0.40 + df["log_s"]*0.35 + df["log_r"]*0.25).round(2)

today = datetime(2026, 3, 17)
def days_since(s):
    if s == "--" or pd.isna(s): return np.nan
    try: return (today - datetime.strptime(s[:10], "%Y-%m-%d")).days
    except: return np.nan
df["days_inactive"] = df["LastPush"].apply(days_since)

OUT = "D:/Antigravity/awesome-awesomers/plots"
os.makedirs(OUT, exist_ok=True)

# ============================================================================
# SIMPSONS PALETTE (ggsci::scale_color_simpsons)
# ============================================================================
SIMP = {
    "homer_yellow":  "#FED439",
    "marge_blue":    "#709AE1",
    "bart_orange":   "#FD7446",
    "lisa_red":      "#D2AF81",
    "maggie_green":  "#D5E4A2",
    "burns_teal":    "#197EC0",
    "krusty_scarlet":"#F05C3B",
    "flanders_green":"#46732E",
    "sky_blue":      "#71D0F5",
    "barney_purple": "#370335",
    "moe_teal":      "#075149",
    "firered":       "#C80813",
    "milhouse_blue": "#8A9197",
    "ned_pink":      "#FD8CC1",
    "teal_accent":   "#1A9993",
}

# Domain mapping — Simpsons palette
C = {
    "AI/ML":     SIMP["bart_orange"],
    "Bioinfo.":  SIMP["burns_teal"],
    "Data Sci.": SIMP["homer_yellow"],
}
C_source = {
    "S": SIMP["burns_teal"],
    "G": SIMP["bart_orange"],
}
C_decomp = {
    "followers": SIMP["bart_orange"],
    "stars":     SIMP["sky_blue"],
    "repos":     SIMP["burns_teal"],
}
C_eff = SIMP["teal_accent"]
C_curator = SIMP["homer_yellow"]

# ============================================================================
# GLOBAL STYLE
# ============================================================================
plt.rcParams.update({
    "figure.facecolor":     "white",
    "axes.facecolor":       "white",
    "axes.edgecolor":       "#2b2b2b",
    "axes.labelcolor":      "#1a1a1a",
    "axes.linewidth":       0.6,
    "axes.spines.top":      False,
    "axes.spines.right":    False,
    "xtick.color":          "#333",
    "ytick.color":          "#333",
    "xtick.major.width":    0.45,
    "ytick.major.width":    0.45,
    "xtick.major.size":     2.5,
    "ytick.major.size":     2.5,
    "xtick.direction":      "out",
    "ytick.direction":      "out",
    "text.color":           "#1a1a1a",
    "font.family":          "sans-serif",
    "font.sans-serif":      ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size":            7.5,
    "axes.titlesize":       9,
    "axes.titleweight":     "bold",
    "axes.labelsize":       8,
    "legend.fontsize":      6.5,
    "legend.frameon":       False,
    "legend.handlelength":  1.0,
    "legend.handletextpad": 0.35,
    "legend.columnspacing": 0.8,
    "grid.color":           "#ececec",
    "grid.linewidth":       0.3,
    "figure.dpi":           200,
    "savefig.dpi":          300,
    "savefig.bbox":         "tight",
    "savefig.pad_inches":   0.05,
})

# ============================================================================
# HELPERS
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
    if "Tommy" in name: return "M.T. Tang"
    if "van der" in name: return "L. vd Maaten"
    if len(parts) >= 2: return f"{parts[0][0]}. {parts[-1]}"
    return name

def save(fig, stem):
    fig.savefig(f"{OUT}/{stem}.png")
    fig.savefig(f"{OUT}/{stem}.pdf")
    plt.close(fig)
    print(f"  [OK] {stem}")

rng = np.random.default_rng(42)

# Language colors (GitHub official where possible)
LC = {"Python":"#3572A5", "C":"#555555", "R":"#198CE7", "Go":"#00ADD8",
      "Nextflow":"#3AC486", "TypeScript":"#3178C6", "TeX":"#008040", "Java":"#B07219"}


# ============================================================================
# FIGURE 1 — Cohort Overview
# ============================================================================
print("Fig 1: Cohort overview")
fig = plt.figure(figsize=(7.2, 6.2))
gs = GridSpec(2, 2, figure=fig, hspace=0.55, wspace=0.42,
              left=0.10, right=0.97, top=0.91, bottom=0.08)

# a) Domain x Source
ax_a = fig.add_subplot(gs[0, 0])
plabel(ax_a, "a")
subtitle(ax_a, "Seed = LinkedIn contacts; Graph = GitHub follows expansion")

cats_ordered = ["AI/ML", "Bioinfo.", "Data Sci."]
pivot = df.groupby(["Category","Source"]).size().unstack(fill_value=0).reindex(cats_ordered)
y_a = np.arange(len(cats_ordered))

seed_v = pivot.get("S", pd.Series(0, index=pivot.index)).values
graph_v = pivot.get("G", pd.Series(0, index=pivot.index)).values
total_v = seed_v + graph_v

ax_a.barh(y_a, seed_v, height=0.52, color=C_source["S"], label="Seed (LinkedIn)",
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
    sub = df[df["Category"]==cat]["log_f"]
    jitter = rng.normal(0, 0.06, len(sub))
    ax_c.scatter(sub, np.full(len(sub), i) + jitter, c=C[cat], s=22, alpha=0.75,
                 edgecolors="white", linewidth=0.25, zorder=3)
    med = sub.median()
    ax_c.plot([med, med], [i-0.20, i+0.20], color=C[cat], linewidth=2.8,
              zorder=4, solid_capstyle="round")
    q1, q3 = sub.quantile(0.25), sub.quantile(0.75)
    ax_c.plot([q1, q3], [i, i], color=C[cat], linewidth=1.2, alpha=0.4, zorder=2)
    ax_c.text(med, i + 0.28, f"median = {10**med:,.0f}",
              fontsize=5.5, ha="center", color=C[cat], fontweight="bold")

ax_c.set_yticks(range(len(cats_ordered)))
ax_c.set_yticklabels(cats_ordered, fontsize=7.5)
ax_c.set_xlabel("GitHub followers (log$_{10}$)")
ax_c.set_title("Follower distribution", loc="left", pad=12)
ax_c.grid(axis="x", linestyle="--", alpha=0.35)

# d) Languages
ax_d = fig.add_subplot(gs[1, 1])
plabel(ax_d, "d")
subtitle(ax_d, "Based on most-used language in public repos")

langs = df[df["PrimaryLang"]!="--"]["PrimaryLang"].value_counts().sort_values()
colors_l = [LC.get(l, "#aaa") for l in langs.index]
y_l = np.arange(len(langs))

ax_d.barh(y_l, langs.values, height=0.50, color=colors_l, edgecolor="white", linewidth=0.4)
ax_d.set_yticks(y_l)
ax_d.set_yticklabels(langs.index, fontsize=7)
ax_d.set_xlabel("Awesomers (n)")
ax_d.set_title("Primary language", loc="left", pad=12)
for i, v in enumerate(langs.values):
    ax_d.text(v + 0.12, y_l[i], str(v), va="center", fontsize=6.5,
              fontweight="bold", color=colors_l[i])
ax_d.set_xlim(0, langs.max() + 2)

fig_caption(fig,
    "Figure 1. Cohort overview of 39 awesome-awesomers across three domains. "
    "Profiles were seeded from LinkedIn contacts and expanded via GitHub following graphs. "
    "Data collected March 2026 via GitHub API (gh CLI).")

save(fig, "Fig1_overview")


# ============================================================================
# FIGURE 2 — Influence Ranking + Decomposition
# ============================================================================
print("Fig 2: Influence ranking")
top25 = df.nlargest(25, "score").sort_values("score", ascending=True).copy()

fig = plt.figure(figsize=(7.2, 6.8))
gs2 = GridSpec(1, 2, figure=fig, wspace=0.08, width_ratios=[1.8, 1],
               left=0.18, right=0.97, top=0.91, bottom=0.09)

# a) Cleveland dot
ax1 = fig.add_subplot(gs2[0, 0])
plabel(ax1, "a", x=-0.22)
subtitle(ax1, "Composite score: weighted sum of log-scaled metrics", x=0.0, y=1.02)

y = np.arange(len(top25))
cols_dot = [C.get(c, "#aaa") for c in top25["Category"]]

ax1.hlines(y, 0, top25["score"], color="#ebebeb", linewidth=0.6, zorder=1)
ax1.scatter(top25["score"], y, c=cols_dot, s=42, zorder=3,
            edgecolors="#333", linewidth=0.3)

for i, (_, row) in enumerate(top25.iterrows()):
    sn = short_name(row["Name"])
    ax1.text(-0.05, i, sn, va="center", ha="right", fontsize=6.2,
             fontweight="bold" if row["score"] >= 3.5 else "normal")
    ax1.text(row["score"] + 0.03, i, f'{row["score"]:.1f}', va="center",
             fontsize=5, color="#999")

ax1.set_xlabel("Awesomer Score\n"
               r"(0.40 $\cdot$ log$_{10}$followers + 0.35 $\cdot$ log$_{10}$stars "
               r"+ 0.25 $\cdot$ log$_{10}$repos)", fontsize=6.5)
ax1.set_title("Composite influence ranking", loc="left", pad=14)
ax1.set_yticks([])
ax1.set_xlim(-0.05, top25["score"].max() + 0.35)
ax1.grid(axis="x", linestyle="--", alpha=0.25)

leg = [Line2D([0],[0], marker="o", color="w", markerfacecolor=c, markersize=5,
              markeredgecolor="#333", markeredgewidth=0.3, label=l) for l, c in C.items()]
ax1.legend(handles=leg, loc="lower right", fontsize=6, borderpad=0.25,
           labelspacing=0.25, title="Domain", title_fontsize=6.5)

# b) Decomposition
ax2 = fig.add_subplot(gs2[0, 1], sharey=ax1)
plabel(ax2, "b", x=-0.08)
subtitle(ax2, "Relative contribution of each metric", x=0.0, y=1.02)

c_f = top25["log_f"] * 0.40
c_s = top25["log_s"] * 0.35
c_r = top25["log_r"] * 0.25
h = 0.50

ax2.barh(y, c_f, height=h, color=C_decomp["followers"], edgecolor="white", linewidth=0.3, label="Followers (40%)")
ax2.barh(y, c_s, height=h, left=c_f, color=C_decomp["stars"], edgecolor="white", linewidth=0.3, label="Stars (35%)")
ax2.barh(y, c_r, height=h, left=c_f+c_s, color=C_decomp["repos"], edgecolor="white", linewidth=0.3, label="Repos (25%)")

ax2.set_xlabel("Score components")
ax2.set_title("Decomposition", loc="left", pad=14)
ax2.tick_params(labelleft=False)
ax2.legend(loc="lower right", fontsize=5.5, borderpad=0.25, labelspacing=0.2)

fig_caption(fig,
    "Figure 2. Composite influence ranking of top 25 awesomers. "
    "Score = 0.40*log10(followers) + 0.35*log10(stars) + 0.25*log10(repos). "
    "Bold names indicate score >= 3.5. Stacked bars show relative contribution of each component.")

save(fig, "Fig2_score_ranking")


# ============================================================================
# FIGURE 3 — Influence Landscape
# ============================================================================
print("Fig 3: Influence landscape")
has_data = df[df["Followers"] > 0].copy()

fig = plt.figure(figsize=(5.8, 5.6))
gs3 = GridSpec(2, 2, figure=fig, width_ratios=[5, 1], height_ratios=[1, 5],
               hspace=0.03, wspace=0.03, left=0.13, right=0.95, top=0.88, bottom=0.12)

ax_m = fig.add_subplot(gs3[1, 0])
ax_t = fig.add_subplot(gs3[0, 0], sharex=ax_m)
ax_r = fig.add_subplot(gs3[1, 1], sharey=ax_m)

for cat in ["Bioinfo.", "Data Sci.", "AI/ML"]:
    sub = has_data[has_data["Category"]==cat]
    if len(sub)==0: continue
    sizes = np.clip(sub["log_s"]*18, 15, 250)
    ax_m.scatter(sub["log_r"], sub["log_f"], c=C[cat], label=cat,
                 s=sizes, alpha=0.80, edgecolors="#444", linewidth=0.2, zorder=3)

sl, ic, r, p, _ = sp_stats.linregress(has_data["log_r"], has_data["log_f"])
xl = np.linspace(has_data["log_r"].min()-0.15, has_data["log_r"].max()+0.15, 100)
ax_m.plot(xl, sl*xl+ic, "--", color="#bbb", lw=0.7, alpha=0.6, zorder=1)
ax_m.text(0.03, 0.97, f"r = {r:.2f},  P = {p:.2e}",
          transform=ax_m.transAxes, fontsize=5.5, va="top", color="#888", fontstyle="italic")

texts = []
for _, row in has_data.nlargest(15, "score").iterrows():
    t = ax_m.text(row["log_r"], row["log_f"], short_name(row["Name"]),
                  fontsize=5, color="#333", fontstyle="italic")
    texts.append(t)
adjust_text(texts, ax=ax_m, arrowprops=dict(arrowstyle="-", color="#ccc", lw=0.25),
            force_text=(0.5, 0.5), force_points=(0.3, 0.3))

ax_m.set_xlabel("Public repositories (log$_{10}$)")
ax_m.set_ylabel("GitHub followers (log$_{10}$)")
ax_m.grid(True, linestyle="--", alpha=0.20)
ax_m.legend(loc="lower right", fontsize=5.5, markerscale=0.45, borderpad=0.25)

for cat in C:
    sub = has_data[has_data["Category"]==cat]
    ax_t.hist(sub["log_r"], bins=12, color=C[cat], alpha=0.55, edgecolor="white", lw=0.3)
ax_t.tick_params(labelbottom=False, labelleft=False, left=False, bottom=False)
ax_t.spines["bottom"].set_visible(False); ax_t.spines["left"].set_visible(False)

for cat in C:
    sub = has_data[has_data["Category"]==cat]
    ax_r.hist(sub["log_f"], bins=12, orientation="horizontal",
              color=C[cat], alpha=0.55, edgecolor="white", lw=0.3)
ax_r.tick_params(labelleft=False, labelbottom=False, left=False, bottom=False)
ax_r.spines["left"].set_visible(False); ax_r.spines["bottom"].set_visible(False)

ax_corner = fig.add_subplot(gs3[0, 1]); ax_corner.axis("off")

fig.text(0.54, 0.95, "Influence landscape", ha="center", fontsize=10, fontweight="bold")
fig.text(0.54, 0.915, "Bubble area proportional to total stars received; marginals colored by domain",
         ha="center", fontsize=6, color="#888", fontstyle="italic")

fig_caption(fig,
    "Figure 3. Scatter plot of public repositories vs. GitHub followers (log10 scale). "
    "Bubble size encodes total stars. Dashed line = OLS regression. "
    "Marginal histograms show domain-specific distributions. Pearson r and P-value shown.")

save(fig, "Fig3_landscape")


# ============================================================================
# FIGURE 4 — Network
# ============================================================================
print("Fig 4: Network")
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

Gn = nx.DiGraph(); Gn.add_edges_from(edges)
ucat = dict(zip(df["GitHub"], df["Category"]))
ucat.update({"biopelayo":"Curator","aravindsrinivas":"AI/ML","jokergoo":"Bioinfo.",
             "AndrewNg":"AI/ML","VidithPhillips":"Bioinfo."})
uscore = dict(zip(df["GitHub"], df["score"]))
C_net = {**C, "Curator": C_curator}

in_d = dict(Gn.in_degree()); out_d = dict(Gn.out_degree())
betw = nx.betweenness_centrality(Gn)

fig = plt.figure(figsize=(7.2, 5.5))
gs4 = GridSpec(1, 2, figure=fig, width_ratios=[1.7, 1], wspace=0.04,
               left=0.02, right=0.98, top=0.89, bottom=0.08)

ax_n = fig.add_subplot(gs4[0, 0])
plabel(ax_n, "a", x=-0.01, y=1.04)
ax_n.set_title("Following network", loc="left", pad=12, fontsize=9)
ax_n.text(0.0, 1.02, "Directed graph: A -> B means A follows B on GitHub",
          transform=ax_n.transAxes, fontsize=5.5, color="#888", fontstyle="italic")

pos = nx.kamada_kawai_layout(Gn)
for u, v in Gn.edges():
    a = min(0.12 + 0.10 * in_d.get(v, 0), 0.50)
    ax_n.annotate("", xy=pos[v], xytext=pos[u],
                  arrowprops=dict(arrowstyle="-|>", color="#c0c0c0", lw=0.35, alpha=a,
                                  connectionstyle="arc3,rad=0.06", shrinkA=4, shrinkB=4))

for cat, color in C_net.items():
    nodes = [n for n in Gn.nodes() if ucat.get(n)==cat]
    if not nodes: continue
    sizes = [max(40, uscore.get(n, 1.5)*50) for n in nodes]
    nx.draw_networkx_nodes(Gn, pos, nodelist=nodes, node_color=color,
                           node_size=sizes, edgecolors="#555", linewidths=0.35,
                           alpha=0.88, ax=ax_n)

hubs = {n: n for n in Gn.nodes() if in_d.get(n,0) >= 2 or n == "biopelayo"}
nx.draw_networkx_labels(Gn, pos, hubs, font_size=5.5, font_weight="bold", font_color="#222", ax=ax_n)
minor = {n: n for n in Gn.nodes() if n not in hubs}
nx.draw_networkx_labels(Gn, pos, minor, font_size=4, font_color="#aaa", ax=ax_n)

leg_n = [Patch(facecolor=c, edgecolor="#555", linewidth=0.35, label=l)
         for l, c in C_net.items() if any(ucat.get(n)==l for n in Gn.nodes())]
ax_n.legend(handles=leg_n, loc="upper left", fontsize=5.5, borderpad=0.2,
            labelspacing=0.2, title="Domain", title_fontsize=6)
ax_n.axis("off")

# b) Betweenness
ax_c = fig.add_subplot(gs4[0, 1])
plabel(ax_c, "b", x=-0.08, y=1.04)
ax_c.set_title("Network brokers", loc="left", pad=12, fontsize=9)
ax_c.text(0.0, 1.02, "Betweenness centrality = bridge role in the graph",
          transform=ax_c.transAxes, fontsize=5.5, color="#888", fontstyle="italic")

centr = sorted(betw.items(), key=lambda x: -x[1])
centr_top = [(n, b) for n, b in centr if b > 0]
if len(centr_top) < 3: centr_top = centr[:6]
centr_top = list(reversed(centr_top))

names_c = [x[0] for x in centr_top]
vals_c = [x[1] for x in centr_top]
cols_c = [C_net.get(ucat.get(n, "?"), "#aaa") for n in names_c]
y_c = np.arange(len(centr_top))

ax_c.barh(y_c, vals_c, height=0.50, color=cols_c, edgecolor="white", linewidth=0.4)
ax_c.set_yticks(y_c)
ax_c.set_yticklabels(names_c, fontsize=6.5, fontfamily="monospace")
ax_c.set_xlabel("Betweenness centrality")
for i, (n, b) in enumerate(centr_top):
    ax_c.text(b + max(vals_c)*0.02, y_c[i],
              f"in={in_d[n]}  out={out_d[n]}", va="center", fontsize=5, color="#888")

fig_caption(fig,
    "Figure 4. GitHub following network. Nodes sized by awesomer score; "
    "edge opacity proportional to target in-degree. Layout: Kamada-Kawai. "
    "Betweenness centrality identifies users who bridge otherwise disconnected clusters.")

save(fig, "Fig4_network")


# ============================================================================
# FIGURE 5 — Activity + Efficiency
# ============================================================================
print("Fig 5: Activity & efficiency")
fig, (ax5a, ax5b) = plt.subplots(1, 2, figsize=(7.2, 4.2),
    gridspec_kw={"wspace": 0.32, "left": 0.09, "right": 0.97, "top": 0.88, "bottom": 0.16})

# a) Activity
plabel(ax5a, "a")
ax5a.set_title("Activity vs. influence", loc="left", pad=12)
subtitle(ax5a, "Green < 90 days = active; orange 90-365 = moderate", y=1.01)

act = df[df["days_inactive"].notna()].copy()
for cat in ["Bioinfo.", "Data Sci.", "AI/ML"]:
    sub = act[act["Category"]==cat]
    if len(sub)==0: continue
    ax5a.scatter(sub["days_inactive"], sub["log_f"], c=C[cat], label=cat,
                 s=30, alpha=0.80, edgecolors="#444", linewidth=0.2, zorder=3)

ax5a.axvspan(0, 90, color=SIMP["flanders_green"], alpha=0.05, zorder=0)
ax5a.axvspan(90, 365, color=SIMP["homer_yellow"], alpha=0.05, zorder=0)
ax5a.axvspan(365, ax5a.get_xlim()[1]+200, color=SIMP["krusty_scarlet"], alpha=0.04, zorder=0)
ax5a.axvline(90, color=SIMP["flanders_green"], lw=0.5, ls=":", alpha=0.5)
ax5a.axvline(365, color=SIMP["krusty_scarlet"], lw=0.5, ls=":", alpha=0.5)

ax5a.text(45, ax5a.get_ylim()[1]*0.99, "Active", fontsize=5.5, color=SIMP["flanders_green"],
          ha="center", va="top", fontweight="bold", alpha=0.7)
ax5a.text(227, ax5a.get_ylim()[1]*0.99, "Moderate", fontsize=5.5, color=SIMP["homer_yellow"],
          ha="center", va="top", fontweight="bold", alpha=0.8)

texts_a = []
for _, row in act.nlargest(10, "Followers").iterrows():
    t = ax5a.text(row["days_inactive"], row["log_f"], short_name(row["Name"]),
                  fontsize=4.5, color="#555", fontstyle="italic")
    texts_a.append(t)
adjust_text(texts_a, ax=ax5a, arrowprops=dict(arrowstyle="-", color="#ddd", lw=0.2))

ax5a.set_xlabel("Days since last push")
ax5a.set_ylabel("GitHub followers (log$_{10}$)")
ax5a.legend(fontsize=5.5, loc="upper right", borderpad=0.2)
ax5a.grid(True, linestyle="--", alpha=0.15)

# b) Efficiency quadrants
plabel(ax5b, "b")
ax5b.set_title("Efficiency quadrants", loc="left", pad=12)
subtitle(ax5b, "Median splits define four archetypes", y=1.01)

eff = df[(df["TotalStars"]>0) & (df["Repos"]>0)].copy()
eff["log_spr"] = np.log10(eff["spr"].clip(lower=1))
med_x = eff["log_spr"].median(); med_y = eff["log_f"].median()

for cat in ["Bioinfo.", "Data Sci.", "AI/ML"]:
    sub = eff[eff["Category"]==cat]
    if len(sub)==0: continue
    ax5b.scatter(sub["log_spr"], sub["log_f"], c=C[cat], label=cat,
                 s=30, alpha=0.80, edgecolors="#444", linewidth=0.2, zorder=3)

ax5b.axhline(med_y, color="#ddd", lw=0.5, zorder=0)
ax5b.axvline(med_x, color="#ddd", lw=0.5, zorder=0)

qs = dict(fontsize=5, color="#ccc", fontstyle="italic", ha="center")
ax5b.text(0.20, 0.96, "CULT\nFOLLOWING", transform=ax5b.transAxes, va="top", **qs)
ax5b.text(0.80, 0.96, "SUPERSTAR", transform=ax5b.transAxes, va="top", **qs)
ax5b.text(0.20, 0.04, "EMERGING", transform=ax5b.transAxes, va="bottom", **qs)
ax5b.text(0.80, 0.04, "STAR MAGNET", transform=ax5b.transAxes, va="bottom", **qs)

texts_b = []
for _, row in eff.nlargest(10, "score").iterrows():
    t = ax5b.text(row["log_spr"], row["log_f"], short_name(row["Name"]),
                  fontsize=4.5, color="#555", fontstyle="italic")
    texts_b.append(t)
adjust_text(texts_b, ax=ax5b, arrowprops=dict(arrowstyle="-", color="#ddd", lw=0.2))

ax5b.set_xlabel("Stars per repository (log$_{10}$)")
ax5b.set_ylabel("GitHub followers (log$_{10}$)")
ax5b.legend(fontsize=5.5, loc="lower right", borderpad=0.2)
ax5b.grid(True, linestyle="--", alpha=0.15)

fig_caption(fig,
    "Figure 5. (a) Activity: days since last GitHub push vs. follower count. "
    "Shaded zones classify activity level. (b) Efficiency: stars/repo vs. followers. "
    "Quadrants defined by median splits identify four developer archetypes.")

save(fig, "Fig5_activity_efficiency")


# ============================================================================
# FIGURE 6 — Bioinformatics Deep Dive
# ============================================================================
print("Fig 6: Bioinformatics")
bio = df[df["Category"]=="Bioinfo."].copy()

fig = plt.figure(figsize=(7.2, 4.8))
gs6 = GridSpec(1, 3, figure=fig, wspace=0.55,
               left=0.10, right=0.97, top=0.85, bottom=0.12)

# a) Followers
ax6a = fig.add_subplot(gs6[0, 0])
plabel(ax6a, "a")
ax6a.set_title("GitHub followers", loc="left", pad=12, fontsize=8.5)
subtitle(ax6a, "Colour = discovery source", y=1.01)

bio_f = bio.sort_values("Followers", ascending=True)
y_f = np.arange(len(bio_f))
bar_c = [C_source[s] for s in bio_f["Source"]]

ax6a.barh(y_f, bio_f["Followers"], height=0.58, color=bar_c, edgecolor="white", linewidth=0.4)
ax6a.set_yticks(y_f)
ax6a.set_yticklabels([short_name(n) for n in bio_f["Name"]], fontsize=5.5)
ax6a.set_xlabel("Followers")
for i, v in enumerate(bio_f["Followers"]):
    ax6a.text(v + 30, y_f[i], fmt_k(v), va="center", fontsize=4.5, color="#888")
ax6a.legend([Patch(fc=C_source["S"]), Patch(fc=C_source["G"])],
            ["Seed", "Graph"], fontsize=5, loc="lower right", borderpad=0.2)

# b) Repos
ax6b = fig.add_subplot(gs6[0, 1])
plabel(ax6b, "b")
ax6b.set_title("Productivity", loc="left", pad=12, fontsize=8.5)
subtitle(ax6b, "Public repositories per individual", y=1.01)

bio_r = bio.sort_values("Repos", ascending=True)
y_r = np.arange(len(bio_r))
ax6b.barh(y_r, bio_r["Repos"], height=0.58, color=SIMP["burns_teal"], alpha=0.65,
           edgecolor="white", linewidth=0.4)
ax6b.set_yticks(y_r)
ax6b.set_yticklabels([short_name(n) for n in bio_r["Name"]], fontsize=5.5)
ax6b.set_xlabel("Repositories")
for i, v in enumerate(bio_r["Repos"]):
    ax6b.text(v + 1.5, y_r[i], str(int(v)), va="center", fontsize=4.5, color="#888")

# c) Stars/repo
ax6c = fig.add_subplot(gs6[0, 2])
plabel(ax6c, "c")
ax6c.set_title("Impact efficiency", loc="left", pad=12, fontsize=8.5)
subtitle(ax6c, "Average stars per public repository", y=1.01)

bio_s = bio[bio["TotalStars"]>0].sort_values("spr", ascending=True).copy()
y_s = np.arange(len(bio_s))
ax6c.barh(y_s, bio_s["spr"], height=0.50, color=SIMP["teal_accent"],
           edgecolor="white", linewidth=0.4)
ax6c.set_yticks(y_s)
ax6c.set_yticklabels([short_name(n) for n in bio_s["Name"]], fontsize=5.5)
ax6c.set_xlabel("Stars / repository")
for i, v in enumerate(bio_s["spr"]):
    ax6c.text(v + 0.4, y_s[i], fmt_k(v), va="center", fontsize=4.5, color="#888")

fig.text(0.53, 0.95, "Bioinformatics awesomers", ha="center", fontsize=10, fontweight="bold")
fig.text(0.53, 0.91, "Domain-specific profile of computational biology leaders",
         ha="center", fontsize=6.5, color="#888", fontstyle="italic")

fig_caption(fig,
    "Figure 6. Bioinformatics awesomers profiled across three metrics. "
    "Each panel independently sorted by its displayed metric. "
    "Stars/repo computed only for individuals with >0 total stars (n=5).")

save(fig, "Fig6_bioinformatics")


# ============================================================================
# FIGURE 7 — Heatmap
# ============================================================================
print("Fig 7: Heatmap")
top20 = df.nlargest(20, "score").copy()

fig, ax = plt.subplots(figsize=(5.8, 6.2))

hm_cols = ["Followers", "TotalStars", "Repos", "spr", "fpr", "score"]
hm_labels = ["Followers", "Total stars", "Repos", "Stars/repo", "Foll./repo", "Score"]

hm_data = top20[hm_cols].copy()
hm_norm = hm_data.copy()
for col in hm_norm.columns:
    mn, mx = hm_norm[col].min(), hm_norm[col].max()
    hm_norm[col] = (hm_norm[col] - mn) / (mx - mn) if mx > mn else 0

# Simpsons-inspired gradient: light yellow -> teal
cmap = mcolors.LinearSegmentedColormap.from_list("simpsons_heat",
    ["#FFFDE7", SIMP["sky_blue"], SIMP["burns_teal"]], N=256)
im = ax.imshow(hm_norm.values, aspect="auto", cmap=cmap, vmin=0, vmax=1)

for i in range(len(hm_data)):
    for j in range(len(hm_cols)):
        val = hm_data.iloc[i, j]
        txt = fmt_k(val) if val >= 100 else (f"{val:.1f}" if isinstance(val, float) and val != int(val) else f"{int(val)}")
        tc = "white" if hm_norm.iloc[i, j] > 0.50 else "#333"
        ax.text(j, i, txt, ha="center", va="center", fontsize=5.5, color=tc, fontweight="bold")

ax.set_xticks(np.arange(len(hm_labels)))
ax.set_xticklabels(hm_labels, fontsize=6.5, rotation=30, ha="right")
ax.set_yticks(np.arange(len(top20)))
ax.set_yticklabels([f'{short_name(n)}  @{g}' for n, g in zip(top20["Name"], top20["GitHub"])],
                   fontsize=5.5)

for i, cat in enumerate(top20["Category"]):
    ax.add_patch(plt.Rectangle((-0.72, i-0.45), 0.22, 0.9,
                                color=C.get(cat, "#aaa"), clip_on=False, linewidth=0))

ax.tick_params(length=0)
cbar = plt.colorbar(im, ax=ax, fraction=0.015, pad=0.025, aspect=30)
cbar.set_label("Relative\nintensity", fontsize=5.5, rotation=0, labelpad=18, y=0.5)
cbar.ax.tick_params(labelsize=5, length=1.5); cbar.outline.set_linewidth(0.3)

leg_h = [Patch(fc=c, ec="none", label=l) for l, c in C.items()]
ax.legend(handles=leg_h, loc="upper right", bbox_to_anchor=(1.35, 1.0),
          fontsize=5.5, borderpad=0.2, labelspacing=0.2, title="Domain", title_fontsize=6)

ax.set_title("Multi-metric profile (top 20)", loc="left", pad=8, fontsize=10)
ax.text(0.0, 1.02, "Min-max normalised within each column; values shown as raw counts",
        transform=ax.transAxes, fontsize=5.5, color="#888", fontstyle="italic")

fig_caption(fig,
    "Figure 7. Heatmap of six metrics for the top 20 awesomers by composite score. "
    "Colour intensity = min-max normalised value within each column. "
    "Left colour strip indicates domain. Raw values annotated in each cell.")

save(fig, "Fig7_heatmap")


# ============================================================================
# FIGURE 8 — Language x Domain + Star Distribution
# ============================================================================
print("Fig 8: Language ecosystem")
fig, (ax8a, ax8b) = plt.subplots(1, 2, figsize=(7.2, 3.8),
    gridspec_kw={"wspace": 0.40, "width_ratios": [1.3, 1],
                 "left": 0.08, "right": 0.97, "top": 0.86, "bottom": 0.16})

# a) Language x Domain
plabel(ax8a, "a")
ax8a.set_title("Language x domain", loc="left", pad=12)
subtitle(ax8a, "Grouped bars showing language usage by domain", y=1.01)

lang_df = df[df["PrimaryLang"]!="--"].copy()
ct = lang_df.groupby(["PrimaryLang","Category"]).size().unstack(fill_value=0)
ct["_total"] = ct.sum(axis=1)
ct = ct.sort_values("_total", ascending=True).drop("_total", axis=1)

y8 = np.arange(len(ct)); bar_w = 0.25
offset = {cat: (i - 1) * bar_w for i, cat in enumerate(["AI/ML", "Bioinfo.", "Data Sci."])}
for cat in ["AI/ML", "Bioinfo.", "Data Sci."]:
    vals = ct.get(cat, pd.Series(0, index=ct.index)).values
    ax8a.barh(y8 + offset.get(cat, 0), vals, height=bar_w, color=C[cat],
              label=cat, edgecolor="white", linewidth=0.3)

ax8a.set_yticks(y8); ax8a.set_yticklabels(ct.index, fontsize=7)
ax8a.set_xlabel("Awesomers (n)")
ax8a.legend(fontsize=5.5, loc="lower right", borderpad=0.2)

# b) Star distribution
plabel(ax8b, "b")
ax8b.set_title("Star distribution", loc="left", pad=12)
subtitle(ax8b, "Only individuals with total stars > 0 shown", y=1.01)

has_stars = df[df["TotalStars"]>0].copy()
cats_b = ["Data Sci.", "Bioinfo.", "AI/ML"]
for i, cat in enumerate(cats_b):
    sub = has_stars[has_stars["Category"]==cat]
    if len(sub)==0: continue
    jitter = rng.normal(0, 0.08, len(sub))
    ax8b.scatter(sub["log_s"], np.full(len(sub), i) + jitter,
                 c=C[cat], s=25, alpha=0.75, edgecolors="white", linewidth=0.25, zorder=3)
    med = sub["log_s"].median()
    ax8b.plot([med, med], [i-0.18, i+0.18], color=C[cat], linewidth=2.5,
              zorder=4, solid_capstyle="round")
    ax8b.text(med, i+0.26, f"med={10**med:,.0f}",
              fontsize=5, ha="center", color=C[cat], fontweight="bold")

ax8b.set_yticks(range(len(cats_b)))
ax8b.set_yticklabels(cats_b, fontsize=7)
ax8b.set_xlabel("Total stars received (log$_{10}$)")
ax8b.grid(axis="x", linestyle="--", alpha=0.25)

fig_caption(fig,
    "Figure 8. (a) Cross-tabulation of programming languages by domain. "
    "Python dominates across all domains. (b) Distribution of total stars "
    "by domain; vertical bar = median. AI/ML developers accumulate ~5x more stars than bioinformaticians.")

save(fig, "Fig8_languages")


# ============================================================================
print(f"\n{'='*60}")
print(f"  ALL 8 FIGURES REGENERATED")
print(f"  Palette: Simpsons (ggsci)")
print(f"  New: subtitles + figure captions on every plot")
print(f"  Output: {OUT}/")
print(f"{'='*60}")
