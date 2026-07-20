# -*- coding: utf-8 -*-
"""Gera assets/Bruno_Garcia_Resume_EN.pdf (versão em inglês do currículo).

Uso: python gerar_curriculo_en.py
Versão em português: gerar_curriculo.py
"""

import os
from itertools import zip_longest

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "Bruno_Garcia_Resume_EN.pdf")

# ---------------------------------------------------------------- fontes
FONTES_WINDOWS = {
    "Corpo": r"C:\Windows\Fonts\segoeui.ttf",
    "Corpo-Bold": r"C:\Windows\Fonts\segoeuib.ttf",
    "Corpo-Italic": r"C:\Windows\Fonts\segoeuii.ttf",
    "Corpo-BoldItalic": r"C:\Windows\Fonts\segoeuiz.ttf",
}

if all(os.path.exists(p) for p in FONTES_WINDOWS.values()):
    for nome, caminho in FONTES_WINDOWS.items():
        pdfmetrics.registerFont(TTFont(nome, caminho))
    pdfmetrics.registerFontFamily(
        "Corpo", normal="Corpo", bold="Corpo-Bold",
        italic="Corpo-Italic", boldItalic="Corpo-BoldItalic",
    )
    F, FB, FI = "Corpo", "Corpo-Bold", "Corpo-Italic"
else:
    F, FB, FI = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"

# ---------------------------------------------------------------- cores
ESCURO = colors.HexColor("#1c2733")
DESTAQUE = colors.HexColor("#1f5fa8")
CINZA = colors.HexColor("#5a6572")
LINHA = colors.HexColor("#c9d4de")

# ---------------------------------------------------------------- estilos
nome_st = ParagraphStyle("nome", fontName=FB, fontSize=23, leading=27, textColor=ESCURO)
cargo_st = ParagraphStyle("cargo", fontName=F, fontSize=11.5, leading=15, textColor=DESTAQUE, spaceBefore=2)
contato_st = ParagraphStyle("contato", fontName=F, fontSize=9, leading=13, textColor=CINZA, spaceBefore=4)
secao_st = ParagraphStyle("secao", fontName=FB, fontSize=11, leading=14, textColor=DESTAQUE, spaceBefore=9)
empresa_st = ParagraphStyle("empresa", fontName=FB, fontSize=10.5, leading=13.5, textColor=ESCURO)
funcao_st = ParagraphStyle("funcao", fontName=FB, fontSize=9.5, leading=12.5, textColor=DESTAQUE)
data_st = ParagraphStyle("data", fontName=FI, fontSize=9, leading=12.5, textColor=CINZA, alignment=2)
nota_st = ParagraphStyle("nota", fontName=FI, fontSize=8.5, leading=11, textColor=CINZA)
corpo_st = ParagraphStyle("corpo", fontName=F, fontSize=9.5, leading=12.3, textColor=ESCURO, alignment=TA_JUSTIFY)
bullet_st = ParagraphStyle("bullet", parent=corpo_st, alignment=0)
hab_cat_st = ParagraphStyle("habcat", fontName=FB, fontSize=9.5, leading=12.3, textColor=ESCURO)


def secao(titulo):
    return [
        Paragraph(titulo.upper(), secao_st),
        HRFlowable(width="100%", thickness=0.8, color=LINHA, spaceBefore=2, spaceAfter=6),
    ]


def linha_empresa_data(empresa, data):
    t = Table(
        [[Paragraph(empresa, empresa_st), Paragraph(data, data_st)]],
        colWidths=[12.2 * cm, 5.7 * cm],
    )
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def linha_funcao_data(funcao, data):
    t = Table(
        [[Paragraph(funcao, funcao_st), Paragraph(data, data_st)]],
        colWidths=[12.2 * cm, 5.7 * cm],
    )
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def bullets(itens):
    return ListFlowable(
        [ListItem(Paragraph(i, bullet_st), leftIndent=14, value="•") for i in itens],
        bulletType="bullet",
        bulletFontName=F,
        bulletFontSize=9.5,
        bulletColor=DESTAQUE,
        spaceBefore=3,
        spaceAfter=2,
    )


story = []

# ---------------------------------------------------------------- cabeçalho
story.append(Paragraph("Bruno Garcia", nome_st))
story.append(Paragraph("RPA Developer | Mid-level", cargo_st))
story.append(Paragraph(
    "Curitiba, Brazil &nbsp;·&nbsp; +55 (41) 99847-6818 &nbsp;·&nbsp; "
    '<a href="mailto:bg5306453@gmail.com" color="#1f5fa8">bg5306453@gmail.com</a>',
    contato_st,
))
story.append(Paragraph(
    '<a href="https://www.linkedin.com/in/bruno-garcia-b0013a254/" color="#1f5fa8">linkedin.com/in/bruno-garcia-b0013a254</a> &nbsp;·&nbsp; '
    '<a href="https://github.com/Bruno-Z-Garcia" color="#1f5fa8">github.com/Bruno-Z-Garcia</a> &nbsp;·&nbsp; '
    '<a href="https://bruno-z-garcia.github.io/Curriculo-Bruno-Garcia/index-en.html" color="#1f5fa8">bruno-z-garcia.github.io/Curriculo-Bruno-Garcia</a>',
    contato_st,
))

