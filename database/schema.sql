DROP TABLE IF EXISTS aurora_colour, image;

CREATE TABLE image (
    image_id BIGINT GENERATED ALWAYS AS IDENTITY,
    image_name VARCHAR(10) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    image_date DATE NOT NULL,
    PRIMARY KEY (image_id)
);

CREATE TABLE aurora_colour (
    aurora_colour_id SMALLINT,
    colour VARCHAR(6) NOT NULL,
    description VARCHAR(30) NOT NULL,
    meaning VARCHAR(50) NOT NULL,
    PRIMARY KEY (aurora_colour_id)
);