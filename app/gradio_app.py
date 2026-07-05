import gradio as gr
from app.onnx_predict import predict_image, predict_webrtc_stream
from fastrtc import WebRTC
from app.config import CONF_THRESHOLD


CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── CSS Variables ────────────────────────────────────── */
:root {
    --bg1: #04080a;
    --bg2: #071210;
    --bg3: #0a1a14;
    --card: rgba(12, 26, 18, 0.88);
    --card2: rgba(18, 36, 24, 0.92);
    --card-hover: rgba(22, 44, 30, 0.95);
    --border: rgba(74, 222, 128, 0.18);
    --border-hover: rgba(74, 222, 128, 0.40);
    --border-glow: rgba(74, 222, 128, 0.55);
    --green: #4ade80;
    --green2: #22c55e;
    --green3: #86efac;
    --green-dim: rgba(74, 222, 128, 0.12);
    --yellow: #facc15;
    --red: #ef4444;
    --red2: #dc2626;
    --orange: #f97316;
    --cyan: #22d3ee;
    --text: #ecffef;
    --muted: #8fb896;
    --shadow: 0 16px 48px rgba(0,0,0,0.50);
    --shadow-glow: 0 0 30px rgba(74,222,128,0.12);
    --radius: 20px;
    --radius-sm: 14px;
    --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Page Background ──────────────────────────────────── */
body, .gradio-container {
    background:
        radial-gradient(ellipse at 10% 10%, rgba(34,197,94,0.10), transparent 35%),
        radial-gradient(ellipse at 90% 20%, rgba(250,204,21,0.06), transparent 30%),
        radial-gradient(ellipse at 50% 80%, rgba(34,211,238,0.04), transparent 30%),
        linear-gradient(160deg, var(--bg1) 0%, var(--bg2) 40%, var(--bg3) 100%);
    background-attachment: fixed;
    color: var(--text) !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
    min-height: 100vh;
    animation: fadeInPage 1s ease-out forwards;
    overflow-x: hidden;
}

@keyframes fadeInPage {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

.gradio-container {
    max-width: 1380px !important;
    margin: auto !important;
    padding: 20px !important;
}

/* ── Floating Ambient Particles (CSS only) ──────────── */
body::before, body::after {
    content: "";
    position: fixed;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    filter: blur(80px);
}
body::before {
    width: 400px; height: 400px;
    top: -100px; left: -80px;
    background: rgba(74,222,128,0.07);
    animation: floatParticle1 20s ease-in-out infinite;
}
body::after {
    width: 350px; height: 350px;
    bottom: -80px; right: -60px;
    background: rgba(250,204,21,0.05);
    animation: floatParticle2 25s ease-in-out infinite;
}
@keyframes floatParticle1 {
    0%,100% { transform: translate(0,0) scale(1); }
    33%     { transform: translate(60px,40px) scale(1.1); }
    66%     { transform: translate(-30px,80px) scale(0.95); }
}
@keyframes floatParticle2 {
    0%,100% { transform: translate(0,0) scale(1); }
    50%     { transform: translate(-50px,-60px) scale(1.15); }
}



/* ── HERO SECTION ─────────────────────────────────────── */
#fs-hero {
    position: relative;
    overflow: hidden;
    text-align: center;
    padding: 48px 28px 38px;
    margin-bottom: 22px;
    border-radius: 28px;
    background:
        linear-gradient(135deg, rgba(34,197,94,0.08), rgba(250,204,21,0.05), rgba(34,211,238,0.04)),
        rgba(255,255,255,0.015);
    border: 1px solid var(--border);
    box-shadow: var(--shadow), var(--shadow-glow);
    animation: heroFloat 8s ease-in-out infinite;
}
@keyframes heroFloat {
    0%,100% { transform: translateY(0); }
    50%     { transform: translateY(-5px); }
}

/* Animated glow ring behind hero */
#fs-hero::before {
    content: "";
    position: absolute;
    top: 50%; left: 50%;
    width: 500px; height: 500px;
    transform: translate(-50%,-50%);
    background: radial-gradient(circle, rgba(74,222,128,0.08), transparent 60%);
    pointer-events: none;
    animation: heroGlow 6s ease-in-out infinite alternate;
}
@keyframes heroGlow {
    from { opacity: 0.5; transform: translate(-50%,-50%) scale(0.9); }
    to   { opacity: 1;   transform: translate(-50%,-50%) scale(1.15); }
}