# ---------------------------------------------------------------- resumo
story += secao("Professional Summary")
story.append(Paragraph(
    "RPA Developer with over 4 years of experience in technology and a degree in Information Technology "
    "Management (UniCuritiba). Specialized in process automation with Python, C#, Selenium, Playwright and "
    "Power Automate Desktop, working across the entire solution lifecycle — from requirements gathering and "
    "architecture to deployment and production support. Experienced in system integrations through REST APIs, "
    "automated document generation and processing (PDF and Word), data extraction and transformation, dashboards "
    "and management indicators, Artificial Intelligence (OpenAI API) applied to business processes and relational "
    "databases (MySQL and SQL Server). Track record of bots and systems that reduce manual work, increase "
    "productivity and make operations more reliable.",
    corpo_st,
))

# ---------------------------------------------------------------- experiência
story += secao("Professional Experience")

story.append(KeepTogether([
    linha_empresa_data("Plenna Comércio Exterior — Curitiba, Brazil", "Apr/2026 – Present"),
    linha_funcao_data("RPA Developer | Mid-level", ""),
    bullets([
        "Development of automation bots (RPA) with Python, C#, Playwright and Selenium for foreign trade "
        "processes and administrative routines.",
        "Automation of document generation and processing, data extraction and transformation.",
        "Creation and maintenance of internal systems, web applications and websites.",
        "System integration through APIs and external services.",
        "Deployment, publishing and support of bots and applications in production.",
        "Server management, system and data migration and cloud management (Microsoft Azure).",
    ]),
]))
story.append(Spacer(1, 8))

story.append(KeepTogether([
    linha_empresa_data("Estalk Advogados (law firm) — Curitiba, Brazil", "Jul/2024 – Present"),
    linha_funcao_data("RPA Developer | Mid-level", "Feb/2026 – Present"),
    bullets([
        "Development of bots and applications with Python, C#, Power Automate Desktop, Selenium, Playwright "
        "and Artificial Intelligence, automating legal and administrative processes.",
        "Responsible for the entire solution lifecycle — from requirements gathering and architecture to "
        "deployment and maintenance in production.",
        "System integration through APIs, including legal systems (CPJ, XJUS and Preâmbulo).",
        "Automated document generation and processing (PDF and Word) and data extraction and transformation.",
        "Development of web applications with Python (Flask), REST APIs and relational databases.",
        "Dashboards and indicators (KPIs), database modeling and optimization.",
        "Artificial Intelligence (OpenAI API) applied to business processes.",
    ]),
]))
story.append(Spacer(1, 5))
story.append(KeepTogether([
    linha_funcao_data("RPA Developer | Junior", "Jul/2024 – Feb/2026"),
    bullets([
        "Creation of bots with Python, Selenium and Power Automate: web automations, automatic document "
        "generation, data processing and information integration across platforms.",
        "Backend development with Python (Flask), web interfaces and MySQL database modeling.",
        "System integrations through APIs.",
        "Involvement in every stage: needs analysis, implementation, testing and maintenance.",
    ]),
]))
story.append(Spacer(1, 8))

story.append(KeepTogether([
    linha_empresa_data("Court of Justice of the State of Paraná (TJPR) — Curitiba, Brazil", "May/2023 – Jul/2024"),
    linha_funcao_data("IT Intern", ""),
    bullets([
        "Technical support for users and maintenance of computers, peripherals and printers.",
        "Infrastructure support: networks, switches, extensions and corporate telephony.",
    ]),
]))
story.append(Spacer(1, 8))

story.append(KeepTogether([
    linha_empresa_data("SpaceSet — Curitiba, Brazil", "Aug/2021 – Sep/2022"),
    linha_funcao_data("IT Analyst", ""),
    bullets([
        "Technical support, systems maintenance and IT infrastructure management.",
        "Administration of corporate systems and implementation of technology improvements.",
    ]),
]))

# ---------------------------------------------------------------- projetos
story += secao("Featured Projects")

