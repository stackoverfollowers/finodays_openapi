import uvicorn
from fastapi import FastAPI
from json2xml import json2xml


def get_application():
    app = FastAPI(title="Parser JSON to XML")

    @app.post("/transfer_json_to_xml")
    def transfer_json_to_xml(data: dict) -> str:
        return json2xml.Json2xml(data).to_xml()

    return app


if __name__ == "__main__":
    app = get_application()
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
