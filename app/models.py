from pony import orm

db = orm.Database()


class Transactions(db.Entity):
    id = orm.PrimaryKey(int)
    query = orm.Required(str)
    timestamp = orm.Required(str)


class Nodes(db.Entity):
    id = orm.PrimaryKey(int)
    ip = orm.Required(str)
    name = orm.Required(str)
    is_connected = orm.Required(bool)
    disconnected_at = orm.Optional(str)
    files = orm.Set("NodesFiles")


class Files(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(str)
    size_bytes = orm.Required(int)
    nodes = orm.Set("NodesFiles")


class NodesFiles(db.Entity):
    node_id = orm.Required(Nodes)
    file_id = orm.Required(Files)
    is_owner = orm.Required(bool)
    is_blacklisted = orm.Required(bool)
    orm.PrimaryKey(node_id, file_id)


db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)
