CREATE DEFINER=`strelkabot`@`%` PROCEDURE `exists_strelka`(IN card_n TEXT)
BEGIN
SELECT EXISTS (SELECT 1 FROM cards_strelka WHERE number = card_n);
END