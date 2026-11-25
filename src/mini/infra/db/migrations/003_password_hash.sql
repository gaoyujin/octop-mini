-- v3: password hashes (course 03).

ALTER TABLE users ADD COLUMN password_hash TEXT;

UPDATE _schema_version SET version = 3;