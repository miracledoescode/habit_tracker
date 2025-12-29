-- Create Tables
CREATE TABLE IF NOT EXISTS habits (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS daily_logs (
    id SERIAL PRIMARY KEY,
    habit_id INTEGER NOT NULL REFERENCES habits (id) ON DELETE CASCADE,
    log_date DATE NOT NULL,
    UNIQUE (habit_id, log_date)
);

-- Enable Row Level Security
ALTER TABLE habits ENABLE ROW LEVEL SECURITY;

ALTER TABLE daily_logs ENABLE ROW LEVEL SECURITY;

-- Create Policies (Permissive for now since we have no Auth)
-- This allows the app (postgres role) and public (with key) to access data if needed.
-- In a real app with users, you would restrict this to (auth.uid() = user_id).

CREATE POLICY "Enable all access to habits" ON habits FOR ALL USING (true)
WITH
    CHECK (true);

CREATE POLICY "Enable all access to logs" ON daily_logs FOR ALL USING (true)
WITH
    CHECK (true);