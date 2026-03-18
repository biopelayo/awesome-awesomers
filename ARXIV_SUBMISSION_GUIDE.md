# arXiv Submission Guide: Awesome-Awesomers Research Paper

## 📋 Paper Details

| Field | Value |
|-------|-------|
| **Title** | Awesome Awesomers: Mapping Influence & Impact in Tech Communities |
| **Subtitle** | A Two-Phase Comparative Analysis of Influential Technologists and Awesome-Repository Curators |
| **Authors** | Pelayo González de Lena Rodríguez (University of Oviedo / ISPA-FINBA) |
| **Date** | March 17, 2026 |
| **Pages** | 18-22 |
| **File Size** | 3.5 MB |
| **Subject Area** | Computer Science (cs.CY - Computers and Society) |

---

## 🎯 arXiv Categories

**Primary:** `cs.CY` (Computers and Society)
**Secondary:** `cs.SO` (Social and Information Networks)
**Tertiary:** `stat.AP` (Statistics - Applications)

---

## 📦 Files to Submit

### Required
- ✅ `awesome-awesomers_RESEARCH_PAPER.pdf` (3.5 MB, publication-ready)

### Optional (Supporting Materials)
- `FIGURE_CAPTIONS.md` (detailed captions)
- `FIGURE_CAPTIONS_LATEX.tex` (LaTeX format)
- `figures_final.py` (Phase 1 generation script)
- `phase2_figures_correct_style.py` (Phase 2 generation script)
- `Phase2_Interactive_Analysis.ipynb` (Jupyter notebook)

---

## 🚀 Step-by-Step Submission to arXiv

### Step 1: Create arXiv Account
1. Go to **https://arxiv.org/user/register**
2. Register with email (can use any email)
3. Verify email address
4. Log in at **https://arxiv.org/user**

### Step 2: Prepare Submission Package

#### Option A: Direct PDF Upload (Easiest)
- File: `awesome-awesomers_RESEARCH_PAPER.pdf`
- Already formatted for arXiv
- No conversion needed

#### Option B: LaTeX Source (Recommended for Reproducibility)
If you want to upload `.tex` source:
1. Use the provided `FIGURE_CAPTIONS_LATEX.tex`
2. Include all figure images in `/plots/` directory
3. Create a `.tar.gz` archive:
   ```bash
   tar -czf awesome-awesomers.tar.gz \
     awesome-awesomers_RESEARCH_PAPER.pdf \
     FIGURE_CAPTIONS_LATEX.tex \
     plots/Fig*.pdf \
     plots/P2_Fig*.pdf
   ```

### Step 3: Submit via Web Interface

1. **Go to:** https://arxiv.org/submit
2. **Select category:** Computer Science → Computers and Society (cs.CY)
3. **Upload file:**
   - Choose `awesome-awesomers_RESEARCH_PAPER.pdf`
   - Click "Upload PDF"
4. **Fill in metadata:**

   **Title:**
   ```
   Awesome Awesomers: Mapping Influence & Impact in Tech Communities
   ```

   **Authors:**
   ```
   Pelayo González de Lena Rodríguez
   ```

   **Abstract:**
   ```
   This paper presents a two-phase comparative analysis of influence and impact
   in technology communities. Phase 1 analyzes 74 influential technologists
   across AI/ML, bioinformatics, and data science domains, identifying power-law
   distribution patterns in follower counts (ρ=0.62 with total stars). Phase 2
   examines 21 curators of awesome-* repositories (179 repos, 4.2M total stars),
   revealing distinct success pathways (ρ=0.31, independent metrics). Network
   analysis identifies 5 communities in Phase 1 and 4 in Phase 2, with
   betweenness centrality revealing key knowledge brokers. Results demonstrate
   that influence in tech is driven by different incentive structures: Phase 1
   emphasizes brand-building through follower accumulation, while Phase 2
   prioritizes niche expertise and curation quality. The study provides
   quantitative evidence for understanding community dynamics and knowledge
   dissemination in open-source and technology sectors.
   ```

   **Subjects:**
   ```
   Computers and Society (cs.CY)
   Social and Information Networks (cs.SO)
   Statistics - Applications (stat.AP)
   ```

   **Comments:**
   ```
   18 pages, 16 figures, 10 references
   ```

   **Journal Reference:**
   ```
   (leave blank for first submission)
   ```

   **Report Number:**
   ```
   (leave blank)
   ```

