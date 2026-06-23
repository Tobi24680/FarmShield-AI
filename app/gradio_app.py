"""
FarmShield AI – Gradio UI
Premium Blocks-based interface optimised for HuggingFace Spaces deployment.
"""

import gradio as gr

from app.onnx_predict import predict_image
from app.config import CLASS_NAMES, CONF_THRESHOLD

# ─────────────────────────────────────────────────────────────────────────────
# Custom CSS  –  premium dark-green agri theme with glassmorphism
# ─────────────────────────────────────────────────────────────────────────────

CUSTOM_CSS = """
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root tokens ── */
:root {
    --fs-bg:          #0a0f0a;
    --fs-surface:     rgba(16, 28, 16, 0.85);
    --fs-card:        rgba(20, 38, 20, 0.90);
    --fs-border:      rgba(74, 222, 128, 0.18);
    --fs-green:       #4ade80;
    --fs-green-dark:  #16a34a;
    --fs-green-glow:  rgba(74, 222, 128, 0.25);
    --fs-amber:       #fbbf24;
    --fs-red:         #f87171;
    --fs-text:        #e2f5e2;
    --fs-muted:       #6b9e6b;
    --fs-radius:      14px;
    --fs-shadow:      0 8px 40px rgba(0, 0, 0, 0.6);
}

/* ── Page background ── */
body, .gradio-container {
    background: radial-gradient(ellipse at 20% 10%, #0f2810 0%, #050a05 60%, #000 100%) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--fs-text) !important;
    min-height: 100vh;
}

/* ── Hero header ── */
#fs-hero {
    text-align: center;
    padding: 40px 20px 20px;
    background: linear-gradient(135deg,
        rgba(22, 163, 74, 0.08) 0%,
        rgba(10, 15, 10, 0.0) 60%);
    border-bottom: 1px solid var(--fs-border);
    margin-bottom: 4px;
}

#fs-hero h1 {
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 800;
    background: linear-gradient(135deg, #4ade80 0%, #86efac 50%, #fbbf24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
    margin: 0 0 8px;
    line-height: 1.15;
}

#fs-hero .subtitle {
    font-size: 1.05rem;
    color: var(--fs-muted);
    font-weight: 400;
    margin-bottom: 20px;
}

/* ── Animated pulse badge ── */
.badge-row {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 8px 0 4px;
}
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--fs-card);
    border: 1px solid var(--fs-border);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--fs-green);
    backdrop-filter: blur(10px);
}
.badge.live::before {
    content: '';
    width: 7px; height: 7px;
    background: #4ade80;
    border-radius: 50%;
    display: inline-block;
    animation: pulse-dot 1.5s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(1.4); }
}

/* ── Main cards ── */
.fs-card {
    background: var(--fs-card);
    border: 1px solid var(--fs-border);
    border-radius: var(--fs-radius);
    padding: 20px;
    backdrop-filter: blur(16px);
    box-shadow: var(--fs-shadow);
    transition: border-color 0.3s ease;
}
.fs-card:hover { border-color: rgba(74, 222, 128, 0.35); }

/* ── Section labels ── */
.section-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: var(--fs-green);
    text-transform: uppercase;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 7px;
}

/* ── Gradio image widget ── */
.gradio-image {
    border-radius: 10px !important;
    border: 1px solid var(--fs-border) !important;
    overflow: hidden !important;
}

/* ── Detect button ── */
#detect-btn {
    background: linear-gradient(135deg, #16a34a 0%, #4ade80 100%) !important;
    color: #000 !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 32px !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(74, 222, 128, 0.3) !important;
    width: 100% !important;
    letter-spacing: 0.02em !important;
}
#detect-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(74, 222, 128, 0.45) !important;
}
#detect-btn:active {
    transform: translateY(0) !important;
}

/* ── Clear button ── */
#clear-btn {
    background: rgba(255,255,255,0.06) !important;
    color: var(--fs-muted) !important;
    border: 1px solid var(--fs-border) !important;
    border-radius: 10px !important;
    padding: 14px 32px !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
#clear-btn:hover {
    background: rgba(255,255,255,0.10) !important;
    color: var(--fs-text) !important;
}

/* ── Alert text box ── */
#alert-box textarea {
    background: rgba(0,0,0,0.4) !important;
    border: 1px solid var(--fs-border) !important;
    border-radius: 10px !important;
    color: var(--fs-green) !important;
    font-family: 'Inter', monospace !important;
    font-size: 0.88rem !important;
    line-height: 1.7 !important;
    min-height: 140px !important;
    resize: none !important;
    padding: 14px !important;
}

/* ── Info / stats strip ── */
.stat-strip {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: center;
    margin: 18px 0 4px;
}
.stat-item {
    background: var(--fs-card);
    border: 1px solid var(--fs-border);
    border-radius: 10px;
    padding: 10px 18px;
    text-align: center;
    min-width: 110px;
    backdrop-filter: blur(10px);
}
.stat-item .val {
    font-size: 1.3rem;
    font-weight: 800;
    color: var(--fs-green);
}
.stat-item .key {
    font-size: 0.68rem;
    color: var(--fs-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 2px;
}

/* ── Examples strip ── */
.example-strip {
    margin-top: 6px;
}

/* ── Footer ── */
#fs-footer {
    text-align: center;
    padding: 24px;
    font-size: 0.78rem;
    color: var(--fs-muted);
    border-top: 1px solid var(--fs-border);
    margin-top: 8px;
}
#fs-footer a { color: var(--fs-green); text-decoration: none; }

/* ── Tabpanel ── */
.tabs > .tab-nav button {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    color: var(--fs-muted) !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    transition: all 0.2s !important;
}
.tabs > .tab-nav button.selected {
    border-bottom-color: var(--fs-green) !important;
    color: var(--fs-green) !important;
}

/* ── Hide Gradio footer branding ── */
footer { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0f0a; }
::-webkit-scrollbar-thumb { background: #254d25; border-radius: 4px; }
"""

