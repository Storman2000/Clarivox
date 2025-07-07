import os
import json

def save_transcript(data_dir, file_id, transcript):
    path = os.path.join(data_dir, f"{file_id}_transcript.txt")
    with open(path, "w") as f:
        f.write(transcript)

def save_fhir_json(data_dir, file_id, data):
    path = os.path.join(data_dir, f"{file_id}_fhir.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)