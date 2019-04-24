CREATE PROCEDURE `get_user_ntf`(IN t_id BIGINT(20))
BEGIN
SELECT notification FROM users WHERE telegram_id = t_id;
END