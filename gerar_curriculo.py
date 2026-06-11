# -*- coding: utf-8 -*-
"""Gera assets/Bruno_Garcia_Curriculo.pdf a partir do conteúdo definido aqui.

Uso: python gerar_curriculo.py
"""

import os

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

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "Bruno_Garcia_Curriculo.pdf")

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
secao_st = ParagraphStyle("secao", fontName=FB, fontSize=11, leading=14, textColor=DESTAQUE, spaceBefore=12)
empresa_st = ParagraphStyle("empresa", fontName=FB, fontSize=10.5, leading=13.5, textColor=ESCURO)
funcao_st = ParagraphStyle("funcao", fontName=FB, fontSize=9.5, leading=12.5, textColor=DESTAQUE)
data_st = ParagraphStyle("data", fontName=FI, fontSize=9, leading=12.5, textColor=CINZA, alignment=2)
nota_st = ParagraphStyle("nota", fontName=FI, fontSize=8.5, leading=11, textColor=CINZA)
corpo_st = ParagraphStyle("corpo", fontName=F, fontSize=9.5, leading=12.8, textColor=ESCURO, alignment=TA_JUSTIFY)
bullet_st = ParagraphStyle("bullet", parent=corpo_st, alignment=0)
hab_cat_st = ParagraphStyle("habcat", fontName=FB, fontSize=9.5, leading=12.8, textColor=ESCURO)


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
story.append(Paragraph("Desenvolvedor Full Stack &amp; RPA | Pleno", cargo_st))
story.append(Paragraph(
    "Curitiba/PR &nbsp;·&nbsp; (41) 99847-6818 &nbsp;·&nbsp; "
    '<a href="mailto:bg5306453@gmail.com" color="#1f5fa8">bg5306453@gmail.com</a>',
    contato_st,
))
story.append(Paragraph(
    '<a href="https://www.linkedin.com/in/bruno-garcia-b0013a254/" color="#1f5fa8">linkedin.com/in/bruno-garcia-b0013a254</a> &nbsp;·&nbsp; '
    '<a href="https://github.com/Bruno-Z-Garcia" color="#1f5fa8">github.com/Bruno-Z-Garcia</a> &nbsp;·&nbsp; '
    '<a href="https://bruno-z-garcia.github.io/Curriculo-Bruno-Garcia/" color="#1f5fa8">bruno-z-garcia.github.io/Curriculo-Bruno-Garcia</a>',
    contato_st,
))

# ---------------------------------------------------------------- resumo
story += secao("Resumo Profissional")
story.append(Paragraph(
    "Desenvolvedor Full Stack e especialista em automação de processos (RPA), com mais de 4 anos de experiência "
    "em tecnologia e formação em Gestão da Tecnologia da Informação (UniCuritiba). Atuação ponta a ponta no "
    "desenvolvimento de sistemas web corporativos — do levantamento de requisitos e modelagem de dados ao deploy "
    "e sustentação em produção — com Python (Flask), MySQL e JavaScript. Experiência em automações com Selenium, "
    "Playwright e Power Automate, integração com Inteligência Artificial (API OpenAI) para geração automática de "
    "documentos, dashboards gerenciais e gestão de ambientes em cloud (Microsoft Azure). Histórico de soluções que "
    "automatizam fluxos operacionais complexos, reduzem retrabalho manual e centralizam informações estratégicas "
    "para tomada de decisão.",
    corpo_st,
))

# ---------------------------------------------------------------- experiência
story += secao("Experiência Profissional")

story.append(KeepTogether([
    linha_empresa_data("Plenna Comércio Exterior — Curitiba/PR", "Abr/2026 – Atual"),
    linha_funcao_data("Desenvolvedor Full Stack, RPA &amp; Sistemas (DevOps &amp; Cloud) | Pleno", ""),
    bullets([
        "Desenvolvimento de automações (RPA) para otimização de processos operacionais e administrativos.",
        "Criação e manutenção de sistemas internos, aplicações web e sites.",
        "Gerenciamento de servidores, deploy e publicação de aplicações em ambiente produtivo.",
        "Migração de sistemas, dados e serviços entre ambientes.",
        "Gestão de ambientes em cloud (Microsoft Azure e ecossistema Microsoft).",
        "Integração com APIs e serviços externos.",
    ]),
]))
story.append(Spacer(1, 8))

story.append(KeepTogether([
    linha_empresa_data("Estalk Advogados — Curitiba/PR", "Jul/2024 – Atual"),
    linha_funcao_data("Desenvolvedor Full Stack &amp; RPA | Pleno", "Fev/2026 – Atual"),
    bullets([
        "Concepção, arquitetura e evolução de sistemas internos completos para a área jurídica, "
        "cobrindo backend, frontend, modelagem de dados e regras de negócio.",
        "Criação de dashboards gerenciais com KPIs dinâmicos e filtros avançados.",
        "Implementação de regras automatizadas de status, prazos e validações críticas.",
        "Integração com sistemas jurídicos (CPJ, XJUS e Preâmbulo).",
        "Desenvolvimento de geradores automáticos de documentos com IA (API OpenAI).",
        "Otimização de consultas SQL com foco em performance de banco de dados.",
        "Deploy, monitoramento e manutenção de aplicações em ambiente produtivo.",
    ]),
]))
story.append(Spacer(1, 5))
story.append(KeepTogether([
    linha_funcao_data("Desenvolvedor Full Stack &amp; RPA | Júnior", "Jul/2024 – Fev/2026"),
    bullets([
        "Desenvolvimento de funcionalidades backend com Python e Flask.",
        "Criação e manutenção de interfaces web com HTML, CSS e JavaScript.",
        "Modelagem e consultas em banco de dados MySQL.",
        "Automações com Python, Selenium e Power Automate, com redução de custos operacionais.",
        "Integrações com APIs externas e geração automática de documentos em PDF e Word.",
    ]),
]))
story.append(Spacer(1, 8))

