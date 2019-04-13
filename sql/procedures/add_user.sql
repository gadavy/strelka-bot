CREATE DEFINER=`strelkabot`@`%` PROCEDURE `add_user`(IN t_id BIGINT(20), IN f_name TEXT, IN l_name TEXT, IN u_name TEXT, IN lang TEXT)
BEGIN
INSERT INTO users (
	telegram_id,
	first_name, 
	last_name, 
	username, 
	language
) VALUES (t_id, f_name, l_name, u_name, lang);
END