import sqlite3
import typing as t
from dataclasses import dataclass


@dataclass
class Database:
    conn: sqlite3.Connection


type ModelID = str
type TextureID = str


@dataclass
class ModelRecord:
    id: ModelID
    path: str


@dataclass
class TextureRecord:
    id: TextureID
    path: str


@dataclass
class ObjectRecord:
    id: str
    name: str
    model: ModelID
    texture: TextureID


MODELS_T = 'models'
TEXTURES_T = 'textures'
OBJECTS_T = 'objects'

MODELS_DECL = f'''{MODELS_T}(
    id TEXT PRIMARY KEY,
    path TEXT NOT NULL
)'''

TEXTURES_DECL = f'''{TEXTURES_T}(
    id TEXT PRIMARY KEY,
    path TEXT NOT NULL
)'''

OBJECTS_DECL = f'''{OBJECTS_T}(
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    model TEXT NOT NULL,
    texture TEXT NOT NULL,

    FOREIGN KEY (model) REFERENCES {MODELS_T} (id),
    FOREIGN KEY (texture) REFERENCES {TEXTURES_T} (id)
)
'''


def db_create() -> Database:
    conn = sqlite3.connect("gamedata.sqlite")
    return Database(conn)


def db_create_tables(self: Database) -> None:
    cur = self.conn.cursor()
    migration = f'''
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS {MODELS_DECL};
        CREATE TABLE IF NOT EXISTS {TEXTURES_DECL};
        CREATE TABLE IF NOT EXISTS {OBJECTS_DECL};
    '''
    cur.executescript(migration)


def db_drop_tables(self: Database) -> None:
    cur = self.conn.cursor()
    drop_migration = f'''
        DROP TABLE {MODELS_T};
        DROP TABLE {TEXTURES_T};
        DROP TABLE {OBJECTS_T};
    '''
    cur.executescript(drop_migration)


def db_get_models(self: Database) -> t.Iterator[ModelRecord]:
    cur = self.conn.cursor()
    query = cur.execute(
        f'SELECT id, path FROM {MODELS_T};'
    )
    return (ModelRecord(*row) for row in query.fetchall())


def db_get_textures(self: Database) -> t.Iterator[TextureRecord]:
    cur = self.conn.cursor()
    query = cur.execute(
        f'SELECT id, path FROM {TEXTURES_T};'
    )
    return (TextureRecord(*row) for row in query.fetchall())


def db_get_objects(self: Database) -> t.Iterator[ObjectRecord]:
    cur = self.conn.cursor()
    query = cur.execute(
        f'SELECT id, name, model, texture FROM {OBJECTS_T};'
    )
    return (ObjectRecord(*row) for row in query.fetchall())
