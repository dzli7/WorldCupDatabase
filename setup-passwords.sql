-- File for Password Management section of Final Project

SET GLOBAL log_bin_trust_function_creators = 1;
DROP FUNCTION IF EXISTS make_salt;
-- (Provided) This function generates a specified number of characters for using as a
-- salt in passwords.
DELIMITER !
CREATE FUNCTION make_salt(num_chars INT) 
RETURNS VARCHAR(20) NOT DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';

    -- Don't want to generate more than 20 characters of salt.
    SET num_chars = LEAST(20, num_chars);

    -- Generate the salt!  Characters used are ASCII code 32 (space)
    -- through 126 ('z').
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;

    RETURN salt;
END !
DELIMITER ;

DROP TABLE IF EXISTS user_info;
CREATE TABLE user_info (
    -- Usernames are up to 20 characters.
    username VARCHAR(20) PRIMARY KEY,

    -- Salt will be 8 characters all the time, so we can make this 8.
    salt CHAR(8) NOT NULL,

    -- We use SHA-2 with 256-bit hashes.  MySQL returns the hash
    -- value as a hexadecimal string, which means that each byte is
    -- represented as 2 characters.  Thus, 256 / 8 * 2 = 64.
    -- We can use BINARY or CHAR here; BINARY simply has a different
    -- definition for comparison/sorting than CHAR.
    password_hash BINARY(64) NOT NULL
);

-- [Problem 1a]
-- Adds a new user to the user_info table, using the specified password (max
-- of 20 characters). Salts the password with a newly-generated salt value,
-- and then the salt and hash values are both stored in the table.
DROP PROCEDURE IF EXISTS sp_add_user;
DELIMITER !
CREATE PROCEDURE sp_add_user(new_username VARCHAR(20), password VARCHAR(20))
BEGIN
  -- TODO
  DECLARE salt CHAR(8);
  DECLARE salted_password VARCHAR(28);
  DECLARE password_hash BINARY(64);

  SET salt = make_salt(8);
  SET salted_password = CONCAT(salt, password);
  SET password_hash = SHA2(salted_password, 256);
  
  INSERT INTO user_info VALUES(new_username, salt, password_hash);
END !
DELIMITER ;

-- [Problem 1b]
-- Authenticates the specified username and password against the data
-- in the user_info table.  Returns 1 if the user appears in the table, and the
-- specified password hashes to the value for the user. Otherwise returns 0.
DELIMITER !
DROP FUNCTION IF EXISTS authenticate;
CREATE FUNCTION authenticate(username VARCHAR(20), password VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN
  DECLARE hashed BINARY(64);
  DECLARE salt CHAR(8);
  IF username NOT IN (SELECT u.username FROM user_info AS u)
    THEN RETURN 0;
  END IF;
  SELECT u.salt, u.password_hash INTO salt, hashed
    FROM user_info AS u
    WHERE u.username = username;
  IF hashed <> SHA2(CONCAT(salt, password), 256)
    THEN RETURN 0;
  END IF;
  RETURN 1;
END !
DELIMITER ;

-- [Problem 1c]
-- Add at least two users into your user_info table so that when we run this file,
-- we will have examples users in the database.
CALL sp_add_user('ding', '6969696969');
CALL sp_add_user('dzli', '123456');

-- [Problem 1d]
-- Optional: Create a procedure sp_change_password to generate a new salt and change the given
-- user's password to the given password (after salting and hashing)
