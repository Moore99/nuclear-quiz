-- Users table (same pattern as CS50 Finance)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    is_admin INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories (CANDU Systems, IAEA Safety Standards, Radiation Protection, etc.)
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT
);

-- Seed categories
INSERT INTO categories (id, name, description, icon) VALUES
(1, 'CANDU Reactor Systems', 'Canadian nuclear reactor design and operations', '⚛️'),
(2, 'CNSC Regulatory Framework', 'Canadian nuclear regulatory standards', '📋'),
(3, 'IAEA Safety Standards', 'International atomic energy standards', '🌍'),
(4, 'Radiation Protection', 'Health physics and dose limits', '☢️'),
(5, 'Nuclear Security & Safeguards', 'Non-proliferation and security measures', '🔒');

-- Questions
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER REFERENCES categories(id),
    question_text TEXT NOT NULL,
    explanation TEXT,
    difficulty INTEGER DEFAULT 1,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Answer options (4 per question)
CREATE TABLE answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER REFERENCES questions(id),
    answer_text TEXT NOT NULL,
    is_correct INTEGER NOT NULL DEFAULT 0
);

-- User quiz results (needed for progress tracking later)
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    question_id INTEGER REFERENCES questions(id),
    answer_id INTEGER REFERENCES answers(id),
    is_correct INTEGER NOT NULL,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Password reset tokens (one-time, 1-hour expiry)
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    used INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API quiz sessions (stateless quiz state for mobile clients; created at runtime by ensure_quiz_sessions_table)
CREATE TABLE IF NOT EXISTS quiz_sessions (
    id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    question_ids TEXT NOT NULL,        -- JSON array of question IDs
    current_index INTEGER NOT NULL DEFAULT 0,
    score INTEGER NOT NULL DEFAULT 0,
    completed INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
