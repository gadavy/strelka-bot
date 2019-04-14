CREATE TABLE user_strelka (
    user_id INT NOT NULL,
    card_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (card_id) REFERENCES cards_strelka (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
)