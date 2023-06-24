import os
import shutil

import uvicorn
from fastapi import FastAPI, Query, Request, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from pony.orm import db_session
from schemas import Files

from p2p import node

app = FastAPI()
node.start()
node.connect_to("3.225.100.86")
node.savestate()


SHARED_FOLDER = f"{os.getcwd()}/shared"
node.setfiledir(SHARED_FOLDER)


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/status")
def get_status():
    # printa os peers
    print(f"peers: {node.peers}")
    print(f"nodes_connected: {node.connected_nodes}")
    return {"peers": node.peers, "nodes_connected": node.connected_nodes}


@app.post("/connect")
def connect_to_peer(peer: str = Query(enum=node.peers)):
    node.connect_to(peer)
    return {"peers": node.peers, "nodes_connected": node.connected_nodes}


@app.get("/peers")
def send_peers():
    node.loadstate()
    node.send_peers()
    return {"peers": node.peers}


@app.get("/hello")
def send_hello():
    node.send_message(data='{"message": "Hello World!"}')
    print(node.peers)
    return {"message": "Hello World!"}


@app.get("/file")
@db_session
def get_files():
    files = [file.to_dict() for file in Files.select()]
    return files


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