projetos = [
    ("Court Data Extraction Bot",
     "Collects case files across Brazilian courts: downloads the records, filters documents and classifies every "
     "procedural update, producing structured JSON for the legal workflow. Architected as independent packages "
     "per court system (EPROC, e-SAJ, PJe and PROJUDI) and integrated with the CNJ DataJud API. Built as a team.",
     "Python · Playwright · DataJud API (CNJ) · RPA"),
    ("Judicial Deposit Receipts Bot",
     "Exports the collateral report from the legal system, resolves the company ID for each account and queries "
     "the Judicial Deposit Withdrawal Receipt on the bank's portal, saving the PDFs and recording each status.",
     "Python · Playwright · PDF · Excel"),
    ("Export Documentation Automation",
     "Bots for issuing DU-E (Brazilian Single Export Declaration), Certificates of Origin and Halal "
     "certification, filling the systems from tracking spreadsheets and filing the issued documents.",
     "Python · Playwright · RPA · Foreign Trade"),
    ("Legal Automation (RPA)",
     "Bots to automate legal tasks: issuing judicial release orders, generating court fee slips, judicial "
     "calculations, initial pleadings and controllership routines.",
     "Python · Selenium · Playwright · RPA"),
    ("Smart Legal Document Generator",
     "System that analyzes case files (PDF and DOCX) and automatically drafts legal documents "
     "with AI integration.",
     "Python · Flask · OpenAI"),
    ("Legal Analysis System",
     "Corporate web platform for the full management of legal analyses, with multiple user levels "
     "(lawyers, supervisors and board members), automatic document generation and analytics dashboards.",
     "Python · Flask · JavaScript · MySQL"),
]
for titulo, desc, tech in projetos:
    story.append(KeepTogether([
        Paragraph(titulo, funcao_st),
        Paragraph(desc, bullet_st),
        Paragraph(tech, nota_st),
        Spacer(1, 5),
    ]))

# ---------------------------------------------------------------- habilidades
story += secao("Technical Skills")

habilidades = [
    ("Automation &amp; RPA", "Selenium, Playwright, Puppeteer, Power Automate Desktop, Web Scraping, bot orchestration"),
    ("Languages", "Python, C#, SQL, JavaScript, TypeScript, Java, VBA"),
    ("Backend &amp; APIs", "Flask, Django, Node.js, Express, REST APIs, integrations between corporate systems"),
    ("Artificial Intelligence", "Integration with AI APIs (OpenAI) applied to automations and business processes; machine learning fundamentals"),
    ("Databases", "MySQL, SQL Server, SQLite and MongoDB — data modeling and query optimization"),
    ("Data &amp; Documents", "Power BI, advanced Excel (VBA), PDF, Word and Excel generation with Python"),
    ("Web Development", "HTML, CSS, Sass, Bootstrap, React, Angular"),
    ("DevOps &amp; Cloud", "Git, GitHub, application deployment, Microsoft Azure, AWS (EC2, RDS, S3), NGINX, PM2"),
]
t = Table(
    [[Paragraph(cat, hab_cat_st), Paragraph(desc, bullet_st)] for cat, desc in habilidades],
    colWidths=[4.6 * cm, 13.3 * cm],
)
t.setStyle(TableStyle([
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 1.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(t)

# ---------------------------------------------------------------- formação
story += secao("Education")
story.append(KeepTogether([
    linha_empresa_data("Information Technology Management — UniCuritiba", "2023 – 2025"),
]))

# ---------------------------------------------------------------- cursos
story += secao("Courses & Certifications")
cursos_esq = [
    "Robotic Process Automation (RPA) — DankiCode (in progress)",
    "C# — DankiCode (2026)",
    "Node.js — DankiCode (2026)",
    "Artificial Intelligence — DankiCode (2026)",
    "DevOps Essential — DankiCode (2026)",
]
cursos_dir = [
    "Complete Python — DankiCode (2025)",
    "Complete Front-End Webmaster — DankiCode (2025)",
    "React Native — DankiCode (2025)",
    "Microsoft Azure — Microsoft (2022)",
    "Office 365 Suite — Educavy (2022)",
]
t = Table(
    [[Paragraph(e, bullet_st), Paragraph(d, bullet_st)] for e, d in zip_longest(cursos_esq, cursos_dir, fillvalue="")],
    colWidths=[8.95 * cm, 8.95 * cm],
)
t.setStyle(TableStyle([
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 1.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(t)

# ---------------------------------------------------------------- idiomas e voluntariado
story += secao("Languages & Volunteer Work")
story.append(Paragraph("<b>Languages:</b> Portuguese — native &nbsp;·&nbsp; English — intermediate", corpo_st))
story.append(Spacer(1, 3))
story.append(Paragraph(
    "Volunteer scout for 12 years — ongoing work in team leadership, activity organization and youth "
    "development; skills applied directly to project management and teamwork.",
    corpo_st,
))

# ---------------------------------------------------------------- build
doc = SimpleDocTemplate(
    SAIDA,
    pagesize=A4,
    leftMargin=1.6 * cm,
    rightMargin=1.6 * cm,
    topMargin=1.25 * cm,
    bottomMargin=1.25 * cm,
    title="Resume — Bruno Garcia",
    author="Bruno Garcia",
    subject="RPA Developer",
)
doc.build(story)
print(f"PDF gerado: {SAIDA}")
