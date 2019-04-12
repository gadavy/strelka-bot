CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT,
    username TEXT,
    language TEXT,
    notification BOOLEAN DEFAULT 1,
    threshold INT NOT NULL DEFAULT 80,
    date_time DATETIME DEFAULT CURRENT_TIMESTAMP
)