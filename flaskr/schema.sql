DROP TABLE IF EXISTS requests;

CREATE TABLE requests (
    key TEXT NOT NULL,
    value INTEGER
);

INSERT INTO requests(key, value) VALUES("n", 0);
INSERT INTO requests(key, value) VALUES("k", 0);
