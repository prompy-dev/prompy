-- Subject to change, just needed something to query
CREATE TABLE user_query (
  id SERIAL PRIMARY KEY,
  user_query TEXT NOT NULL,
  task BOOLEAN NOT NULL DEFAULT FALSE,
  role BOOLEAN NOT NULL DEFAULT FALSE,
  context BOOLEAN NOT NULL DEFAULT FALSE,
  rules BOOLEAN NOT NULL DEFAULT FALSE,
  examples BOOLEAN NOT NULL DEFAULT FALSE,
  format BOOLEAN NOT NULL DEFAULT FALSE
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
  user_query_id INTEGER REFERENCES user_query(id)
);
