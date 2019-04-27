CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `telegram_id` BIGINT NOT NULL,
    `first_name` TEXT NOT NULL,
    `last_name` TEXT NULL DEFAULT NULL,
    `username` TEXT NULL DEFAULT NULL,
    `language` TEXT NULL DEFAULT NULL,
    `notification` BOOLEAN DEFAULT 1,
    `threshold` INT NOT NULL DEFAULT 8000,
    `date_time` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4