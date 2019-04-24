CREATE PROCEDURE `add_user_strelka`(IN t_id BIGINT(20), IN c_num TEXT)
BEGIN
INSERT INTO user_strelka ( 
	user_id,
    card_id
) 
SELECT u.id, c.id FROM users AS u, cards_strelka AS c 
WHERE u.telegram_id = t_id AND c.number = c_num;
END