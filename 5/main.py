import uvicorn
from fastapi import FastAPI, Response
from json2xml import json2xml

APP_PORT = 8001


def get_application():
    app = FastAPI(title="Parser JSON to XML")

    @app.post("/transfer_json_to_xml")
    def transfer_json_to_xml(data: dict) -> str:
        if not data:
            return '<?xml version="1.0" ?><metadata></metadata>'
        content = json2xml.Json2xml(data).to_xml()
        return Response(content=content, media_type="application/xml")


    return app


if __name__ == "__main__":
    app = get_application()
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT, log_level="info")
