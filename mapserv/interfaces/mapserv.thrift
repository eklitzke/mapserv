namespace py mapserv

typedef i64 Timestamp

enum Sort {
  TIME_DESC = 1,
  ID_DESC = 2,
  ID_ASC = 3
}

struct Coord {
  1: double lat,
  2: double lng
}

struct Cell {
  1: optional i64 id,
  2: Coord pos,
  3: optional Timestamp timestamp,
  4: optional binary data
}

struct Query {
  1: Coord nw,
  2: Coord se,
  3: optional Timestamp start,
  4: optional Sort sortby
  5: optional i32 limit,
}

service GeoBoxService {
  i64 insert(1: Cell cell);
  void expunge(1: i64 id);
  #void update(1: Cell cell);
  list<Cell> select(1: Query query);
}
