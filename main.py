import os
import sqlite3
from contextlib import closing
from dataclasses import dataclass, astuple
from typing import Generator
from uuid import UUID

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

dsl = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
}

BATCH_SIZE = 100


def extract_data(sqlite_cursor: sqlite3.Cursor) -> Generator[list[sqlite3.Row], None, None]:
    sqlite_cursor.execute('SELECT * FROM students')
    while results := sqlite_cursor.fetchmany(BATCH_SIZE):
        yield results


@dataclass
class Student:
    id: UUID
    name: str
    class_name: str
    age: int

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)


def transform_data(sqlite_cursor: sqlite3.Cursor) -> Generator[list[Student], None, None]:
    for batch in extract_data(sqlite_cursor):
        yield [Student(**dict(student)) for student in batch]


def load_data(sqlite_cursor: sqlite3.Cursor, pg_cursor: psycopg.Cursor):
    for batch in transform_data(sqlite_cursor):
        query = 'INSERT INTO students (id, name, class_name, age) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
        batch_as_tuples = [astuple(student) for student in batch]
        pg_cursor.executemany(query, batch_as_tuples)


def test_transfer(sqlite_cursor: sqlite3.Cursor, pg_cursor: psycopg.Cursor):
    sqlite_cursor.execute('SELECT * FROM students')

    while batch := sqlite_cursor.fetchmany(BATCH_SIZE):
        original_students_batch = [Student(**dict(student)) for student in batch]
        ids = [student.id for student in original_students_batch]

        pg_cursor.execute('SELECT * FROM students WHERE id = ANY(%s)', [ids])
        transferred_students_batch = [Student(**student) for student in pg_cursor.fetchall()]

        assert len(original_students_batch) == len(transferred_students_batch)
        assert original_students_batch == transferred_students_batch


if __name__ == '__main__':
    with closing(sqlite3.connect('db.sqlite')) as sqlite_conn, closing(psycopg.connect(**dsl)) as pg_conn:
        sqlite_conn.row_factory = sqlite3.Row
        with closing(sqlite_conn.cursor()) as sqlite_cur, closing(pg_conn.cursor(row_factory=dict_row)) as pg_cur:
            load_data(sqlite_cur, pg_cur)
            pg_conn.commit()

            test_transfer(sqlite_cur, pg_cur)

    print('🎉 Данные успешно перенесены !!!')
