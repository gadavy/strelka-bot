CREATE DEFINER=`strelkabot`@`%` PROCEDURE `add_strelka`(IN card_n TEXT)
BEGIN
INSERT INTO cards_strelka (number) VALUES (card_n);
END


CREATE DEFINER=`strelkabot`@`%` PROCEDURE `add_user`(IN t_id BIGINT(20), IN f_name TEXT, IN l_name TEXT, IN u_name TEXT, IN lang TEXT)
BEGIN
INSERT INTO users (
	telegram_id,
	first_name, 
	last_name, 
	username, 
	language
) VALUES (t_id, f_name, l_name, u_name, lang);
END


CREATE DEFINER=`strelkabot`@`%` PROCEDURE `add_user_strelka`(IN t_id BIGINT(20), IN c_num TEXT)
BEGIN
INSERT INTO user_strelka ( 
	user_id,
    card_id
) 
SELECT u.id, c.id FROM users AS u, cards_strelka AS c 
WHERE u.telegram_id = t_id AND c.number = c_num;
END


CREATE DEFINER=`strelkabot`@`%` PROCEDURE `del_user_strelka`(IN t_id BIGINT(20), IN c_num TEXT)
BEGIN
DELETE FROM user_strelka WHERE user_id = (SELECT id FROM users WHERE telegram_id = t_id) AND card_id = (SELECT id FROM cards_strelka WHERE number = c_num);
END


CREATE DEFINER=`strelkabot`@`%` PROCEDURE `exists_strelka`(IN card_n TEXT)
BEGIN
SELECT EXISTS (SELECT 1 FROM cards_strelka WHERE number = card_n);
END


CREATE DEFINER=`strelkabot`@`%` PROCEDURE `exists_user`(IN t_id BIGINT(20))
BEGIN
SELECT EXISTS (SELECT 1 FROM users WHERE telegram_id = t_id);
END


CREATE DEFINER=`strelkabot`@`%` PROCEDURE `exists_user_strelka`(IN t_id BIGINT(20), IN card_n TEXT)
BEGIN
SELECT EXISTS (SELECT 1 FROM user_strelka WHERE 
user_id = (SELECT id FROM users WHERE telegram_id = t_id) AND
card_id = (SELECT id FROM cards_strelka WHERE number = card_n));
END


CREATE DEFINER=`strelkabot`@`%` PROCEDURE `get_cards`()
BEGIN
SELECT number FROM cards_strelka;
END


CREATE DEFINER=`strelkabot`@`%` PROCEDURE `get_user_cards`(IN t_id BIGINT(20))
BEGIN
SELECT number FROM (users JOIN user_strelka ON (users.id = user_strelka.user_id)) 
JOIN cards_strelka ON (user_strelka.card_id = cards_strelka.id) AND users.telegram_id = t_id;
END


CREATE DEFINER=`strelkabot`@`%` PROCEDURE `get_user_ntf`(IN t_id BIGINT(20))
BEGIN
SELECT notification FROM users WHERE telegram_id = t_id;
END


CREATE DEFINER=`strelkabot`@`%` PROCEDURE `get_users_low_balance`()
BEGIN
SELECT telegram_id, first_name, number, balance FROM (users JOIN user_strelka ON (users.id = user_strelka.user_id)) 
JOIN cards_strelka ON (user_strelka.card_id = cards_strelka.id) WHERE balance < threshold;
END


CREATE DEFINER=`strelkabot`@`%` PROCEDURE `get_user_thr`(IN t_id BIGINT(20))
BEGIN
SELECT threshold FROM users WHERE telegram_id = t_id;
END


CREATE DEFINER=`strelkabot`@`%` PROCEDURE `update_strelka_balance`(IN c_num TEXT, IN bal INT)
BEGIN
UPDATE cards_strelka SET balance = bal WHERE number = c_num;
END


CREATE DEFINER=`strelkabot`@`%` PROCEDURE `update_user_ntf`(IN t_id BIGINT(20), IN st BOOL)
BEGIN
UPDATE users SET notification = st WHERE telegram_id = t_id;
END


CREATE DEFINER=`strelkabot`@`%` PROCEDURE `update_user_thr`(IN t_id BIGINT(20), IN thr INT)
BEGIN
UPDATE users SET threshold = thr WHERE telegram_id = t_id;
END