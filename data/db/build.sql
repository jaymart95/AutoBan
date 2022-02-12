CREATE TABLE IF NOT EXISTS users(
    UserID integer PRIMARY KEY,
    GuildID integer DEFAULT 0,
    is_blacklisted integer DEFAULT False
);

CREATE TABLE IF NOT EXISTS names(
    dName text PRIMARY KEY
);