#fs-hero::after {
    content: "";
    position: absolute;
    top: -2px; right: -2px; bottom: -2px; left: -2px;
    border-radius: 29px;
    background: linear-gradient(135deg, rgba(74,222,128,0.15), transparent 40%, rgba(250,204,21,0.10), transparent);
    pointer-events: none;
    z-index: -1;
}

.hero-emoji {
    font-size: 3.8rem;
    display: block;
    margin-bottom: 8px;
    animation: emojiPulse 3s ease-in-out infinite;
}
@keyframes emojiPulse {
    0%,100% { transform: scale(1); }
    50%     { transform: scale(1.08); }
}

#fs-hero h1 {
    margin: 0;
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 900;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #4ade80 0%, #a7f3d0 30%, #facc15 60%, #fde68a 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientText 5s ease infinite;
}
@keyframes gradientText {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

#fs-hero .subtitle {
    margin-top: 14px;
    color: var(--muted);
    font-size: 1.08rem;
    line-height: 1.75;
    max-width: 780px;
    margin-left: auto;
    margin-right: auto;
}

#fs-hero .hero-tagline {
    margin-top: 12px;
    font-size: 1.15rem;
    color: #bbf7d0;
    font-weight: 800;
    letter-spacing: 0.02em;
}

/* ── Hero Feature Pills ───────────────────────────────── */
.hero-slogan-row {
    margin-top: 22px;
    display: flex;
    gap: 12px;
    justify-content: center;
    flex-wrap: wrap;
}

.hero-slogan {
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    color: var(--green3);
    padding: 12px 20px;
    border-radius: 999px;
    font-size: 0.88rem;
    font-weight: 700;
    backdrop-filter: blur(12px);
    transition: var(--transition);
    cursor: default;
    position: relative;
    overflow: hidden;
}
.hero-slogan::before {
    content: "";
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(74,222,128,0.12), transparent);
    transition: left 0.5s ease;
}
.hero-slogan:hover::before { left: 100%; }
.hero-slogan:hover {
    background: rgba(74,222,128,0.15);
    transform: translateY(-2px) scale(1.04);
    box-shadow: 0 6px 20px rgba(74,222,128,0.20);
    border-color: var(--border-hover);
}

/* ── Badges ───────────────────────────────────────────── */
.badge-row {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 18px;
}
.fs-badge {
    background: rgba(255,255,255,0.05);
    color: var(--green);
    border: 1px solid var(--border);
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
    backdrop-filter: blur(10px);
    transition: var(--transition);
}
.fs-badge:hover {
    background: rgba(74,222,128,0.10);
    transform: scale(1.03);
}
.fs-badge.live::before {
    content: "";
    width: 9px; height: 9px;
    border-radius: 50%;
    background: #4ade80;
    display: inline-block;
    margin-right: 8px;
    animation: livePulse 1.4s ease-in-out infinite;
    box-shadow: 0 0 8px rgba(74,222,128,0.5);
}
@keyframes livePulse {
    0%,100% { transform: scale(1); opacity: 1; box-shadow: 0 0 8px rgba(74,222,128,0.5); }
    50%     { transform: scale(1.6); opacity: 0.4; box-shadow: 0 0 16px rgba(74,222,128,0.8); }
}

/* ── Glass Cards ──────────────────────────────────────── */
.fs-card {
    background: linear-gradient(180deg, var(--card), var(--card2));
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 22px;
    box-shadow: var(--shadow);
    backdrop-filter: blur(20px);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}
.fs-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(74,222,128,0.25), transparent);
}
.fs-card:hover {
    transform: translateY(-3px);
    border-color: var(--border-hover);
    box-shadow: var(--shadow), 0 0 25px rgba(74,222,128,0.10);
    background: linear-gradient(180deg, var(--card-hover), var(--card2));
}

