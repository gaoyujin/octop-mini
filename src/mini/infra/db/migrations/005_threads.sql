-- v5: threads and messages (course 06).

CREATE TABLE IF NOT EXISTS threads (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  thread_id     TEXT NOT NULL UNIQUE,
  agent_id      TEXT NOT NULL REFERENCES agents(agent_id) ON DELETE CASCADE,
  user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  channel_type  TEXT NOT NULL DEFAULT 'dashboard',
  session_key   TEXT NOT NULL,
  title         TEXT,
  last_active   INTEGER NOT NULL,
  created_at    INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_threads_agent_active ON threads(agent_id, last_active DESC);

CREATE TABLE IF NOT EXISTS messages (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  thread_id   TEXT NOT NULL REFERENCES threads(thread_id) ON DELETE CASCADE,
  role        TEXT NOT NULL,
  content     TEXT NOT NULL,
  created_at  INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_messages_thread ON messages(thread_id, created_at ASC);

UPDATE _schema_version SET version = 5;