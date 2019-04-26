CREATE TABLE IF NOT EXISTS `balance` (
    `date_time` DATETIME NOT NULL,
    `card_id` INT NOT NULL,
    `balance` INT,
    `baserate` INT,
    INDEX `card_id_UNIQUE` (`card_id` ASC),
    INDEX `date_time_UNIQUE` (`date_time` ASC),
    CONSTRAINT `fk_card_id`
        FOREIGN KEY (`card_id`)
        REFERENCES `card` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4