.section-label {
    font-size: 0.82rem;
    font-weight: 800;
    color: var(--green);
    margin-bottom: 14px;
    text-transform: uppercase;
    letter-spacing: 0.10em;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
}

/* ── Image Components ─────────────────────────────────── */
.gradio-image {
    border-radius: 16px !important;
    overflow: hidden !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    transition: var(--transition) !important;
}
.gradio-image:hover {
    border-color: rgba(74,222,128,0.20) !important;
}

/* ── Buttons ──────────────────────────────────────────── */
#detect-btn {
    background: linear-gradient(135deg, #16a34a, #22c55e, #4ade80) !important;
    background-size: 200% 200% !important;
    color: #041106 !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 15px 20px !important;
    box-shadow: 0 10px 30px rgba(34,197,94,0.30) !important;
    transition: var(--transition) !important;
    position: relative !important;
    overflow: hidden !important;
    letter-spacing: 0.02em !important;
    animation: btnGradient 4s ease infinite !important;
}
@keyframes btnGradient {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
#detect-btn:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 16px 40px rgba(34,197,94,0.45) !important;
}
#detect-btn:active {
    transform: translateY(0) scale(0.98) !important;
}

#clear-btn {
    background: rgba(255,255,255,0.04) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    padding: 15px 20px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    transition: var(--transition) !important;
}
#clear-btn:hover {
    background: rgba(255,255,255,0.08) !important;
    border-color: var(--border-hover) !important;
    transform: translateY(-2px) !important;
}

/* ── Alert Box ────────────────────────────────────────── */
#alert-box textarea {
    background: rgba(0,0,0,0.40) !important;
    color: #bbf7d0 !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-size: 0.92rem !important;
    font-family: 'Inter', monospace !important;
    line-height: 1.75 !important;
    padding: 16px !important;
    min-height: 160px !important;
    transition: border-color 0.3s ease !important;
}
#alert-box textarea:focus {
    border-color: var(--border-hover) !important;
    box-shadow: 0 0 20px rgba(74,222,128,0.08) !important;
}

/* Alert box state indicators */
#alert-box.has-alert textarea {
    border-color: rgba(239,68,68,0.40) !important;
    box-shadow: 0 0 20px rgba(239,68,68,0.08) !important;
}
#alert-box.has-safe textarea {
    border-color: rgba(74,222,128,0.35) !important;
    box-shadow: 0 0 20px rgba(74,222,128,0.08) !important;
}

/* ── Stats Strip ──────────────────────────────────────── */
.stat-strip {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin: 20px 0;
}
.stat-item {
    background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015));
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px 14px;
    text-align: center;
    box-shadow: var(--shadow);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}
.stat-item::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--green), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.stat-item:hover::before { opacity: 1; }
.stat-item:hover {
    transform: translateY(-3px);
    border-color: var(--border-hover);
}
.stat-item .emoji { font-size: 1.5rem; display: block; margin-bottom: 6px; }
.stat-item .val {
    font-size: 1.2rem;
    font-weight: 800;
    color: var(--green);
}
.stat-item .key {
    font-size: 0.72rem;
    color: var(--muted);
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.10em;
    font-weight: 600;
}

/* ── Live Status Bar ──────────────────────────────────── */
.live-status {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 18px;
}
.live-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 14px;
    text-align: center;
    transition: var(--transition);
}
.live-box:hover {
    border-color: var(--border-hover);
    background: rgba(255,255,255,0.05);
}
.live-box .title {
    font-size: 0.70rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.10em;
    font-weight: 700;
}
.live-box .value {
    margin-top: 6px;
    font-size: 1rem;
    font-weight: 800;
    color: var(--green3);
}



/* ── Tabs ─────────────────────────────────────────────── */
.tabs > .tab-nav {
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 0 !important;
}
.tabs > .tab-nav button {
    background: transparent !important;
    border: none !important;
    color: var(--muted) !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    padding: 12px 18px !important;
    border-bottom: 3px solid transparent !important;
    transition: var(--transition) !important;
    position: relative !important;
}
.tabs > .tab-nav button:hover {
    color: var(--green3) !important;
    background: rgba(74,222,128,0.04) !important;
}
.tabs > .tab-nav button.selected {
    color: var(--green) !important;
    border-bottom-color: var(--green) !important;
    background: rgba(74,222,128,0.06) !important;
}

