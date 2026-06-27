import gradio as gr

from app.onnx_predict import predict_image
from app.config import CONF_THRESHOLD


CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg1: #061108;
    --bg2: #0d1d11;
    --bg3: #122918;
    --card: rgba(16, 30, 18, 0.92);
    --card2: rgba(22, 38, 24, 0.94);
    --border: rgba(74, 222, 128, 0.20);
    --green: #4ade80;
    --green2: #22c55e;
    --green3: #86efac;
    --yellow: #facc15;
    --red: #ef4444;
    --red2: #dc2626;
    --text: #ecffef;
    --muted: #9bc49f;
    --shadow: 0 14px 38px rgba(0,0,0,0.42);
    --radius: 18px;
}

/* Page */
body, .gradio-container {
    background:
        radial-gradient(circle at top left, rgba(34,197,94,0.15), transparent 28%),
        radial-gradient(circle at top right, rgba(250,204,21,0.10), transparent 25%),
        linear-gradient(135deg, var(--bg1), var(--bg2), var(--bg3));
    background-size: 200% 200%;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    min-height: 100vh;
    animation: gradientShift 15s ease infinite, fadeInPage 0.8s ease-out forwards;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes fadeInPage {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

.gradio-container {
    max-width: 1320px !important;
    margin: auto !important;
    padding: 18px !important;
}

/* ---------------- TOP DANGER BANNER ---------------- */
#danger-banner {
    display: none;
    width: 100%;
    margin-bottom: 16px;
    padding: 14px 20px;
    border-radius: 16px;
    background: linear-gradient(135deg, #7f1d1d, #b91c1c);
    border: 1px solid rgba(255,255,255,0.12);
    color: white;
    font-weight: 800;
    font-size: 1rem;
    letter-spacing: 0.03em;
    text-align: center;
    box-shadow: 0 12px 30px rgba(127,29,29,0.4);
}

#danger-banner.show {
    display: block;
    animation: blinkBanner 1s infinite;
}

@keyframes blinkBanner {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.65; transform: scale(1.01); }
}

/* ---------------- HERO ---------------- */
#fs-hero {
    position: relative;
    overflow: hidden;
    text-align: center;
    padding: 34px 24px 26px;
    margin-bottom: 18px;
    border-radius: 24px;
    background:
        linear-gradient(135deg, rgba(34,197,94,0.12), rgba(250,204,21,0.08)),
        rgba(255,255,255,0.02);
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    animation: floatHero 6s ease-in-out infinite;
}

@keyframes floatHero {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
}

#fs-hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 20% 20%, rgba(74,222,128,0.12), transparent 25%);
    pointer-events: none;
}

#fs-hero h1 {
    margin: 0;
    font-size: clamp(2.2rem, 4vw, 3.6rem);
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #4ade80, #d9f99d, #facc15);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

#fs-hero .subtitle {
    margin-top: 10px;
    color: var(--muted);
    font-size: 1.08rem;
    line-height: 1.7;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}

#fs-hero .hero-tagline {
    margin-top: 14px;
    font-size: 1.05rem;
    color: #d9ffe0;
    font-weight: 700;
}

.hero-slogan-row {
    margin-top: 18px;
    display: flex;
    gap: 12px;
    justify-content: center;
    flex-wrap: wrap;
}

.hero-slogan {
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--border);
    color: var(--green3);
    padding: 10px 16px;
    border-radius: 999px;
    font-size: 0.88rem;
    font-weight: 700;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}
.hero-slogan:hover {
    background: rgba(74,222,128,0.2);
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(74,222,128,0.3);
}

/* ---------------- BADGES ---------------- */
.badge-row {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 18px;
}
.fs-badge {
    background: rgba(255,255,255,0.06);
    color: var(--green);
    border: 1px solid var(--border);
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 700;
    backdrop-filter: blur(10px);
}
.fs-badge.live::before {
    content: "";
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #4ade80;
    display: inline-block;
    margin-right: 8px;
    animation: pulse 1.2s infinite;
}
@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.5); opacity: 0.5; }
    100% { transform: scale(1); opacity: 1; }
}

