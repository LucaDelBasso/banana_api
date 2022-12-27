CREATE DATABASE IF NOT EXISTS banana_dev;
CREATE DATABASE IF NOT EXISTS banana_test;

USE banana_test;

CREATE TABLE bananas (
    id mediumint,
    origin char(30),
    date date,
    price float,
    unit char(30),
    created_at timestamp
);