/* ── How It Works ─────────────────────────────────────── */
.hiw-container {
    display: flex;
    flex-direction: column;
    gap: 0;
    margin-top: 14px;
    position: relative;
}
/* Vertical connector line */
.hiw-container::before {
    content: "";
    position: absolute;
    left: 37px;
    top: 24px;
    bottom: 24px;
    width: 2px;
    background: linear-gradient(180deg, var(--green), rgba(74,222,128,0.15));
    border-radius: 2px;
}
.hiw-step {
    display: flex;
    align-items: center;
    background: rgba(255,255,255,0.025);
    border: 1px solid transparent;
    padding: 18px 20px;
    border-radius: 18px;
    transition: var(--transition);
    position: relative;
    z-index: 1;
    margin-bottom: 6px;
}
.hiw-step:hover {
    transform: translateX(10px);
    background: rgba(255,255,255,0.05);
    border-color: var(--border-hover);
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}
.hiw-icon {
    font-size: 1.8rem;
    min-width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 18px;
    background: var(--green-dim);
    border: 1px solid var(--border);
    border-radius: 16px;
    transition: var(--transition);
}
.hiw-step:hover .hiw-icon {
    background: rgba(74,222,128,0.18);
    border-color: var(--border-hover);
    transform: scale(1.05);
}
.hiw-content b {
    color: var(--green);
    font-size: 1.05rem;
}
.hiw-content p {
    margin: 5px 0 0;
    color: var(--muted);
    font-size: 0.92rem;
    line-height: 1.5;
}

/* ── Creator Section ──────────────────────────────────── */
.creator-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 28px;
    line-height: 1.9;
    color: #dfffe4;
    position: relative;
    overflow: hidden;
}
.creator-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--green), var(--yellow), var(--cyan));
}
.creator-card h3 {
    margin-top: 0;
    color: var(--green);
    font-size: 1.2rem;
}
.creator-card b { color: var(--green); }
.creator-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 18px;
}
.creator-mini {
    background: rgba(255,255,255,0.035);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 18px;
    transition: var(--transition);
    text-align: center;
}
.creator-mini:hover {
    border-color: var(--border-hover);
    transform: translateY(-3px);
    background: rgba(255,255,255,0.05);
}
.creator-mini b {
    display: block;
    margin-bottom: 6px;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.creator-mini span {
    font-size: 0.92rem;
    color: var(--text);
}

/* ── Tech Stack Strip ─────────────────────────────────── */
.tech-strip {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 22px;
    padding-top: 18px;
    border-top: 1px solid var(--border);
}
.tech-badge {
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    color: var(--muted);
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 0.80rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: var(--transition);
}
.tech-badge:hover {
    border-color: var(--border-hover);
    color: var(--green3);
    transform: scale(1.03);
}

/* ── Footer ───────────────────────────────────────────── */
#fs-footer {
    margin-top: 24px;
    padding: 28px 20px;
    text-align: center;
    color: var(--muted);
    border-top: 1px solid var(--border);
    font-size: 0.88rem;
}
#fs-footer b { color: var(--green); }
#fs-footer .footer-links {
    margin-top: 10px;
    display: flex;
    gap: 18px;
    justify-content: center;
    flex-wrap: wrap;
}
#fs-footer .footer-links a {
    color: var(--muted);
    text-decoration: none;
    font-weight: 600;
    font-size: 0.82rem;
    transition: color 0.2s;
}
#fs-footer .footer-links a:hover { color: var(--green); }

