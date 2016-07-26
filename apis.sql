DROP database IF EXISTS apis;
create database apis;
use apis;
create table account (
    user VARCHAR(32) NOT NULL,
    pass BINARY(16),
    token BINARY(16),
    mail VARCHAR(64),
    update_token TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user)
);
create table notes (
    id int NOT NULL AUTO_INCREMENT,
    title VARCHAR(256),
    path VARCHAR(256),
    context VARCHAR(8192),
    creat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lastmodified TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uc_path_title UNIQUE (path,title),
    PRIMARY KEY (id)
);
create table logs (
    id int NOT NULL AUTO_INCREMENT,
    tag VARCHAR(128),
    path VARCHAR(256),
    context VARCHAR(8192),
    creat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
create user 'api'@'%' IDENTIFIED BY 'apiapi';
grant select on apis.notes to 'api'@'%';
grant insert on apis.notes to 'api'@'%';
grant update on apis.notes to 'api'@'%';
grant select on apis.logs to 'api'@'%';
grant insert on apis.logs to 'api'@'%';
flush privileges;