# ─────────────────────────────────────────────────────────────────────────────
# Hero HTML
# ─────────────────────────────────────────────────────────────────────────────

HERO_HTML = """
<div id="fs-hero">
  <h1>🌾 FarmShield AI</h1>
  <p class="subtitle">Wildlife Intrusion Detection &amp; Alert System for Smart Agriculture</p>
  <div class="badge-row">
    <span class="badge live">Live Detection</span>
    <span class="badge">🐻 Bear</span>
    <span class="badge">🐗 Boar</span>
    <span class="badge">🐘 Elephant</span>
    <span class="badge">⚡ ONNX CPU</span>
    <span class="badge">🤗 HuggingFace Ready</span>
  </div>
</div>
"""

STATS_HTML = f"""
<div class="stat-strip">
  <div class="stat-item"><div class="val">3</div><div class="key">Animal Classes</div></div>
  <div class="stat-item"><div class="val">YOLO</div><div class="key">Model Arch</div></div>
  <div class="stat-item"><div class="val">640²</div><div class="key">Input Size</div></div>
  <div class="stat-item"><div class="val">{int(CONF_THRESHOLD*100)}%</div><div class="key">Confidence</div></div>
  <div class="stat-item"><div class="val">CPU</div><div class="key">Inference</div></div>
</div>
"""

HOW_IT_WORKS_HTML = """
<div style="padding:10px 0; color:#6b9e6b; font-size:0.85rem; line-height:1.8;">
  <b style="color:#4ade80;">How it works</b><br>
  1️⃣  Upload a farm field image <em>or</em> capture one from your webcam.<br>
  2️⃣  The YOLO ONNX model analyses the image at 640×640 resolution on CPU.<br>
  3️⃣  Any detected Bear / Boar / Elephant triggers a colour-coded bounding box.<br>
  4️⃣  An alert is generated with timestamp and saved to <code>alerts/screenshots/</code>.<br>
  5️⃣  All detections are logged to <code>alerts/alert_log.csv</code>.
</div>
"""