/* ═══════════════════ RESPONSIVE ═══════════════════════ */
@media (max-width: 1024px) {
    .stat-strip { grid-template-columns: repeat(3, 1fr); }
    .creator-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
    .gradio-container { padding: 12px !important; }

    #fs-hero { padding: 32px 18px 26px; border-radius: 22px; }
    #fs-hero h1 { font-size: 2rem; }
    #fs-hero .subtitle { font-size: 0.95rem; }

    .stat-strip { grid-template-columns: repeat(2, 1fr); gap: 10px; }
    .live-status { grid-template-columns: repeat(2, 1fr); gap: 10px; }

    .fs-card { padding: 16px; border-radius: 16px; }

    .creator-grid { grid-template-columns: 1fr; }
    .creator-card { padding: 18px; }

    .hiw-container::before { left: 33px; }

    #detect-btn, #clear-btn {
        width: 100% !important;
        padding: 14px !important;
    }
}

@media (max-width: 600px) {
    #fs-hero h1 { font-size: 1.7rem; letter-spacing: -0.5px; }
    #fs-hero .hero-tagline { font-size: 0.95rem; }
    .hero-slogan { padding: 8px 14px; font-size: 0.78rem; }
    .hero-emoji { font-size: 2.8rem; }

    .stat-strip { grid-template-columns: 1fr 1fr; }
    .live-status { grid-template-columns: 1fr 1fr; }

    .hiw-step { padding: 14px; }
    .hiw-icon { min-width: 44px; height: 44px; font-size: 1.4rem; margin-right: 12px; }

    #animal-popup, #safe-popup {
        min-width: unset;
        left: 12px; right: 12px;
        max-width: unset;
    }
}

@media (max-width: 480px) {
    .gradio-container { padding: 8px !important; }
    #fs-hero { padding: 24px 14px 20px; }
    #fs-hero h1 { font-size: 1.45rem; }
    .stat-strip { grid-template-columns: 1fr; }
    .hero-slogan-row { gap: 8px; }
    .section-label { font-size: 0.75rem; }

    .tabs > .tab-nav button {
        font-size: 0.80rem !important;
        padding: 10px 12px !important;
    }
}

/* ── Scrollbar ────────────────────────────────────────── */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--bg1); }
::-webkit-scrollbar-thumb {
    background: rgba(74,222,128,0.20);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(74,222,128,0.35); }

/* ── Gradio overrides ─────────────────────────────────── */
.gradio-container .prose { color: var(--text) !important; }
.gradio-container .prose a { color: var(--green) !important; }
label, .label-wrap { color: var(--muted) !important; }

/* ── WebRTC specific ───────────────────────────────────── */
.my-group {max-width: 900px !important; margin: 0 auto !important;}
.my-column {display: flex !important; flex-direction: column; justify-content: center !important; align-items: center !important; text-align: center;}
#hidden-audio { position: absolute; width: 0; height: 0; opacity: 0; pointer-events: none; z-index: -1; }
"""

#  HTML TEMPLATES

DANGER_BANNER_HTML = """
<div id="danger-banner">
</div>
"""

HERO_HTML = """
<div id="fs-hero">
    <span class="hero-emoji">🛡️</span>
    <h1>FarmShield AI</h1>
    <div class="hero-tagline">Your Farm's 24 / 7 AI Guardian</div>
    <p class="subtitle">
        AI-powered wildlife monitoring system for safest farming.
        Real-time monitoring with instant alerts to protect your crops from
        <b>Elephants</b>, <b>Bears</b>, and <b>Wild Boars</b>.
    </p>

    <div class="hero-slogan-row">
        <span class="hero-slogan">⚡ Real-Time Detection</span>
        <span class="hero-slogan">🔊 Smart Alarm System</span>
    </div>

    <div class="badge-row">
        <span class="fs-badge live">System Active</span>
        <span class="fs-badge">YOLOv26 </span>
    </div>
