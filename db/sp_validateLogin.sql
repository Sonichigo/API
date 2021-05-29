DELIMITER $$
CREATE PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(20)
)
BEGIN
    select * from tbl_user where user_username = p_username;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE `sp_GetAllWishes`()
BEGIN
    select wish_id,wish_title,wish_description,wish_file_path from tbl_wish where wish_accomplished = 1;
END$$
 
DELIMITER ;