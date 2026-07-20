document.addEventListener("DOMContentLoaded", function () {

    // =============================
    // PREFERÊNCIA DE MOVIMENTO
    // =============================

    const reduzirMovimento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    // =============================
    // IDIOMA DA PÁGINA
    // =============================

    // o mesmo script atende index.html (pt-BR), index-en.html (en) e index-es.html (es);
    // os textos gerados via JS mudam conforme o lang do documento
    const langDocumento = (document.documentElement.lang || "").toLowerCase();

    const idioma = langDocumento.startsWith("en") ? "en"
        : langDocumento.startsWith("es") ? "es"
        : "pt";

    // traduz a partir de um dicionário { pt, en, es }; cai no pt se faltar a chave
    const t = (dic) => (dic[idioma] !== undefined ? dic[idioma] : dic.pt);

    // =============================
    // FUNDO INTERATIVO — PLACA DE CIRCUITO
    // =============================

    function iniciarFundoCircuito() {

        const canvas = document.getElementById("bg-canvas");
        const divFundo = document.getElementById("circuito-fundo");
        const divFrente = document.getElementById("circuito-frente");
        const divGlow = document.getElementById("circuito-glow");

        if (!canvas || !divFundo || !divFrente || !divGlow) return false;

        let ctx;

        try {
            ctx = canvas.getContext("2d");
        } catch (e) {
            return false;
        }

        if (!ctx) return false;

        const mobile = window.innerWidth < 768;
        const dpr = Math.min(window.devicePixelRatio || 1, mobile ? 1 : 1.5);

        const CIANO = "0,195,255";
        const DOIS_PI = Math.PI * 2;

        // direções permitidas: horizontal, vertical e diagonais de 45° (estilo PCB)
        const PASSO_ANGULO = Math.PI / 4;

        const PALAVRAS_TECH = [
            "RPA", "Python", "C#", "Playwright", "Selenium", "Power Automate",
            "Flask", t({ pt: "API REST", en: "REST API", es: "API REST" }), "MySQL", "SQL Server", "OpenAI", "Azure",
            "bot.run()", "page.click()", "web scraping",
            t({ pt: "automação", en: "automation", es: "automatización" }),
            t({ pt: "robôs", en: "bots", es: "robots" }),
            t({ pt: "IA", en: "AI", es: "IA" }), "</>", "{ }", "git push", "deploy", "async/await", "SELECT *"
        ];

        let largura, altura, extra;
        let camadaFundo, camadaFrente;

        const pulsos = [];
        const flashes = [];
        const palavras = [];

        const maxPulsos = mobile ? 6 : 12;
        const maxPalavras = mobile ? 5 : 10;

        let energia = 0;
        let ultimoScroll = window.scrollY;
        let ultimaPalavraMouse = 0;
        let antesMs = 0;

        const mouse = { x: 0, y: 0 };

        // sprite do halo dos pulsos, desenhado uma única vez
        // (createRadialGradient a cada quadro era um dos maiores custos)
        const RAIO_HALO = 10;

        const spriteHalo = (function () {
            const cv = document.createElement("canvas");
            cv.width = cv.height = RAIO_HALO * 2;
            const g = cv.getContext("2d");
            const grad = g.createRadialGradient(RAIO_HALO, RAIO_HALO, 0, RAIO_HALO, RAIO_HALO, RAIO_HALO);
            grad.addColorStop(0, "rgba(170,238,255,.95)");
            grad.addColorStop(1, "rgba(0,195,255,0)");
            g.fillStyle = grad;
            g.fillRect(0, 0, RAIO_HALO * 2, RAIO_HALO * 2);
            return cv;
        })();

        // ---- geração procedural de um traço estilo placa de circuito

        function gerarTraco(w, h) {

            const pontos = [];

            let x = Math.random() * w;
            let y = Math.random() * h;
            let dir = Math.floor(Math.random() * 8) * PASSO_ANGULO;

            pontos.push({ x: x, y: y });

            const segmentos = 3 + Math.floor(Math.random() * 5);

            for (let i = 0; i < segmentos; i++) {

                const comprimento = 50 + Math.random() * 150;

                x += Math.cos(dir) * comprimento;
                y += Math.sin(dir) * comprimento;
                pontos.push({ x: x, y: y });

                // curva de 45° ou 90°, como roteamento de PCB
                dir += (Math.random() < 0.5 ? -1 : 1) * PASSO_ANGULO * (Math.random() < 0.8 ? 1 : 2);
            }

            // comprimento acumulado de cada segmento (para animar os pulsos)
            const acumulado = [0];
            let total = 0;

            for (let i = 1; i < pontos.length; i++) {
                total += Math.hypot(pontos[i].x - pontos[i - 1].x, pontos[i].y - pontos[i - 1].y);
                acumulado.push(total);
            }

            return { pontos: pontos, acumulado: acumulado, total: total, anel: Math.random() < 0.5 };
        }

        // ---- desenha uma camada estática de circuito em canvas separado

        function desenharCamada(w, h, qtd, alfa) {

            const cv = document.createElement("canvas");
            cv.width = w * dpr;
            cv.height = h * dpr;

            const g = cv.getContext("2d");
            g.scale(dpr, dpr);
            g.lineCap = "round";
            g.lineJoin = "round";

            const tracos = [];

            for (let i = 0; i < qtd; i++) {

                const t = gerarTraco(w, h);
                tracos.push(t);

                g.strokeStyle = "rgba(" + CIANO + "," + alfa + ")";
                g.lineWidth = 1.4;
                g.beginPath();
                g.moveTo(t.pontos[0].x, t.pontos[0].y);

                for (let j = 1; j < t.pontos.length; j++) {
                    g.lineTo(t.pontos[j].x, t.pontos[j].y);
                }

                g.stroke();

                // nó inicial (via) e terminal (pad em anel ou ponto)
                const inicio = t.pontos[0];
                const fim = t.pontos[t.pontos.length - 1];

                g.fillStyle = "rgba(" + CIANO + "," + (alfa * 2) + ")";
                g.beginPath();
                g.arc(inicio.x, inicio.y, 2.2, 0, DOIS_PI);
                g.fill();

                if (t.anel) {
                    g.strokeStyle = "rgba(" + CIANO + "," + (alfa * 2.2) + ")";
                    g.lineWidth = 1.6;
                    g.beginPath();
                    g.arc(fim.x, fim.y, 5, 0, DOIS_PI);
                    g.stroke();
                } else {
                    g.beginPath();
                    g.arc(fim.x, fim.y, 3, 0, DOIS_PI);
                    g.fill();
                }
            }

            // vias soltas espalhadas pela placa
            for (let i = 0; i < qtd * 2; i++) {
                g.fillStyle = "rgba(" + CIANO + "," + (alfa * 1.4) + ")";
                g.beginPath();
                g.arc(Math.random() * w, Math.random() * h, 1.6, 0, DOIS_PI);
                g.fill();
            }

            return { cv: cv, tracos: tracos, w: w, h: h };
        }

        // ---- posição ao longo de um traço, dada a distância percorrida

        function pontoNoTraco(t, dist) {

            let i = 1;

            while (i < t.acumulado.length - 1 && t.acumulado[i] < dist) i++;

            const d0 = t.acumulado[i - 1];
            const d1 = t.acumulado[i];
            const f = d1 > d0 ? (dist - d0) / (d1 - d0) : 0;
            const p0 = t.pontos[i - 1];
            const p1 = t.pontos[i];

            return { x: p0.x + (p1.x - p0.x) * f, y: p0.y + (p1.y - p0.y) * f };
        }

        // ---- palavras de tecnologia flutuantes

        function criarPalavra(x, y) {

            if (palavras.length >= maxPalavras) return;

            palavras.push({
                texto: PALAVRAS_TECH[Math.floor(Math.random() * PALAVRAS_TECH.length)],
                x: x,
                y: y,
                tamanho: 11 + Math.random() * 4,
                vida: 0,
                duracao: 4.5 + Math.random() * 3
            });
        }

        // ---- montagem (e remontagem ao redimensionar)
        // as camadas estáticas viram imagem de fundo de divs movidas por CSS
        // transform (compositor/GPU); o canvas só desenha os efeitos dinâmicos

        function montar() {

            largura = window.innerWidth;
            altura = window.innerHeight;
            extra = 460;

            canvas.width = largura * dpr;
            canvas.height = altura * dpr;
            canvas.style.width = largura + "px";
            canvas.style.height = altura + "px";
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

            const wCamada = largura + 60;
            const hCamada = altura + extra;

            camadaFundo = desenharCamada(wCamada, hCamada, mobile ? 10 : 20, 0.07);
            camadaFrente = desenharCamada(wCamada, hCamada, mobile ? 14 : 26, 0.13);

            // os canvases entram direto como filhos das divs — converter para
            // dataURL (base64) travava a página na carga e em cada resize
            function clonarCanvas(cv) {
                const copia = document.createElement("canvas");
                copia.width = cv.width;
                copia.height = cv.height;
                copia.getContext("2d").drawImage(cv, 0, 0);
                return copia;
            }

            [[divFundo, camadaFundo.cv], [divFrente, camadaFrente.cv], [divGlow, clonarCanvas(camadaFrente.cv)]].forEach(par => {
                const div = par[0];
                const cv = par[1];
                cv.style.display = "block";
                cv.style.width = wCamada + "px";
                cv.style.height = hCamada + "px";
                div.style.width = wCamada + "px";
                div.style.height = hCamada + "px";
                div.replaceChildren(cv);
            });

            pulsos.length = 0;
            flashes.length = 0;
        }

        montar();

        // ---- interação: scroll carrega "energia" e mouse cria parallax + palavras

        window.addEventListener("scroll", () => {
            energia = Math.min(energia + Math.abs(window.scrollY - ultimoScroll) * 0.0015, 1.2);
            ultimoScroll = window.scrollY;
        }, { passive: true });

        if (!reduzirMovimento) {

            window.addEventListener("mousemove", (e) => {

                mouse.x = (e.clientX / largura) - 0.5;
                mouse.y = (e.clientY / altura) - 0.5;

                const agora = performance.now();

                if (agora - ultimaPalavraMouse > 600 && Math.random() < 0.5) {
                    ultimaPalavraMouse = agora;
                    criarPalavra(
                        e.clientX + (Math.random() - 0.5) * 120,
                        e.clientY + (Math.random() - 0.5) * 80
                    );
                }
            }, { passive: true });
        }

        let aguardandoResize;

        window.addEventListener("resize", () => {
            clearTimeout(aguardandoResize);
            aguardandoResize = setTimeout(montar, 200);
        });

        // ---- desenho de cada quadro

        function desenharPulsos(dt) {

            // novos pulsos: fluxo constante + extra conforme a energia do scroll
            if (pulsos.length < maxPulsos && Math.random() < (1.5 + energia * 4.8) * dt) {
                const tracos = camadaFrente.tracos;
                pulsos.push({
                    traco: tracos[Math.floor(Math.random() * tracos.length)],
                    dist: 0,
                    vel: 70 + Math.random() * 70
                });
            }

            for (let i = pulsos.length - 1; i >= 0; i--) {

                const p = pulsos[i];
                p.dist += p.vel * (1 + energia * 0.6) * dt;

                if (p.dist >= p.traco.total) {
                    const fim = p.traco.pontos[p.traco.pontos.length - 1];
                    flashes.push({ x: fim.x, y: fim.y, vida: 0 });
                    pulsos.splice(i, 1);
                    continue;
                }

                // cauda do pulso
                for (let k = 7; k >= 1; k--) {
                    const d = p.dist - k * 7;
                    if (d < 0) continue;
                    const pt = pontoNoTraco(p.traco, d);
                    ctx.fillStyle = "rgba(120,225,255," + ((1 - k / 8) * 0.7) + ")";
                    ctx.beginPath();
                    ctx.arc(pt.x, pt.y, 1.6, 0, DOIS_PI);
                    ctx.fill();
                }

                // cabeça com halo de luz (sprite pré-renderizado)
                const cabeca = pontoNoTraco(p.traco, p.dist);
                ctx.drawImage(spriteHalo, cabeca.x - RAIO_HALO, cabeca.y - RAIO_HALO);
            }
        }

        function desenharFlashes(dt) {

            for (let i = flashes.length - 1; i >= 0; i--) {

                const f = flashes[i];
                f.vida += dt * 1.8;

                if (f.vida >= 1) {
                    flashes.splice(i, 1);
                    continue;
                }

                const alfa = 1 - f.vida;

                ctx.strokeStyle = "rgba(140,230,255," + (alfa * 0.9) + ")";
                ctx.lineWidth = 1.6;
                ctx.beginPath();
                ctx.arc(f.x, f.y, 4 + f.vida * 16, 0, DOIS_PI);
                ctx.stroke();

                ctx.fillStyle = "rgba(190,242,255," + alfa + ")";
                ctx.beginPath();
                ctx.arc(f.x, f.y, 2.5, 0, DOIS_PI);
                ctx.fill();
            }
        }

        function desenharPalavras(dt) {

            // surgimento espontâneo (mais frequente quando há energia de scroll)
            if (Math.random() < (0.72 + energia * 1.1) * dt) {
                criarPalavra(Math.random() * largura, Math.random() * altura);
            }

            ctx.textBaseline = "middle";

            for (let i = palavras.length - 1; i >= 0; i--) {

                const w = palavras[i];
                w.vida += dt;
                w.y -= 7 * dt;

                if (w.vida >= w.duracao) {
                    palavras.splice(i, 1);
                    continue;
                }

                const alfa = Math.min(w.vida / 1.2, 1, (w.duracao - w.vida) / 1.5) * 0.38;

                ctx.font = w.tamanho + "px 'Consolas','Courier New',monospace";
                ctx.fillStyle = "rgba(0,210,255," + alfa + ")";
                ctx.fillText(w.texto, w.x, w.y);
            }
        }

        // o canvas dinâmico roda a ~30 fps; o parallax (só transform, barato
        // na GPU) continua a cada quadro — corta quase metade do custo
        const INTERVALO_CANVAS = 1 / 32;
        let acumuladoCanvas = 0;

        function quadro(agoraMs) {

            const dt = Math.min((agoraMs - antesMs) / 1000, 0.05);
            antesMs = agoraMs;

            // parallax: camadas deslizam com o scroll e com o mouse (via GPU)
            const scroll = window.scrollY;
            const oxFundo = -30 + mouse.x * -8;
            const oyFundo = -Math.min(scroll * 0.015, extra - 10) + mouse.y * -5;
            const oxFrente = -30 + mouse.x * -18;
            const oyFrente = -Math.min(scroll * 0.035, extra - 10) + mouse.y * -10;

            divFundo.style.transform = "translate3d(" + oxFundo + "px," + oyFundo + "px,0)";

            const transformFrente = "translate3d(" + oxFrente + "px," + oyFrente + "px,0)";
            divFrente.style.transform = transformFrente;
            divGlow.style.transform = transformFrente;

            acumuladoCanvas += dt;

            if (acumuladoCanvas >= INTERVALO_CANVAS) {

                const passo = Math.min(acumuladoCanvas, 0.05);
                acumuladoCanvas = 0;

                // decai para 25% por segundo, independente da taxa de quadros
                energia *= Math.pow(0.25, passo);

                // a placa inteira acende conforme a energia do scroll;
                // com brilho ~0 a camada sai da composição (blur é caro)
                const brilho = Math.min(energia * 0.45, 0.55);
                divGlow.style.opacity = brilho.toFixed(3);
                divGlow.style.visibility = brilho < 0.02 ? "hidden" : "visible";

                // canvas dinâmico: apenas pulsos, flashes e palavras
                ctx.clearRect(0, 0, largura, altura);

                ctx.save();
                ctx.translate(oxFrente, oyFrente);
                desenharPulsos(passo);
                desenharFlashes(passo);
                ctx.restore();

                desenharPalavras(passo);
            }

            if (!reduzirMovimento) requestAnimationFrame(quadro);
        }

        requestAnimationFrame(quadro);

        return true;
    }

    if (!iniciarFundoCircuito()) {
        document.body.classList.add("fundo-fallback");
    }

    // =============================
    // MENU MOBILE
    // =============================

    window.toggleMenu = function () {
        const aberto = document.getElementById("menu").classList.toggle("show");
        const botao = document.querySelector(".menu-toggle");
        if (botao) {
            botao.setAttribute("aria-expanded", aberto);
            botao.setAttribute("aria-label", aberto
                ? t({ pt: "Fechar menu", en: "Close menu", es: "Cerrar menú" })
                : t({ pt: "Abrir menu", en: "Open menu", es: "Abrir menú" }));
        }
    };

    document.querySelectorAll('.menu li a').forEach(link => {
        link.addEventListener('click', () => {
            const menu = document.getElementById("menu");
            if (menu.classList.contains("show")) {
                menu.classList.remove("show");
            }
        });
    });

    // =============================
    // NAVBAR E BOTÃO VOLTAR AO TOPO
    // (efeitos de scroll aplicados no manipulador único, mais abaixo)
    // =============================

    const navbar = document.querySelector(".navbar");
    const btnTopo = document.getElementById("btnTopo");

    if (btnTopo) {

        btnTopo.addEventListener("click", () => {

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

        });

    }

    // =============================
    // SEMPRE COMEÇAR NO TOPO
    // =============================

    history.scrollRestoration = "manual";

    // só força o topo quando não há âncora na URL — assim links diretos
    // como site/#projetos continuam levando à seção certa
    window.onload = () => {
        if (!location.hash) {
            window.scrollTo({
                top: 0,
                behavior: "instant"
            });
        }
    };

    // =============================
    // ANIMAÇÃO AO SCROLL
    // =============================

    const reveals = document.querySelectorAll("section, .projeto-card, .timeline-item, .metrica, .cert-card, .contato-card");

    // delay escalonado para os cards dentro de grids (efeito cascata)
    document.querySelectorAll(".metricas-grid, .projetos-grid, .cert-grid, .contato-grid").forEach(grid => {
        grid.querySelectorAll(".metrica, .projeto-card, .cert-card, .contato-card").forEach((el, i) => {
            el.style.transitionDelay = Math.min(i * 80, 400) + "ms";
        });
    });

    const observadorReveal = new IntersectionObserver((entradas) => {

        entradas.forEach(entrada => {

            if (entrada.isIntersecting) {

                const el = entrada.target;

                el.classList.add("visible");
                observadorReveal.unobserve(el);

                // terminado o reveal, zera o delay da cascata e ativa
                // transições curtas — senão o hover demora a responder
                const atraso = parseFloat(el.style.transitionDelay) || 0;

                setTimeout(() => {
                    el.style.transitionDelay = "0ms";
                    el.classList.add("revelado");
                }, atraso + 750);
            }

        });

    }, { threshold: 0.1 });

    reveals.forEach(el => observadorReveal.observe(el));

    // =============================
    // CONTADORES DAS MÉTRICAS
    // =============================

    function animarContador(el) {

        const valor = parseInt(el.dataset.valor, 10);
        const prefixo = el.dataset.prefixo || "";
        const sufixo = el.dataset.sufixo || "";

        if (reduzirMovimento || isNaN(valor)) {
            el.textContent = prefixo + (el.dataset.valor || "") + sufixo;
            return;
        }

        const duracao = 1600;
        const inicio = performance.now();

        function passo(agora) {

            const t = Math.min(1, (agora - inicio) / duracao);
            const suave = 1 - Math.pow(1 - t, 3);

            el.textContent = prefixo + Math.round(valor * suave) + sufixo;

            if (t < 1) requestAnimationFrame(passo);

        }

        requestAnimationFrame(passo);

    }

    const observadorContador = new IntersectionObserver((entradas) => {

        entradas.forEach(entrada => {

            if (entrada.isIntersecting) {
                animarContador(entrada.target);
                observadorContador.unobserve(entrada.target);
            }

        });

    }, { threshold: 0.6 });

    document.querySelectorAll(".contador").forEach(el => observadorContador.observe(el));

    // =============================
    // TYPEWRITER DO HEADER
    // =============================

    const typewriter = document.getElementById("typewriter");

    if (typewriter) {

        const frases = t({
            pt: [
                "RPA · Automação de Processos",
                "Playwright · Selenium · Power Automate",
                "Python · C# · Flask",
                "APIs REST · Integrações de Sistemas",
                "IA aplicada · API OpenAI",
                "MySQL · SQL Server",
                "DevOps · Microsoft Azure"
            ],
            en: [
                "RPA · Process Automation",
                "Playwright · Selenium · Power Automate",
                "Python · C# · Flask",
                "REST APIs · System Integrations",
                "Applied AI · OpenAI API",
                "MySQL · SQL Server",
                "DevOps · Microsoft Azure"
            ],
            es: [
                "RPA · Automatización de Procesos",
                "Playwright · Selenium · Power Automate",
                "Python · C# · Flask",
                "APIs REST · Integraciones de Sistemas",
                "IA aplicada · API OpenAI",
                "MySQL · SQL Server",
                "DevOps · Microsoft Azure"
            ]
        });

        if (reduzirMovimento) {

            typewriter.textContent = frases[0];

        } else {

            let fraseAtual = 0;
            let caractere = 0;
            let apagando = false;

            function digitar() {

                const frase = frases[fraseAtual];

                caractere += apagando ? -1 : 1;
                typewriter.textContent = frase.slice(0, caractere);

                let espera = apagando ? 30 : 65;

                if (!apagando && caractere === frase.length) {
                    espera = 1800;
                    apagando = true;
                } else if (apagando && caractere === 0) {
                    apagando = false;
                    fraseAtual = (fraseAtual + 1) % frases.length;
                    espera = 350;
                }

                setTimeout(digitar, espera);

            }

            digitar();

        }

    }

    // =============================
    // MANIPULADOR ÚNICO DE SCROLL
    // (navbar, botão topo, barra de progresso, timeline e menu ativo)
    // =============================

    const barraProgresso = document.getElementById("barra-progresso");
    const timeline = document.querySelector(".timeline");
    const secoes = document.querySelectorAll("section[id]");
    const linksMenu = document.querySelectorAll(".menu li a[href^='#']");

    // medidas em cache: ler offsetTop/scrollHeight a cada scroll força
    // recálculo de layout e era uma das causas das travadas
    let alturaRolavel = 0;
    let topoSecoes = [];
    let topoTimeline = 0;
    let alturaTimeline = 0;

    function medirPagina() {

        alturaRolavel = document.documentElement.scrollHeight - window.innerHeight;

        topoSecoes = Array.from(secoes, s => ({ id: s.id, topo: s.offsetTop }));

        if (timeline) {

            // soma offsetTop pela cadeia de offsetParent: ignora os
            // transforms temporários das animações de reveal
            let el = timeline;
            let topo = 0;

            while (el) {
                topo += el.offsetTop;
                el = el.offsetParent;
            }

            topoTimeline = topo;
            alturaTimeline = timeline.offsetHeight;
        }
    }

    function atualizarScroll() {

        const y = window.scrollY;

        if (navbar) navbar.classList.toggle("navbar-scroll", y > 50);

        if (btnTopo) btnTopo.style.display = y > 300 ? "flex" : "none";

        // barra de progresso no topo da página
        if (barraProgresso) {
            barraProgresso.style.width = (alturaRolavel > 0 ? (y / alturaRolavel) * 100 : 0) + "%";
        }

        // linha da timeline se desenha conforme o scroll
        if (timeline && alturaTimeline > 0) {
            const progresso = (y + window.innerHeight * 0.8 - topoTimeline) / alturaTimeline;
            timeline.style.setProperty("--progresso", (Math.min(1, Math.max(0, progresso)) * 100) + "%");
        }

        // destaca no menu a seção visível
        let secaoAtual = "";

        topoSecoes.forEach(s => {
            if (y + 150 >= s.topo) {
                secaoAtual = s.id;
            }
        });

        linksMenu.forEach(link => {
            link.classList.toggle("ativo", link.getAttribute("href") === "#" + secaoAtual);
        });

    }

    // agrupa todo o trabalho de scroll em no máximo 1 execução por quadro
    let scrollAgendado = false;

    window.addEventListener("scroll", () => {

        if (scrollAgendado) return;
        scrollAgendado = true;

        requestAnimationFrame(() => {
            scrollAgendado = false;
            atualizarScroll();
        });

    }, { passive: true });

    let aguardandoMedida;

    window.addEventListener("resize", () => {
        clearTimeout(aguardandoMedida);
        aguardandoMedida = setTimeout(() => {
            medirPagina();
            atualizarScroll();
        }, 200);
    });

    window.addEventListener("load", () => {
        medirPagina();
        atualizarScroll();
    });

    medirPagina();
    atualizarScroll();

    // =============================
    // EFEITO TILT 3D NOS CARDS DE PROJETO
    // =============================

    if (!reduzirMovimento && window.matchMedia("(hover: hover)").matches) {

        document.querySelectorAll(".projeto-card, .cert-card, .contato-card").forEach(card => {

            // mede o card uma vez ao entrar — getBoundingClientRect a cada
            // mousemove força recálculo de layout
            let rectCard = null;

            card.addEventListener("mouseenter", () => {
                rectCard = card.getBoundingClientRect();
            });

            card.addEventListener("mousemove", (e) => {

                if (!rectCard) rectCard = card.getBoundingClientRect();

                const x = (e.clientX - rectCard.left) / rectCard.width - 0.5;
                const y = (e.clientY - rectCard.top) / rectCard.height - 0.5;

                card.style.transform =
                    "perspective(800px) rotateX(" + (-y * 6).toFixed(2) + "deg) rotateY(" + (x * 6).toFixed(2) + "deg) translateY(-6px)";

            }, { passive: true });

            card.addEventListener("mouseleave", () => {
                rectCard = null;
                card.style.transform = "";
            });

        });

    }

    // =============================
    // CALCULAR DURAÇÃO AUTOMÁTICA
    // =============================

    function calcularDuracao(inicio, fim = null) {

        // parse manual (ano, mês) — "AAAA-MM-01" no new Date() é lido em UTC
        // e no fuso do Brasil voltava um dia, caindo no mês anterior
        function mesLocal(valor) {
            const partes = valor.split("-");
            return new Date(Number(partes[0]), Number(partes[1]) - 1, 1);
        }

        const start = mesLocal(inicio);
        const end = fim ? mesLocal(fim) : new Date();

        // contagem inclusiva do mês corrente, seguindo o padrão do LinkedIn
        let anos = end.getFullYear() - start.getFullYear();
        let meses = end.getMonth() - start.getMonth() + 1;

        if (meses < 0) {
            anos--;
            meses += 12;
        }

        if (meses >= 12) {
            anos++;
            meses -= 12;
        }

        const palavras = t({
            pt: { singAno: " ano", plurAno: " anos", singMes: " mês", plurMes: " meses", e: " e ", vazio: "menos de 1 mês" },
            en: { singAno: " year", plurAno: " years", singMes: " month", plurMes: " months", e: " and ", vazio: "less than 1 month" },
            es: { singAno: " año", plurAno: " años", singMes: " mes", plurMes: " meses", e: " y ", vazio: "menos de 1 mes" }
        });

        let resultado = "";

        if (anos > 0) {
            resultado += anos + (anos > 1 ? palavras.plurAno : palavras.singAno);
        }

        if (meses > 0) {
            if (resultado !== "") resultado += palavras.e;
            resultado += meses + (meses > 1 ? palavras.plurMes : palavras.singMes);
        }

        return resultado || palavras.vazio;
    }

    document.querySelectorAll(".duracao").forEach(el => {

        const inicio = el.dataset.inicio;
        const fim = el.dataset.fim;

        el.textContent = calcularDuracao(inicio, fim);

    });

    // =============================
    // MODAL DE DOWNLOAD DO CURRÍCULO
    // (escolha do idioma do PDF)
    // =============================

    const modalCurriculo = document.getElementById("modal-curriculo");

    if (modalCurriculo) {

        function abrirModal() {
            modalCurriculo.hidden = false;
            document.body.classList.add("modal-aberto");
        }

        function fecharModal() {
            modalCurriculo.hidden = true;
            document.body.classList.remove("modal-aberto");
        }

        // os botões "Currículo"/"Resume" abrem o modal em vez de baixar direto;
        // o href original fica como fallback para quem estiver sem JS
        document.querySelectorAll(".curriculo-download a, .mobile-download a").forEach(link => {
            link.removeAttribute("target");
            link.addEventListener("click", (e) => {
                e.preventDefault();
                abrirModal();
            });
        });

        modalCurriculo.querySelectorAll("[data-fechar]").forEach(el => {
            el.addEventListener("click", fecharModal);
        });

        // escolher um idioma fecha o modal e deixa o download seguir pelo <a>
        modalCurriculo.querySelectorAll(".modal-opcao").forEach(opcao => {
            opcao.addEventListener("click", fecharModal);
        });

        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && !modalCurriculo.hidden) fecharModal();
        });

    }

});
