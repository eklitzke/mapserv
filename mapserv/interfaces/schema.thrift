//////////////////
// SCHEMATA IDL //
//////////////////

enum ColType {
  INTEGER = 1,
  FLOAT = 2,
  TEXT = 3,
  BLOB = 4
}

struct ColDecl {
  1: string name,
  2: ColType type,
  3: bool spatial
}

struct TableDecl {
  1: string name,
  2: list<ColType> cols, // id, lat, lng, time are are all implicit
}

service SchemaService {
  void add_schema(1: TableDecl decl);
  void del_schema(1: string name);
}
