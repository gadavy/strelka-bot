CREATE PROCEDURE `get_user_thr`(IN t_id BIGINT(20))
BEGIN
SELECT threshold FROM users WHERE telegram_id = t_id;
END