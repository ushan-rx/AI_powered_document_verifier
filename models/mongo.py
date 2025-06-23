import os
from datetime import datetime
import motor.motor_asyncio

MONGO_URI = os.getenv("MONGO_URI")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["id_validator"]
collection = db["insights"]

async def save_insights(doc_id: str, payload: dict):
    await collection.update_one(
        {"doc_id": doc_id},
        {"$set": {"doc_id": doc_id, "timestamp": datetime.utcnow(), **payload}},
        upsert=True
    )

async def get_insights(doc_id: str) -> dict | None:
    return await collection.find_one({"doc_id": doc_id}, {"_id": 0})