from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    resourceType: str = "Task"
    status: str = "requested"
    intent: str = "order"
    authoredOn: str = datetime.utcnow().isoformat()
    description: str

def build_task(transcript: str, intent: str) -> Task:
    return Task(description=f"{intent.capitalize()} requested: {transcript}")