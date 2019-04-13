CREATE DEFINER=`strelkabot`@`%` PROCEDURE `exists_user`(IN t_id BIGINT(20))
BEGIN
SELECT EXISTS (SELECT 1 FROM users WHERE telegram_id = t_id);
END