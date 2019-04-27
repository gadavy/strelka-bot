CREATE PROCEDURE `select_user`(IN `in_telegram_id` BIGINT)
BEGIN
SELECT * FROM `user` WHERE `telegram_id` = `in_telegram_id`;
END