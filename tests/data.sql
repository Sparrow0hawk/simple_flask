INSERT INTO user (username, password)
VALUES
    ('test', 'pbkdf2:sha256:600000$qptDAxsWXLlDSEoF$9e7a21e6da8ca084373abae0ebc40e5d3873299bd11df2678d6833dadf19a1c4'),
    ('other', 'pbkdf2:sha256:600000$aD1VZh1uMkORNhZe$bf5adf359e8a6033c58a8a7581cd320b6f6bfa9b45aeed5e57c821934d39ab16');

INSERT INTO post (title, body, author_id, created)
VALUES
    ('test title', 'test' || x'0a' || 'body', 1, '2023-07-07 10:00:00');
