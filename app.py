from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from loaders import load_documents
from services.validator import validate_and_match
from models import save_insights, get_insights

app = FastAPI()

class ProcessRequest(BaseModel):
    doc_id: str
    id_uris: list[str]
    med_uris: list[str]

@app.post("/process")
async def process(req: ProcessRequest):
    # Load and process ID and medical documents\_n    id_docs  = await load_documents(req.id_uris)
    med_docs = await load_documents(req.med_uris)
    id_docs = await load_documents(req.id_uris)

    insights = await validate_and_match(id_docs, med_docs)
    await save_insights(req.doc_id, insights)
    return {"status": "ok", "doc_id": req.doc_id}

@app.get("/insights/{doc_id}")
async def read_insights(doc_id: str):
    record = await get_insights(doc_id)
    if not record:
        raise HTTPException(status_code=404, detail="No insights found")
    return record