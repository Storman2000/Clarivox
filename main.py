from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
import whisper

app = FastAPI()

@app.post("/voicemail/upload")
async def upload_voicemail(file: UploadFile = File(...)):
    try:
        # Save file to disk
        file_location = f"temp_voicemails/{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Load Whisper model and transcribe
        model = whisper.load_model("base")  # You must have this downloaded already
        result = model.transcribe(file_location)

        return JSONResponse(content={"transcription": result["text"]})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

