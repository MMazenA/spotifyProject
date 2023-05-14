DROP PROCEDURE IF EXISTS get_weekly_streams;

DELIMITER //

CREATE PROCEDURE get_weekly_streams(
    IN table_name VARCHAR(255)
)
BEGIN
    SET @sql = CONCAT('SELECT *, COUNT(*) as play_count FROM ', table_name, ' WHERE WEEK(date) = WEEK(CURDATE()) GROUP BY song_id ORDER BY play_count DESC LIMIT 10');
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //

DELIMITER ;