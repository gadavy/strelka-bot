CREATE PROCEDURE `insert_user_card`(IN `in_telegram_id` BIGINT, IN `in_number` TEXT)
BEGIN
INSERT INTO `user_card` ( 
	`user_id`,
    `card_id`
) 
SELECT `u`.`id`, `c`.`id` FROM `user` AS `u`, `card` AS `c` 
WHERE `u`.`telegram_id` = `in_telegram_id` AND `c`.`number` = `in_number`;
END