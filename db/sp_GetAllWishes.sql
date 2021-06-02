DELIMITER $$
USE `USER`$$
CREATE PROCEDURE `sp_GetAllWishes`()
BEGIN
    select wish_id,wish_title,wish_description,wish_file_path from tbl_wish where wish_private = 0;
END$$
 
DELIMITER ;