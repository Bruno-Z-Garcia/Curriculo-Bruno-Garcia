document.addEventListener("DOMContentLoaded", function () {

    // =============================
    // PARTICLES BACKGROUND
    // =============================

    particlesJS("particles-js", {
        particles: {
            number: { value: 100 },
            color: { value: "#00c3ff" },
            shape: { type: "circle" },
            opacity: { value: 0.3 },
            size: { value: 3 },
            line_linked: {
                enable: true,
                distance: 170,
                color: "#00c3ff",
                opacity: 0.2,
                width: 1
            },
            move: { enable: true, speed: 0.5 }
        },
        interactivity: {
            detect_on: "canvas",
            events: {
                onhover: { enable: true, mode: "grab" }
            }
        },
        retina_detect: true
    });

    // =============================
    // MENU MOBILE
    // =============================

    window.toggleMenu = function () {
        document.getElementById("menu").classList.toggle("show");
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
    // NAVBAR SCROLL
    // =============================

    window.addEventListener("scroll", () => {

        const navbar = document.querySelector(".navbar");

        if (window.scrollY > 50) {
            navbar.classList.add("navbar-scroll");
        } else {
            navbar.classList.remove("navbar-scroll");
        }

    });

    // =============================
    // BOTÃO VOLTAR AO TOPO
    // =============================

    const btnTopo = document.getElementById("btnTopo");

    if (btnTopo) {

        window.addEventListener("scroll", () => {

            if (window.scrollY > 300) {
                btnTopo.style.display = "flex";
            } else {
                btnTopo.style.display = "none";
            }

        });

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

    window.onload = () => {
        window.scrollTo({
            top: 0,
            behavior: "instant"
        });
    };

    // =============================
    // ANIMAÇÃO AO SCROLL
    // =============================

    const reveals = document.querySelectorAll("section, .projeto-card, .timeline-item, .metrica");

    function revealScroll() {

        const windowHeight = window.innerHeight;

        reveals.forEach(el => {

            const elementTop = el.getBoundingClientRect().top;

            if (elementTop < windowHeight - 100) {

                el.classList.add("visible");

            }

        });

    }

    window.addEventListener("scroll", revealScroll);

    revealScroll();

    // =============================
    // CALCULAR DURAÇÃO AUTOMÁTICA
    // =============================

    function calcularDuracao(inicio, fim = null) {

        const start = new Date(inicio + "-01");
        const end = fim ? new Date(fim + "-01") : new Date();

        let anos = end.getFullYear() - start.getFullYear();
        let meses = end.getMonth() - start.getMonth();

        if (meses < 0) {
            anos--;
            meses += 12;
        }

        let resultado = "";

        if (anos > 0) {
            resultado += anos + (anos > 1 ? " anos" : " ano");
        }

        if (meses > 0) {
            if (resultado !== "") resultado += " e ";
            resultado += meses + (meses > 1 ? " meses" : " mês");
        }

        return resultado || "menos de 1 mês";
    }

    document.querySelectorAll(".duracao").forEach(el => {

        const inicio = el.dataset.inicio;
        const fim = el.dataset.fim;

        el.textContent = calcularDuracao(inicio, fim);

    });

});