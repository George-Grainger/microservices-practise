CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Hs0%EUovc$R9pEPV';

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('gg@gmail.com', 'Yn23*re8*ikMMT2@');