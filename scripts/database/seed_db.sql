-- set search path
SET
    search_path TO PUBLIC;

-- drop all rows table before insertion
DELETE FROM
    "version";

DELETE FROM
    "card";

-- restart sequence
ALTER SEQUENCE "card_id_seq" RESTART WITH 1;

-- seed version table
INSERT INTO
    "version" ("version")
VALUES
    ('1.0');

-- seed card table
INSERT INTO
    "card" ("name", "img_path")
VALUES
    ('raw', 'raw.jpg');