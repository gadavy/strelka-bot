CREATE DEFINER=`strelkabot`@`%` PROCEDURE `get_users_low_balance`()
BEGIN
SELECT telegram_id, first_name, number, balance FROM (users JOIN user_strelka ON (users.id = user_strelka.user_id)) 
JOIN cards_strelka ON (user_strelka.card_id = cards_strelka.id) WHERE balance < threshold;
END