5. **License:** Select `Creative Commons Attribution 4.0` (CC-BY)

6. **Review & Submit**
   - Check all metadata
   - Accept arXiv agreement
   - Click "Submit"

### Step 4: Verification

You'll receive:
- **Confirmation email** with arXiv ID (e.g., `2603.12345`)
- **Moderation period** (usually 24-48 hours)
- **Publication link:** `https://arxiv.org/abs/2603.12345`

---

## 📊 Expected arXiv ID Format

After approval, your paper will be available at:
```
https://arxiv.org/abs/2603.[5-digit-number]
```

Example: `https://arxiv.org/abs/2603.12345`

---

## ✅ Pre-Submission Checklist

- [ ] PDF file is named clearly (`awesome-awesomers_RESEARCH_PAPER.pdf`)
- [ ] All 16 figures are embedded in PDF
- [ ] Figure captions are visible and readable
- [ ] Bibliography is complete (10 references included)
- [ ] Page numbers are correct (18-22 pages)
- [ ] Abstract is 150-250 words
- [ ] No author identifiable information (anonymous)
- [ ] arXiv account is created and verified
- [ ] Title is < 80 characters
- [ ] Metadata is complete (title, authors, abstract)

---

## 📝 Sample Metadata

| Field | Value |
|-------|-------|
| Title | Awesome Awesomers: Mapping Influence & Impact in Tech Communities |
| Authors | Pelayo González de Lena Rodríguez |
| Category | cs.CY (Computer Science - Computers and Society) |
| Subjects | cs.CY, cs.SO, stat.AP |
| Keywords | influence, networks, open-source, GitHub, curators, power-law |
| License | CC-BY 4.0 |
| Comments | 18 pages, 16 figures (8 Phase 1 + 8 Phase 2) |

---

## 🔗 Useful Links

- **arXiv Submission:** https://arxiv.org/submit
- **arXiv Help:** https://arxiv.org/help/submit
- **Category List:** https://arxiv.org/category_taxonomy
- **License Info:** https://creativecommons.org/licenses/by/4.0/

---

## 💡 Tips for arXiv Success

1. **Category Selection:** cs.CY is best for social/impact analysis
2. **Abstract Quality:** First-time readers use abstract to decide to read full paper
3. **Figures:** All embedded in PDF — no separate uploads needed
4. **License:** CC-BY allows maximum visibility and reuse
5. **Keywords:** Include "GitHub", "influence", "networks", "open-source"
6. **Timing:** Submit on weekdays (Tue-Thu) for faster review

---

## ⏱️ Timeline

| Stage | Duration |
|-------|----------|
| Account creation | 5 minutes |
| File upload & metadata | 10 minutes |
| arXiv moderation | 24-48 hours |
| **Total time to publication** | ~1-2 days |

---

## 📞 Support

If submission fails:
1. Check file format (PDF must be 3.5 MB or less)
2. Verify abstract length (150-250 words)
3. Check title length (< 80 chars)
4. Try uploading again
5. Contact arXiv support if persistent issues

---

## 🎉 After Publication

Once published on arXiv:

1. **Get Permanent Link:**
   ```
   https://arxiv.org/abs/2603.[ID]
   ```

2. **View as PDF:**
   ```
   https://arxiv.org/pdf/2603.[ID].pdf
   ```

3. **Share on:**
   - Twitter: "Just published on arXiv: Awesome Awesomers... [link]"
   - GitHub: Add badge to README
   - LinkedIn: Announce new research

4. **Update References:**
   - Add arXiv ID to papers/citations
   - Link from GitHub repo main README

---

## 📄 Sample GitHub Badge

```markdown
[![arXiv](https://img.shields.io/badge/arXiv-2603.12345-b31b1b.svg)](https://arxiv.org/abs/2603.12345)
```

---

**Ready to publish? Follow the steps above and your paper will be on arXiv within 1-2 days! 🚀**
