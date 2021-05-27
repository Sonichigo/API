DELIMITER $$
CREATE DEFINER=`Asuna1219`@`api12192001` PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(20)
)
BEGIN
    select * from tbl_user where user_username = p_username;
END$$
DELIMITER ;