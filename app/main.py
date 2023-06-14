import os
import shutil

import uvicorn
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import RedirectResponse
from models import Files
from pony.orm import db_session

app = FastAPI()


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/hello")
def hello():
    return {"Hello": "World"}


@app.post("/file")
@db_session
def create_file(request: Request, upload: UploadFile):
    destination = f"{os.getcwd()}/misc/{upload.filename}"
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload.file, buffer)
        upload.file.close()
        file = {
            "name": upload.filename,
            "size_bytes": upload.size,
        }
        Files(**file)
        return file
    except Exception as e:
        shutil.rmtree(destination)
        raise e


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=1337, reload=True)
