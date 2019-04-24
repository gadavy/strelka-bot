CREATE PROCEDURE `get_user_cards`(IN t_id BIGINT(20))
BEGIN
SELECT number FROM (users JOIN user_strelka ON (users.id = user_strelka.user_id)) 
JOIN cards_strelka ON (user_strelka.card_id = cards_strelka.id) AND users.telegram_id = t_id;
END