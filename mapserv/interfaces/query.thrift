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
  1: string table,
  2: string name,
  3: bool spatial
}

// N.B. this is a union type
struct Target {
  1: optional Column col,      // logical targets
  2: optional i64 ival,    // literal targets
  3: optional double fval,
  4: optional string sval,
  5: optional bool nullity
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

// N.B. this is a union type
struct Comparison {
  1: optional EqComparison eqcomp,
  2: optional NullComparison nullcomp,
  3: optional InComparison incomp
}

struct OrderClause {
  1: Column col,
  2: optional Order order
}

struct QueryClause {
  1: string table,
  2: list<Comparison> exprs,
  3: list<OrderClause> orderby,
  4: optional i32 offset,
  5: optional i32 limit
}
