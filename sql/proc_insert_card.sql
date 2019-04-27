CREATE PROCEDURE `insert_card`(IN `in_number` TEXT)
BEGIN
INSERT INTO `card` (`number`) VALUES (`in_number`);
END
