CREATE PROCEDURE `update_user`(
    IN `in_telegram_id` BIGINT,
    IN `in_first_name` TEXT,
    IN `in_last_name` TEXT,
    IN `in_username` TEXT,
    IN `in_language` TEXT,
    IN `in_notification` BOOL,
    IN `in_threshold` INT
)
BEGIN
UPDATE `user` SET
    `first_name` = `in_first_name`,
	`last_name` = `in_last_name`,
	`username` = `in_username`,
	`language` = `in_language`,
    `notification` = `in_notification`,
    `threshold` = `in_threshold`
WHERE `telegram_id` = `in_telegram_id`;
END
