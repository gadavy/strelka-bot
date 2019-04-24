CREATE PROCEDURE `update_user_thr`(IN t_id BIGINT(20), IN thr INT)
BEGIN
UPDATE users SET threshold = thr WHERE telegram_id = t_id;
END