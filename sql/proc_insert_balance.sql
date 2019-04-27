CREATE PROCEDURE `insert_balance`(
    IN `in_date_time` DATETIME,
    IN `in_card_number` TEXT,
    IN `in_balance` INT,
    IN `in_baserate` INT
)
BEGIN
INSERT INTO `balance` (
    `date_time`,
    `card_id`,
    `balance`,
    `baserate`
)
VALUES (
    `in_date_time`,
    (SELECT `id` FROM `card` WHERE `number` = `in_card_number`),
    `in_balance`,
    `in_baserate`
);
END
