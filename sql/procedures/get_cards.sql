CREATE DEFINER=`strelkabot`@`%` PROCEDURE `get_cards`()
BEGIN
SELECT number FROM cards_strelka;
END