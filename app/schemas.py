from uuid import uuid4 as _uuid

from pony import orm as _orm

db_session = _orm.db_session
db = _orm.Database()


class Transactions(db.Entity):
    id = _orm.PrimaryKey(str)
    query = _orm.Required(str)
    timestamp = _orm.Required(str)


class Nodes(db.Entity):
    id = _orm.PrimaryKey(str)
    ip = _orm.Required(str)
    name = _orm.Required(str)
    is_connected = _orm.Required(bool)
    disconnected_at = _orm.Optional(str)
    files = _orm.Set("NodesFiles")


class Files(db.Entity):
    id = _orm.PrimaryKey(str)
    name = _orm.Required(str, unique=True)
    size_bytes = _orm.Required(int)
    nodes = _orm.Set("NodesFiles")


class NodesFiles(db.Entity):
    node_id = _orm.Required(Nodes)
    file_id = _orm.Required(Files)
    is_owner = _orm.Required(bool, default=True)
    is_blacklisted = _orm.Required(bool, default=False)
    _orm.PrimaryKey(node_id, file_id)


db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)
