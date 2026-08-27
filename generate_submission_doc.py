"""
Generates the official technical submission document in Word (.docx) format
for the Mastercard Innovation Challenge @ GFF 2026.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def create_submission_document(filename="SENTRIX_AI_Mastercard_Submission.docx"):
    doc = Document()
    
    # ── Page Margins ──
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # ── Title & Header ──
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run("SENTRIX AI")
    title_run.font.name = "Arial"
    title_run.font.size = Pt(26)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(235, 0, 27)  # Mastercard Red

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = sub_p.add_run("Autonomous Multi-Modal Red Teaming & Self-Healing Defense Platform for Next-Gen Payment Security")
    sub_run.font.name = "Arial"
    sub_run.font.size = Pt(13)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(100, 100, 100)

    meta_p = doc.add_paragraph()
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta_run = meta_p.add_run("Mastercard Innovation Challenge @ Global Fintech Fest (GFF) 2026 | Submission Category: AI Defense Lab")
    meta_run.font.name = "Arial"
    meta_run.font.size = Pt(10)
    meta_run.font.bold = True
    meta_run.font.color.rgb = RGBColor(255, 95, 0)  # Mastercard Orange

    doc.add_paragraph("―" * 55).alignment = WD_ALIGN_PARAGRAPH.CENTER

    # ── Team Information Box ──
    team_table = doc.add_table(rows=3, cols=2)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    team_table.autofit = False
    
    headers = ["Project & Repository Links", "Submission & Team Metadata"]
    for i, h in enumerate(headers):
        cell = team_table.cell(0, i)
        cell.paragraphs[0].add_run(h).font.bold = True
        set_cell_background(cell, "F2F2F2")

    team_table.cell(1, 0).paragraphs[0].add_run("• Live Web Platform: https://abuzaid-01-master-card-frontend.pages.dev/\n• FastAPI API Docs: https://master-card.onrender.com/docs\n• Public GitHub Repo: https://github.com/Abuzaid-01/master_card")
    team_table.cell(1, 1).paragraphs[0].add_run("• Team Name: Abuzaid_2005\n• Target Event: GFF 2026, Mumbai (Jio World Centre)\n• Track: Red Team / Blue Team AI Defense Lab\n• Submission Deadline: 31st August 2026")
    
    team_table.cell(2, 0).paragraphs[0].add_run("Team Members & Registered Email IDs:").font.bold = True
    team_table.cell(2, 1).paragraphs[0].add_run("1. Abuzaid — abuzaid0205@gmail.com\n2. Dipesh Kumar — dipeshkumar0853822@gmail.com")
    set_cell_background(team_table.cell(2, 0), "FAFAFA")
    set_cell_background(team_table.cell(2, 1), "FAFAFA")

    doc.add_paragraph()

    # ── Section 1: Executive Summary ──
    h1 = doc.add_heading("1. Executive Summary & Core Innovation", level=1)
    h1.runs[0].font.color.rgb = RGBColor(235, 0, 27)

    doc.add_paragraph(
        "Generative AI has fundamentally reshaped financial cybercrime by lowering attack costs, enabling dynamic behavioral evasion, and weaponizing conversational interfaces at scale. Traditional payment defenses operate in isolated silos—the chatbot safety team, payment authorization gateway, and anti-money laundering (AML) graph units evaluate events independently. Modern fraud syndicates exploit these blind spots via compound kill-chains: using conversational prompt injection to suppress SMS alerts, executing automated card testing micro-bursts across merchant channels, and instantly laundering funds through multi-hop mule networks within seconds."
    )
    doc.add_paragraph(
        "SENTRIX AI delivers an end-to-end, closed-loop Red Team/Blue Team platform designed specifically for payment networks. It operates across three tightly integrated pillars: (1) an exhaustive 36-vector threat taxonomy grounded in FinCEN Alert FIN-2024-Alert004 and Federal Reserve FraudClassifier standards, (2) high-fidelity synthetic attack generators verified against real IEEE-CIS data with 100% domain invariant compliance across 38 rules, and (3) a multi-model defense suite featuring sub-millisecond ONNX-quantized inference, dense semantic prompt injection detectors, topological graph GBDTs, financial cost optimization, and active learning retraining that eliminates catastrophic forgetting."
    )

    # ── Section 2: Threat Taxonomy (Pillar 1 - Identify) ──
    h2 = doc.add_heading("2. Pillar 1: Threat Identification & 36-Vector Taxonomy", level=1)
    h2.runs[0].font.color.rgb = RGBColor(235, 0, 27)

    doc.add_paragraph(
        "Rather than focusing on narrow fraud patterns, SENTRIX AI establishes an exhaustive 36-vector threat taxonomy categorized across 5 distinct operational pillars. Every vector is grounded in real payment protocols, cardholder behavioral data, and official regulatory advisories:"
    )

    pillar_summary = [
        ("Pillar 1: AI Red-Teaming & Social Engineering (8 Vectors)", "V01: Admin Impersonation Override, V02: API Tool Hijack, V03: AML Officer Pretext, V04: Voice Clone Vishing, V05: Safe-Account Coercion, V06: Pig-Butchering Romance, V07: B2B Invoice Forgery, V08: Agentic MCP Tool Hijack."),
        ("Pillar 2: Synthetic Data & Obfuscation (7 Vectors)", "V09: Base64/Unicode Masking, V10: Indirect Memo Injection, V11: Multi-Turn Context Poisoning, V12: Multilingual Cross-Lingual Evasion, V13: Prompt Leaking Recon, V14: Social Urgency Hijack, V15: DAN Persona Jailbreak."),
        ("Pillar 3: Multi-Rail & Digital Payment Exploits (7 Vectors)", "V16: Digital Wallet Push Provisioning Bypass, V17: Ghost Tap & Contactless NFC Relay, V18: BOPIS Mule Laundering, V19: BNPL Synthetic Stacking, V20: Refund-as-a-Service (RaaS), V21: Distributed Low-and-Slow BIN Enumeration, V22: Synthetic Merchant Bust-Out."),
        ("Pillar 4: Money Laundering & Network Topologies (7 Vectors)", "V23: Multi-Hop Linear Mule Chains, V24: Fan-Out Dispersal Sweeps, V25: Smurfing & Structuring Funnels, V26: Round-Trip Wash Cycles, V27: Instant Micro-Smurfing (UPI/FedNow), V28: Chameleon Mule Networks (90/10 noise), V29: Crypto Off-Ramp Mixers."),
        ("Pillar 5: Adversarial Evasion & Active Learning (7 Vectors)", "V30: Amount Skirting ($1.99), V31: Velocity Dilution (Poisson throttling), V32: Canvas & Residential Geo-Spoofing, V33: Decline Masking & Age Inflation, V34: Training Set Model Poisoning, V35: Adaptive RL Boundary Prober, V36: Black-Box Surrogate Boundary Gradient Probing.")
    ]

    t_pillar = doc.add_table(rows=len(pillar_summary)+1, cols=2)
    t_pillar.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_pillar.cell(0, 0).paragraphs[0].add_run("Operational Threat Pillar").font.bold = True
    t_pillar.cell(0, 1).paragraphs[0].add_run("Vectors & Real-World Threat Mechanics").font.bold = True
    set_cell_background(t_pillar.cell(0, 0), "EAEAEA")
    set_cell_background(t_pillar.cell(0, 1), "EAEAEA")

    for idx, (p_title, p_desc) in enumerate(pillar_summary):
        r_idx = idx + 1
        t_pillar.cell(r_idx, 0).paragraphs[0].add_run(p_title).font.bold = True
        t_pillar.cell(r_idx, 1).paragraphs[0].add_run(p_desc)

    doc.add_paragraph()

    # ── Section 3: Synthetic Generation & Fidelity (Pillar 2 - Generate) ──
    h3 = doc.add_heading("3. Pillar 2: Synthetic Attack Generation & Statistical Fidelity", level=1)
    h3.runs[0].font.color.rgb = RGBColor(235, 0, 27)

    doc.add_paragraph(
        "To ensure generated attack datasets are genuinely useful for training production defenses, SENTRIX AI deploys modality-specific synthetic generators governed by strict domain invariants:"
    )

    gen_stats = [
        ("Tabular Card Testing", "50,000 Transactions", "12 sub-types across 15 enterprise features (Amount, Velocity, Device Risk, Decline, Diurnal Sin/Cos, MCC Weight, Geo Distance, Card Age, Failed Attempts, Provisioning Channel, NFC Tap Latency, BNPL Inquiries, RaaS Dispute Score, BOPIS Delay).", "100.0% Pass Rate (13 Invariant Rules TAB.1–TAB.13)"),
        ("Prompt Injection Text", "1,500 Prompts", "18 categories (17 adversarial + legitimate inquiries) synthesized via Groq Cloud (GPT OSS 120B / Llama 3.3 70B) and Google Gemini 3.5 Flash Lite with Platt-calibrated embeddings.", "100.0% Pass Rate (6 Invariant Rules T.1–T.6)"),
        ("Money Mule Network Graph", "7,478 Transfers", "1,000 nodes, 100 mule rings, 7 laundering topologies generated using NetworkX directed multi-graphs with conserved monetary flow and realistic timestamp delays.", "100.0% Pass Rate (6 Invariant Rules G.1–G.6)"),
        ("Adversarial Evasion", "50,000 Perturbations", "7 adversarial attack strategies applying boundary-skirting perturbations, model poisoning triggers, and reinforcement learning policy shifts.", "100.0% Pass Rate (13 Invariant Rules EV.1–EV.13)"),
        ("Cross-Vector Scenarios", "100 Unique Campaigns", "Procedural multi-stage campaigns correlating chatbot text injection, gateway card testing, and graph laundering flows with 100% unique entity IDs.", "100.0% Unique Entities & Valid Timelines")
    ]

    t_gen = doc.add_table(rows=len(gen_stats)+1, cols=4)
    t_gen.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, col_name in enumerate(["Modality", "Volume", "Feature Space & Architecture", "Domain Pass Rate"]):
        c = t_gen.cell(0, i)
        c.paragraphs[0].add_run(col_name).font.bold = True
        set_cell_background(c, "EAEAEA")

    for idx, (m, v, f, p) in enumerate(gen_stats):
        r = idx + 1
        t_gen.cell(r, 0).paragraphs[0].add_run(m).font.bold = True
        t_gen.cell(r, 1).paragraphs[0].add_run(v)
        t_gen.cell(r, 2).paragraphs[0].add_run(f)
        t_gen.cell(r, 3).paragraphs[0].add_run(p)

    doc.add_paragraph(
        "\nFidelity Benchmark: Evaluated using Train-on-Synthetic, Test-on-Real (TSTR) protocol against 20,000 real IEEE-CIS fraud benchmark records (TransactionAmt, C12 velocity, V201 device risk), confirming statistical distributional alignment without synthetic artifacts."
    )

    # ── Section 4: Multi-Model Defense Heads (Pillar 3 - Defend) ──
    h4 = doc.add_heading("4. Pillar 3: Multi-Model Defense Heads & Efficacy", level=1)
    h4.runs[0].font.color.rgb = RGBColor(235, 0, 27)

    doc.add_paragraph(
        "The defense suite features three specialized heads operating in parallel, combined via a unified mathematical fusion engine:"
    )

    def_metrics = [
        ("Tabular Fraud Detector", "ONNX-Quantized XGBoost + Isolation Forest", "AUC-PR: 0.8031\nF1 Score: 0.8147\nFPR: 0.0035 (0.35%)", "0.006 ms", "sub-50ms SLA met (8,300x faster than threshold)"),
        ("NLP Injection Detector", "SentenceTransformers (all-MiniLM-L6-v2) + Platt Scaling", "Semantic AUC-PR: 1.0000\nParaphrased Lift: +9.19% vs TF-IDF\nOptimal Threshold: 0.2927", "1.42 ms", "Captures zero-day semantic shifts invisible to keywords"),
        ("Mule Graph Classifier", "HistGradientBoosting on NetworkX Graph Topologies", "AUC-PR: 0.9630\nF1 Score: 0.9025\nOptimal Threshold: 0.50", "0.082 ms", "Identifies instant smurfing, crypto mixers, and chameleon rings"),
        ("Financial Cost Optimizer", "Asymmetric Loss Sweeper ($1.2*Amt FN vs $15.00 FP)", "Optimal Tau: 0.36\nMin Financial Loss: $46,218.98\nSavings vs Default: $3,071.97", "Pre-computed", "Reduces chargeback losses while maintaining frictionless commerce"),
        ("Cross-Vector Fusion Engine", "Correlated Joint Risk Formula + Autonomous Kill Switch", "Joint Score: 1 - Prod(1-Pi) + Delta\nCritical Action: Instant Kill Switch (>=0.80)\nHigh Action: Step-Up 2FA (0.50-0.79)", "15.5 - 32.9 ms", "Autonomous real-time token revocation and wire interception")
    ]

    t_def = doc.add_table(rows=len(def_metrics)+1, cols=5)
    t_def.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, col_name in enumerate(["Defense Head", "Model Architecture", "Benchmark Accuracy", "Latency", "Enterprise Impact"]):
        c = t_def.cell(0, i)
        c.paragraphs[0].add_run(col_name).font.bold = True
        set_cell_background(c, "EAEAEA")

    for idx, (dh, ma, ba, lat, imp) in enumerate(def_metrics):
        r = idx + 1
        t_def.cell(r, 0).paragraphs[0].add_run(dh).font.bold = True
        t_def.cell(r, 1).paragraphs[0].add_run(ma)
        t_def.cell(r, 2).paragraphs[0].add_run(ba)
        t_def.cell(r, 3).paragraphs[0].add_run(lat)
        t_def.cell(r, 4).paragraphs[0].add_run(imp)

    doc.add_paragraph(
        "\nExplainability & Compliance: Global and local TreeSHAP attribution computed across all 15 features (Top: failed_attempts_24h = 0.1281, nfc_tap_latency_ms = 0.1078, bnpl_bureau_inquiries = 0.1058), satisfying PCI-DSS and SR 11-7 model governance standards."
    )

    # ── Section 5: Closed-Loop Active Learning Engine ──
    h5 = doc.add_heading("5. Pillar 4: Closed-Loop Adversarial Active Learning", level=1)
    h5.runs[0].font.color.rgb = RGBColor(235, 0, 27)

    doc.add_paragraph(
        "The cornerstone of SENTRIX AI is its self-healing feedback loop. Simulated attacks are not static test benchmarks—they become the dynamic training ground for active model retraining:"
    )

    loop_steps = [
        "1. Holdout Partitioning: Step 4 holdout data is split strictly 50/50 into a Mining Partition and an Unseen Final Evaluation Partition.",
        "2. Model-Aware Probing: A multi-strategy prober (7 tabular strategies including push provisioning spoofing, NFC delay compression, and BNPL masking; 5 graph strategies; 3 semantic prompt mutations) iteratively attacks Round 1 defenses to discover decision-boundary blind spots.",
        "3. Automated Failure Mining: Mined samples that successfully evaded Round 1 (34.7% tabular evasion rate, 57.9% graph evasion rate) are automatically labeled and merged into the training pool (+4,683 tabular, +711 graph records) without human annotation.",
        "4. Round 2 Active Retraining: Round 2 models are trained and exported to ONNX.",
        "5. Generalization & Catastrophic Forgetting Audit: Evaluated on the unseen adversarial test set. Graph Mule Catch Rate jumped from 39.8% in Round 1 to 87.5% in Round 2 (+42 adversarial mule rings intercepted, AUC-PR increased from 0.7114 to 0.9404, delta = +0.2290). Baseline validation FPR halved from 0.97% to 0.45%, verifying ZERO catastrophic forgetting."
    ]

    for step in loop_steps:
        doc.add_paragraph(step)

    # ── Section 6: Evaluation Criteria Alignment Matrix ──
    h6 = doc.add_heading("6. Official Evaluation Criteria Alignment Matrix", level=1)
    h6.runs[0].font.color.rgb = RGBColor(235, 0, 27)

    criteria = [
        ("Diversity of Attacks Identified", "High (Exhaustive)", "36 Real-World Vectors across 5 Pillars covering conversational LLMs, tool calling, wallet push provisioning, NFC ghost tap relays, instant UPI/FedNow smurfing, crypto mixers, and adversarial RL evasion."),
        ("Fidelity of Attacks in Simulation", "100% Invariant Compliance", "50,000 Tabular (15 features), 1,500 Text, 7,478 Graph edges, 50,000 Evasion records. 100% pass rate across 38 domain rules and verified against 20,000 real IEEE-CIS records via TSTR."),
        ("Detection Algorithms & Efficacy", "Sub-Millisecond & High AUC", "ONNX Tabular (0.006 ms latency, AUC-PR 0.8031), Dense Semantic Text (AUC-PR 1.0, +9.19% lift on paraphrased zero-days), Graph GBDT (AUC-PR 0.9630, F1 0.9025)."),
        ("Novelty of the Solution", "Industry Firsts", "First cross-vector mathematical risk fusion correlating Chatbot + Gateway + Mule Layering. First model-aware multi-strategy active learning feedback loop with automated anti-forgetting audit."),
        ("Real-World Feasibility in Live Payments", "Production-Ready", "Zero PyTorch runtime overhead in production (pure ONNX Runtime C++ engine), sub-50ms SLA compliance, $3,071.97 financial threshold optimization, and live PCI-DSS SHAP attribution.")
    ]

    t_crit = doc.add_table(rows=len(criteria)+1, cols=3)
    t_crit.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, col_name in enumerate(["Challenge Evaluation Criterion", "SENTRIX AI Benchmark", "Technical Implementation Evidence"]):
        c = t_crit.cell(0, i)
        c.paragraphs[0].add_run(col_name).font.bold = True
        set_cell_background(c, "EAEAEA")

    for idx, (cr, bm, ev) in enumerate(criteria):
        r = idx + 1
        t_crit.cell(r, 0).paragraphs[0].add_run(cr).font.bold = True
        t_crit.cell(r, 1).paragraphs[0].add_run(bm)
        t_crit.cell(r, 2).paragraphs[0].add_run(ev)

    doc.add_paragraph()

    # ── Section 7: Conclusion & Deployment ──
    h7 = doc.add_heading("7. Conclusion & Live Deployment Links", level=1)
    h7.runs[0].font.color.rgb = RGBColor(235, 0, 27)

    doc.add_paragraph(
        "SENTRIX AI proves that the most effective way to defeat GenAI-enabled financial fraud is to build a unified system that generates, stress-tests, and actively evolves its own defenses. All components—from synthetic generation to real-time ONNX inference and active retraining—are fully open-source, reproducible, and live in production:"
    )

    doc.add_paragraph("• Interactive Web Dashboard: https://abuzaid-01-master-card-frontend.pages.dev/")
    doc.add_paragraph("• Live FastAPI Backend & API Docs: https://master-card.onrender.com/docs")
    doc.add_paragraph("• GitHub Public Source Code: https://github.com/Abuzaid-01/master_card")

    # Save to disk
    out_path = os.path.join(PROJECT_ROOT, filename)
    doc.save(out_path)
    print(f"[Success] Generated Word Submission Document: {out_path}")
    return out_path


if __name__ == "__main__":
    create_submission_document("Abuzaid_2005.docx")
    create_submission_document("Mastercard_Innovation_Challenge_Submission_Report.docx")
    create_submission_document("TeamName.docx")
