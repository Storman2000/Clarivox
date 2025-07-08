import os
from uuid import UUID
from typing import Union
from pydantic import BaseModel

def save_outputs(uuid: UUID, transcript: str, fhir_data: Union[str, BaseModel], base_dir: str = "data") -> None:
    os.makedirs(base_dir, exist_ok=True)

    transcript_path = os.path.join(base_dir, f"{uuid}_transcript.txt")
    fhir_path = os.path.join(base_dir, f"{uuid}_fhir.json")

    with open(transcript_path, "w") as f:
        f.write(transcript)

    with open(fhir_path, "w") as f:
        if isinstance(fhir_data, BaseModel):
            f.write(fhir_data.json(indent=2))
        else:
            f.write(str(fhir_data))