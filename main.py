"""
FarmShield AI - Entry Point
Run with: uv run python main.py
"""

from app.gradio_app import demo, _theme, CUSTOM_CSS

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",   # required for HuggingFace Spaces
        server_port=7860,
        share=False,
        show_error=True,
        theme=_theme,
        css=CUSTOM_CSS,
    )