/* ---------------- CARDS ---------------- */
.fs-card {
    background: linear-gradient(180deg, var(--card), var(--card2));
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px;
    box-shadow: var(--shadow);
    backdrop-filter: blur(12px);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.fs-card:hover {
    transform: translateY(-2px);
    border-color: rgba(74, 222, 128, 0.35);
}

.section-label {
    font-size: 0.85rem;
    font-weight: 800;
    color: var(--green);
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* image */
.gradio-image {
    border-radius: 16px !important;
    overflow: hidden !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* ---------------- BUTTONS ---------------- */
#detect-btn {
    background: linear-gradient(135deg, #16a34a, #4ade80) !important;
    color: #041106 !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    box-shadow: 0 10px 25px rgba(34,197,94,0.30) !important;
    transition: 0.25s ease !important;
}
#detect-btn:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 14px 30px rgba(34,197,94,0.42) !important;
}

#clear-btn {
    background: rgba(255,255,255,0.06) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    font-weight: 700 !important;
}
#clear-btn:hover {
    background: rgba(255,255,255,0.10) !important;
}

/* ---------------- ALERT BOX ---------------- */
#alert-box textarea {
    background: rgba(0,0,0,0.35) !important;
    color: #bbf7d0 !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    font-size: 0.92rem !important;
    line-height: 1.7 !important;
    padding: 14px !important;
    min-height: 150px !important;
}

/* ---------------- STATS ---------------- */
.stat-strip {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin: 18px 0;
}
.stat-item {
    background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 16px;
    text-align: center;
    box-shadow: var(--shadow);
}
.stat-item .val {
    font-size: 1.3rem;
    font-weight: 800;
    color: var(--green);
}
.stat-item .key {
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ---------------- LIVE STATUS BAR ---------------- */
.live-status {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 16px;
}
.live-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 12px;
    text-align: center;
}
.live-box .title {
    font-size: 0.72rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.live-box .value {
    margin-top: 6px;
    font-size: 1rem;
    font-weight: 800;
    color: var(--green3);
}

/* ---------------- POPUP ---------------- */
#animal-popup {
    position: fixed;
    top: 24px;
    right: 24px;
    z-index: 9999;
    min-width: 320px;
    max-width: 430px;
    background: linear-gradient(135deg, #7f1d1d, #991b1b);
    color: white;
    border-radius: 18px;
    box-shadow: 0 18px 45px rgba(0,0,0,0.5);
    padding: 18px 18px 16px;
    border: 1px solid rgba(255,255,255,0.15);
    display: none;
    animation: popupSlide 0.35s ease;
}
#animal-popup.show {
    display: block;
}
#animal-popup h3 {
    margin: 0 0 8px;
    font-size: 1.1rem;
}
#animal-popup p {
    margin: 0;
    font-size: 0.95rem;
    line-height: 1.5;
}
@keyframes popupSlide {
    from { transform: translateY(-20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

/* tabs */
.tabs > .tab-nav button {
    background: transparent !important;
    border: none !important;
    color: var(--muted) !important;
    font-weight: 700 !important;
    border-bottom: 2px solid transparent !important;
}
.tabs > .tab-nav button.selected {
    color: var(--green) !important;
    border-bottom-color: var(--green) !important;
}

/* creator card */
.creator-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px;
    line-height: 1.9;
    color: #dfffe4;
}
.creator-card b {
    color: var(--green);
}
.creator-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-top: 14px;
}
.creator-mini {
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 14px;
}

/* footer */
#fs-footer {
    margin-top: 18px;
    padding: 20px;
    text-align: center;
    color: var(--muted);
    border-top: 1px solid var(--border);
}

