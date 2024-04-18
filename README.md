# Simple IR-based Chatbot
This a sample chatbot project using FastAPI back-end and gradio front-end.

# How to run
- Copy your json file(s) dataset to `data` folder.
- Copy your model to `models` folder or just set huggingface model name (like `SajjadAyoubi/bert-base-fa-qa`) in `config.yml`. You can use any question-answering model from huggingface.
- Customize `config.yml` file.
- Open a new terminal and run:
    ```
    bash run_server.sh
    ```
- Open another terminal and run:
    ```
    bash run_ui.sh
    ```
- Open ui_ip:ui_port in your browser and start asking questions.
