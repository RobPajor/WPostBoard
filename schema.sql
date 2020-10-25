DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS dislikes;
DROP TABLE IF EXISTS pictures;


CREATE TABLE User (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
bio TEXT,
password TEXT NOT NULL,
joindate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
avatar_id INTEGER DEFAULT 0
);

CREATE TABLE post (
id INTEGER PRIMARY KEY AUTOINCREMENT,
author_id INTEGER NOT NULL,
created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
title TEXT NOT NULL,
body TEXT NOT NULL,
likes INTEGER DEFAULT 0,
FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE likes (
like_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
post_id INTEGER
);

CREATE TABLE dislikes (
dislike_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
post_id INTEGER
);

CREATE TABLE pictures (
picture_id INTEGER PRIMARY KEY AUTOINCREMENT,
picture_path TEXT
);



