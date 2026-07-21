CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY ,
    telegram_id BIGINT UNIQUE NOT NULL ,
    full_name TEXT ,
    state TEXT NOT NULL ,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE dongs (
    id SERIAL PRIMARY KEY ,
    name TEXT  ,
    amount INTEGER ,
    participants TEXT ,
    additional_info TEXT ,
    big_prompt_message TEXT ,
    group_id BIGINT UNIQUE NOT NULL ,
    creator_id INTEGER
                   REFERENCES users(id)
);