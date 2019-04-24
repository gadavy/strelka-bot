CREATE PROCEDURE `update_strelka_balance`(IN c_num TEXT, IN bal INT)
BEGIN
UPDATE cards_strelka SET balance = bal WHERE number = c_num;
END