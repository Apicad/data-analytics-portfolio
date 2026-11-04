#!/usr/bin/env python3
"""Load the MySQL schema dump into SQLite, fill it with the synthetic CSVs, run the dashboard queries.

PORTFOLIO IMPROVEMENT. The capstone ran on MySQL with Power BI on top. Neither is
needed to inspect this project: this script translates the mysqldump DDL to SQLite
(types only, keys and foreign keys are kept), loads ./synthetic_data/*.csv with
foreign-key checks ON, then runs every query in ../reconstruction/queries/.

Stock Python only.

    python build_sqlite.py             # build hospital.sqlite (if missing) and print each query
    python build_sqlite.py --rebuild   # start over
"""
from __future__ import annotations

import argparse
import csv
import re
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
DUMP = PROJECT / "original" / "dump-Hospital-202512151315.sql"
DATA_DIR = HERE / "synthetic_data"
QUERY_DIR = PROJECT / "reconstruction" / "queries"
DB_PATH = HERE / "hospital.sqlite"

# Parents before children so foreign keys validate during the load.
LOAD_ORDER = [
    "Physician", "Department", "Affiliated_With", "Procedures", "Trained_In", "Patient",
    "Nurse", "Appointment", "Medication", "Prescribes", "Room", "Stay", "Undergoes",
]

TYPE_MAP = [
    (r"\bbit\(1\)", "INTEGER"),
    (r"\bint\b", "INTEGER"),
    (r"\bdouble\b", "REAL"),
    (r"\bdatetime\b", "TEXT"),
    (r"\bvarchar\(\d+\)", "TEXT"),
    (r"\btext\b", "TEXT"),
]


def mysql_to_sqlite(dump_sql: str) -> list[str]:
    """Keep only CREATE/DROP TABLE statements and translate MySQL-isms.

    mysqldump writes secondary indexes as `KEY name (cols)` lines inside CREATE TABLE.
    SQLite has no such clause, so each one becomes a separate CREATE INDEX statement.
    """
    sql = re.sub(r"/\*!\d+.*?\*/;?", "", dump_sql, flags=re.S)   # /*!40101 ... */ directives
    sql = re.sub(r"^--.*$", "", sql, flags=re.M)                  # line comments
    sql = sql.replace("`", '"')
    statements = []
    for chunk in sql.split(";"):
        stmt = chunk.strip()
        if not stmt.upper().startswith(("CREATE TABLE", "DROP TABLE")):
            continue
        stmt = re.sub(r"\)\s*ENGINE=.*$", ")", stmt, flags=re.S)  # ) ENGINE=InnoDB DEFAULT CHARSET=...
        for pattern, replacement in TYPE_MAP:
            stmt = re.sub(pattern, replacement, stmt, flags=re.I)
        indexes = []
        table = re.search(r'CREATE TABLE "([^"]+)"', stmt)
        if table:
            for name, cols in re.findall(r'^\s*KEY "([^"]+)" \(([^)]*)\),?\s*$', stmt, flags=re.M):
                indexes.append(f'CREATE INDEX "{name}" ON "{table.group(1)}" ({cols});')
            stmt = re.sub(r'^\s*KEY "[^"]+" \([^)]*\),?\s*$\n?', "", stmt, flags=re.M)
            stmt = re.sub(r",\s*\)$", "\n)", stmt)                  # tidy a trailing comma if KEY was last
        statements.append(stmt + ";")
        statements.extend(indexes)
    return statements


def build(db_path: Path = DB_PATH, rebuild: bool = False) -> sqlite3.Connection:
    if rebuild and db_path.exists():
        db_path.unlink()
    fresh = not db_path.exists()
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    if fresh:
        if not DATA_DIR.exists():
            raise SystemExit(f"{DATA_DIR} is missing. Run generate_synthetic_data.py first.")
        for stmt in mysql_to_sqlite(DUMP.read_text()):
            conn.execute(stmt)
        for table in LOAD_ORDER:
            load_csv(conn, table, DATA_DIR / f"{table}.csv")
        conn.commit()
    return conn


def load_csv(conn: sqlite3.Connection, table: str, path: Path) -> None:
    with path.open(newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        rows = [[None if v == "" else v for v in row] for row in reader]
    cols = ", ".join(f'"{c}"' for c in header)
    marks = ", ".join("?" for _ in header)
    conn.executemany(f'INSERT INTO "{table}" ({cols}) VALUES ({marks})', rows)


def run_query(conn: sqlite3.Connection, path: Path):
    cur = conn.execute(path.read_text())
    columns = [d[0] for d in cur.description]
    return columns, cur.fetchall()


def print_table(columns, rows, limit: int = 12) -> None:
    shown = rows[:limit]
    widths = [max(len(str(c)), *(len(str(r[i])) for r in shown)) if shown else len(str(c)) for i, c in enumerate(columns)]
    line = " | ".join(str(c).ljust(w) for c, w in zip(columns, widths))
    print(line)
    print("-" * len(line))
    for r in shown:
        print(" | ".join(str(v).ljust(w) for v, w in zip(r, widths)))
    if len(rows) > limit:
        print(f"... {len(rows) - limit} more rows")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build hospital.sqlite and run the dashboard queries.")
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    conn = build(rebuild=args.rebuild)
    counts = {t: conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in LOAD_ORDER}
    print("Row counts:", ", ".join(f"{t}={n}" for t, n in counts.items()))
    for path in sorted(QUERY_DIR.glob("*.sql")):
        print(f"\n== {path.name} ==")
        print_table(*run_query(conn, path))
    conn.close()


if __name__ == "__main__":
    main()