@media (max-width: 950px) {
    .stat-strip {
        grid-template-columns: repeat(2, 1fr);
    }
    .live-status {
        grid-template-columns: repeat(2, 1fr);
    }
    .creator-grid {
        grid-template-columns: 1fr;
    }
}

/* How it works grid */
.hiw-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-top: 10px;
}
.hiw-step {
    display: flex;
    align-items: center;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    padding: 16px;
    border-radius: 16px;
    transition: transform 0.2s, background 0.2s;
}
.hiw-step:hover {
    transform: translateX(8px);
    background: rgba(255,255,255,0.06);
    border-color: rgba(74, 222, 128, 0.4);
}
.hiw-icon {
    font-size: 2rem;
    margin-right: 16px;
    background: rgba(74,222,128,0.1);
    padding: 12px;
    border-radius: 50%;
}
.hiw-content b {
    color: var(--green);
    font-size: 1.1rem;
}
.hiw-content p {
    margin: 4px 0 0 0;
    color: var(--muted);
    font-size: 0.95rem;
}
"""

POPUP_HTML = """
<div id="animal-popup">
    <h3>🚨 Wildlife Alert</h3>
    <p id="animal-popup-text">Animal detected!</p>
</div>
"""

DANGER_BANNER_HTML = """
<div id="danger-banner">
    🚨 ALERT — WILDLIFE DETECTED IN FARM LAND
</div>
"""

HERO_HTML = """
<div id="fs-hero">
    <h1>🌾 FarmShield AI</h1>
    <div class="hero-tagline">Your Farm's 24/7 AI Gaurdian</div>
    <p class="subtitle">
        AI-powered wildlife intrusion detection for modern agriculture.
        FarmShield helps farmers monitor fields and receive alerts.
    </p>

    <div class="hero-slogan-row">
        <span class="hero-slogan">⚡ Real-Time Detection</span>
        <span class="hero-slogan">🎤 Warning System</span>
        <span class="hero-slogan">🛡️ Crop Protection Through AI</span>
    </div>

</div>
"""

HOW_IT_WORKS_HTML = """
<div class="hiw-container">
    <div class="hiw-step">
        <div class="hiw-icon">📸</div>
        <div class="hiw-content">
            <b>1. Capture</b>
            <p>Upload a farm image or stream live from a webcam.</p>
        </div>
    </div>
    <div class="hiw-step">
        <div class="hiw-icon">🧠</div>
        <div class="hiw-content">
            <b>2. AI Analysis</b>
            <p>FarmShield AI analyzes the frame in real-time using our specialized wildlife detector.</p>
        </div>
    </div>
    <div class="hiw-step">
        <div class="hiw-icon">🎯</div>
        <div class="hiw-content">
            <b>3. Detection</b>
            <p>Elephant, Bear, or Boar intrusions are highlighted instantly with bounding boxes.</p>
        </div>
    </div>
    <div class="hiw-step">
        <div class="hiw-icon">🚨</div>
        <div class="hiw-content">
            <b>4. Alert System</b>
            <p>A danger banner, popup, and Tamil voice warning trigger immediately to alert you.</p>
        </div>
    </div>
    <div class="hiw-step">
        <div class="hiw-icon">💾</div>
        <div class="hiw-content">
            <b>5. Logging</b>
            <p>Alert screenshots and history are saved securely for your records.</p>
        </div>
    </div>
</div>
"""

CREATOR_HTML = """
<div class="creator-card">
    <h3 style="margin-top:0; color:#4ade80;">👨‍💻 Creator Details</h3>
    <p>
        <b>Project:</b> FarmShield AI – Your Farm's 24/7 AI Gaurdian<br>
    </p>

    <div class="creator-grid">
        <div class="creator-mini">
            <b>Creator</b><br>
            SHREERAM M K
        </div>
        <div class="creator-mini">
            <b>College / Department</b><br>
            Annamalai University / CSE-AI&ML
        </div>
        <div class="creator-mini">
            <b>Email</b><br>
            sumathidevan2006@gmail.com
        </div>
        <div class="creator-mini">
            <b>Phone</b><br>
            +91 9087418802
        </div>
        <div class="creator-mini">
            <b>GitHub / LinkedIn</b><br>
            github.com/Tobi24680
        </div>
    </div>

    <p style="margin-top:16px;">
        <b>Startup Vision</b><br>
        FarmShield AI aims to bring affordable AI-based wildlife monitoring to farms,
        reduce crop losses, improve farmer safety, and build a scalable smart agriculture security platform.
    </p>
