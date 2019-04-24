CREATE PROCEDURE `exists_user_strelka`(IN t_id BIGINT(20), IN card_n TEXT)
BEGIN
SELECT EXISTS (SELECT 1 FROM user_strelka WHERE 
user_id = (SELECT id FROM users WHERE telegram_id = t_id) AND
card_id = (SELECT id FROM cards_strelka WHERE number = card_n));
END