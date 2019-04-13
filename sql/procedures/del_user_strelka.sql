CREATE DEFINER=`strelkabot`@`%` PROCEDURE `del_user_strelka`(IN t_id BIGINT(20), IN c_num TEXT)
BEGIN
DELETE FROM user_strelka WHERE user_id = (SELECT id FROM users WHERE telegram_id = t_id) AND card_id = (SELECT id FROM cards_strelka WHERE number = c_num);
END