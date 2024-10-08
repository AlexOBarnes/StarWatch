DROP TABLE IF EXISTS aurora_colour, image;

CREATE TABLE image (
    image_id BIGINT,
    image_name VARCHAR(10),
    image_url VARCHAR(255),
    image_date DATE,
    PRIMARY KEY (image_id)
);

CREATE TABLE aurora_colour (
    aurora_colour_id SMALLINT,
    colour VARCHAR(6),
    description VARCHAR(30),
    meaning VARCHAR(50),
    PRIMARY KEY (aurora_colour_id)
);