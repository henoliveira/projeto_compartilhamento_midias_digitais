from pydantic import BaseModel


class Transaction(BaseModel):
    id: str
    query: str
    timestamp: str


class Node(BaseModel):
    id: str
    ip: str
    name: str
    is_connected: bool
    disconnected_at: str = ""


class File(BaseModel):
    id: str
    name: str
    size_bytes: int


class NodesFile(BaseModel):
    node_id: str
    file_id: str
    is_owner: bool
    is_blacklisted: bool
