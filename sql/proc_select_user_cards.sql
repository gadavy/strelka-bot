CREATE PROCEDURE `select_user_cards`(IN `in_telegram_id` BIGINT)
BEGIN
SELECT `number` FROM (`user` JOIN `user_card` ON (`user`.`id` = `user_card`.`user_id`)) 
JOIN `card` ON (`user_card`.`card_id` = `card`.`id`) AND `user`.`telegram_id` = `in_telegram_id`;
END