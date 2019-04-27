CREATE PROCEDURE `exists_user` (IN `in_telegram_id` BIGINT)
BEGIN
SELECT EXISTS (SELECT 1 FROM `user` WHERE `telegram_id` = `in_telegram_id`);
END