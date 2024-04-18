from model import Model
from fastapi import FastAPI
import uvicorn
import yaml
from pydantic import BaseModel

app = FastAPI()

with open("config.yml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
model = Model()


class QuestionItem(BaseModel):
    question: str

    class Config:
        orm_mode = True


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/ask-question")
def ask_question(item: QuestionItem):
    return model.ask_question(question=item.question)


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        port=config["server_port"],
        host=config["server_ip"],
        log_level="info",
    )
