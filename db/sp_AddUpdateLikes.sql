DELIMITER $$
USE 'USER'
CREATE PROCEDURE `sp_AddUpdateLikes`(
    p_wish_id int,
    p_user_id int,
    p_like int
)
BEGIN
    if (select exists (select 1 from tbl_likes where wish_id = p_wish_id and user_id = p_user_id)) then
 
        update tbl_likes set wish_like = p_like where wish_id = p_wish_id and user_id = p_user_id;
         
    else
         
        insert into tbl_likes(
            wish_id,
            user_id,
            wish_like
        )
        values(
            p_wish_id,
            p_user_id,
            p_like
        );
 
    end if;
END