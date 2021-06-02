USE `user`;
DROP procedure IF EXISTS `user`.`sp_addWish`;
 
DELIMITER $$

USE `user`$$

CREATE PROCEDURE `sp_addWish`(
p_title varchar(45),
p_description varchar(1000),
p_user_id bigint,
p_file_path varchar(200),
p_is_done int
)
BEGIN
insert into tbl_wish(
wish_title,
wish_description,
wish_user_id,
wish_date,
wish_file_path,
wish_accomplished
)
values
(
p_title,
p_description,
p_user_id,
NOW(),
p_file_path,
p_is_done
);

END$$

DELIMITER ;