</div>
"""

HOW_IT_WORKS_HTML = """
<div class="hiw-container">
    <div class="hiw-step">
        <div class="hiw-icon">📸</div>
        <div class="hiw-content">
            <b>1. Capture</b>
            <p>Upload a farm image or stream live from your webcam for real-time monitoring.</p>
        </div>
    </div>
    <div class="hiw-step">
        <div class="hiw-icon">🧠</div>
        <div class="hiw-content">
            <b>2. AI Analysis</b>
            <p>FarmShield's YOLOv26 model analyzes every frame in milliseconds using ONNX Runtime.</p>
        </div>
    </div>
    <div class="hiw-step">
        <div class="hiw-icon">🎯</div>
        <div class="hiw-content">
            <b>3. Detection & Labelling</b>
            <p>Elephants, Bears, or Boars are highlighted instantly with colour-coded bounding boxes and confidence labels.</p>
        </div>
    </div>
    <div class="hiw-step">
        <div class="hiw-icon">🔊</div>
        <div class="hiw-content">
            <b>4. Multi-Layer Alert</b>
            <p>On detection: a popup notification, alarm sound, and Tamil voice warning all fire together instantly.</p>
        </div>
    </div>
    <div class="hiw-step">
        <div class="hiw-icon">💾</div>
        <div class="hiw-content">
            <b>5. Logging & Records</b>
            <p>Alert screenshots are saved automatically with CSV logging — timestamps, animals, and confidence scores.</p>
        </div>
    </div>
</div>
"""

CREATOR_HTML = """
<div class="creator-card">
    <h3>👨‍💻 Creator Profile</h3>
    <p>
        <b>Project:</b> FarmShield AI — Your Farm's 24/7 AI Guardian<br>
    </p>

    <div class="creator-grid">
        <div class="creator-mini">
            <b>👤 Creator</b><br>
            <span>SHREERAM M K</span>
        </div>
        <div class="creator-mini">
            <b>🎓 Institution</b><br>
            <span>Annamalai University<br>CSE - AI & ML</span>
        </div>
        <div class="creator-mini">
            <b>📧 Email</b><br>
            <span>sumathidevan2006@gmail.com</span>
        </div>
        <div class="creator-mini">
            <b>📱 Phone</b><br>
            <span>+91 9087418802</span>
        </div>
        <div class="creator-mini">
            <b>🔗 GitHub</b><br>
            <span>github.com/Tobi24680</span>
        </div>
        <div class="creator-mini">
            <b>🚀 Focus</b><br>
            <span>AI Integration · Computer Vision · Security</span>
        </div>
    </div>

    <p style="margin-top:20px;">
        <b>🌟 Startup Vision</b><br>
        FarmShield AI aims to bring affordable AI-based wildlife monitoring to farms,
        reduce crop losses, improve farmer safety, and build a scalable smart agriculture security platform.
    </p>

    <div class="tech-strip">
        <span class="tech-badge">🧠 YOLOv26</span>
        <span class="tech-badge">⚡ ONNX Runtime</span>
        <span class="tech-badge">🎨 Gradio</span>
        <span class="tech-badge">🐍 Python</span>
    </div>
</div>
"""

FOOTER_HTML = """
<div id="fs-footer">
    <b>FarmShield AI</b> — Protect Crops · Prevent Losses · Detect Wildlife<br>
    Built by <b>SHREERAM M K</b> · Annamalai University · © 2026
    <div class="footer-links">
        <a href="https://github.com/Tobi24680" target="_blank">GitHub</a>
        <a href="mailto:sumathidevan2006@gmail.com">Email</a>
    </div>
</div>
"""

STATS_HTML = """
<div class="stat-strip">
    <div class="stat-item">
        <span class="emoji">🎯</span>
        <div class="val">3</div>
        <div class="key">Animal Classes</div>
    </div>
    <div class="stat-item">
        <span class="emoji">⚡</span>
        <div class="val">ONNX</div>
        <div class="key">Engine</div>
    </div>
