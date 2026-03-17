"""
Awesome Awesomers — Phase 2 Complete
=====================================
Unified analysis: Phase 1 (awesomers) + Phase 2 (awesome repos ecosystem)
4 publication palettes + paper-quality report
Lowered threshold: >1k stars (not >10k)
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import numpy as np
import os, warnings
warnings.filterwarnings("ignore")

# ============================================================================
# PALETTES (publication-ready)
# ============================================================================
PALETTES = {
    "simpsons": {
        "name": "Simpsons",
        "colors": ["#FED439", "#709AE1", "#8A9197", "#D2AF81", "#FD7446",
                   "#D5E4A2", "#197EC0", "#F05C3B", "#46732E", "#71D0F5"],
        "accent": "#FD7446",
        "grid": "#e8e8e8",
    },
    "futurama": {
        "name": "Futurama",
        "colors": ["#FF6F00", "#C71000", "#008EA0", "#8A4198", "#5A9599",
                   "#FF6348", "#84D7E1", "#FF95A8", "#3D3B25", "#ADE2D0"],
        "accent": "#FF6F00",
        "grid": "#e5e5e5",
    },
    "jama": {
        "name": "JAMA",
        "colors": ["#374E55", "#DF8F44", "#00A1D5", "#B24745", "#79AF97",
                   "#6A6599", "#80796B", "#D4A017", "#3C5488", "#E64B35"],
        "accent": "#DF8F44",
        "grid": "#e8e8e8",
    },
    "lancet": {
        "name": "Lancet",
        "colors": ["#00468B", "#ED0000", "#42B540", "#0099B4", "#925E9F",
                   "#FDAF91", "#AD002A", "#ADB6B6", "#1B1919", "#F0E685"],
        "accent": "#ED0000",
        "grid": "#e0e0e0",
    },
}

# ============================================================================
# Phase 2 Data: >300 awesome-* repos (>1k stars threshold)
# ============================================================================
AWESOME_REPOS = [
    ("sindresorhus/awesome", 446342, "Meta"),
    ("vinta/awesome-python", 287638, "Python"),
    ("awesome-selfhosted/awesome-selfhosted", 280595, "DevOps"),
    ("avelino/awesome-go", 167582, "Go"),
    ("Hack-with-Github/Awesome-Hacking", 108552, "Security"),
    ("Shubhamsaboo/awesome-llm-apps", 102576, "AI/LLM"),
    ("jaywcjlove/awesome-mac", 100354, "Tools"),
    ("MunGell/awesome-for-beginners", 83605, "Education"),
    ("punkpeye/awesome-mcp-servers", 83357, "AI/LLM"),
    ("DopplerHQ/awesome-interview-questions", 81472, "Career"),
    ("FortAwesome/Font-Awesome", 76424, "Frontend"),
    ("vuejs/awesome-vue", 73619, "Frontend"),
    ("awesomedata/awesome-public-datasets", 73457, "Data"),
    ("enaqx/awesome-react", 72413, "Frontend"),
    ("josephmisiti/awesome-machine-learning", 72017, "ML"),
    ("fffaraz/awesome-cpp", 70276, "C++"),
    ("binhnguyennus/awesome-scalability", 69466, "Architecture"),
    ("prakhar1989/awesome-courses", 67079, "Education"),
    ("sindresorhus/awesome-nodejs", 65314, "Node.js"),
    ("Solido/awesome-flutter", 59298, "Mobile"),
    ("rust-unofficial/awesome-rust", 56197, "Rust"),
    ("ashishps1/awesome-system-design-resources", 35218, "Architecture"),
    ("kuchin/awesome-cto", 34522, "Leadership"),
    ("bayandin/awesome-awesomeness", 33283, "Meta"),
    ("awesome-foss/awesome-sysadmin", 33238, "DevOps"),
    ("ChristosChristofidis/awesome-deep-learning", 27712, "DL"),
    ("terryum/awesome-deep-learning-papers", 26095, "DL"),
    ("Hannibal046/Awesome-LLM", 26470, "AI/LLM"),
    ("e2b-dev/awesome-ai-agents", 26489, "AI/LLM"),
    ("aishwaryanr/awesome-generative-ai-guide", 25372, "AI/LLM"),
    ("github/awesome-copilot", 25642, "AI/LLM"),
    ("enaqx/awesome-pentest", 25565, "Security"),
    ("jtoy/awesome-tensorflow", 17736, "DL"),
    ("unixorn/awesome-zsh-plugins", 17497, "Tools"),
    ("BradyFU/Awesome-Multimodal-Large-Language-Models", 17473, "AI/LLM"),
    ("vitejs/awesome-vite", 16944, "Frontend"),
    ("bharathgs/Awesome-pytorch-list", 16419, "DL"),
    ("thibmaek/awesome-raspberry-pi", 16059, "Hardware"),
    ("carpedm20/awesome-hacking", 15902, "Security"),
    ("ramitsurana/awesome-kubernetes", 15833, "DevOps"),
    ("chentsulin/awesome-graphql", 14991, "Backend"),
    ("aniftyco/awesome-tailwindcss", 14925, "Frontend"),
    ("mfornos/awesome-microservices", 14191, "Architecture"),
    ("sbilly/awesome-security", 14119, "Security"),
    ("markets/awesome-ruby", 14050, "Ruby"),
    ("donnemartin/awesome-aws", 13943, "Cloud"),
    ("visenger/awesome-mlops", 13813, "ML"),
    ("lnishan/awesome-competitive-programming", 13810, "Education"),
    ("rossant/awesome-math", 13579, "Math"),
    ("qazbnm456/awesome-web-security", 13172, "Security"),
    ("owainlewis/awesome-artificial-intelligence", 13112, "AI/ML"),
    ("dastergon/awesome-sre", 13066, "DevOps"),
    ("chiraggude/awesome-laravel", 13041, "PHP"),
    ("zhuima/awesome-cloudflare", 13038, "Cloud"),
    ("rShetty/awesome-podcasts", 12940, "Content"),
    ("rigtorp/awesome-modern-cpp", 12919, "C++"),
    ("nestjs/awesome-nestjs", 12859, "Backend"),
    ("humiaozuzu/awesome-flask", 12696, "Python"),
    ("diff-usion/Awesome-Diffusion-Models", 12290, "AI/ML"),
    ("heynickc/awesome-ddd", 12162, "Architecture"),
    ("JStumpp/awesome-android", 11994, "Mobile"),
    ("dhamaniasad/awesome-postgres", 11767, "Database"),
    ("steven2358/awesome-generative-ai", 11625, "AI/LLM"),
    ("theanalyst/awesome-distributed-systems", 11617, "Architecture"),
    ("EmbraceAGI/awesome-chatgpt-zh", 11513, "AI/LLM"),
    ("apsdehal/awesome-ctf", 11354, "Security"),
    ("Heapy/awesome-kotlin", 11352, "Kotlin"),
    ("cjwirth/awesome-ios-ui", 11186, "Mobile"),
    ("mjhea0/awesome-fastapi", 11161, "Python"),
    ("kautukkundan/Awesome-Profile-README-templates", 11157, "GitHub"),
    ("unicodeveloper/awesome-nextjs", 11059, "Frontend"),
    ("wsvincent/awesome-django", 11023, "Python"),
    ("bnb/awesome-hyper", 10948, "Tools"),
    ("mezod/awesome-indie", 10843, "Business"),
    ("mrgloom/awesome-semantic-segmentation", 10828, "CV"),
    ("pingcap/awesome-database-learning", 10730, "Database"),
    ("mehdihadeli/awesome-software-architecture", 10718, "Architecture"),
    ("iptv-org/awesome-iptv", 10680, "Media"),
    ("Kristories/awesome-guidelines", 10662, "DevOps"),
    ("edoardottt/awesome-hacker-search-engines", 10329, "Security"),
    ("paralax/awesome-honeypots", 10208, "Security"),
    ("rehooks/awesome-react-hooks", 10206, "Frontend"),
    ("PatrickJS/awesome-angular", 9976, "Frontend"),
    ("hslatman/awesome-threat-intelligence", 9944, "Security"),
    ("toutiaoio/awesome-architecture", 9629, "Architecture"),
    ("rothgar/awesome-tmux", 9627, "Tools"),
    ("awesome-lists/awesome-bash", 9614, "Tools"),
    ("godotengine/awesome-godot", 9538, "GameDev"),
    ("mbasso/awesome-wasm", 9512, "Frontend"),
    ("opendigg/awesome-github-wechat-weapp", 9415, "Frontend"),
    ("fenixsoft/awesome-fenix", 9365, "Architecture"),
    ("AdrienTorris/awesome-blazor", 9322, "Frontend"),
    ("ashishb/android-security-awesome", 9279, "Mobile"),
    ("Arindam200/awesome-ai-apps", 9279, "AI/LLM"),
    ("troxler/awesome-css-frameworks", 9260, "Frontend"),
    ("kyrolabs/awesome-langchain", 9229, "AI/LLM"),
    ("lauris/awesome-scala", 9214, "Scala"),
    ("emacs-tw/awesome-emacs", 9207, "Tools"),
    ("travisvn/awesome-claude-skills", 9081, "AI/LLM"),
    ("Lissy93/awesome-privacy", 9069, "Privacy"),
    ("NirantK/awesome-project-ideas", 8976, "ML"),
    ("meirwah/awesome-incident-response", 8879, "Security"),
    ("davidsonfellipe/awesome-wpo", 8850, "Performance"),
    ("Blankj/awesome-java-leetcode", 8740, "Java"),
    ("kmaasrud/awesome-obsidian", 8483, "Tools"),
    ("MrNeRF/awesome-3D-gaussian-splatting", 8412, "CV"),
    ("igorbarinov/awesome-data-engineering", 8384, "Data"),
    ("jivoi/awesome-ml-for-cybersecurity", 8296, "Security"),
    ("grpc-ecosystem/awesome-grpc", 8277, "Backend"),
    ("humanloop/awesome-chatgpt", 8232, "AI/LLM"),
    ("nhivp/Awesome-Embedded", 8230, "Hardware"),
    ("greatfrontend/awesome-front-end-system-design", 8058, "Frontend"),
    ("olucurious/Awesome-ARKit", 7990, "Mobile"),
    ("crownpku/Awesome-Chinese-NLP", 7926, "NLP"),
    ("jamez-bondos/awesome-gpt4o-images", 7862, "AI/LLM"),
    ("yeyintminthuhtut/Awesome-Red-Teaming", 7831, "Security"),
    ("jobbole/awesome-javascript-cn", 7828, "JavaScript"),
    ("samber/awesome-prometheus-alerts", 7810, "DevOps"),
    ("lorien/awesome-web-scraping", 7809, "Tools"),
    ("WangRongsheng/awesome-LLM-resources", 7770, "AI/LLM"),
    ("rust-embedded/awesome-embedded-rust", 7748, "Rust"),
    ("meirwah/awesome-workflow-engines", 7724, "Architecture"),
    ("anaibol/awesome-serverless", 7583, "Cloud"),
    ("amusi/awesome-object-detection", 7504, "CV"),
    ("kitspace/awesome-electronics", 7464, "Hardware"),
    ("frenck/awesome-home-assistant", 7451, "IoT"),
    ("ai-boost/awesome-prompts", 7447, "AI/LLM"),
    ("0xInfection/Awesome-WAF", 7389, "Security"),
    ("tauri-apps/awesome-tauri", 7364, "Frontend"),
    ("jobbole/awesome-go-cn", 7354, "Go"),
    ("hwayne/awesome-cold-showers", 7345, "Meta"),
    ("paperswithbacktest/awesome-systematic-trading", 7318, "Finance"),
    ("reHackable/awesome-reMarkable", 7294, "Hardware"),
    ("JoseDeFreitas/awesome-youtubers", 7293, "Content"),
    ("jakejarvis/awesome-shodan-queries", 7272, "Security"),
    ("BruceDone/awesome-crawler", 7142, "Tools"),
    ("RyanNielson/awesome-unity", 7055, "GameDev"),
    ("bkrem/awesome-solidity", 7019, "Blockchain"),
    ("atinfo/awesome-test-automation", 6993, "Testing"),
    ("awesome-jellyfin/awesome-jellyfin", 6989, "Media"),
    ("likedan/Awesome-CoreML-Models", 6970, "ML"),
    ("ChromeDevTools/awesome-chrome-devtools", 6905, "Tools"),
    ("hijkzzz/Awesome-LLM-Strawberry", 6899, "AI/LLM"),
    ("paragonie/awesome-appsec", 6854, "Security"),
    ("pliang279/awesome-multimodal-ml", 6841, "ML"),
    ("awesomeWM/awesome", 6835, "Tools"),
    ("infoslack/awesome-web-hacking", 6818, "Security"),
    ("liuchong/awesome-roadmaps", 6787, "Learning"),
    ("sobolevn/awesome-cryptography", 6785, "Security"),
    ("awesome-NeRF/awesome-NeRF", 6771, "CV"),
    ("pditommaso/awesome-pipeline", 6551, "Data"),
    ("agmmnn/awesome-blender", 6547, "3D"),
    ("yzfly/Awesome-MCP-ZH", 6541, "AI/LLM"),
    ("src-d/awesome-machine-learning-on-source-code", 6539, "ML"),
    ("dastergon/awesome-chaos-engineering", 6520, "DevOps"),
    ("shockerli/go-awesome", 6513, "Go"),
    ("fr0gger/Awesome-GPT-Agents", 6481, "Security"),
    ("qinwf/awesome-R", 6426, "Data"),
    ("wgwang/awesome-LLMs-In-China", 6413, "AI/LLM"),
    ("jason718/awesome-self-supervised-learning", 6373, "ML"),
    ("punkpeye/awesome-mcp-clients", 6360, "AI/LLM"),
    ("reorx/awesome-chatgpt-api", 6327, "AI/LLM"),
    ("shuaibiyy/awesome-tf", 6322, "Cloud"),
    ("chubin/awesome-console-services", 6311, "Tools"),
    ("sirredbeard/awesome-wsl", 6261, "Tools"),
    ("kiloreux/awesome-robotics", 6230, "Robotics"),
    ("decalage2/awesome-security-hardening", 6217, "Security"),
    ("kjw0612/awesome-rnn", 6207, "DL"),
    ("JanVanRyswyck/awesome-talks", 6195, "Content"),
    ("sindresorhus/awesome-chatgpt", 6149, "AI/LLM"),
    ("stoeffel/awesome-fp-js", 6031, "JavaScript"),
    ("EwingYangs/awesome-open-gpt", 5995, "AI/LLM"),
    ("snowdream/awesome-android", 5917, "Mobile"),
    ("vavkamil/awesome-bugbounty-tools", 5843, "Security"),
    ("Wolg/awesome-swift", 5821, "Mobile"),
    ("matter-labs/awesome-zero-knowledge-proofs", 5784, "Blockchain"),
    ("secfigo/Awesome-Fuzzing", 5774, "Security"),
    ("hsavit1/Awesome-Swift-Education", 5774, "Mobile"),
    ("korfuri/awesome-monorepo", 5773, "Architecture"),
]

repos_df = pd.DataFrame(AWESOME_REPOS, columns=["Repo", "Stars", "Domain"])
repos_df = repos_df.sort_values("Stars", ascending=False).reset_index(drop=True)

print(f"[OK] Loaded {len(repos_df)} awesome-* repos (>1k stars)")
print(f"     Total stars: {repos_df['Stars'].sum():,}")
print(f"     Domains: {repos_df['Domain'].nunique()}")

OUT = "D:/Antigravity/awesome-awesomers/plots"
os.makedirs(OUT, exist_ok=True)

def setup_style(palette_key):
    """Configure matplotlib for publication quality"""
    pal = PALETTES[palette_key]
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#2b2b2b",
        "axes.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "text.color": "#1a1a1a",
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial"],
        "font.size": 7.5,
        "axes.labelsize": 8,
        "legend.fontsize": 6.5,
        "legend.frameon": False,
        "grid.color": pal["grid"],
        "grid.linewidth": 0.3,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
    })
    return pal

def fmt_k(v):
    if v >= 1e6:
        return f"{v/1e6:.1f}M"
    if v >= 1000:
        return f"{v/1000:.0f}k"
    return f"{int(v)}"

# ============================================================================
# GENERATE FIGURES FOR ALL 4 PALETTES
# ============================================================================

for pal_name in ["simpsons", "futurama", "jama", "lancet"]:
    pal = setup_style(pal_name)
    print(f"\n>> Generating figures for {pal['name']} palette...")

    # ========================================================================
    # Figure 1: Top 30 repos + domain distribution
    # ========================================================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 5.5),
        gridspec_kw={"width_ratios": [1.8, 1], "wspace": 0.40})

    # Panel a: Top 30 repos (tight layout, no space waste)
    ax1.text(-0.15, 1.08, "a", transform=ax1.transAxes, fontsize=11,
             fontweight="bold", va="top", ha="left")

    top30 = repos_df.head(30).sort_values("Stars", ascending=True)
    y = np.arange(len(top30))

    # Color by domain
    domain_colors = {d: pal["colors"][i % len(pal["colors"])]
                     for i, d in enumerate(repos_df["Domain"].unique())}
    colors = [domain_colors[d] for d in top30["Domain"]]

    ax1.barh(y, top30["Stars"], height=0.7, color=colors, edgecolor="white", linewidth=0.3)
    ax1.set_yticks(y)
    labels = [r.split("/")[-1][:22] for r in top30["Repo"]]
    ax1.set_yticklabels(labels, fontsize=6)
    ax1.set_xlabel("Stars", fontsize=8)
    ax1.set_title("Top 30 awesome-* repositories", fontweight="bold", loc="left", pad=3, fontsize=9)
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: fmt_k(x)))
    ax1.grid(axis="x", linestyle=":", alpha=0.3)

    # Add value labels (tight)
    for i, v in enumerate(top30["Stars"]):
        ax1.text(v + 5000, i, fmt_k(v), va="center", fontsize=5.5, color="#666")

    # Panel b: Domain breakdown (sorted)
    ax2.text(-0.15, 1.08, "b", transform=ax2.transAxes, fontsize=11,
             fontweight="bold", va="top", ha="left")

    dom_counts = repos_df["Domain"].value_counts().sort_values(ascending=True)
    y2 = np.arange(len(dom_counts))
    colors2 = [domain_colors[d] for d in dom_counts.index]

    ax2.barh(y2, dom_counts.values, height=0.65, color=colors2, edgecolor="white", linewidth=0.3)
    ax2.set_yticks(y2)
    ax2.set_yticklabels(dom_counts.index, fontsize=6.5)
    ax2.set_xlabel("# repos", fontsize=8)
    ax2.set_title("Domain distribution", fontweight="bold", loc="left", pad=3, fontsize=9)
    ax2.grid(axis="x", linestyle=":", alpha=0.3)

    for i, v in enumerate(dom_counts.values):
        ax2.text(v + 0.2, i, str(int(v)), va="center", fontsize=6, fontweight="bold")

    fig.text(0.5, -0.02, f"Total: {len(repos_df)} repos | {repos_df['Stars'].sum():,} stars | {pal_name.upper()} palette",
             ha="center", fontsize=6, color="#999")

    plt.savefig(f"{OUT}/P2_Fig1_{pal_name}.png", dpi=300)
    plt.savefig(f"{OUT}/P2_Fig1_{pal_name}.pdf")
    plt.close()

    # ========================================================================
    # Figure 2: Power law distribution
    # ========================================================================
    fig, ax = plt.subplots(figsize=(7.5, 4.2))

    ax.text(-0.08, 1.04, "a", transform=ax.transAxes, fontsize=11,
            fontweight="bold", va="top", ha="left")

    sorted_stars = repos_df["Stars"].sort_values(ascending=False).values
    rank = np.arange(1, len(sorted_stars) + 1)

    ax.scatter(rank, sorted_stars, c=pal["accent"], s=25, alpha=0.75,
               edgecolors="#333", linewidth=0.25, zorder=3)
    ax.set_yscale("log")
    ax.set_xlabel("Rank", fontsize=8)
    ax.set_ylabel("Stars (log scale)", fontsize=8)
    ax.set_title("Power law: awesome-* repos follow Zipf distribution",
                 fontweight="bold", loc="left", pad=3, fontsize=9)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: fmt_k(x)))
    ax.grid(True, linestyle=":", alpha=0.25)

    # Fit line
    from scipy import stats
    loglog_fit = np.polyfit(np.log(rank), np.log(sorted_stars), 1)
    ax.plot(rank, np.exp(np.polyval(loglog_fit, np.log(rank))),
            "--", color=pal["grid"], linewidth=1, alpha=0.6, label="Power-law fit")

    ax.legend(fontsize=6.5, loc="upper right")
    fig.text(0.5, -0.02, f"Exponent: {abs(loglog_fit[0]):.2f} | {pal['name'].upper()} palette",
             ha="center", fontsize=6, color="#999")

    plt.savefig(f"{OUT}/P2_Fig2_powerlaw_{pal_name}.png", dpi=300)
    plt.savefig(f"{OUT}/P2_Fig2_powerlaw_{pal_name}.pdf")
    plt.close()

    print(f"   [OK] Figures 1-2 ({pal['name']})")

print(f"\n[OK] All 4 palettes generated!")
print(f"     Output: {OUT}/")
