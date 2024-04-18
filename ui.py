import gradio as gr
import requests
import yaml

with open("config.yml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


def ask_question_api(question: str):
    url = f"http://{config['server_ip']}:{config['server_port']}/ask-question"
    data = {"question": question}
    try:
        response = requests.post(url=url, json=data)
        if response.status_code != 200:
            raise Exception(
                f"Failed to get response from server. status code: {response.status_code}"
            )
        return response.json()
    except Exception as e:
        print(e.args, response.json())


if __name__ == "__main__":
    ui = gr.Interface(
        fn=ask_question_api,
        inputs=["text"],
        outputs=["text"],
    )
    ui.launch(server_name=config["ui_ip"], server_port=config["ui_port"])
