-- v2: users table (password_hash added in course 03).

CREATE TABLE IF NOT EXISTS users (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  username   TEXT UNIQUE NOT NULL,
  created_at INTEGER NOT NULL
);

UPDATE _schema_version SET version = 2;