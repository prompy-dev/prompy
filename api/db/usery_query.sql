----------------------------------------------------------------------
-- COPY AND PASTE THIS INTO SUPABASE
----------------------------------------------------------------------
DROP TABLE IF EXISTS feedback_response CASCADE;
DROP TABLE IF EXISTS scores CASCADE;
DROP TABLE IF EXISTS user_query_version CASCADE;
DROP TABLE IF EXISTS user_query CASCADE;

CREATE TABLE user_query (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMPTZ,
  created_by TEXT NOT NULL
);

CREATE TABLE user_query_version (
  id SERIAL PRIMARY KEY,
  user_query TEXT NOT NULL,
  task BOOLEAN NOT NULL DEFAULT FALSE,
  role BOOLEAN NOT NULL DEFAULT FALSE,
  context BOOLEAN NOT NULL DEFAULT FALSE,
  rules BOOLEAN NOT NULL DEFAULT FALSE,
  examples BOOLEAN NOT NULL DEFAULT FALSE,
  format BOOLEAN NOT NULL DEFAULT FALSE,
  user_query_id INTEGER REFERENCES user_query(id)
);

CREATE TABLE scores (
  id SERIAL PRIMARY KEY,
  total_score FLOAT,
  max_possible_score INTEGER,
  percentage_score FLOAT,
  task_score INTEGER,
  role_score INTEGER,
  context_score INTEGER,
  rules_score INTEGER,
  examples_score INTEGER,
  format_score INTEGER,
  word_count_score FLOAT,
  user_query_version_id INTEGER REFERENCES user_query_version(id)
);

CREATE TABLE feedback_response (
  id SERIAL PRIMARY KEY,
  improvements TEXT[],
  score INTEGER,
  strengths TEXT[],
  tags TEXT[],
  user_query_version_id INTEGER REFERENCES user_query_version(id)
);
----------------------------------------------------------------------
-- END
----------------------------------------------------------------------



-- Example query to get full data set
SELECT
  *
FROM
  user_query u
  JOIN user_query_version v ON u.id = v.user_query_id
  JOIN scores s ON s.user_query_version_id = v.id
  JOIN feedback_response f ON f.user_query_version_id = v.id
