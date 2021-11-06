DROP DATABASE IF EXISTS website;
CREATE DATABASE website;
USE website;
CREATE TABLE user(username VARCHAR(100) PRIMARY KEY,password VARCHAR(100) NOT NULL,first VARCHAR(100) NOT NULL,last VARCHAR(100) NOT NULL,email VARCHAR(100) NOT NULL);
INSERT INTO user VALUES('ad@m', 'abc543', 'Adam', 'Back', 'adam@gmail.com');
INSERT INTO user VALUES('jack', '123!!!', 'Jack', 'Black', 'jacks@gmail.com');
INSERT INTO user VALUES('mark5', 'what@@@', 'Mark', 'Cuban', 'marks@gmail.com');