</div>
"""

FOOTER_HTML = """
<div id="fs-footer">
    <b>FarmShield AI</b> · Protect Crops. Prevent Losses. Detect Wildlife. SHREERAM M K · @2026
</div>
"""

ALERT_JS = """
function startAnimalAlertWatcher() {
    let lastMessage = "";

    function speakTamil(text) {
        if (!window.speechSynthesis) return;

        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = "ta-IN";
        utter.rate = 1.0;
        utter.pitch = 1.0;
        utter.volume = 1.0;

        const voices = speechSynthesis.getVoices();
        const tamilVoice = voices.find(v => v.lang && v.lang.toLowerCase().includes("ta"));
        if (tamilVoice) {
            utter.voice = tamilVoice;
        }

        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utter);
    }

    function showPopup(msg) {
        const popup = document.getElementById("animal-popup");
        const text = document.getElementById("animal-popup-text");
        if (!popup || !text) return;

        text.innerText = msg;
        popup.classList.add("show");

        setTimeout(() => {
            popup.classList.remove("show");
        }, 5000);
    }

    function showDangerBanner(msg) {
        const banner = document.getElementById("danger-banner");
        if (!banner) return;
        banner.innerText = "🚨 " + msg.toUpperCase();
        banner.classList.add("show");

        setTimeout(() => {
            banner.classList.remove("show");
        }, 7000);
    }

    function buildTamilMessage(alertText) {
        const lower = alertText.toLowerCase();
        let animals = [];

        if (lower.includes("elephant")) animals.push("யானை");
        if (lower.includes("bear")) animals.push("கரடி");
        if (lower.includes("boar")) animals.push("காட்டு பன்றி");

        if (animals.length === 0) return null;

        const joined = animals.join(" மற்றும் ");
        return `எச்சரிக்கை! ${joined} கண்டறியப்பட்டது. தயவுசெய்து உடனே கவனிக்கவும்.`;
    }

    function buildBannerMessage(alertText) {
        const lower = alertText.toLowerCase();
        let animals = [];

        if (lower.includes("elephant")) animals.push("ELEPHANT");
        if (lower.includes("bear")) animals.push("BEAR");
        if (lower.includes("boar")) animals.push("BOAR");

        if (animals.length === 0) {
            return "WILDLIFE DETECTED IN FARM SURVEILLANCE ZONE";
        }

        return `INTRUSION ALERT — ${animals.join(" & ")} DETECTED IN FARM ZONE`;
    }

    function watchAlertBox() {
        const wrapper = document.getElementById("alert-box");
        if (!wrapper) {
            setTimeout(watchAlertBox, 1000);
            return;
        }

        let area = null;
        const findField = () => {
            return wrapper.querySelector("textarea, input, div, span, pre")
                || document.querySelector("#alert-box textarea, #alert-box input, #alert-box div, #alert-box span, #alert-box pre");
        };

        const readValue = () => {
            if (!area) return "";
            if (area.value !== undefined) return area.value.trim();
            return (area.textContent || area.innerText || "").trim();
        };

        const handleAlert = () => {
            const value = readValue();
            if (!value || value === lastMessage) return;

            lastMessage = value;

            if (value.includes("ALERT TRIGGERED")) {
                const tamilMsg = buildTamilMessage(value) || "எச்சரிக்கை! விலங்கு கண்டறியப்பட்டது. தயவுசெய்து கவனிக்கவும்.";
                const bannerMsg = buildBannerMessage(value);

                showPopup(tamilMsg);
                showDangerBanner(bannerMsg);
                speakTamil(tamilMsg);
            }
        };

        const updateArea = () => {
            const newArea = findField();
            if (newArea && newArea !== area) {
                area = newArea;
                if (area.addEventListener) {
                    area.removeEventListener("input", handleAlert);
                    area.addEventListener("input", handleAlert);
                }
            }
        };

        updateArea();
        const observer = new MutationObserver(() => {
            updateArea();
            handleAlert();
        });

        observer.observe(wrapper, { childList: true, characterData: true, subtree: true });
        setInterval(handleAlert, 1200);
    }

    watchAlertBox();
}

