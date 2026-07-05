from app.gradio_app import demo

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        show_error=True,
    )