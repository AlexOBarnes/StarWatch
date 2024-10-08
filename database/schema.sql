DROP TABLE IF EXISTS body, constellation, region, aurora_alert, aurora_colour, image;

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
    meaning VARCHAR(255) NOT NULL,
    PRIMARY KEY (aurora_colour_id)
);

CREATE TABLE aurora_alert (
    alert_id BIGINT GENERATED ALWAYS AS IDENTITY,
    alert_time TIMESTAMP NOT NULL,
    aurora_colour_id SMALLINT NOT NULL,
    PRIMARY KEY (alert_id),
    FOREIGN KEY (aurora_colour_id) REFERENCES aurora_colour(aurora_colour_id)
);

CREATE TABLE region (
    region_id SMALLINT,
    region_name VARCHAR(25) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    PRIMARY KEY (region_id)
);

CREATE TABLE constellation (
    constellation_id SMALLINT,
    constellation_name VARCHAR(35) NOT NULL,
    PRIMARY KEY (constellation_id)
)

CREATE TABLE body (
    body_id BIGINT,
    body_name VARCHAR(35) NOT NULL,
    constellation_id SMALLINT,
    PRIMARY KEY (body_id),
    FOREIGN KEY (constellation_id) REFERENCES constellation(constellation_id)
);