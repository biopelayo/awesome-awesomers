"""
Awesome Awesomers — Master Figure Generator
=============================================
Phase 1 (awesomers) + Phase 2 (awesome repos ecosystem)
4 palettes: Simpsons, Futurama, JAMA, Lancet
Publication-quality (300 dpi PNG + PDF vector)
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Patch, FancyBboxPatch
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec
import matplotlib.patheffects as pe
import numpy as np
import networkx as nx
from scipy import stats as sp_stats
from adjustText import adjust_text
from datetime import datetime
import warnings, os, sys
warnings.filterwarnings("ignore")

# ============================================================================
# PALETTES (ggsci-inspired)
# ============================================================================
PALETTES = {
    "simpsons": {
        "name": "Simpsons",
        "colors": ["#FED439","#709AE1","#8A9197","#D2AF81","#FD7446",
                    "#D5E4A2","#197EC0","#F05C3B","#46732E","#71D0F5",
                    "#370335","#075149","#C80813","#91331F","#1A9993","#FD8CC1"],
        "bg": "#FEFEFE",
        "accent": "#FD7446",
        "text": "#2b2b2b",
        "grid": "#e8e8e8",
    },
    "futurama": {
        "name": "Futurama",
        "colors": ["#FF6F00","#C71000","#008EA0","#8A4198","#5A9599",
                    "#FF6348","#84D7E1","#FF95A8","#3D3B25","#ADE2D0",
                    "#1A5354","#3F4041","#FFA500","#4B0082","#2E8B57","#DC143C"],
        "bg": "#FEFEFE",
        "accent": "#FF6F00",
        "text": "#1a1a1a",
        "grid": "#e5e5e5",
    },
    "jama": {
        "name": "JAMA",
        "colors": ["#374E55","#DF8F44","#00A1D5","#B24745","#79AF97",
                    "#6A6599","#80796B","#D4A017","#3C5488","#E64B35",
                    "#00A087","#F39B7F","#8491B4","#91D1C2","#B09C85","#7E6148"],
        "bg": "#FEFEFE",
        "accent": "#DF8F44",
        "text": "#1a1a1a",
        "grid": "#e8e8e8",
    },
    "lancet": {
        "name": "Lancet",
        "colors": ["#00468B","#ED0000","#42B540","#0099B4","#925E9F",
                    "#FDAF91","#AD002A","#ADB6B6","#1B1919","#F0E685",
                    "#3C5488","#E64B35","#00A087","#F39B7F","#8491B4","#DC0000"],
        "bg": "#FEFEFE",
        "accent": "#ED0000",
        "text": "#1a1a1a",
        "grid": "#e0e0e0",
    },
}

# ============================================================================
# PHASE 1 DATA: Awesomers (people)
# ============================================================================
p1_raw = [
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
    ("Laurens vd Maaten","AI/ML","lvdmaaten",1975,23,0,"--",0,"--","--","G"),
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
    ("Lior Pachter","Bioinfo.","pachterlab",377,169,0,"--",0,"--","--","S"),
    ("Boas Pucker","Bioinfo.","bpucker",187,80,0,"--",0,"Python","--","S"),
    ("Sahar Mor","AI/ML","saharmor",205,86,0,"--",0,"--","--","S"),
    ("Ben Johnson","Bioinfo.","biobenkj",121,132,0,"--",0,"--","--","G"),
    ("Dean Lee","Bioinfo.","deanslee",118,2,0,"--",0,"--","--","S"),
    ("Oriol Vinyals","AI/ML","OriolVinyals",84,3,0,"--",0,"--","--","G"),
]

p1_cols = ["Name","Category","GitHub","Followers","Repos","TotalStars",
           "TopRepo","TopStars","PrimaryLang","LastPush","Source"]
df1 = pd.DataFrame(p1_raw, columns=p1_cols)
df1["log_f"] = np.log10(df1["Followers"].clip(lower=1))
df1["log_r"] = np.log10(df1["Repos"].clip(lower=1))
df1["log_s"] = np.log10(df1["TotalStars"].clip(lower=1))
df1["spr"] = (df1["TotalStars"] / df1["Repos"].clip(lower=1)).round(0)
df1["fpr"] = (df1["Followers"] / df1["Repos"].clip(lower=1)).round(0)
df1["score"] = (df1["log_f"]*0.40 + df1["log_s"]*0.35 + df1["log_r"]*0.25).round(2)
today = datetime(2026, 3, 17)
def parse_date(d):
    if d == "--": return None
    try: return datetime.strptime(d, "%Y-%m-%d")
    except: return None
df1["last_dt"] = df1["LastPush"].apply(parse_date)
df1["days_since"] = df1["last_dt"].apply(lambda x: (today - x).days if x else None)

# ============================================================================
# PHASE 2 DATA: Awesome repos ecosystem (fresh scrape 2026-03-17)
# ============================================================================
p2_repos_raw = [
    ("sindresorhus/awesome",446331,"sindresorhus","Meta",33594),
    ("vinta/awesome-python",287631,"vinta","Python",27420),
    ("awesome-selfhosted/awesome-selfhosted",280586,"awesome-selfhosted","DevOps",12886),
    ("avelino/awesome-go",167576,"avelino","Go",13066),
    ("Hack-with-Github/Awesome-Hacking",108547,"Hack-with-Github","Security",10062),
    ("Shubhamsaboo/awesome-llm-apps",102573,"Shubhamsaboo","AI/LLM",14953),
    ("jaywcjlove/awesome-mac",100351,"jaywcjlove","Tools",7501),
    ("MunGell/awesome-for-beginners",83601,"MunGell","Education",7794),
    ("punkpeye/awesome-mcp-servers",83355,"punkpeye","AI/LLM",8280),
    ("DopplerHQ/awesome-interview-questions",81471,"DopplerHQ","Career",9390),
    ("FortAwesome/Font-Awesome",76422,"FortAwesome","Frontend",12242),
    ("vuejs/awesome-vue",73619,"vuejs","Frontend",9494),
    ("awesomedata/awesome-public-datasets",73456,"awesomedata","Data",11194),
    ("enaqx/awesome-react",72413,"enaqx","Frontend",7536),
    ("josephmisiti/awesome-machine-learning",72017,"josephmisiti","ML",15343),
    ("fffaraz/awesome-cpp",70274,"fffaraz","C++",8253),
    ("binhnguyennus/awesome-scalability",69466,"binhnguyennus","Architecture",6892),
    ("prakhar1989/awesome-courses",67078,"prakhar1989","Education",8335),
    ("sindresorhus/awesome-nodejs",65315,"sindresorhus","Node.js",6204),
    ("xingshaocheng/architect-awesome",60843,"xingshaocheng","Architecture",17785),
    ("Solido/awesome-flutter",59299,"Solido","Mobile",6873),
    ("PlexPt/awesome-chatgpt-prompts-zh",58751,"PlexPt","AI/LLM",13574),
    ("rust-unofficial/awesome-rust",56196,"rust-unofficial","Rust",3233),
    ("wasabeef/awesome-android-ui",55672,"wasabeef","Mobile",10276),
    ("vsouza/awesome-ios",51553,"vsouza","Mobile",6964),
    ("justjavac/awesome-wechat-weapp",50630,"justjavac","Frontend",9014),
    ("akullpp/awesome-java",47331,"akullpp","Java",7649),
    ("brillout/awesome-react-components",47060,"brillout","Frontend",3744),
    ("DovAmir/awesome-design-patterns",46448,"DovAmir","Architecture",3219),
    ("LeCoupa/awesome-cheatsheets",45493,"LeCoupa","Education",6673),
    ("docker/awesome-compose",44414,"docker","DevOps",8083),
    ("lukasz-madon/awesome-remote-job",44102,"lukasz-madon","Career",4497),
    ("goabstract/Awesome-Design-Tools",39294,"goabstract","Design",2205),
    ("PatrickJS/awesome-cursorrules",38530,"PatrickJS","AI/LLM",3259),
    ("alebcay/awesome-shell",36656,"alebcay","Tools",2480),
    ("deepseek-ai/awesome-deepseek-integration",35941,"deepseek-ai","AI/LLM",3994),
    ("veggiemonk/awesome-docker",35692,"veggiemonk","DevOps",3257),
    ("ashishps1/awesome-system-design-resources",35216,"ashishps1","Architecture",7720),
    ("sorrycc/awesome-javascript",34931,"sorrycc","Frontend",4525),
    ("kuchin/awesome-cto",34522,"kuchin","Leadership",2168),
    ("bayandin/awesome-awesomeness",33283,"bayandin","Meta",3591),
    ("awesome-foss/awesome-sysadmin",33238,"awesome-foss","DevOps",1958),
    ("ziadoz/awesome-php",32427,"ziadoz","PHP",5149),
    ("herrbischoff/awesome-macos-command-line",30353,"herrbischoff","Tools",1433),
    ("hehonghui/awesome-english-ebooks",29612,"hehonghui","Education",2401),
    ("abhisheknaiidu/awesome-github-profile-readme",29386,"abhisheknaiidu","Meta",4303),
    ("academic/awesome-datascience",28642,"academic","Data",6409),
    ("ChristosChristofidis/awesome-deep-learning",27711,"ChristosChristofidis","DL",6291),
    ("sdras/awesome-actions",27555,"sdras","DevOps",1618),
    ("kdeldycke/awesome-falsehood",27176,"kdeldycke","Education",633),
    ("posquit0/Awesome-CV",27038,"posquit0","Career",5202),
    ("e2b-dev/awesome-ai-agents",26487,"e2b-dev","AI/LLM",2422),
    ("Hannibal046/Awesome-LLM",26470,"Hannibal046","AI/LLM",2356),
    ("terryum/awesome-deep-learning-papers",26095,"terryum","DL",4449),
    ("matteocrippa/awesome-swift",25951,"matteocrippa","Mobile",3117),
    ("enaqx/awesome-pentest",25565,"enaqx","Security",4762),
    ("aishwaryanr/awesome-generative-ai-guide",25370,"aishwaryanr","AI/LLM",5364),
    ("wilsonfreitas/awesome-quant",24958,"wilsonfreitas","Data",3295),
    ("tayllan/awesome-algorithms",24834,"tayllan","Education",2939),
    ("jbhuang0604/awesome-computer-vision",23118,"jbhuang0604","DL",4432),
    ("djsime1/awesome-flipperzero",23010,"djsime1","Security",1002),
    ("ashishps1/awesome-low-level-design",22767,"ashishps1","Architecture",5594),
    ("HqWu-HITCS/Awesome-Chinese-LLM",22405,"HqWu-HITCS","AI/LLM",2116),
    ("quozd/awesome-dotnet",21173,"quozd",".NET",2850),
    # Bioinformatics awesome repos (lower threshold)
    ("danielecook/Awesome-Bioinformatics",3900,"danielecook","Bioinformatics",544),
    ("gokceneraslan/awesome-deepbio",1968,"gokceneraslan","Bioinformatics",320),
    ("j-andrews7/awesome-bioinformatics-benchmarks",355,"j-andrews7","Bioinformatics",42),
    ("lskatz/awesome-bioinformatics-education",102,"lskatz","Bioinformatics",18),
    ("twoXes/awesome-structural-bioinformatics",76,"twoXes","Bioinformatics",12),
    ("kmhernan/awesome-bioinformatics-formats",54,"kmhernan","Bioinformatics",8),
]
p2r_df = pd.DataFrame(p2_repos_raw, columns=["Repo","Stars","Owner","Domain","Forks"])

# Phase 2 curators (fresh scrape)
p2_curators_raw = [
    ("Sindre Sorhus","sindresorhus",77927,1133,"Meta","awesome",446331),
    ("Vinta Chen","vinta",9112,28,"Python","awesome-python",287631),
    ("Avelino","avelino",6268,241,"Go","awesome-go",167576),
    ("Shubham Saboo","Shubhamsaboo",7615,164,"AI/LLM","awesome-llm-apps",102573),
    ("Kenny Wong","jaywcjlove",9005,211,"Tools","awesome-mac",100351),
    ("Shmavon Gazanchyan","MunGell",2303,137,"Education","awesome-for-beginners",83601),
    ("Frank Fiegel","punkpeye",1721,4827,"AI/LLM","awesome-mcp-servers",83355),
    ("Joseph Misiti","josephmisiti",4430,291,"ML","awesome-machine-learning",72017),
    ("J. Le Coupanec","LeCoupa",2774,20,"Education","awesome-cheatsheets",45493),
    ("PatrickJS","PatrickJS",3507,961,"AI/LLM","awesome-cursorrules",38530),
    ("Ashish P. Singh","ashishps1",12684,42,"Architecture","awesome-system-design",35216),
    ("Julien Bisconti","veggiemonk",680,182,"DevOps","awesome-docker",35692),
    ("Lukasz Madon","lukasz-madon",667,59,"Career","awesome-remote-job",44102),
    ("Sarah Drasner","sdras",24842,102,"DevOps","awesome-actions",27555),
    ("sorrycc","sorrycc",14677,250,"Frontend","awesome-javascript",34931),
    ("Wasabeef","wasabeef",9614,58,"Mobile","awesome-android-ui",55672),
    ("Prakhar Srivastav","prakhar1989",6451,178,"Education","awesome-courses",67078),
    ("Kevin Deldycke","kdeldycke",1881,54,"Education","awesome-falsehood",27176),
    ("Christos Christofidis","ChristosChristofidis",1351,140,"DL","awesome-deep-learning",27711),
    ("Terry T. Um","terryum",1486,7,"DL","awesome-deep-learning-papers",26095),
    ("Alexander Bayandin","bayandin",720,27,"Meta","awesome-awesomeness",33283),
    ("Dima Kuchin","kuchin",635,13,"Leadership","awesome-cto",34522),
    ("Daniel Cook","danielecook",415,76,"Bioinformatics","Awesome-Bioinformatics",3900),
    ("Gokcen Eraslan","gokceneraslan",483,101,"Bioinformatics","awesome-deepbio",1968),
    ("Jia-Bin Huang","jbhuang0604",1971,23,"DL","awesome-computer-vision",23118),
    ("Wilson Freitas","wilsonfreitas",1429,122,"Data","awesome-quant",24958),
    ("enaqx","enaqx",2612,54,"Frontend","awesome-react",72413),
]
p2c_df = pd.DataFrame(p2_curators_raw, columns=["Name","GitHub","Followers","Repos","Domain","TopAwesome","TopStars"])
p2c_df["log_f"] = np.log10(p2c_df["Followers"].clip(lower=1))
p2c_df["log_top"] = np.log10(p2c_df["TopStars"].clip(lower=1))
p2c_df["log_r"] = np.log10(p2c_df["Repos"].clip(lower=1))
p2c_df["curator_score"] = (p2c_df["log_top"]*0.50 + p2c_df["log_f"]*0.30 + p2c_df["log_r"]*0.20).round(2)

# Phase 1 github set for cross-reference
p1_ghset = set(df1["GitHub"])

# ============================================================================
# HELPERS
# ============================================================================
def fmt_k(v):
    if v >= 1e6: return f"{v/1e6:.1f}M"
    if v >= 10000: return f"{v/1000:.0f}k"
    if v >= 1000: return f"{v/1000:.1f}k"
    return str(int(v))

def short_name(n, maxlen=18):
    if len(n) <= maxlen: return n
    parts = n.split()
    if len(parts) >= 2: return f"{parts[0][0]}. {parts[-1]}"
    return n[:maxlen]

def plabel(ax, letter, x=-0.06, y=1.03):
    ax.text(x, y, letter, transform=ax.transAxes, fontsize=11,
            fontweight="bold", va="top", ha="left", fontfamily="Arial")

def subtitle(ax, text, x=0.0, y=1.0):
    ax.text(x, y, text, transform=ax.transAxes, fontsize=6.5,
            color="#777", va="top", ha="left", fontstyle="italic")

def caption(fig, text, y=0.005):
    fig.text(0.05, y, text, fontsize=5.5, color="#999", fontstyle="italic",
             va="bottom", ha="left", wrap=True)

def setup_style(pal):
    p = PALETTES[pal]
    plt.rcParams.update({
        "figure.facecolor": p["bg"], "axes.facecolor": p["bg"],
        "axes.edgecolor": "#999", "axes.labelcolor": p["text"],
        "axes.linewidth": 0.5, "axes.spines.top": False, "axes.spines.right": False,
        "xtick.color": "#666", "ytick.color": "#666",
        "xtick.major.width": 0.4, "ytick.major.width": 0.4,
        "xtick.major.size": 2.5, "ytick.major.size": 2.5,
        "xtick.major.pad": 2, "ytick.major.pad": 2,
        "text.color": p["text"],
        "font.family": "sans-serif", "font.sans-serif": ["Arial"],
        "font.size": 7, "axes.titlesize": 9, "axes.labelsize": 7,
        "legend.fontsize": 6, "legend.frameon": False,
        "grid.color": p["grid"], "grid.linewidth": 0.3,
        "figure.dpi": 200, "savefig.dpi": 300,
        "savefig.bbox": "tight", "savefig.pad_inches": 0.04,
    })
    return p

def get_domain_colors(pal_colors):
    """Map domains to palette colors deterministically."""
    domains = ["AI/ML","Bioinfo.","Data Sci.","AI/LLM","ML","DL","Frontend","Mobile",
               "DevOps","Security","Architecture","Education","Data","Career",
               "Tools","Meta","Leadership","Python","Go","C++","Rust","Java",
               "Node.js","PHP",".NET","Design","Bioinformatics"]
    return {d: pal_colors[i % len(pal_colors)] for i, d in enumerate(domains)}

# ============================================================================
# FIGURE GENERATION
# ============================================================================
def generate_all_figures(pal_key):
    p = setup_style(pal_key)
    C = p["colors"]
    DC = get_domain_colors(C)
    OUT = f"D:/Antigravity/awesome-awesomers/plots/{pal_key}"
    os.makedirs(OUT, exist_ok=True)

    # Short alias
    c1, c2, c3, c4, c5, c6 = C[0], C[1], C[2], C[3], C[4], C[5]

    # ========================================================================
    # FIG 1: Phase 1 Overview (4 tight panels)
    # ========================================================================
    fig = plt.figure(figsize=(7.2, 5.8))
    gs = GridSpec(2, 2, hspace=0.38, wspace=0.35,
                  left=0.08, right=0.97, top=0.92, bottom=0.10)

    # 1a: Category distribution (horizontal lollipop)
    ax = fig.add_subplot(gs[0, 0])
    plabel(ax, "a")
    cats = df1["Category"].value_counts().sort_values()
    y = np.arange(len(cats))
    cat_c = [DC.get(c, C[7]) for c in cats.index]
    ax.hlines(y, 0, cats.values, color=[c+"88" for c in cat_c], linewidth=1.5)
    ax.scatter(cats.values, y, c=cat_c, s=35, zorder=3, edgecolors="white", linewidth=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(cats.index, fontsize=6)
    for i, v in enumerate(cats.values):
        ax.text(v + 0.3, i, str(v), va="center", fontsize=6, fontweight="bold", color=cat_c[i])
    ax.set_xlabel("Count", fontsize=6.5)
    ax.set_title("Category distribution", fontweight="bold", loc="left", fontsize=8, pad=2)
    subtitle(ax, "n = 39 awesomers", y=-0.08)
    ax.set_xlim(0, cats.max() + 2)

    # 1b: Source (seed vs graph) donut
    ax = fig.add_subplot(gs[0, 1])
    plabel(ax, "b")
    src = df1["Source"].value_counts()
    wedges, texts, autotexts = ax.pie(
        src.values, labels=None, colors=[c1, c2],
        autopct=lambda p: f'{p:.0f}%', startangle=90,
        pctdistance=0.75, wedgeprops=dict(width=0.35, edgecolor="white", linewidth=1.5))
    for t in autotexts: t.set_fontsize(7); t.set_fontweight("bold")
    ax.text(0, 0, f"n={len(df1)}", ha="center", va="center", fontsize=9, fontweight="bold", color=p["text"])
    ax.legend([f"Seed ({src.get('S',0)})", f"Graph ({src.get('G',0)})"],
              loc="lower center", fontsize=6, ncol=2, bbox_to_anchor=(0.5, -0.08))
    ax.set_title("Discovery source", fontweight="bold", loc="left", fontsize=8, pad=2)

    # 1c: Language bar
    ax = fig.add_subplot(gs[1, 0])
    plabel(ax, "c")
    langs = df1[df1["PrimaryLang"] != "--"]["PrimaryLang"].value_counts().sort_values()
    y = np.arange(len(langs))
    lang_c = [C[i % len(C)] for i in range(len(langs))]
    ax.barh(y, langs.values, height=0.6, color=lang_c, edgecolor="white", linewidth=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(langs.index, fontsize=6)
    for i, v in enumerate(langs.values):
        ax.text(v + 0.15, i, str(v), va="center", fontsize=5.5, color="#666")
    ax.set_xlabel("Count", fontsize=6.5)
    ax.set_title("Primary language", fontweight="bold", loc="left", fontsize=8, pad=2)

    # 1d: Followers strip by category
    ax = fig.add_subplot(gs[1, 1])
    plabel(ax, "d")
    cat_order = df1.groupby("Category")["Followers"].median().sort_values().index.tolist()
    for i, cat in enumerate(cat_order):
        vals = df1[df1["Category"]==cat]["Followers"]
        ax.scatter(np.log10(vals.clip(lower=1)), [i]*len(vals),
                   c=DC.get(cat, C[0]), s=20, alpha=0.8, edgecolors="white", linewidth=0.3, zorder=3)
        med = vals.median()
        ax.plot(np.log10(max(med,1)), i, "D", color="black", markersize=4, zorder=4)
    ax.set_yticks(range(len(cat_order)))
    ax.set_yticklabels(cat_order, fontsize=6)
    ax.set_xlabel("Followers (log₁₀)", fontsize=6.5)
    ax.set_title("Followers by category", fontweight="bold", loc="left", fontsize=8, pad=2)
    subtitle(ax, "◆ = median", y=-0.08)
    ax.grid(axis="x", linestyle="--", alpha=0.3)

    caption(fig, f"Fig. 1 | Phase 1 overview. (a) Category distribution of {len(df1)} awesomers. "
            f"(b) Discovery source: seed from LinkedIn/web vs. graph expansion via GitHub following. "
            f"(c) Primary programming language. (d) Followers distribution by category (log scale); diamonds = medians. "
            f"Data: GitHub API, scraped 2026-03-17. Palette: {p['name']}.")

    fig.savefig(f"{OUT}/Fig1_overview.png")
    fig.savefig(f"{OUT}/Fig1_overview.pdf")
    plt.close(fig)
    print(f"  [OK] Fig1 overview")

    # ========================================================================
    # FIG 2: Score ranking + decomposition
    # ========================================================================
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 6.2),
        gridspec_kw={"width_ratios": [1.3, 1], "wspace": 0.40,
                     "left": 0.22, "right": 0.97, "top": 0.93, "bottom": 0.10})

    # 2a: Cleveland dot plot
    ax = axes[0]
    plabel(ax, "a", x=-0.25)
    ranked = df1.nlargest(25, "score").sort_values("score", ascending=True)
    y = np.arange(len(ranked))
    ax.hlines(y, 0, ranked["score"], color=p["grid"], linewidth=0.6)
    ax.scatter(ranked["score"], y, c=c1, s=30, zorder=3, edgecolors="#333", linewidth=0.3)
    ax.set_yticks(y)
    labels = [f'{short_name(r["Name"],14)}' for _, r in ranked.iterrows()]
    ax.set_yticklabels(labels, fontsize=5.5)
    for i, (_, row) in enumerate(ranked.iterrows()):
        ax.text(row["score"] + 0.03, i, f'{row["score"]:.1f}', va="center", fontsize=5, color="#888")
    # Bold top 5
    for tick in ax.get_yticklabels()[-5:]:
        tick.set_fontweight("bold")
    ax.set_xlabel("Influence Score", fontsize=6.5)
    ax.set_title("Top 25 awesomers", fontweight="bold", loc="left", fontsize=8, pad=2)
    subtitle(ax, "Score = 0.4·log₁₀(followers) + 0.35·log₁₀(stars) + 0.25·log₁₀(repos)", x=0.0, y=-0.05)
    ax.set_xlim(0, ranked["score"].max() + 0.35)

    # 2b: Score decomposition (stacked bar)
    ax = axes[1]
    plabel(ax, "b", x=-0.12)
    ranked2 = ranked.copy()
    comp_f = ranked2["log_f"] * 0.40
    comp_s = ranked2["log_s"] * 0.35
    comp_r = ranked2["log_r"] * 0.25
    ax.barh(y, comp_f.values, height=0.55, color=c1, label="Followers", edgecolor="white", linewidth=0.3)
    ax.barh(y, comp_s.values, height=0.55, left=comp_f.values, color=c2, label="Stars", edgecolor="white", linewidth=0.3)
    ax.barh(y, comp_r.values, height=0.55, left=(comp_f+comp_s).values, color=c3, label="Repos", edgecolor="white", linewidth=0.3)
    ax.set_yticks([])
    ax.set_xlabel("Score components", fontsize=6.5)
    ax.set_title("Score decomposition", fontweight="bold", loc="left", fontsize=8, pad=2)
    ax.legend(loc="lower right", fontsize=5.5, ncol=1)

    caption(fig, f"Fig. 2 | Influence score ranking. (a) Top 25 awesomers by composite score. "
            f"(b) Score decomposition into follower, star, and repo components. "
            f"Palette: {p['name']}.")

    fig.savefig(f"{OUT}/Fig2_score.png")
    fig.savefig(f"{OUT}/Fig2_score.pdf")
    plt.close(fig)
    print(f"  [OK] Fig2 score")

    # ========================================================================
    # FIG 3: Scatter repos vs followers + marginals
    # ========================================================================
    fig = plt.figure(figsize=(5.5, 5.0))
    gs = GridSpec(2, 2, width_ratios=[4,1], height_ratios=[1,4],
                  hspace=0.04, wspace=0.04,
                  left=0.12, right=0.95, top=0.92, bottom=0.12)

    ax_main = fig.add_subplot(gs[1, 0])
    ax_top = fig.add_subplot(gs[0, 0], sharex=ax_main)
    ax_right = fig.add_subplot(gs[1, 1], sharey=ax_main)
    fig.add_subplot(gs[0, 1]).axis("off")

    has_data = df1[(df1["TotalStars"] > 0) & (df1["Repos"] > 0)].copy()
    cat_colors = [DC.get(c, C[7]) for c in has_data["Category"]]

    ax_main.scatter(has_data["log_r"], has_data["log_f"], c=cat_colors,
                    s=np.clip(has_data["log_s"]*12, 15, 120), alpha=0.85,
                    edgecolors="#333", linewidth=0.3, zorder=3)

    # Labels
    texts = []
    for _, row in has_data.iterrows():
        sn = row["GitHub"][:12]
        t = ax_main.text(row["log_r"], row["log_f"], sn, fontsize=4.5, color="#555")
        texts.append(t)
    if texts:
        adjust_text(texts, ax=ax_main, arrowprops=dict(arrowstyle="-", color="#ccc", lw=0.2),
                    force_text=(0.3, 0.3), max_move=2.0)

    # Correlation
    r, pv = sp_stats.pearsonr(has_data["log_r"], has_data["log_f"])
    ax_main.text(0.97, 0.03, f"r = {r:.2f}, p = {pv:.1e}", transform=ax_main.transAxes,
                 fontsize=5.5, ha="right", color="#888")

    ax_main.set_xlabel("Repos (log₁₀)", fontsize=6.5)
    ax_main.set_ylabel("Followers (log₁₀)", fontsize=6.5)
    ax_main.grid(True, linestyle="--", alpha=0.2)

    # Marginals
    for cat in has_data["Category"].unique():
        sub = has_data[has_data["Category"]==cat]
        color = DC.get(cat, C[7])
        ax_top.hist(sub["log_r"], bins=8, alpha=0.5, color=color, edgecolor="white", linewidth=0.3)
        ax_right.hist(sub["log_f"], bins=8, alpha=0.5, color=color, edgecolor="white", linewidth=0.3, orientation="horizontal")

    ax_top.set_title("Repos vs Followers landscape", fontweight="bold", loc="left", fontsize=8, pad=2)
    subtitle(ax_top, "Bubble size ∝ total stars", x=0.55, y=0.85)
    plt.setp(ax_top.get_xticklabels(), visible=False)
    plt.setp(ax_right.get_yticklabels(), visible=False)
    ax_top.tick_params(axis="x", length=0)
    ax_right.tick_params(axis="y", length=0)
    for a in [ax_top, ax_right]:
        a.spines["top"].set_visible(False)
        a.spines["right"].set_visible(False)

    # Legend
    cats_in_plot = has_data["Category"].unique()
    handles = [Line2D([0],[0], marker="o", color="w", markerfacecolor=DC.get(c, C[7]),
                       markersize=5, label=c) for c in cats_in_plot]
    ax_main.legend(handles=handles, loc="upper left", fontsize=5, ncol=1)

    caption(fig, f"Fig. 3 | Repos vs followers landscape. Bubble size proportional to total stars. "
            f"Colored marginal histograms by category. Pearson r = {r:.2f}. Palette: {p['name']}.")

    fig.savefig(f"{OUT}/Fig3_landscape.png")
    fig.savefig(f"{OUT}/Fig3_landscape.pdf")
    plt.close(fig)
    print(f"  [OK] Fig3 landscape")

    # ========================================================================
    # FIG 4: Social network
    # ========================================================================
    following_edges = [
        ("rasbt","karpathy"),("rasbt","fchollet"),("rasbt","soumith"),("rasbt","colah"),
        ("rasbt","rwightman"),("rasbt","mlabonne"),("rasbt","srush"),("rasbt","tridao"),
        ("rasbt","cbfinn"),("rasbt","lvdmaaten"),("rasbt","dpkingma"),("rasbt","Atcold"),
        ("rasbt","akosiorek"),("rasbt","GaelVaroquaux"),("rasbt","jakevdp"),
        ("rasbt","OriolVinyals"),("rasbt","DrJimFan"),
        ("crazyhottommy","lh3"),("crazyhottommy","hadley"),("crazyhottommy","rafalab"),
        ("crazyhottommy","shenwei356"),("crazyhottommy","ewels"),("crazyhottommy","arq5x"),
        ("crazyhottommy","lindenb"),("crazyhottommy","biobenkj"),("crazyhottommy","nh13"),
        ("crazyhottommy","thegenemyers"),("crazyhottommy","richarddurbin"),("crazyhottommy","bpucker"),
        ("geohot","karpathy"),("geohot","soumith"),("geohot","fchollet"),
        ("lh3","arq5x"),("lh3","richarddurbin"),("lh3","thegenemyers"),("lh3","lindenb"),
        ("nh13","lh3"),("nh13","ewels"),("nh13","arq5x"),
        ("bpucker","ewels"),("bpucker","crazyhottommy"),
        ("biopelayo","rasbt"),("biopelayo","crazyhottommy"),
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 4.5),
        gridspec_kw={"width_ratios": [2.5, 1], "wspace": 0.08,
                     "left": 0.02, "right": 0.98, "top": 0.92, "bottom": 0.10})

    G = nx.DiGraph()
    for _, row in df1.iterrows():
        G.add_node(row["GitHub"], cat=row["Category"], followers=row["Followers"], score=row["score"])
    G.add_node("biopelayo", cat="You", followers=1, score=0)
    for src, tgt in following_edges:
        if src in G and tgt in G:
            G.add_edge(src, tgt)

    pos = nx.kamada_kawai_layout(G)

    # Edges
    nx.draw_networkx_edges(G, pos, ax=ax1, edge_color="#ccc", width=0.4,
                           alpha=0.4, arrows=True, arrowsize=4, arrowstyle="-|>",
                           connectionstyle="arc3,rad=0.08")

    # Nodes by category
    for cat in df1["Category"].unique():
        nodes = [n for n in G if G.nodes[n].get("cat") == cat]
        sizes = [max(15, G.nodes[n].get("score", 1) * 12) for n in nodes]
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color=DC.get(cat, C[7]),
                               node_size=sizes, edgecolors="#444", linewidths=0.3,
                               alpha=0.9, ax=ax1)

    # biopelayo node
    if "biopelayo" in G:
        nx.draw_networkx_nodes(G, pos, nodelist=["biopelayo"], node_color=C[4],
                               node_size=60, edgecolors="#333", linewidths=0.8,
                               alpha=1.0, ax=ax1, node_shape="*")

    # Labels for top nodes
    top_nodes = df1.nlargest(12, "score")["GitHub"].tolist() + ["biopelayo"]
    labels = {n: n for n in top_nodes if n in G}
    nx.draw_networkx_labels(G, pos, labels, font_size=4.5, font_weight="bold",
                            font_color="#333", ax=ax1)

    ax1.set_title("Following network", fontweight="bold", loc="left", fontsize=8, pad=2)
    ax1.axis("off")

    # Legend
    cats_legend = list(df1["Category"].unique()) + ["You"]
    handles = [Line2D([0],[0], marker="o" if c!="You" else "*", color="w",
                       markerfacecolor=DC.get(c, C[4]), markersize=5 if c!="You" else 7,
                       label=c) for c in cats_legend]
    ax1.legend(handles=handles, loc="lower left", fontsize=5, ncol=2)

    # 4b: Betweenness centrality
    bc = nx.betweenness_centrality(G)
    bc_top = sorted(bc.items(), key=lambda x: x[1], reverse=True)[:15]
    names_bc = [x[0] for x in bc_top][::-1]
    vals_bc = [x[1] for x in bc_top][::-1]
    y = np.arange(len(names_bc))
    bc_colors = [DC.get(G.nodes[n].get("cat",""), C[7]) for n in names_bc]

    ax2.barh(y, vals_bc, height=0.55, color=bc_colors, edgecolor="white", linewidth=0.4)
    ax2.set_yticks(y)
    ax2.set_yticklabels(names_bc, fontsize=5, fontfamily="monospace")
    ax2.set_xlabel("Betweenness", fontsize=6)
    ax2.set_title("Centrality", fontweight="bold", loc="left", fontsize=8, pad=2)

    caption(fig, f"Fig. 4 | Social following network. Nodes sized by influence score, colored by category. "
            f"Edges = 'follows' relationships on GitHub. (b) Betweenness centrality top 15. "
            f"Palette: {p['name']}.")

    fig.savefig(f"{OUT}/Fig4_network.png")
    fig.savefig(f"{OUT}/Fig4_network.pdf")
    plt.close(fig)
    print(f"  [OK] Fig4 network")

    # ========================================================================
    # FIG 5: Activity + Efficiency quadrants
    # ========================================================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 4.2),
        gridspec_kw={"wspace": 0.32, "left": 0.08, "right": 0.97, "top": 0.90, "bottom": 0.14})

    active = df1[df1["days_since"].notna()].copy()

    # 5a: Activity timeline
    plabel(ax1, "a")
    act_sorted = active.sort_values("days_since", ascending=False)
    y = np.arange(len(act_sorted))
    act_colors = [DC.get(c, C[7]) for c in act_sorted["Category"]]

    ax1.barh(y, act_sorted["days_since"], height=0.6, color=act_colors, edgecolor="white", linewidth=0.3)
    ax1.set_yticks(y)
    ax1.set_yticklabels([short_name(n, 12) for n in act_sorted["Name"]], fontsize=4.5)
    ax1.set_xlabel("Days since last push", fontsize=6.5)
    ax1.set_title("Activity recency", fontweight="bold", loc="left", fontsize=8, pad=2)

    # Zone shading
    ax1.axvspan(0, 90, alpha=0.06, color="green")
    ax1.axvspan(90, 365, alpha=0.06, color="orange")
    ax1.axvspan(365, ax1.get_xlim()[1], alpha=0.06, color="red")
    ax1.text(45, len(act_sorted)-1, "Active", fontsize=5, ha="center", color="green", alpha=0.6)
    ax1.text(180, len(act_sorted)-1, "Moderate", fontsize=5, ha="center", color="orange", alpha=0.6)

    # 5b: Efficiency quadrants
    plabel(ax2, "b")
    eff = df1[(df1["TotalStars"]>0) & (df1["Followers"]>0)].copy()
    eff_colors = [DC.get(c, C[7]) for c in eff["Category"]]

    ax2.scatter(eff["log_r"], np.log10(eff["spr"].clip(lower=1)),
                c=eff_colors, s=np.clip(eff["log_f"]*15, 15, 100),
                alpha=0.8, edgecolors="#333", linewidth=0.3, zorder=3)

    # Labels
    texts = []
    for _, row in eff.iterrows():
        t = ax2.text(row["log_r"], np.log10(max(row["spr"],1)), row["GitHub"][:10],
                     fontsize=4, color="#666")
        texts.append(t)
    if texts:
        adjust_text(texts, ax=ax2, arrowprops=dict(arrowstyle="-", color="#ddd", lw=0.2))

    # Quadrant lines
    med_r = eff["log_r"].median()
    med_spr = np.log10(eff["spr"].clip(lower=1)).median()
    ax2.axhline(med_spr, color="#ccc", lw=0.5, ls="--")
    ax2.axvline(med_r, color="#ccc", lw=0.5, ls="--")

    ax2.set_xlabel("Repos (log₁₀)", fontsize=6.5)
    ax2.set_ylabel("Stars/repo (log₁₀)", fontsize=6.5)
    ax2.set_title("Efficiency quadrants", fontweight="bold", loc="left", fontsize=8, pad=2)
    subtitle(ax2, "Bubble size ∝ followers", x=0.55, y=1.0)

    # Quadrant labels
    xlim, ylim = ax2.get_xlim(), ax2.get_ylim()
    qstyle = dict(fontsize=5, alpha=0.35, fontstyle="italic", ha="center")
    ax2.text(med_r + (xlim[1]-med_r)/2, med_spr + (ylim[1]-med_spr)/2, "SUPERSTAR", **qstyle)
    ax2.text(med_r - (med_r-xlim[0])/2, med_spr + (ylim[1]-med_spr)/2, "FOCUSED\nEXPERT", **qstyle)
    ax2.text(med_r + (xlim[1]-med_r)/2, med_spr - (med_spr-ylim[0])/2, "PROLIFIC\nBUILDER", **qstyle)
    ax2.text(med_r - (med_r-xlim[0])/2, med_spr - (med_spr-ylim[0])/2, "EMERGING", **qstyle)

    caption(fig, f"Fig. 5 | Activity and efficiency. (a) Days since last GitHub push; green <90d, orange <365d, red >365d. "
            f"(b) Efficiency quadrants: repos vs. stars-per-repo (log scale). Bubble size ∝ followers. "
            f"Palette: {p['name']}.")

    fig.savefig(f"{OUT}/Fig5_activity.png")
    fig.savefig(f"{OUT}/Fig5_activity.pdf")
    plt.close(fig)
    print(f"  [OK] Fig5 activity")

    # ========================================================================
    # FIG 6: Bioinformatics deep-dive (3 panels)
    # ========================================================================
    bio = df1[df1["Category"]=="Bioinfo."].copy()

    fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.5),
        gridspec_kw={"wspace": 0.45, "left": 0.10, "right": 0.97, "top": 0.88, "bottom": 0.16})

    # 6a: Followers
    ax = axes[0]
    plabel(ax, "a")
    bsort = bio.sort_values("Followers", ascending=True)
    y = np.arange(len(bsort))
    ax.barh(y, bsort["Followers"], height=0.6, color=c2, edgecolor="white", linewidth=0.4)
    ax.set_yticks(y)
    ax.set_yticklabels([short_name(n, 14) for n in bsort["Name"]], fontsize=5)
    for i, v in enumerate(bsort["Followers"]):
        ax.text(v + 30, i, fmt_k(v), va="center", fontsize=4.5, color="#888")
    ax.set_xlabel("Followers", fontsize=6)
    ax.set_title("Followers", fontweight="bold", loc="left", fontsize=8, pad=2)

    # 6b: Repos
    ax = axes[1]
    plabel(ax, "b")
    bsort2 = bio.sort_values("Repos", ascending=True)
    y = np.arange(len(bsort2))
    ax.barh(y, bsort2["Repos"], height=0.6, color=c3, edgecolor="white", linewidth=0.4)
    ax.set_yticks(y)
    ax.set_yticklabels([short_name(n, 14) for n in bsort2["Name"]], fontsize=5)
    for i, v in enumerate(bsort2["Repos"]):
        ax.text(v + 1, i, str(v), va="center", fontsize=4.5, color="#888")
    ax.set_xlabel("Public repos", fontsize=6)
    ax.set_title("Productivity", fontweight="bold", loc="left", fontsize=8, pad=2)

    # 6c: Stars/repo (efficiency)
    ax = axes[2]
    plabel(ax, "c")
    bio_eff = bio[bio["TotalStars"]>0].copy()
    bio_eff = bio_eff.sort_values("spr", ascending=True)
    y = np.arange(len(bio_eff))
    ax.barh(y, bio_eff["spr"], height=0.6, color=c4, edgecolor="white", linewidth=0.4)
    ax.set_yticks(y)
    ax.set_yticklabels([short_name(n, 14) for n in bio_eff["Name"]], fontsize=5)
    for i, v in enumerate(bio_eff["spr"]):
        ax.text(v + 0.5, i, f"{v:.0f}", va="center", fontsize=4.5, color="#888")
    ax.set_xlabel("Stars/repo", fontsize=6)
    ax.set_title("Efficiency", fontweight="bold", loc="left", fontsize=8, pad=2)

    caption(fig, f"Fig. 6 | Bioinformatics deep-dive. (a) GitHub followers. (b) Public repos (productivity). "
            f"(c) Stars per repo (impact efficiency). Each panel independently sorted. "
            f"n = {len(bio)} bioinformaticians. Palette: {p['name']}.")

    fig.savefig(f"{OUT}/Fig6_bioinformatics.png")
    fig.savefig(f"{OUT}/Fig6_bioinformatics.pdf")
    plt.close(fig)
    print(f"  [OK] Fig6 bioinformatics")

    # ========================================================================
    # FIG 7: Heatmap multi-metric (top 20)
    # ========================================================================
    top20 = df1.nlargest(20, "score").copy()

    fig, ax = plt.subplots(figsize=(5.5, 5.5),
        gridspec_kw={"left": 0.22, "right": 0.92, "top": 0.92, "bottom": 0.12})

    metrics = ["Followers","Repos","TotalStars","spr","fpr","score"]
    metric_labels = ["Followers","Repos","Total Stars","Stars/repo","Followers/repo","Score"]

    hm_data = top20[metrics].copy()
    # Normalize each column 0-1
    for col in metrics:
        mx = hm_data[col].max()
        if mx > 0: hm_data[col] = hm_data[col] / mx

    # Sort by score
    hm_data = hm_data.sort_values("score", ascending=True)
    top20_sorted = top20.loc[hm_data.index]

    im = ax.imshow(hm_data.values, aspect="auto", cmap="YlOrRd", vmin=0, vmax=1)

    ax.set_yticks(range(len(hm_data)))
    ylabels = [f'@{row["GitHub"][:14]}' for _, row in top20_sorted.iterrows()]
    ax.set_yticklabels(ylabels, fontsize=5, fontfamily="monospace")
    ax.set_xticks(range(len(metric_labels)))
    ax.set_xticklabels(metric_labels, fontsize=5.5, rotation=35, ha="right")

    # Annotate cells with actual values
    raw_vals = top20_sorted[metrics].values
    for i in range(len(hm_data)):
        for j in range(len(metrics)):
            val = raw_vals[i, j]
            txt = fmt_k(val) if val >= 100 else f"{val:.1f}" if val < 10 else str(int(val))
            color = "white" if hm_data.values[i, j] > 0.6 else "#333"
            ax.text(j, i, txt, ha="center", va="center", fontsize=4, color=color)

    # Category color strip
    for i, (_, row) in enumerate(top20_sorted.iterrows()):
        ax.add_patch(FancyBboxPatch((-0.8, i-0.4), 0.3, 0.8,
                     boxstyle="round,pad=0.05", facecolor=DC.get(row["Category"], C[7]),
                     edgecolor="none", alpha=0.8, clip_on=False))

    ax.set_title("Multi-metric heatmap — Top 20", fontweight="bold", loc="left", fontsize=8, pad=4)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label("Normalized", fontsize=5.5)
    cbar.ax.tick_params(labelsize=5)

    caption(fig, f"Fig. 7 | Multi-metric heatmap. Each column normalized 0–1. Cell values show raw data. "
            f"Left color strip indicates category. Sorted by composite score. "
            f"Palette: {p['name']}.")

    fig.savefig(f"{OUT}/Fig7_heatmap.png")
    fig.savefig(f"{OUT}/Fig7_heatmap.pdf")
    plt.close(fig)
    print(f"  [OK] Fig7 heatmap")

    # ========================================================================
    # FIG 8 (P2): Top awesome-* repos + domain breakdown
    # ========================================================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 6.0),
        gridspec_kw={"width_ratios": [2, 1], "wspace": 0.35,
                     "left": 0.24, "right": 0.97, "top": 0.92, "bottom": 0.10})

    plabel(ax1, "a", x=-0.32)
    top30 = p2r_df.nlargest(30, "Stars").sort_values("Stars", ascending=True).copy()
    y = np.arange(len(top30))
    colors = [DC.get(d, C[7]) for d in top30["Domain"]]

    ax1.barh(y, top30["Stars"], height=0.62, color=colors, edgecolor="white", linewidth=0.3)
    ax1.set_yticks(y)
    labels = [r.split("/")[1][:30] for r in top30["Repo"]]
    ax1.set_yticklabels(labels, fontsize=4.5, fontfamily="monospace")
    ax1.set_xlabel("GitHub stars", fontsize=6.5)
    ax1.set_title("Top 30 awesome-* repositories", fontweight="bold", loc="left", fontsize=8, pad=2)
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: fmt_k(x)))

    for i, v in enumerate(top30["Stars"]):
        ax1.text(v + 1500, i, fmt_k(v), va="center", fontsize=4, color="#999")

    # 8b: Domain breakdown
    plabel(ax2, "b", x=-0.12)
    dom = p2r_df["Domain"].value_counts().sort_values()
    y2 = np.arange(len(dom))
    dom_c = [DC.get(d, C[7]) for d in dom.index]

    ax2.barh(y2, dom.values, height=0.55, color=dom_c, edgecolor="white", linewidth=0.4)
    ax2.set_yticks(y2)
    ax2.set_yticklabels(dom.index, fontsize=5.5)
    ax2.set_xlabel("Repos (n)", fontsize=6.5)
    ax2.set_title("Domain distribution", fontweight="bold", loc="left", fontsize=8, pad=2)
    for i, v in enumerate(dom.values):
        ax2.text(v + 0.1, i, str(v), va="center", fontsize=5.5, fontweight="bold", color=dom_c[i])

    caption(fig, f"Fig. 8 | Phase 2 — Awesome repos ecosystem. (a) Top 30 awesome-* repos by stars "
            f"(quality threshold: >1k stars for general, >50 for bioinformatics). "
            f"(b) Domain distribution across {len(p2r_df)} repos. Scraped 2026-03-17. Palette: {p['name']}.")

    fig.savefig(f"{OUT}/Fig8_P2_repos.png")
    fig.savefig(f"{OUT}/Fig8_P2_repos.pdf")
    plt.close(fig)
    print(f"  [OK] Fig8 P2 repos")

    # ========================================================================
    # FIG 9 (P2): Curator ranking + scatter
    # ========================================================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 5.5),
        gridspec_kw={"width_ratios": [1.3, 1], "wspace": 0.35,
                     "left": 0.20, "right": 0.97, "top": 0.92, "bottom": 0.10})

    # 9a: Curator score ranking
    plabel(ax1, "a", x=-0.22)
    ranked = p2c_df.sort_values("curator_score", ascending=True).copy()
    y = np.arange(len(ranked))
    cur_colors = [DC.get(d, C[7]) for d in ranked["Domain"]]

    ax1.hlines(y, 0, ranked["curator_score"], color=[c+"55" for c in cur_colors], linewidth=1)
    ax1.scatter(ranked["curator_score"], y, c=cur_colors, s=30, zorder=3,
                edgecolors="#333", linewidth=0.3)
    ax1.set_yticks(y)
    ax1.set_yticklabels([f'{short_name(row["Name"],14)}' for _, row in ranked.iterrows()],
                        fontsize=5)
    for i, (_, row) in enumerate(ranked.iterrows()):
        ax1.text(row["curator_score"] + 0.03, i, f'{row["curator_score"]:.1f}',
                 va="center", fontsize=4.5, color="#888")
    for tick in ax1.get_yticklabels()[-5:]:
        tick.set_fontweight("bold")
    ax1.set_xlabel("Curator Score", fontsize=6.5)
    ax1.set_title("Awesome curators ranking", fontweight="bold", loc="left", fontsize=8, pad=2)
    subtitle(ax1, "Score = 0.5·log₁₀(top_stars) + 0.3·log₁₀(followers) + 0.2·log₁₀(repos)",
             x=0.0, y=-0.05)

    # 9b: Personal followers vs top repo stars
    plabel(ax2, "b", x=-0.10)
    ax2.scatter(p2c_df["log_f"], p2c_df["log_top"], c=[DC.get(d, C[7]) for d in p2c_df["Domain"]],
                s=35, alpha=0.85, edgecolors="#333", linewidth=0.3, zorder=3)

    texts = []
    for _, row in p2c_df.iterrows():
        t = ax2.text(row["log_f"], row["log_top"], row["GitHub"][:12],
                     fontsize=4.5, color="#555", fontstyle="italic")
        texts.append(t)
    adjust_text(texts, ax=ax2, arrowprops=dict(arrowstyle="-", color="#ddd", lw=0.2))

    # Diagonal
    lims = [min(ax2.get_xlim()[0], ax2.get_ylim()[0]),
            max(ax2.get_xlim()[1], ax2.get_ylim()[1])]
    ax2.plot(lims, lims, "--", color="#ddd", lw=0.5, zorder=0)
    ax2.text(0.05, 0.92, "Above = repo > creator", transform=ax2.transAxes,
             fontsize=5, color="#bbb", fontstyle="italic")

    ax2.set_xlabel("Personal followers (log₁₀)", fontsize=6.5)
    ax2.set_ylabel("Top repo stars (log₁₀)", fontsize=6.5)
    ax2.set_title("Personal vs project influence", fontweight="bold", loc="left", fontsize=8, pad=2)
    ax2.grid(True, linestyle="--", alpha=0.2)

    caption(fig, f"Fig. 9 | Phase 2 — Curator profiles. (a) Curator score ranking. "
            f"(b) Personal followers vs. top awesome repo stars (log-log). Points above diagonal: "
            f"repo influence exceeds personal following. n = {len(p2c_df)} curators. Palette: {p['name']}.")

    fig.savefig(f"{OUT}/Fig9_P2_curators.png")
    fig.savefig(f"{OUT}/Fig9_P2_curators.pdf")
    plt.close(fig)
    print(f"  [OK] Fig9 P2 curators")

    # ========================================================================
    # FIG 10 (P2): Power law + bioinformatics zoom
    # ========================================================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.8),
        gridspec_kw={"wspace": 0.30, "left": 0.08, "right": 0.97, "top": 0.88, "bottom": 0.16})

    # 10a: Power law
    plabel(ax1, "a")
    sorted_stars = p2r_df["Stars"].sort_values(ascending=False).values
    rank = np.arange(1, len(sorted_stars) + 1)

    is_bio = p2r_df.sort_values("Stars", ascending=False)["Domain"].values == "Bioinformatics"
    colors_rank = [c2 if b else c1 for b in is_bio]

    ax1.scatter(rank, sorted_stars, c=colors_rank, s=20, alpha=0.85,
                edgecolors="#333", linewidth=0.25, zorder=3)
    ax1.set_yscale("log")
    ax1.set_xlabel("Rank", fontsize=6.5)
    ax1.set_ylabel("Stars (log)", fontsize=6.5)
    ax1.set_title("Stars power law", fontweight="bold", loc="left", fontsize=8, pad=2)
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: fmt_k(x)))
    ax1.grid(True, linestyle="--", alpha=0.2)

    # Annotate extremes
    for i, row in p2r_df.nlargest(3, "Stars").iterrows():
        r = np.where(sorted_stars == row["Stars"])[0][0] + 1
        ax1.annotate(row["Repo"].split("/")[1][:18], (r, row["Stars"]),
                     fontsize=4.5, color="#555", xytext=(4, 4), textcoords="offset points")

    ax1.legend([Line2D([0],[0],marker="o",color="w",markerfacecolor=c1,markersize=4),
                Line2D([0],[0],marker="o",color="w",markerfacecolor=c2,markersize=4)],
               ["General","Bioinformatics"], fontsize=5, loc="upper right")

    # 10b: Bioinformatics zoom
    plabel(ax2, "b")
    bio_r = p2r_df[p2r_df["Domain"]=="Bioinformatics"].sort_values("Stars", ascending=True).copy()
    y = np.arange(len(bio_r))
    ax2.barh(y, bio_r["Stars"], height=0.55, color=c2, edgecolor="white", linewidth=0.4)
    ax2.set_yticks(y)
    ax2.set_yticklabels([r.split("/")[1][:28] for r in bio_r["Repo"]], fontsize=5, fontfamily="monospace")
    ax2.set_xlabel("Stars", fontsize=6.5)
    ax2.set_title("Bioinformatics awesome repos", fontweight="bold", loc="left", fontsize=8, pad=2)

    for i, (_, row) in enumerate(bio_r.iterrows()):
        ax2.text(row["Stars"] + 15, i, f'{fmt_k(row["Stars"])} (@{row["Owner"][:12]})',
                 va="center", fontsize=4.5, color="#888")

    # Quality threshold
    ax2.axvline(1000, color=c1, lw=0.6, ls="--", alpha=0.5)
    ax2.text(1050, 0.3, ">1k threshold", fontsize=4.5, color=c1, alpha=0.6)

    caption(fig, f"Fig. 10 | Phase 2 — Stars distribution. (a) Power-law rank-stars plot; bioinformatics repos "
            f"highlighted. (b) Bioinformatics awesome repos zoom. Dashed line = 1k stars quality threshold. "
            f"Palette: {p['name']}.")

    fig.savefig(f"{OUT}/Fig10_P2_powerlaw.png")
    fig.savefig(f"{OUT}/Fig10_P2_powerlaw.pdf")
    plt.close(fig)
    print(f"  [OK] Fig10 P2 power law")

    # ========================================================================
    # FIG 11 (P2): Cross-reference Phase 1 × Phase 2 network
    # ========================================================================
    fig, ax = plt.subplots(figsize=(6.5, 5.0),
        gridspec_kw={"left": 0.02, "right": 0.98, "top": 0.92, "bottom": 0.08})

    G2 = nx.Graph()
    for _, row in p2c_df.iterrows():
        G2.add_node(row["GitHub"], type="curator", score=row["curator_score"],
                    in_p1=row["GitHub"] in p1_ghset)
        G2.add_node(row["TopAwesome"], type="repo", stars=row["TopStars"])
        G2.add_edge(row["GitHub"], row["TopAwesome"])

    pos2 = nx.kamada_kawai_layout(G2)

    nx.draw_networkx_edges(G2, pos2, ax=ax, edge_color="#ddd", width=0.5, alpha=0.4)

    cur_nodes = [n for n,d in G2.nodes(data=True) if d.get("type")=="curator"]
    repo_nodes = [n for n,d in G2.nodes(data=True) if d.get("type")=="repo"]

    # Curators: color by P1 overlap
    cur_c = [C[0] if G2.nodes[n].get("in_p1") else c1 for n in cur_nodes]
    cur_s = [max(20, G2.nodes[n].get("score",2)*15) for n in cur_nodes]
    nx.draw_networkx_nodes(G2, pos2, cur_nodes, node_color=cur_c, node_size=cur_s,
                           edgecolors="#333", linewidths=0.3, alpha=0.9, ax=ax)

    # Repos
    repo_s = [max(12, np.log10(max(G2.nodes[n].get("stars",1),1))*8) for n in repo_nodes]
    nx.draw_networkx_nodes(G2, pos2, repo_nodes, node_color=c2, node_size=repo_s,
                           edgecolors="#333", linewidths=0.2, alpha=0.5, ax=ax, node_shape="s")

    # Labels for top
    top_curators = {n: n for n in cur_nodes if G2.nodes[n].get("score",0) > 4.0}
    top_repos = {n: n[:18] for n in repo_nodes if G2.nodes[n].get("stars",0) > 50000}
    nx.draw_networkx_labels(G2, pos2, {**top_curators, **top_repos}, font_size=4.5,
                            font_weight="bold", font_color="#333", ax=ax)
    minor = {n: n for n in cur_nodes if n not in top_curators}
    nx.draw_networkx_labels(G2, pos2, minor, font_size=3.5, font_color="#aaa", ax=ax)

    ax.legend([Line2D([0],[0],marker="o",color="w",markerfacecolor=c1,markersize=5),
               Line2D([0],[0],marker="o",color="w",markerfacecolor=C[0],markersize=5),
               Line2D([0],[0],marker="s",color="w",markerfacecolor=c2,markersize=4)],
              ["P2 curator","Also in P1","Awesome repo"], fontsize=5, loc="lower left")

    ax.set_title("Phase 1 × Phase 2 cross-reference", fontweight="bold", loc="left", fontsize=8, pad=4)
    ax.axis("off")

    caption(fig, f"Fig. 11 | Cross-reference network. Circles = curators (gold if also in Phase 1). "
            f"Squares = awesome repos. Edges connect curators to their top awesome repo. "
            f"Node sizes ∝ score/stars. Palette: {p['name']}.")

    fig.savefig(f"{OUT}/Fig11_P2_crossref.png")
    fig.savefig(f"{OUT}/Fig11_P2_crossref.pdf")
    plt.close(fig)
    print(f"  [OK] Fig11 P2 cross-reference")


# ============================================================================
# MAIN: Generate for all 4 palettes
# ============================================================================
if __name__ == "__main__":
    for pal in ["simpsons", "futurama", "jama", "lancet"]:
        print(f"\n{'='*60}")
        print(f"Generating palette: {PALETTES[pal]['name']}")
        print(f"{'='*60}")
        generate_all_figures(pal)

    print(f"\n{'='*60}")
    print("ALL DONE — 11 figures × 4 palettes = 44 figures + 44 PDFs")
    print(f"Output: D:/Antigravity/awesome-awesomers/plots/[simpsons|futurama|jama|lancet]/")
    print(f"{'='*60}")
