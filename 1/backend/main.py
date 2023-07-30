import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"result": "fasd[pjkofasjkl[fasjklfaskjlasf"}


if __name__ == "__main__":
    uvicorn.run(app, port=7000)
