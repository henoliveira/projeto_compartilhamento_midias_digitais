import os
import shutil

import uvicorn
from fastapi import FastAPI, Query, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pony.orm import db_session

# from pythonp2p.portforwardlib import forwardPort
from requests import get
from schemas import Files

from p2p import node

# fw = forwardPort("1337", "1337", None, None, False, "TCP", 0, "", True)


app = FastAPI()
# node.ip = get("https://api.ipify.org").content.decode("utf8")
node.start()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
SHARED_FOLDER = f"{os.getcwd()}/shared/"
if not os.path.exists(SHARED_FOLDER):
    os.makedirs(os.path.dirname(SHARED_FOLDER), exist_ok=True)
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
def connect_to_peer(
    known_peers: str = Query(enum=node.peers, default=""),
    address: str = "",
    port: int = 65432,
):
    if address:
        node.connect_to(address, port)
    else:
        node.connect_to(known_peers)
    return {"peers": node.peers, "nodes_connected": node.connected_nodes}


@app.get("/request")
def request_file(file_id: str):
    node.requestFile(file_id)
    return {"peers": node.peers, "nodes_connected": node.connected_nodes}


@app.get("/file", tags=["file"])
@db_session
def get_files():
    files = [file.to_dict() for file in Files.select()]
    return files


@app.get("/file/{file_name}", tags=["file"])
@db_session
def get_file(file_name: str):
    file = Files.get(name=file_name).to_dict()
    if not file:
        return JSONResponse(content={"message": "File not found"}, status_code=404)
    return file


@app.post("/file", tags=["file"])
@db_session
def create_file(request: Request, upload: UploadFile):
    file_destination = f"{SHARED_FOLDER}/{upload.filename}"

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
    return JSONResponse(content=response, status_code=201)


@app.delete("/file/{file_name}", tags=["file"])
@db_session
def delete_file(file_name: str):
    file = Files.get(name=file_name)
    if not file:
        return JSONResponse(content={"message": "File not found"}, status_code=404)
    response = file.to_dict()
    file.delete()
    os.remove(f"{SHARED_FOLDER}/{file_name}")
    return JSONResponse(content=response, status_code=200)


@app.get("/peers", tags=["misc"])
def send_peers():
    node.loadstate()
    node.send_peers()
    return {"peers": node.peers}


@app.get("/hello", tags=["misc"])
def send_hello():
    node.send_message(data='{"message": "Hello World!"}')
    print(node.peers)
    return {"message": "Hello World!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=1337, reload=True)
