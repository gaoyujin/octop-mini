-- octop-mini v1: schema watermark + minimal settings KV (course 02 expands).

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS _schema_version (
  version INTEGER NOT NULL
);

INSERT INTO _schema_version (version) VALUES (1);

CREATE TABLE IF NOT EXISTS settings (
  key   TEXT PRIMARY KEY NOT NULL,
  value TEXT NOT NULL
);