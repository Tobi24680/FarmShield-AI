from app.gradio_app import demo, CUSTOM_CSS

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        share=True,
        show_error=True,
        css=CUSTOM_CSS,
    )