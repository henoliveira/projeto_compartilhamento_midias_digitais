import os
import shutil

import uvicorn
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from pony.orm import db_session
from schemas import Files

from p2p import node

SHARED_FOLDER = f"{os.getcwd()}/shared"
node.setfiledir(SHARED_FOLDER)
app = FastAPI()


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/file")
@db_session
def get_files():
    files_names = [file.to_dict() for file in Files.select()]
    return files_names


@app.get("/file/{file_name}")
@db_session
def get_file(file_name: str):
    file = Files.get(name=file_name).to_dict()
    if not file:
        return JSONResponse(content={"message": "File not found"}, status_code=404)
    return file


@app.post("/file")
@db_session
def create_file(request: Request, upload: UploadFile):
    file_destination = f"{SHARED_FOLDER}/{upload.filename}"

    if not os.path.exists(file_destination):
        os.makedirs(os.path.dirname(file_destination), exist_ok=True)

    if upload.filename in [file.name for file in Files.select()]:
        return JSONResponse(content={"message": "File already exists"}, status_code=400)

    try:
        with open(file_destination, "wb") as buffer:
            shutil.copyfileobj(upload.file, buffer)
        upload.file.close()

    except Exception as e:
        shutil.rmtree(file_destination)
        raise e

    file_id = node.addfile(file_destination)

    file = Files(id=file_id, name=upload.filename, size_bytes=upload.size)
    response = file.to_dict()
    response.pop("id")
    return JSONResponse(content=response, status_code=201)


@app.delete("/file/{file_name}")
@db_session
def delete_file(file_name: str):
    file = Files.get(name=file_name)
    if not file:
        return JSONResponse(content={"message": "File not found"}, status_code=404)
    response = file.to_dict()
    file.delete()
    os.remove(f"{SHARED_FOLDER}/{file_name}")
    return JSONResponse(content=response, status_code=200)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=1337, reload=True)
