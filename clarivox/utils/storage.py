import os
from uuid import UUID

def save_outputs(uuid: UUID, transcript: str, fhir_data: dict, base_dir: str = "data"):
    os.makedirs(base_dir, exist_ok=True)

    with open(os.path.join(base_dir, f"{uuid}_transcript.txt"), "w") as f:
        f.write(transcript)

    with open(os.path.join(base_dir, f"{uuid}_fhir.json"), "w") as f:
        f.write(fhir_data.json(indent=2) if hasattr(fhir_data, "json") else str(fhir_data))