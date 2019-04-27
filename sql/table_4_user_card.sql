CREATE TABLE IF NOT EXISTS `user_card` (
    `user_id` INT NOT NULL,
    `card_id` INT NOT NULL,
    INDEX `fk_user_id_idx` (`user_id` ASC),
    INDEX `fk_card_id_idx` (`card_id` ASC),
    CONSTRAINT `fk_user_id_op`
        FOREIGN KEY (`user_id`)
        REFERENCES `user` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT `fk_card_id_op`
        FOREIGN KEY (`card_id`)
        REFERENCES `card` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4