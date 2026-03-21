"""
Build v3 CSV: integrate all sources into comprehensive Spain bioinfo directory.
Sources: v2 CSV + 3 PDF extraction agents + INB-ELIXIR nodes + IIS ISCIII
"""
import csv, os

# Geocoordinates by city
COORDS = {
    "Madrid": (40.4168, -3.7038),
    "Barcelona": (41.3851, 2.1734),
    "Sevilla": (37.3886, -5.9823),
    "Valencia": (39.4699, -0.3763),
    "Zaragoza": (41.6488, -0.8891),
    "Oviedo": (43.3614, -5.8593),
    "Santiago de Compostela": (42.8768, -8.5449),
    "A Coruna": (43.3623, -8.4115),
    "Vigo": (42.2406, -8.7207),
    "Pamplona": (42.8125, -1.6458),
    "Bilbao": (43.2630, -2.9350),
    "San Sebastian": (43.3183, -1.9812),
    "Vitoria-Gasteiz": (42.8467, -2.6716),
    "Santander": (43.4623, -3.8100),
    "Salamanca": (40.9688, -5.6631),
    "Granada": (37.1773, -3.5986),
    "Malaga": (36.7213, -4.4214),
    "Cordoba": (37.8882, -4.7794),
    "Cadiz": (36.5271, -6.2886),
    "Logrono": (42.4627, -2.4445),
    "Murcia": (37.9922, -1.1307),
    "Cartagena": (37.6057, -0.9913),
    "Palma": (39.5696, 2.6502),
    "Las Palmas": (28.1235, -15.4363),
    "Santa Cruz de Tenerife": (28.4636, -16.2518),
    "Tenerife": (28.4636, -16.2518),
    "Badajoz": (38.8794, -6.9707),
    "Caceres": (39.4753, -6.3724),
    "Merida": (38.9160, -6.3434),
    "Albacete": (38.9942, -1.8585),
    "Toledo": (39.8628, -4.0273),
    "Ciudad Real": (38.9848, -3.9274),
    "Valladolid": (41.6523, -4.7245),
    "Leon": (42.5987, -5.5671),
    "Burgos": (42.3439, -3.6969),
    "Badalona": (41.4500, 2.2474),
    "L Hospitalet": (41.3596, 2.0997),
    "Bellaterra": (41.5008, 2.1072),
    "Sabadell": (41.5463, 2.1086),
    "Lleida": (41.6176, 0.6200),
    "Girona": (41.9794, 2.8214),
    "Reus": (41.1549, 1.1087),
    "Tarragona": (41.1189, 1.2445),
    "Elche": (38.2669, -0.6983),
    "Alicante": (38.3452, -0.4810),
    "Castellon": (39.9864, -0.0513),
    "Barakaldo": (43.2956, -2.9978),
    "Derio": (43.2949, -2.8761),
    "Galdakao": (43.2321, -2.8430),
    "Majadahonda": (40.4730, -3.8720),
    "Huesca": (42.1401, -0.4089),
    "Lugo": (43.0097, -7.5560),
    "Vic": (41.8863, 2.2549),
    "Trujillo": (39.4580, -5.8810),
    "Alcorcon": (40.3489, -3.8247),
    "Getafe": (40.3050, -3.7332),
    "Leganes": (40.3281, -3.7636),
    "Esplugues": (41.3764, 2.0886),
    "Granadilla de Abona": (28.1193, -16.5769),
}