</div>
"""


def build_app() -> gr.Blocks:
    with gr.Blocks(
        title="FarmShield AI — Wildlife Intrusion Detection & Alert System",
        css=CUSTOM_CSS,
    ) as demo:

        # ── Overlays ──
        gr.HTML(DANGER_BANNER_HTML)

        # ── Hero ──
        gr.HTML(HERO_HTML)

        with gr.Tabs():
            
            with gr.Tab("🎯 Detection Dashboard"):
                gr.HTML(STATS_HTML)
                with gr.Tabs():
                    with gr.Tab("📤 Image Upload"):
                        with gr.Row(equal_height=False):
                            with gr.Column(scale=5, elem_classes=["fs-card"]):
                                gr.HTML('<div class="section-label">📷 Input — Image Upload</div>')
                                image_input = gr.Image(
                                    type="pil",
                                    sources=["upload", "clipboard", "webcam"],
                                    label="Upload Image",
                                    show_label=False,
                                    height=370,
                                    elem_classes=["gradio-image"],
                                )
                                with gr.Row():
                                    detect_btn = gr.Button(
                                        "🔍  Run Detection",
                                        elem_id="detect-btn",
                                    )
                                    clear_btn = gr.ClearButton(
                                        components=[image_input],
                                        value="🗑  Clear",
                                        elem_id="clear-btn",
                                    )

                            with gr.Column(scale=5, elem_classes=["fs-card"]):
                                gr.HTML('<div class="section-label">🎯 Detection Result — Monitored Output</div>')
                                image_output = gr.Image(
                                    type="pil",
                                    show_label=False,
                                    height=410,
                                    elem_classes=["gradio-image"],
                                    interactive=False,
                                )

                    with gr.Tab("📹 Live Webcam"):
                        with gr.Row():
                            with gr.Column(scale=6, elem_classes=["fs-card", "my-column"]):
                                gr.HTML('<div class="section-label" style="justify-content: center;">📷 Live WebRTC Feed</div>')
                                gr.HTML('<div style="color: #4ade80; font-size: 0.9rem; margin-bottom: 12px; text-align: center;">🚀 Ultra-fast peer-to-peer video streaming with real-time AI detection</div>')
                                with gr.Group(elem_classes=["my-group"]):
                                    webcam_input = WebRTC(label="Live Webcam", rtc_configuration={}, mode="send-receive")
                                    conf_threshold_webrtc = gr.Slider(
                                        label="Confidence Threshold",
                                        minimum=0.0,
                                        maximum=1.0,
                                        step=0.05,
                                        value=CONF_THRESHOLD,
                                        interactive=True,
                                    )
                            with gr.Column(scale=4, elem_classes=["fs-card"]):
                                gr.HTML('<div class="section-label">🧠 How YOLO Detects Animals</div>')
                                gr.HTML('''
                                <div style="margin-bottom: 15px; color: var(--text); font-size: 0.95rem; line-height: 1.6;">
                                    <b>📹 FarmShield AI in Action:</b> Watch this real-world demonstration showing how the system instantly detects wildlife and triggers alerts.
                                </div>
                                <div style="border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.3); border: 1px solid var(--border-color); background: #000;">
                                    <iframe width="100%" height="380" src="https://www.youtube.com/embed/-PqtzxrDXPI?autoplay=0&mute=0" title="FarmShield AI Action" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                                </div>
                                ''')

                with gr.Row():
                    with gr.Column(elem_classes=["fs-card"]):
                        gr.HTML('<div class="section-label">🚨 Alert Status & Incident Log</div>')
                        alert_output = gr.Textbox(
                            label="",
                            placeholder="Detection alerts, warning messages and live monitoring status will appear here...",
                            lines=7,
                            max_lines=12,
                            elem_id="alert-box",
                            interactive=False,
                        )
                        audio_output = gr.Audio(label="Alert Audio", autoplay=True, elem_id="hidden-audio")

            
            with gr.Tab("ℹ️ How It Works"):
                gr.HTML(HOW_IT_WORKS_HTML)
                gr.Markdown(
                    "**📋 Alert Log:** All detections are automatically stored in `alerts/alert_log.csv` "
                    "and annotated screenshots are saved in `alerts/screenshots/`."
                )

           
            with gr.Tab("📞 Contact & About"):
                gr.HTML(CREATOR_HTML)

        # ── Footer ──
        gr.HTML(FOOTER_HTML)


        # Image upload → detect button
        detect_btn.click(
            fn=predict_image,
            inputs=[image_input],
            outputs=[image_output, alert_output, audio_output],
            api_name="detect",
        )

        # WebRTC → real-time ultra-low latency detection
        webcam_input.stream(
            fn=predict_webrtc_stream,
            inputs=[webcam_input, conf_threshold_webrtc],
            outputs=[webcam_input, alert_output, audio_output],
            time_limit=10
        )



    return demo


demo = build_app()