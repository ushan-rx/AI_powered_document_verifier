from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from loaders import load_pdf, load_image
from models import save_insights, get_insights

app = FastAPI()

class ProcessRequest(BaseModel):
    doc_id: str
    uris: list[str]

@app.post("/process")
async def process(req: ProcessRequest):
    all_docs = []
    for uri in req.uris:
        path = uri  #download locally or stream
        if path.lower().endswith(".pdf"):
            docs = await load_pdf(path)
        else:
            docs = await load_image(path)
        all_docs += docs

    result_json = await validate(all_docs)
    import json
    payload = json.loads(result_json)
    await save_insights(req.doc_id, {"fields": payload["fields"], "issues": payload["issues"]})
    return {"status": "ok", "doc_id": req.doc_id}

@app.get("/insights/{doc_id}")
async def read_insights(doc_id: str):
    record = await get_insights(doc_id)
    if not record:
        raise HTTPException(404, "No insights found")
    return record