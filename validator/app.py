from fastapi import FastAPI, HTTPException

from urllib.parse import urlparse

from pydantic import BaseModel

from loaders.doc_loaders import load_pdf, load_image


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

    print(all_docs)
    if not all_docs:
        raise HTTPException(400, "No documents found")
    return {"status": "ok", "doc_id": req.doc_id}

