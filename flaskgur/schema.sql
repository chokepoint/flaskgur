-- User table.
CREATE TABLE IF NOT EXISTS user (
    id SERIAL,
    username VARCHAR(100) NOT NULL UNIQUE,
    email_address VARCHAR(255) NOT NULL UNIQUE,
    created_on DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')),
    created_by_id INT NOT NULL REFERENCES user(id) DEFAULT 0,
    updated_on DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')),
    updated_by_id INT NOT NULL REFERENCES user(id) DEFAULT 0
);

-- CREATE Admin user if one does not yet exist.
WITH exst AS (
    SELECT id
    FROM user 
    WHERE username = 'admin'
)
INSERT INTO user
(id, username, email_address)
SELECT 0 AS id, 'admin' AS username, 'admin@flaskgur.com' AS email_address
WHERE NOT EXISTS (SELECT id FROM exst);


-- Basic pics table.
CREATE TABLE IF NOT EXISTS pics ( 
    id SERIAL,
    filename VARCHAR(37) NOT NULL UNIQUE,
    created_on DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')),
    created_by_id INT NOT NULL REFERENCES user(id) DEFAULT 0,
    updated_on DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')),
    updated_by_id INT NOT NULL REFERENCES user(id) DEFAULT 0
);

-- Gallery table.
CREATE TABLE IF NOT EXISTS gallery (
    id SERIAL,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_on DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')),
    created_by_id INT NOT NULL REFERENCES user(id) DEFAULT 0,
    updated_on DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')),
    updated_by_id INT NOT NULL REFERENCES user(id) DEFAULT 0
);

-- Many-to-many association table indicating which
-- image is in which gallery.
CREATE TABLE IF NOT EXISTS gallery_pic (
    id SERIAL,
    gallery_id INT NOT NULL REFERENCES gallery(id),
    pic_id INT NOT NULL REFERENCES pics(id),
    created_on DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')),
    created_by_id INT NOT NULL REFERENCES user(id) DEFAULT 0,
    updated_on DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')),
    updated_by_id INT NOT NULL REFERENCES user(id) DEFAULT 0,
    CONSTRAINT uniq_gallery_pic__gallery_pic UNIQUE (gallery_id, pic_id)
);