story.append(KeepTogether([
    linha_empresa_data("Tribunal de Justiça do Estado do Paraná (TJPR) — Curitiba/PR", "Mai/2023 – Jul/2024"),
    linha_funcao_data("Estagiário de TI", ""),
    bullets([
        "Suporte técnico a usuários e manutenção de computadores, periféricos e impressoras.",
        "Apoio à infraestrutura: redes, switches, ramais e telefonia corporativa.",
    ]),
]))
story.append(Spacer(1, 8))

story.append(KeepTogether([
    linha_empresa_data("SpaceSet — Curitiba/PR", "Ago/2021 – Set/2022"),
    linha_funcao_data("Analista de TI", ""),
    bullets([
        "Suporte técnico, manutenção de sistemas e gerenciamento de infraestrutura de TI.",
        "Administração de sistemas corporativos e implementação de melhorias tecnológicas.",
    ]),
]))

# ---------------------------------------------------------------- projetos
story += secao("Projetos em Destaque")

projetos = [
    ("Sistema de Análises Jurídicas",
     "Plataforma web corporativa para gestão completa de análises jurídicas, com múltiplos níveis de usuários "
     "(advogados, supervisores e diretoria), geração automática de documentos e dashboards analíticos.",
     "Python · Flask · JavaScript · MySQL"),
    ("Gerador Inteligente de Documentos Jurídicos",
     "Sistema que analisa documentos processuais (PDF e DOCX) e gera peças jurídicas automaticamente "
     "com integração de IA.",
     "Python · Flask · OpenAI"),
    ("Automação Jurídica (RPA)",
     "Robôs para automação de tarefas jurídicas: emissão de alvarás, geração de guias, cálculos judiciais, "
     "petições iniciais e rotinas da controladoria.",
     "Python · Selenium · RPA"),
    ("Plataforma de Gestão de Automações",
     "Sistema interno para cadastro, monitoramento e gerenciamento de múltiplos robôs e processos "
     "automatizados da empresa.",
     "Python · Dashboards · Automação"),
    ("Site Imobiliária Miami",
     "Site institucional para imobiliária, com catálogo de imóveis, busca com filtros e design responsivo "
     "focado em experiência do usuário e captação de clientes.",
     "Web · Front-End · Design Responsivo"),
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
    ("Linguagens", "Python, JavaScript, TypeScript, Java, C#, SQL"),
    ("Desenvolvimento Web", "Flask, Node.js, React, Angular, HTML, CSS, Bootstrap"),
    ("Automação &amp; RPA", "Selenium, Playwright, Power Automate, Web Scraping"),
    ("Inteligência Artificial", "Integração com APIs de IA (OpenAI) aplicada a automações e geração de documentos"),
    ("Bancos de Dados", "MySQL e SQLite — modelagem e otimização de consultas"),
    ("DevOps &amp; Cloud", "Git, GitHub, deploy de aplicações, Microsoft Azure"),
    ("Dados &amp; Documentos", "Power BI, Excel avançado (VBA), geração de PDF, Word e Excel com Python"),
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
story += secao("Formação Acadêmica")
story.append(KeepTogether([
    linha_empresa_data("Gestão da Tecnologia da Informação — UniCuritiba", "2023 – 2025"),
]))

# ---------------------------------------------------------------- cursos
story += secao("Cursos e Certificações")
cursos_esq = [
    "Node.js — DankiCode (2026)",
    "Inteligência Artificial — DankiCode (2026)",
    "DevOps Essential — DankiCode (2026)",
    "Python Completo — DankiCode (2025)",
]
cursos_dir = [
    "Webmaster Front-End Completo — DankiCode (2025)",
    "React Native — DankiCode (2025)",
    "Microsoft Azure — Microsoft (2022)",
    "Pacote Office 365 — Educavy (2022)",
]
t = Table(
    [[Paragraph(e, bullet_st), Paragraph(d, bullet_st)] for e, d in zip(cursos_esq, cursos_dir)],
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
story += secao("Idiomas")
story.append(Paragraph("Português — nativo &nbsp;·&nbsp; Inglês — intermediário", corpo_st))

story += secao("Atividades Voluntárias")
story.append(Paragraph(
    "Escoteiro voluntário há 12 anos — atuação contínua em liderança de equipes, organização de atividades e "
    "formação de jovens; competências aplicadas diretamente na condução de projetos e no trabalho em equipe.",
    corpo_st,
))

# ---------------------------------------------------------------- build
doc = SimpleDocTemplate(
    SAIDA,
    pagesize=A4,
    leftMargin=1.6 * cm,
    rightMargin=1.6 * cm,
    topMargin=1.4 * cm,
    bottomMargin=1.4 * cm,
    title="Currículo — Bruno Garcia",
    author="Bruno Garcia",
    subject="Desenvolvedor Full Stack & RPA",
)
doc.build(story)
print(f"PDF gerado: {SAIDA}")
