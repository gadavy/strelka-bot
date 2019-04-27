CREATE PROCEDURE `select_user_balance`(IN `in_telegram_id` BIGINT, IN `in_card_number` TEXT)
BEGIN
IF `in_telegram_id` = 0 THEN
	SELECT `telegram_id`, `first_name`, `number`, `balance` FROM (`user`
		JOIN `user_card` ON (`user`.`id` = `user_card`.`user_id`)) 
		JOIN `card` ON (`user_card`.`card_id` = `card`.`id`) 
		JOIN `balance` ON (`card`.`id` = `balance`.`card_id`)
	WHERE 
		`balance`.`date_time` = (SELECT MAX(`date_time`) FROM `balance`)
		AND `balance` < `threshold`;
ELSE
	SELECT `telegram_id`, `first_name`, `number`, `balance` FROM (`user`
		JOIN `user_card` ON (`user`.`id` = `user_card`.`user_id`)) 
		JOIN `card` ON (`user_card`.`card_id` = `card`.`id`) 
		JOIN `balance` ON (`card`.`id` = `balance`.`card_id`)
	WHERE 
		`balance`.`date_time` = (SELECT MAX(`date_time`) FROM `balance`)
		AND `telegram_id` = `in_telegram_id`
		AND `number` = `in_card_number`;
END IF;
END