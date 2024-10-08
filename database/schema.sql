DROP TABLE IF EXISTS image;

CREATE TABLE image (
    image_id BIGINT,
    image_name VARCHAR(10),
    image_url VARCHAR(255),
    image_date DATE,
    PRIMARY KEY (image_id)
);

