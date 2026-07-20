# -*- coding: utf-8 -*-
"""Gera assets/Bruno_Garcia_Curriculum_ES.pdf (versão em espanhol do currículo).

Uso: py gerar_curriculo_es.py
Versão em português: gerar_curriculo.py
Versão em inglês: gerar_curriculo_en.py
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

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "Bruno_Garcia_Curriculum_ES.pdf")

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
story.append(Paragraph("Desarrollador RPA | Semisenior", cargo_st))
story.append(Paragraph(
    "Curitiba, Brasil &nbsp;·&nbsp; +55 (41) 99847-6818 &nbsp;·&nbsp; "
    '<a href="mailto:bg5306453@gmail.com" color="#1f5fa8">bg5306453@gmail.com</a>',
    contato_st,
))
story.append(Paragraph(
    '<a href="https://www.linkedin.com/in/bruno-garcia-b0013a254/" color="#1f5fa8">linkedin.com/in/bruno-garcia-b0013a254</a> &nbsp;·&nbsp; '
    '<a href="https://github.com/Bruno-Z-Garcia" color="#1f5fa8">github.com/Bruno-Z-Garcia</a> &nbsp;·&nbsp; '
    '<a href="https://bruno-z-garcia.github.io/Curriculo-Bruno-Garcia/index-es.html" color="#1f5fa8">bruno-z-garcia.github.io/Curriculo-Bruno-Garcia</a>',
    contato_st,
))

# ---------------------------------------------------------------- resumo
story += secao("Resumen Profesional")
story.append(Paragraph(
    "Desarrollador RPA con más de 4 años de experiencia en tecnología y graduado en Gestión de Tecnología de "
    "la Información (UniCuritiba). Especializado en automatización de procesos con Python, C#, Selenium, "
    "Playwright y Power Automate Desktop, actuando en todo el ciclo de vida de la solución — desde el "
    "levantamiento de requisitos y la arquitectura hasta la implantación y el soporte en producción. Experiencia "
    "en integraciones entre sistemas mediante APIs REST, generación y procesamiento automatizado de documentos "
    "(PDF y Word), extracción y tratamiento de datos, dashboards e indicadores de gestión, Inteligencia "
    "Artificial (API OpenAI) aplicada a procesos corporativos y bases de datos relacionales (MySQL y SQL "
    "Server). Trayectoria de robots y sistemas que reducen el trabajo manual, aumentan la productividad y "
    "hacen las operaciones más confiables.",
    corpo_st,
))

# ---------------------------------------------------------------- experiência
story += secao("Experiencia Profesional")

story.append(KeepTogether([
    linha_empresa_data("Plenna Comércio Exterior — Curitiba, Brasil", "Abr/2026 – Actual"),
    linha_funcao_data("Desarrollador RPA | Semisenior", ""),
    bullets([
        "Desarrollo de robots de automatización (RPA) con Python, C#, Playwright y Selenium para procesos de "
        "comercio exterior y rutinas administrativas.",
        "Automatización de la generación y del procesamiento de documentos, extracción y tratamiento de datos.",
        "Creación y mantenimiento de sistemas internos, aplicaciones web y sitios.",
        "Integración entre sistemas mediante APIs y servicios externos.",
        "Deploy, publicación y soporte de robots y aplicaciones en producción.",
        "Gestión de servidores, migración de sistemas y datos y gestión de entornos en cloud (Microsoft Azure).",
    ]),
]))
story.append(Spacer(1, 8))

story.append(KeepTogether([
    linha_empresa_data("Estalk Advogados (bufete de abogados) — Curitiba, Brasil", "Jul/2024 – Actual"),
    linha_funcao_data("Desarrollador RPA | Semisenior", "Feb/2026 – Actual"),
    bullets([
        "Desarrollo de robots y aplicaciones con Python, C#, Power Automate Desktop, Selenium, Playwright e "
        "Inteligencia Artificial, automatizando procesos jurídicos y administrativos.",
        "Responsable de todo el ciclo de la solución — desde el levantamiento de requisitos y la arquitectura "
        "hasta la implantación y el mantenimiento en producción.",
        "Integración entre sistemas mediante APIs, incluyendo sistemas jurídicos (CPJ, XJUS y Preâmbulo).",
        "Generación y procesamiento automatizado de documentos (PDF y Word) y extracción y tratamiento de datos.",
        "Desarrollo de aplicaciones web con Python (Flask), APIs REST y bases de datos relacionales.",
        "Dashboards e indicadores (KPIs), modelado y optimización de bases de datos.",
        "Inteligencia Artificial (API OpenAI) aplicada a procesos corporativos.",
    ]),
]))
story.append(Spacer(1, 5))
story.append(KeepTogether([
    linha_funcao_data("Desarrollador RPA | Junior", "Jul/2024 – Feb/2026"),
    bullets([
        "Creación de robots con Python, Selenium y Power Automate: automatizaciones web, generación automática "
        "de documentos, tratamiento de datos e integración de información entre plataformas.",
        "Desarrollo backend con Python (Flask), interfaces web y modelado de base de datos MySQL.",
        "Integraciones entre sistemas mediante APIs.",
        "Participación en todas las etapas: análisis de la necesidad, implementación, pruebas y mantenimiento.",
    ]),
]))
story.append(Spacer(1, 8))

story.append(KeepTogether([
    linha_empresa_data("Tribunal de Justicia del Estado de Paraná (TJPR) — Curitiba, Brasil", "May/2023 – Jul/2024"),
    linha_funcao_data("Pasante de TI", ""),
    bullets([
        "Soporte técnico a usuarios y mantenimiento de computadoras, periféricos e impresoras.",
        "Apoyo en infraestructura: redes, switches, extensiones y telefonía corporativa.",
    ]),
]))
story.append(Spacer(1, 8))

story.append(KeepTogether([
    linha_empresa_data("SpaceSet — Curitiba, Brasil", "Ago/2021 – Sep/2022"),
    linha_funcao_data("Analista de TI", ""),
    bullets([
        "Soporte técnico, mantenimiento de sistemas y gestión de infraestructura de TI.",
        "Administración de sistemas corporativos e implementación de mejoras tecnológicas.",
    ]),
]))

# ---------------------------------------------------------------- projetos
story += secao("Proyectos Destacados")

projetos = [
    ("Robot de Extracción de Tribunales",
     "Recopila procesos en los tribunales brasileños: descarga los autos, filtra documentos y clasifica cada "
     "movimiento procesal, generando JSON para el flujo jurídico. Arquitectura en paquetes independientes por "
     "sistema procesal (EPROC, e-SAJ, PJe y PROJUDI) e integración con la API DataJud del CNJ. Hecho en equipo.",
     "Python · Playwright · API DataJud (CNJ) · RPA"),
    ("Robot de Comprobantes Judiciales",
     "Exporta el informe de garantías del sistema jurídico, resuelve el identificador fiscal de cada cuenta y "
     "consulta el Comprobante de Rescate de Depósito Judicial en el portal del banco, guardando los PDF y "
     "registrando el estado.",
     "Python · Playwright · PDF · Excel"),
    ("Automatización de Documentos de Exportación",
     "Robots para la emisión de DU-E (Declaración Única de Exportación), Certificado de Origen y certificación "
     "Halal, completando los sistemas desde planillas de control y archivando los documentos emitidos.",
     "Python · Playwright · RPA · Comercio Exterior"),
    ("Automatización Jurídica (RPA)",
     "Robots para la automatización de tareas jurídicas: emisión de autorizaciones judiciales, generación de "
     "guías, cálculos judiciales, demandas iniciales y rutinas de contraloría.",
     "Python · Selenium · Playwright · RPA"),
    ("Generador Inteligente de Documentos Jurídicos",
     "Sistema que analiza documentos procesales (PDF y DOCX) y genera piezas jurídicas automáticamente con "
     "integración de IA.",
     "Python · Flask · OpenAI"),
    ("Sistema de Análisis Jurídicos",
     "Plataforma web corporativa para la gestión completa de análisis jurídicos, con múltiples niveles de "
     "usuarios (abogados, supervisores y dirección), generación automática de documentos y dashboards analíticos.",
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
story += secao("Habilidades Técnicas")

habilidades = [
    ("Automatización &amp; RPA", "Selenium, Playwright, Puppeteer, Power Automate Desktop, Web Scraping, orquestación de robots"),
    ("Lenguajes", "Python, C#, SQL, JavaScript, TypeScript, Java, VBA"),
    ("Backend &amp; APIs", "Flask, Django, Node.js, Express, APIs REST, integraciones entre sistemas corporativos"),
    ("Inteligencia Artificial", "Integración con APIs de IA (OpenAI) aplicada a automatizaciones y procesos corporativos; fundamentos de aprendizaje automático"),
    ("Bases de Datos", "MySQL, SQL Server, SQLite y MongoDB — modelado y optimización de consultas"),
    ("Datos &amp; Documentos", "Power BI, Excel avanzado (VBA), generación de PDF, Word y Excel con Python"),
    ("Desarrollo Web", "HTML, CSS, Sass, Bootstrap, React, Angular"),
    ("DevOps &amp; Cloud", "Git, GitHub, deploy de aplicaciones, Microsoft Azure, AWS (EC2, RDS, S3), NGINX, PM2"),
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
story += secao("Formación Académica")
story.append(KeepTogether([
    linha_empresa_data("Gestión de Tecnología de la Información — UniCuritiba", "2023 – 2025"),
]))

# ---------------------------------------------------------------- cursos
story += secao("Cursos y Certificaciones")
cursos_esq = [
    "Automatización Robótica de Procesos (RPA) — DankiCode (en curso)",
    "C# — DankiCode (2026)",
    "Node.js — DankiCode (2026)",
    "Inteligencia Artificial — DankiCode (2026)",
    "DevOps Essential — DankiCode (2026)",
]
cursos_dir = [
    "Python Completo — DankiCode (2025)",
    "Webmaster Front-End Completo — DankiCode (2025)",
    "React Native — DankiCode (2025)",
    "Microsoft Azure — Microsoft (2022)",
    "Paquete Office 365 — Educavy (2022)",
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
story += secao("Idiomas y Trabajo Voluntario")
story.append(Paragraph("<b>Idiomas:</b> Portugués — nativo &nbsp;·&nbsp; Inglés — intermedio", corpo_st))
story.append(Spacer(1, 3))
story.append(Paragraph(
    "Scout voluntario durante 12 años — trabajo continuo en liderazgo de equipos, organización de actividades y "
    "desarrollo juvenil; competencias aplicadas directamente en la conducción de proyectos y en el trabajo en equipo.",
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
    title="Currículum — Bruno Garcia",
    author="Bruno Garcia",
    subject="Desarrollador RPA",
)
doc.build(story)
print(f"PDF gerado: {SAIDA}")
