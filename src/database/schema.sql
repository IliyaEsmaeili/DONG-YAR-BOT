CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY ,
    telegram_id BIGINT UNIQUE NOT NULL ,
    full_name TEXT ,
    state TEXT  ,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dongs (
    id SERIAL PRIMARY KEY ,
    name TEXT  ,
    amount INTEGER CHECK (amount > 0),
    additional_info TEXT ,
    big_prompt_message TEXT ,
    group_id BIGINT NOT NULL ,
    creator_id BIGINT NOT NULL
                   REFERENCES users(telegram_id) ,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dong_participants(
    id SERIAL PRIMARY KEY ,

    dong_id BIGINT NOT NULL
                    REFERENCES dongs(id)
                    ON DELETE CASCADE ,
    user_id BIGINT
                    REFERENCES users(telegram_id)
                    ON DELETE CASCADE ,
    user_name TEXT ,
    UNIQUE(user_id , dong_id)
);

