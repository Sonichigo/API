USE `USER`;
DROP procedure IF EXISTS `sp_GetWishByUser`;
 
DELIMITER $$
USE `USER`$$
CREATE PROCEDURE `sp_GetWishByUser` (
IN p_user_id bigint
)
BEGIN
    select * from tbl_wish where wish_user_id = p_user_id;
END$$
 
DELIMITER ;