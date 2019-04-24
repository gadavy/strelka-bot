CREATE PROCEDURE `add_strelka`(IN card_n TEXT)
BEGIN
INSERT INTO cards_strelka (number) VALUES (card_n);
END
