INSERT INTO user (username, password)
VALUES
    ('test', 'pbkdf2:sha256:600000$J2W8q8XFhmdezKmf$aa26d4b0aba24452c5983ee6205494f097827b138b7957f5beb33a9dbf3ef3d6'),
    ('other', 'pbkdf2:sha256:600000$aD1VZh1uMkORNhZe$bf5adf359e8a6033c58a8a7581cd320b6f6bfa9b45aeed5e57c821934d39ab16');

INSERT INTO post (title, body, author_id, created)
VALUES
    ('test title', 'test' || x'0a' || 'body', 1, '2023-07-07 10:00:00');
