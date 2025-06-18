from fastapi import FastAPI

from pydantic import BaseModel
from validator.loaders.doc_loaders import load_pdf, load_image
from validator.chains.validator_chain import validate

app = FastAPI()

class ProcessRequest(BaseModel):
    doc_id: str
    uris: list[str]

@app.post("/process")
async def process(req: ProcessRequest):
    all_docs = []
    for uri in req.uris:
        path = uri  # download locally or stream
        if path.lower().endswith(".pdf"):
            docs = await load_pdf(path)
        else:
            docs = await load_image(path)
        all_docs += docs

    result_json = await validate(all_docs) # JSON string from the validation chain
    import json
    payload = json.loads(result_json)
    print(payload)
    return {"status": "ok", "doc_id": req.doc_id}

