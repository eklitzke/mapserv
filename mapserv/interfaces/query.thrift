///////////////
// QUERY IDL //
///////////////

enum Order {
  ASC = 1,
  DESC = 2
}

enum Equality {
  EQ  = 1,
  NEQ = 2,
  LT  = 3,
  LTE = 4,
  GT  = 5,
  GTE = 6
}

struct Column {
  1: optional string table,
  2: string name,
  3: bool spatial
}

enum ColumnType {
  INTEGER = 1,
  REAL = 2,
  TEXT = 3,
  BLOB = 4
  SPATIAL = 5,
}

struct CreateColumn {
  1: string name,
  2: ColumnType type
}

// N.B. this is a union type
struct Target {
  1: optional Column col,  // logical targets
  2: optional i64 ival,    // literal targets
  3: optional double fval,
  4: optional string sval,
  5: optional binary bval,
  6: optional bool nullity
}

struct EqComparison {
  1: Equality eq,
  2: Target lhs,
  3: Target rhs,
}

struct NullComparison {
  1: Column col,
  2: bool isnull
}

struct InComparison {
  1: Target lhs,
  2: list<Target> targets,
  3: optional bool notin
}

// This is a hack, but it simplifies certain things a lot
struct BetweenComparison {
  1: Column col,
  2: Target lo,
  3: Target hi,
  3: optional inclusive
}

// N.B. this is a union type
struct Comparison {
  1: optional EqComparison eqcomp,
  2: optional NullComparison nullcomp,
  3: optional InComparison incomp,
  4: optional BetweenComparison betweencomp
}

struct OrderClause {
  1: Column col,
  2: optional Order order
}

struct QueryClause {
  1: list<Comparison> exprs,
  2: list<OrderClause> orderby,
  3: optional i32 offset,
  4: optional i32 limit
}

enum QueryType {
  INSERT = 1,
  SELECT = 2,
  DELETE = 3,
}

struct FloatBounds {
  1: double lo,
  2: double hi
}

struct Row {
  1: string table_name,
  2: map<Column,Target> columns
}

struct Query {
  1: QueryType variety,
  2: optional QueryClause clause,
  3: optional Row insert_row
}

service QueryService {
  void         create(1: string name, 2: list<CreateColumn> cols)
  void         drop(1: string name)
  list<string> existing_tables()
  i64          insert(1: Row row)
  list<Row>    select(1: QueryClause query)
  i64          truncate(1: QueryClause query) // "delete" is a thrift reserved keyword
}