# Region mapping
REGION_MAP = {
    "Madrid": "Comunidad de Madrid", "Majadahonda": "Comunidad de Madrid",
    "Alcorcon": "Comunidad de Madrid", "Getafe": "Comunidad de Madrid",
    "Leganes": "Comunidad de Madrid",
    "Barcelona": "Catalunya", "Badalona": "Catalunya", "L Hospitalet": "Catalunya",
    "Bellaterra": "Catalunya", "Sabadell": "Catalunya", "Lleida": "Catalunya",
    "Girona": "Catalunya", "Reus": "Catalunya", "Tarragona": "Catalunya",
    "Vic": "Catalunya", "Esplugues": "Catalunya",
    "Sevilla": "Andalucia", "Granada": "Andalucia", "Malaga": "Andalucia",
    "Cordoba": "Andalucia", "Cadiz": "Andalucia",
    "Valencia": "Comunitat Valenciana", "Alicante": "Comunitat Valenciana",
    "Elche": "Comunitat Valenciana", "Castellon": "Comunitat Valenciana",
    "Zaragoza": "Aragon", "Huesca": "Aragon",
    "Oviedo": "Asturias",
    "Santiago de Compostela": "Galicia", "A Coruna": "Galicia",
    "Vigo": "Galicia", "Lugo": "Galicia",
    "Pamplona": "Navarra",
    "Bilbao": "Pais Vasco", "San Sebastian": "Pais Vasco",
    "Vitoria-Gasteiz": "Pais Vasco", "Barakaldo": "Pais Vasco",
    "Derio": "Pais Vasco", "Galdakao": "Pais Vasco",
    "Santander": "Cantabria",
    "Salamanca": "Castilla y Leon", "Valladolid": "Castilla y Leon",
    "Leon": "Castilla y Leon", "Burgos": "Castilla y Leon",
    "Logrono": "La Rioja",
    "Murcia": "Region de Murcia", "Cartagena": "Region de Murcia",
    "Palma": "Illes Balears",
    "Las Palmas": "Canarias", "Santa Cruz de Tenerife": "Canarias",
    "Tenerife": "Canarias", "Granadilla de Abona": "Canarias",
    "Badajoz": "Extremadura", "Caceres": "Extremadura", "Merida": "Extremadura",
    "Trujillo": "Extremadura",
    "Albacete": "Castilla-La Mancha", "Toledo": "Castilla-La Mancha",
    "Ciudad Real": "Castilla-La Mancha",
}

