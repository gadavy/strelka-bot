CREATE PROCEDURE `insert_user`(IN `in_telegram_id` BIGINT, IN `in_first_name` TEXT, IN `in_last_name` TEXT, IN `in_username` TEXT, IN `in_language` TEXT)
BEGIN
INSERT INTO `user` (
	`telegram_id`,
	`first_name`, 
	`last_name`, 
	`username`, 
	`language`
) VALUES (`in_telegram_id`, `in_first_name`, `in_last_name`, `in_username`, `in_language`);
END