FOOTER_HTML = """
<div id="fs-footer">
  Built with ❤️ using
  <a href="https://gradio.app" target="_blank">Gradio</a> ·
  <a href="https://onnxruntime.ai" target="_blank">ONNX Runtime</a> ·
  <a href="https://opencv.org" target="_blank">OpenCV</a>
  &nbsp;|&nbsp; FarmShield AI &copy; 2026
</div>
"""


# ─────────────────────────────────────────────────────────────────────────────
# Gradio Blocks app
# ─────────────────────────────────────────────────────────────────────────────

def build_app() -> gr.Blocks:
    with gr.Blocks(
        title="FarmShield AI - Wildlife Intrusion Detection",
    ) as demo:

        # ── Hero ──────────────────────────────────────────────────────────
        gr.HTML(HERO_HTML)
        gr.HTML(STATS_HTML)

        # ── Main workspace ────────────────────────────────────────────────
        with gr.Row(equal_height=False):

            # Left column – input
            with gr.Column(scale=5, elem_classes=["fs-card"]):
                gr.HTML('<div class="section-label">📷 &nbsp;Input Image</div>')
                image_input = gr.Image(
                    type="pil",
                    sources=["upload", "webcam"],
                    label="Upload a farm image or use webcam",
                    show_label=False,
                    height=380,
                    elem_classes=["gradio-image"],
                )
                with gr.Row():
                    detect_btn = gr.Button(
                        "🔍  Run Detection",
                        elem_id="detect-btn",
                        variant="primary",
                    )
                    clear_btn = gr.ClearButton(
                        components=[image_input],
                        value="🗑  Clear",
                        elem_id="clear-btn",
                    )

            # Right column – output
            with gr.Column(scale=5, elem_classes=["fs-card"]):
                gr.HTML('<div class="section-label">🎯 &nbsp;Detection Result</div>')
                image_output = gr.Image(
                    type="pil",
                    label="Annotated Output",
                    show_label=False,
                    height=380,
                    elem_classes=["gradio-image"],
                    interactive=False,
                )

        # ── Alert panel ───────────────────────────────────────────────────
        with gr.Row():
            with gr.Column(elem_classes=["fs-card"]):
                gr.HTML('<div class="section-label">🚨 &nbsp;Alert Status</div>')
                alert_output = gr.Textbox(
                    label="",
                    placeholder="Detection results and alerts will appear here...",
                    lines=7,
                    max_lines=10,
                    elem_id="alert-box",
                    interactive=False,
                )

        # ── Info tabs ─────────────────────────────────────────────────────
        with gr.Accordion("ℹ️  How it works & Project Info", open=False):
            with gr.Tabs():
                with gr.Tab("How It Works"):
                    gr.HTML(HOW_IT_WORKS_HTML)
                with gr.Tab("Animal Classes"):
                    gr.Dataframe(
                        value=[
                            ["0", "🐻 Bear",     "BGR (60, 20, 220)  – deep violet"],
                            ["1", "🐗 Boar",     "BGR (34,139, 34)  – forest green"],
                            ["2", "🐘 Elephant", "BGR (255,140,  0)  – vivid orange"],
                        ],
                        headers=["Class ID", "Animal", "Box Colour"],
                        datatype=["str", "str", "str"],
                        interactive=False,
                        row_count=3,
                    )
                with gr.Tab("Alert Log"):
                    gr.Markdown(
                        "Alerts are saved to `alerts/alert_log.csv` and "
                        "screenshots to `alerts/screenshots/` automatically."
                    )

        # ── Footer ────────────────────────────────────────────────────────
        gr.HTML(FOOTER_HTML)

        # ── Event wiring ──────────────────────────────────────────────────
        detect_btn.click(
            fn=predict_image,
            inputs=[image_input],
            outputs=[image_output, alert_output],
            api_name="detect",
        )

        # Also trigger on image change (upload / webcam snap)
        image_input.change(
            fn=predict_image,
            inputs=[image_input],
            outputs=[image_output, alert_output],
        )

    return demo


_theme = gr.themes.Base(
    primary_hue="green",
    neutral_hue="stone",
    font=gr.themes.GoogleFont("Inter"),
)

demo = build_app()