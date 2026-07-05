# FarmShield on Hugging Face Spaces

This repository is prepared for deployment as a Hugging Face Space.

## Files to add in the Space
- app.py
- requirements.txt
- app/
- models/
- alerts/

## Launch command
The Space should run:
```bash
python app.py
```

## Notes
- The app uses Gradio and listens on port 7860.
- The ONNX model file is tracked via Git LFS.