window.addEventListener("load", startAnimalAlertWatcher);
"""


def build_app() -> gr.Blocks:
    with gr.Blocks(
        title="FarmShield AI - Wildlife Intrusion Detection"
    ) as demo:

        gr.HTML(POPUP_HTML)
        gr.HTML(DANGER_BANNER_HTML)
        gr.HTML(HERO_HTML)

        with gr.Tabs():
            with gr.Tab("🎯 Detection Dashboard"):
                with gr.Row(equal_height=False):
                    with gr.Column(scale=5, elem_classes=["fs-card"]):
                        gr.HTML('<div class="section-label">📷 Input Image / Farm Camera Capture</div>')
                        with gr.Tabs():
                            with gr.Tab("Upload Image"):
                                image_input = gr.Image(
                                    type="pil",
                                    sources=["upload", "clipboard"],
                                    label="Upload Image",
                                    show_label=False,
                                    height=350,
                                    elem_classes=["gradio-image"],
                                )
                            with gr.Tab("Live Stream"):
                                webcam_input = gr.Image(
                                    type="pil",
                                    sources=["webcam"],
                                    streaming=True,
                                    label="Live Webcam",
                                    show_label=False,
                                    height=350,
                                    elem_classes=["gradio-image"],
                                )

                        with gr.Row():
                            detect_btn = gr.Button(
                                "🔍 Run Detection",
                                elem_id="detect-btn"
                            )
                            clear_btn = gr.ClearButton(
                                components=[image_input, webcam_input],
                                value="🗑 Clear",
                                elem_id="clear-btn"
                            )

                    with gr.Column(scale=5, elem_classes=["fs-card"]):
                        gr.HTML('<div class="section-label">🎯 Detection Result / Monitored Output</div>')
                        image_output = gr.Image(
                            type="pil",
                            show_label=False,
                            height=390,
                            elem_classes=["gradio-image"],
                            interactive=False,
                        )

                with gr.Row():
                    with gr.Column(elem_classes=["fs-card"]):
                        gr.HTML('<div class="section-label">🚨 Alert Status & Incident Log</div>')
                        alert_output = gr.Textbox(
                            label="",
                            placeholder="Detection alerts, warning messages and log status will appear here...",
                            lines=7,
                            max_lines=10,
                            elem_id="alert-box",
                            interactive=False,
                        )

            with gr.Tab("ℹ️ About App"):
                gr.HTML(HOW_IT_WORKS_HTML)
                gr.Markdown(
                    "**Alert Log:** Alerts are automatically stored in `alerts/alert_log.csv` and screenshots are saved in `alerts/screenshots/`."
                )

            with gr.Tab("📞 Contact Us"):
                gr.HTML(CREATOR_HTML)

        gr.HTML(FOOTER_HTML)

        detect_btn.click(
            fn=predict_image,
            inputs=[image_input],
            outputs=[image_output, alert_output],
            api_name="detect",
        )

        image_input.change(
            fn=predict_image,
            inputs=[image_input],
            outputs=[image_output, alert_output],
        )

        webcam_input.stream(
            fn=predict_image,
            inputs=[webcam_input],
            outputs=[image_output, alert_output],
        )

        demo.load(js=ALERT_JS)

    return demo


demo = build_app()