DROP TABLE IF EXISTS image, subscriber_county_assignment, subscriber, forecast, solar_feature, county, body_assignment, body, constellation, region, aurora_alert, aurora_colour;

CREATE TABLE aurora_colour (
    aurora_colour_id SMALLINT,
    colour VARCHAR(6) NOT NULL UNIQUE,
    description VARCHAR(30) NOT NULL UNIQUE,
    meaning VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY (aurora_colour_id)
);

CREATE TABLE aurora_alert (
    alert_id BIGINT GENERATED ALWAYS AS IDENTITY,
    alert_time TIMESTAMP NOT NULL CHECK(alert_time<=CURRENT_TIMESTAMP),
    aurora_colour_id SMALLINT NOT NULL,
    PRIMARY KEY (alert_id),
    FOREIGN KEY (aurora_colour_id) REFERENCES aurora_colour(aurora_colour_id)
);

CREATE TABLE region (
    region_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    region_name VARCHAR(25) NOT NULL UNIQUE,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    PRIMARY KEY (region_id)
);

CREATE TABLE constellation (
    constellation_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    constellation_name VARCHAR(35) NOT NULL UNIQUE,
    constellation_short_name VARCHAR(3) NOT NULL UNIQUE,
    PRIMARY KEY (constellation_id)
);

CREATE TABLE body (
    body_id INT GENERATED ALWAYS AS IDENTITY,
    body_name VARCHAR(35) NOT NULL UNIQUE,
    constellation_id SMALLINT,
    PRIMARY KEY (body_id),
    FOREIGN KEY (constellation_id) REFERENCES constellation(constellation_id)
);

CREATE TABLE body_assignment (
    assignment_id BIGINT GENERATED ALWAYS AS IDENTITY,
    region_id SMALLINT NOT NULL,
    body_id BIGINT NOT NULL,
    at TIMESTAMP NOT NULL,
    azimuth FLOAT NOT NULL,
    altitude FLOAT NOT NULL,
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (region_id) REFERENCES region(region_id),
    FOREIGN KEY (body_id) REFERENCES body(body_id)
);

CREATE TABLE county (
    county_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    county_name VARCHAR(35) NOT NULL UNIQUE,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    region_id SMALLINT NOT NULL,
    PRIMARY KEY (county_id),
    FOREIGN KEY (region_id) REFERENCES region(region_id)
);

CREATE TABLE solar_feature (
    feature_id BIGINT GENERATED ALWAYS AS IDENTITY,
    sunrise_timestamp TIMESTAMP NOT NULL,
    sunset_timestamp TIMESTAMP NOT NULL,
    county_id SMALLINT NOT NULL,
    PRIMARY KEY (sunrise_id),
    FOREIGN KEY (county_id) REFERENCES county(county_id)
);

CREATE TABLE forecast (
    forecast_id BIGINT GENERATED ALWAYS AS IDENTITY,
    county_id SMALLINT NOT NULL,
    temperature_c FLOAT NOT NULL,
    precipitation_probability_percent SMALLINT NOT NULL,
    precipitation_mm FLOAT NOT NULL,
    cloud_coverage_percent SMALLINT NOT NULL,
    visibility_m SMALLINT NOT NULL,
    at TIMESTAMP NOT NULL,
    PRIMARY KEY (forecast_id),
    FOREIGN KEY (county_id) REFERENCES county(county_id)
);

CREATE TABLE subscriber (
    subscriber_id BIGINT GENERATED ALWAYS AS IDENTITY,
    subscriber_username VARCHAR(30) NOT NULL UNIQUE,
    subscriber_phone VARCHAR(15),
    subscriber_email VARCHAR(255),
    PRIMARY KEY (subscriber_id),
    CONSTRAINT phone_or_email_exist CHECK (
        subscriber_phone IS NOT NULL OR subscriber_email IS NOT NULL
    )
);

CREATE TABLE subscriber_county_assignment (
    assignment_id BIGINT GENERATED ALWAYS AS IDENTITY,
    subscriber_id BIGINT NOT NULL,
    county_id SMALLINT NOT NULL,
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (subscriber_id) REFERENCES subscriber(subscriber_id),
    FOREIGN KEY (county_id) REFERENCES county(county_id)
);

CREATE TABLE image (
    image_id BIGINT GENERATED ALWAYS AS IDENTITY,
    image_name VARCHAR(10) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    image_date DATE NOT NULL,
    region_id SMALLINT,
    constellation_id SMALLINT,
    PRIMARY KEY (image_id),
    FOREIGN KEY (region_id) REFERENCES region(region_id),
    FOREIGN KEY (constellation_id) REFERENCES constellation(constellation_id)
);

INSERT INTO aurora_colour (aurora_colour_id, colour, description, meaning) VALUES
(0, 'Green', 'No significant activity', 'Aurora is unlikely to be visible by eye or camera from anywhere in the UK.'),
(1, 'Yellow', 'Minor geomagnetic activity', 'Aurora may be visible by eye from Scotland and may be visible by camera from Scotland, northern England and Northern Ireland.'),
(2, 'Amber', 'Amber alert: possible aurora', 'Aurora is likely to be visible by eye from Scotland, northern England and Northern Ireland; possibly visible from elsewhere in the UK. Photographs of aurora are likely from anywhere in the UK.'),
(3, 'Red', 'Red alert: aurora likely', 'It is likely that aurora will be visible by eye and camera from anywhere in the UK.');