# Comprehensive institution list (deduplicated, key entries only — no biobanks)
ENTRIES = [
    # === CATALUNA ===
    ("center", "CNAG-CRG", "CRG", "Barcelona", "large-scale genomics; sequencing", "Ivo Gut; Sergi Beltran"),
    ("center", "CRG", "UPF; CERCA", "Barcelona", "genomics; systems biology", ""),
    ("group", "Bioinformatics and Genomics Programme", "CRG", "Barcelona", "genomics; evolutionary genomics", "Roderic Guigo"),
    ("group", "Comparative Bioinformatics", "CRG", "Barcelona", "comparative genomics", "Cedric Notredame"),
    ("center", "BSC-CNS", "Ministerio de Ciencia", "Barcelona", "HPC; computational biology", "Alfonso Valencia"),
    ("group", "Genome Informatics", "BSC", "Barcelona", "genome informatics", "Miguel Vazquez"),
    ("group", "NLP for Biomedical Information", "BSC", "Barcelona", "NLP; text mining", "Martin Krallinger"),
    ("unit", "INB Coordination Node", "BSC", "Barcelona", "ELIXIR coordination", "Salvador Capella-Gutierrez"),
    ("center", "IRB Barcelona", "UB; CERCA", "Barcelona", "biomedical research", ""),
    ("group", "BBGLab (Biomedical Genomics)", "IRB Barcelona", "Barcelona", "cancer genomics", "Nuria Lopez-Bigas"),
    ("group", "Structural Bioinformatics", "IRB Barcelona", "Barcelona", "structural bioinformatics", "Patrick Aloy"),
    ("group", "MMB Group", "IRB Barcelona / BSC", "Barcelona", "molecular modelling", "Modesto Orozco"),
    ("group", "Comparative Genomics", "BSC / IRB Barcelona", "Barcelona", "comparative genomics", "Toni Gabaldon"),
    ("center", "IDIBAPS", "Hospital Clinic; UB", "Barcelona", "biomedical research", ""),
    ("center", "IDIBELL", "Hospital Bellvitge; UB", "L Hospitalet", "cancer genomics; epigenomics", ""),
    ("center", "VHIR", "Hospital Vall d Hebron", "Barcelona", "clinical genomics", ""),
    ("center", "VHIO", "Hospital Vall d Hebron", "Barcelona", "precision oncology", ""),
    ("center", "IIB Sant Pau", "Hospital de Sant Pau", "Barcelona", "biomedical research", ""),
    ("center", "IMIM", "Hospital del Mar; UPF", "Barcelona", "biomedical informatics", ""),
    ("center", "UPF-GRIB", "UPF; IMIM", "Barcelona", "biomedical informatics", "Ferran Sanz"),
    ("center", "IGTP", "ICS; CERCA", "Badalona", "biomedical genomics", ""),
    ("group", "GCAT GenomesForLife", "IGTP", "Badalona", "population genomics", "Rafael de Cid"),
    ("center", "IRB Lleida", "Hospital Arnau de Vilanova", "Lleida", "biomedical research", ""),
    ("center", "PARC TAULI", "Hospital Parc Tauli", "Sabadell", "innovation", ""),
    ("center", "CRAG", "CSIC; IRTA; UAB; UB", "Bellaterra", "plant genomics", ""),
    ("center", "ISGlobal", "Hospital Clinic; UB", "Barcelona", "global health; genomics", ""),
    ("center", "ICO", "Generalitat de Catalunya", "L Hospitalet", "cancer; precision oncology", ""),
    ("center", "IDIBGI", "Hospital Josep Trueta", "Girona", "biomedical research", ""),
    ("center", "IJC", "Fundacion Josep Carreras", "Badalona", "leukemia genomics", ""),
    ("university", "UAB", "Universitat Autonoma", "Bellaterra", "bioinformatics", ""),
    ("university", "UPF", "Universitat Pompeu Fabra", "Barcelona", "bioinformatics; genomics", ""),
    ("university", "UB", "Universitat de Barcelona", "Barcelona", "bioinformatics", ""),
    ("network", "BIB", "Consorci BIB", "Barcelona", "bioinformatics network", ""),
    # === COMUNIDAD DE MADRID ===
    ("center", "CNIO", "ISCIII", "Madrid", "cancer genomics; bioinformatics", ""),
    ("unit", "Bioinformatics Unit (CNIO)", "CNIO", "Madrid", "cancer genomics", "Fatima Al-Shahrour"),
    ("unit", "Bioinformatics Unit GENCODE", "CNIO", "Madrid", "gene annotation", "Michael L. Tress"),
    ("center", "CNIC", "ISCIII", "Madrid", "cardiovascular genomics", ""),
    ("unit", "Bioinformatics Unit (CNIC)", "CNIC", "Madrid", "multi-omics; AI", ""),
    ("center", "ISCIII", "Ministerio de Ciencia", "Madrid", "public health; clinical genomics", ""),
    ("unit", "Bioinformatics Unit (BU-ISCIII)", "ISCIII", "Madrid", "clinical bioinformatics", "Isabel Cuesta"),
    ("center", "CNB-CSIC", "CSIC", "Madrid", "biotechnology; genomics", ""),
    ("group", "Biocomputing Unit", "CNB-CSIC", "Madrid", "biocomputing; cryo-EM", "Jose Maria Carazo"),
    ("center", "CBM Severo Ochoa", "CSIC; UAM", "Madrid", "molecular biology", ""),
    ("group", "Systems Biomedicine", "CNC-CSIC", "Madrid", "systems biology", "Monica Chagoyen"),
    ("center", "CBGP", "UPM-INIA", "Madrid", "plant genomics", ""),
    ("group", "Comparative Genomics and Metagenomics", "CBGP", "Madrid", "plant metagenomics", "Jaime Huerta Cepas"),
    ("center", "IMDEA Food", "Comunidad de Madrid", "Madrid", "nutrition; computational biology", ""),
    ("center", "IIBm Alberto Sols", "CSIC-UAM", "Madrid", "biomedical research", ""),
    ("center", "IDIPAZ", "Hospital La Paz", "Madrid", "biomedical research; INGEMM", ""),
    ("center", "IISFJD", "Fundacion Jimenez Diaz", "Madrid", "biomedical research", ""),
    ("center", "i+12", "Hospital 12 de Octubre", "Madrid", "biomedical research", ""),
    ("center", "IiSGM", "Hospital Gregorio Maranon", "Madrid", "microbiome; precision medicine", ""),
    ("center", "IRYCIS", "Hospital Ramon y Cajal", "Madrid", "biomedical research", ""),
    ("center", "IIS-PRINCESA", "Hospital de La Princesa", "Madrid", "immunology; precision medicine", ""),
    ("center", "IdISSC", "Hospital Clinico San Carlos", "Madrid", "biomedical research", ""),
    ("center", "IDIPHIM", "Hospital Puerta de Hierro", "Majadahonda", "biomedical research", ""),
    ("center", "CIEN", "Fundacion CIEN", "Madrid", "neurology", ""),
    ("university", "UAM", "Universidad Autonoma", "Madrid", "bioinformatics; computational biology", ""),
    ("university", "UPM", "Universidad Politecnica", "Madrid", "bioinformatics; health informatics", ""),
    ("university", "UCM", "Universidad Complutense", "Madrid", "oncology", ""),
    ("university", "UC3M", "Universidad Carlos III", "Leganes", "machine learning; genomics", ""),
    # === ANDALUCIA ===
    ("center", "IBiS", "HUVR; CSIC; US", "Sevilla", "biomedical research", ""),
    ("center", "ibs.GRANADA", "Hospital Universitario", "Granada", "biomedical research", ""),
    ("center", "IMIBIC", "Hospital Reina Sofia; UCO", "Cordoba", "biomedical research", ""),
    ("center", "IBIMA-BIONAND", "Hospital Regional", "Malaga", "biomedical research", ""),
    ("center", "INiBICA", "Hospital Puerta del Mar", "Cadiz", "biomedical research", ""),
    ("center", "CABD", "CSIC; UPO; JA", "Sevilla", "developmental biology", ""),
    ("center", "GENYO", "Junta de Andalucia", "Granada", "pharmacogenomics", ""),
    ("center", "CABIMER", "CSIC; JA", "Sevilla", "molecular biology; regenerative medicine", ""),
    ("center", "MEDINA", "CSIC", "Granada", "drug discovery", ""),
    ("group", "Computational Medicine Platform", "FPS", "Sevilla", "computational medicine", "Joaquin Dopazo"),
    ("group", "Clinical Bioinformatics (HUVR)", "FPS / HUVR", "Sevilla", "clinical bioinformatics; OpenCGA", ""),
    ("group", "Computational Health Informatics", "HUVdR", "Sevilla", "health informatics", "Carlos L. Parra-Calderon"),
    ("center", "IPBLN-CSIC", "CSIC", "Granada", "molecular biology", ""),
    ("university", "UMA", "Universidad de Malaga", "Malaga", "bioinformatics; ELIXIR", ""),
    ("university", "UGR", "Universidad de Granada", "Granada", "translational medicine", ""),
    # === COMUNITAT VALENCIANA ===
    ("center", "CIPF", "Generalitat Valenciana", "Valencia", "genomics; bioinformatics; ELIXIR", ""),
    ("center", "IIS LA FE", "Hospital La Fe", "Valencia", "biomedical research; HARMONY", ""),
    ("center", "INCLIVA", "Hospital Clinico Valencia", "Valencia", "biomedical research", ""),
    ("center", "ISABIAL", "Hospital General Alicante", "Alicante", "biomedical research", ""),
    ("center", "FISABIO", "Generalitat Valenciana", "Valencia", "public health; microbiome", ""),
    ("center", "IVO", "Fundacion IVO", "Valencia", "precision oncology", ""),
    ("center", "I2SysBio", "CSIC; UV", "Valencia", "systems biology", ""),
    ("group", "Genomics of Gene Expression", "I2SysBio; UPV", "Valencia", "transcriptomics", "Ana Conesa"),
    ("center", "Instituto Neurociencias", "CSIC-UMH", "Alicante", "neurosciences", ""),
    ("university", "UV", "Universitat de Valencia", "Valencia", "bioinformatics", ""),
    # === GALICIA ===
    ("center", "FPGMX", "SERGAS", "Santiago de Compostela", "genomic medicine; reference centre", ""),
    ("center", "IDIS", "Hospital Clinico Santiago", "Santiago de Compostela", "biomedical research", ""),
    ("center", "INIBIC", "CHUAC", "A Coruna", "biomedical research", ""),
    ("center", "IIS Galicia Sur", "Hospital Alvaro Cunqueiro", "Vigo", "biomedical research", ""),
    ("center", "CESGA", "Xunta; CSIC", "Santiago de Compostela", "HPC", ""),
    ("university", "USC", "Universidad Santiago", "Santiago de Compostela", "CeGen node; genomics", ""),
    # === PAIS VASCO ===
    ("center", "IIS Biocruces Bizkaia", "Hospital Cruces", "Barakaldo", "genomics; bioinformatics", ""),
    ("center", "IIS Biodonostia", "Hospital Donostia", "San Sebastian", "bioinformatics; genomics", ""),
    ("center", "Bioaraba", "Hospital Universitario Araba", "Vitoria-Gasteiz", "biomedical research", ""),
    ("center", "CIC bioGUNE", "BRTA", "Derio", "proteomics; metabolomics", ""),
    ("university", "UPV/EHU", "Universidad Pais Vasco", "Bilbao", "bioinformatics", ""),
    # === NAVARRA ===
    ("center", "CIMA", "Universidad de Navarra", "Pamplona", "biomedical research", ""),
    ("center", "IdiSNA", "CHN; CUN; CIMA", "Pamplona", "health research", ""),
    ("center", "Navarrabiomed", "Gobierno de Navarra", "Pamplona", "genomic medicine; NAGEN", ""),
    ("center", "CUN", "Universidad de Navarra", "Pamplona", "clinical genomics", ""),
    # === ARAGON ===
    ("center", "IIS Aragon", "Gobierno de Aragon", "Zaragoza", "health research", ""),
    ("center", "IACS", "Gobierno de Aragon", "Zaragoza", "health research; BIGAN Big Data", ""),
    ("center", "BIFI", "Universidad de Zaragoza", "Zaragoza", "supercomputing; proteomics", ""),
    ("group", "Computational and Structural Biology", "EEAD-CSIC", "Zaragoza", "structural biology; plants", "Bruno Contreras Moreira"),
    # === ASTURIAS ===
    ("center", "ISPA", "Hospital HUCA", "Oviedo", "biomedical research", ""),
    ("center", "FINBA", "Principado de Asturias", "Oviedo", "digital health; bioinformatics", ""),
    ("group", "DREAMgenics", "Universidad de Oviedo", "Oviedo", "bioinformatics spin-off", ""),
    ("university", "UniOvi", "Universidad de Oviedo", "Oviedo", "biomedicine; molecular oncology", ""),
    # === CANTABRIA ===
    ("center", "IDIVAL", "Hospital Valdecilla", "Santander", "biomedical research", ""),
    ("center", "IBBTEC", "CSIC; UC; SODERCAN", "Santander", "NGS; supercomputing", ""),
    # === CASTILLA Y LEON ===
    ("center", "IBSAL", "Hospital Universitario Salamanca", "Salamanca", "pharmacogenetics; genomics", ""),
    ("center", "CIC Cancer", "CSIC; USAL", "Salamanca", "cancer research; HARMONY", "Javier De Las Rivas"),
    ("center", "SCAYLE", "Junta CyL", "Leon", "supercomputing", ""),
    ("unit", "DiERCyL", "SACYL", "Salamanca", "rare disease genomics", ""),
    # === CASTILLA-LA MANCHA ===
    ("center", "Hospital Virgen de la Salud", "SESCAM", "Toledo", "genetics service (only in CLM)", ""),
    ("center", "CRIB", "UCLM", "Albacete", "metabolomics; proteomics", ""),
    # === LA RIOJA ===
    ("center", "CIBIR", "Gobierno La Rioja", "Logrono", "genomics; bioinformatics", ""),
    ("center", "Hospital San Pedro", "SERIS", "Logrono", "genetics; bioinformatics", ""),
    # === CANARIAS ===
    ("center", "ITER Genomics", "ITER", "Granadilla de Abona", "TeideHPC; NGS; population genomics", ""),
    ("center", "HUGCDN", "SCS", "Las Palmas", "immunogenetics; NGS", ""),
    ("center", "HUNSC", "SCS", "Santa Cruz de Tenerife", "genomics; bioinformatics", ""),
    # === EXTREMADURA ===
    ("center", "CenitS", "COMPUTAEX", "Trujillo", "supercomputing; Lusitania", ""),
    ("center", "INUBE", "UEx", "Badajoz", "pharmacogenetics; precision medicine", ""),
    # === REGION DE MURCIA ===
    ("center", "IMIB", "Hospital Virgen Arrixaca", "Murcia", "genomics; bioinformatics", ""),
    ("center", "CBGC", "Hospital Virgen Arrixaca", "Murcia", "clinical genetics; NGS", ""),
    # === ILLES BALEARS ===
    ("center", "IdISBa", "Hospital Son Espases", "Palma", "health research", ""),
    ("unit", "GENIB", "Hospital Son Espases", "Palma", "genetics; genomics (regional ref)", ""),
    # === NATIONAL ===
    ("network", "INB-ELIXIR-ES", "ELIXIR Spain", "Madrid", "bioinformatics infrastructure", ""),
    ("society", "SEBiBC", "SEBiBC", "Madrid", "professional society", ""),
    ("platform", "CeGen", "ISCIII", "Santiago de Compostela", "national genotyping", ""),
    ("platform", "PRB2/ProteoRed", "ISCIII", "Madrid", "national proteomics (22 nodes)", ""),
    ("platform", "Banco Nacional ADN", "ISCIII", "Salamanca", "national DNA biobank", ""),
]

# Build CSV
outpath = "D:/Antigravity/awesome-awesomers/spain_bioinfo/centros_bioinfo_spain_v3.csv"
with open(outpath, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["type", "name", "parent_institution", "city", "region", "lat", "lon", "main_area", "pi_lead"])
    for entry in ENTRIES:
        typ, name, parent, city, area, pi = entry
        coords = COORDS.get(city, (None, None))
        region = REGION_MAP.get(city, "")
        w.writerow([typ, name, parent, city, region, coords[0], coords[1], area, pi])

print(f"Written {len(ENTRIES)} entries to {outpath}")

# Stats
from collections import Counter
types = Counter(e[0] for e in ENTRIES)
regions = Counter(REGION_MAP.get(e[3], "unknown") for e in ENTRIES)
pis = [e[5] for e in ENTRIES if e[5]]
print(f"\nTypes: {dict(types)}")
print(f"Regions: {len(set(regions))} CCAA")
for r, n in sorted(regions.items(), key=lambda x: -x[1]):
    print(f"  {r}: {n}")
print(f"\nNamed PIs: {len(pis)}")
