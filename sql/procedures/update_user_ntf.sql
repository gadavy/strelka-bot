CREATE DEFINER=`strelkabot`@`%` PROCEDURE `update_user_ntf`(IN t_id BIGINT(20), IN st BOOL)
BEGIN
UPDATE users SET notification = st WHERE telegram_id = t_id;
END