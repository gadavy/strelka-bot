CREATE PROCEDURE `exists_card`(IN `in_number` TEXT)
BEGIN
SELECT EXISTS (SELECT 1 FROM `card` WHERE `number` = `in_number`);
END