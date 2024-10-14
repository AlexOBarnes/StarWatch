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
    alert_time TIMESTAMP NOT NULL,
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
    PRIMARY KEY (body_id)
);

CREATE TABLE body_assignment (
    assignment_id BIGINT GENERATED ALWAYS AS IDENTITY,
    region_id SMALLINT NOT NULL,
    body_id BIGINT NOT NULL,
    at TIMESTAMP NOT NULL,
    azimuth FLOAT NOT NULL,
    altitude FLOAT NOT NULL,
    distance_km FLOAT NOT NULL,
    constellation_id SMALLINT,
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (region_id) REFERENCES region(region_id),
    FOREIGN KEY (body_id) REFERENCES body(body_id),
    FOREIGN KEY (constellation_id) REFERENCES constellation(constellation_id)
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
    PRIMARY KEY (feature_id),
    FOREIGN KEY (county_id) REFERENCES county(county_id)
);

CREATE TABLE forecast (
    forecast_id BIGINT GENERATED ALWAYS AS IDENTITY,
    county_id SMALLINT NOT NULL,
    temperature_c FLOAT NOT NULL,
    precipitation_probability_percent SMALLINT NOT NULL,
    precipitation_mm FLOAT NOT NULL,
    cloud_coverage_percent SMALLINT NOT NULL,
    visibility_m INT NOT NULL,
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
    image_name VARCHAR(100) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    image_date DATE NOT NULL,
    region_id SMALLINT,
    constellation_id SMALLINT,
    PRIMARY KEY (image_id),
    FOREIGN KEY (region_id) REFERENCES region(region_id),
    FOREIGN KEY (constellation_id) REFERENCES constellation(constellation_id)
);

INSERT INTO aurora_colour (aurora_colour_id, colour, description, meaning) VALUES
(1, 'Green', 'No significant activity', 'Aurora is unlikely to be visible by eye or camera from anywhere in the UK.'),
(2, 'Yellow', 'Minor geomagnetic activity', 'Aurora may be visible by eye from Scotland and may be visible by camera from Scotland, northern England and Northern Ireland.'),
(3, 'Amber', 'Amber alert: possible aurora', 'Aurora is likely to be visible by eye from Scotland, northern England and Northern Ireland; possibly visible from elsewhere in the UK. Photographs of aurora are likely from anywhere in the UK.'),
(4, 'Red', 'Red alert: aurora likely', 'It is likely that aurora will be visible by eye and camera from anywhere in the UK.');

INSERT INTO region (region_name, latitude, longitude) VALUES
('Northern Ireland', 54.61, -6.62),
('Scotland', 56.49, -4.20),
('Wales', 52.13, -3.78),
('North East', 54.97, -1.61),
('North West', 53.78, -2.70),
('Yorkshire and the Humber', 53.80, -1.54),
('East Midlands', 52.90, -1.23),
('West Midlands', 52.48, -1.89),
('East of England', 52.24, 0.90),
('London', 51.51, -0.13),
('South East', 51.28, -0.78),
('South West', 50.78, -3.79);

INSERT INTO county (county_name, latitude, longitude, region_id) VALUES
('Antrim', 54.71, -6.22, 1),
('Armagh', 54.35, -6.65, 1),
('Down', 54.5, -5.72, 1),
('Fermanagh', 54.35, -7.63, 1),
('Londonderry', 54.98, -7.31, 1),
('Tyrone', 54.6, -7.0, 1),

('Aberdeen City', 57.15, -2.11, 2),
('Aberdeenshire', 57.28, -2.52, 2),
('Angus', 56.73, -2.91, 2),
('Argyll and Bute', 56.25, -5.42, 2),
('Clackmannanshire', 56.11, -3.79, 2),
('Dumfries and Galloway', 55.07, -3.61, 2),
('Dundee City', 56.46, -2.97, 2),
('East Ayrshire', 55.45, -4.37, 2),
('East Dunbartonshire', 55.94, -4.21, 2),
('East Lothian', 55.95, -2.77, 2),
('East Renfrewshire', 55.78, -4.37, 2),
('Edinburgh', 55.95, -3.19, 2),
('Falkirk', 56.0, -3.79, 2),
('Fife', 56.2, -3.16, 2),
('Glasgow City', 55.86, -4.25, 2),
('Highland', 57.48, -4.22, 2),
('Inverclyde', 55.91, -4.69, 2),
('Midlothian', 55.84, -3.08, 2),
('Moray', 57.61, -3.32, 2),
('North Ayrshire', 55.68, -4.78, 2),
('North Lanarkshire', 55.85, -3.99, 2),
('Orkney Islands', 58.97, -2.95, 2),
('Perth and Kinross', 56.4, -3.43, 2),
('Renfrewshire', 55.84, -4.42, 2),
('Scottish Borders', 55.55, -2.78, 2),
('Shetland Islands', 60.27, -1.29, 2),
('South Ayrshire', 55.42, -4.62, 2),
('South Lanarkshire', 55.61, -3.94, 2),
('Stirling', 56.12, -3.94, 2),
('West Dunbartonshire', 55.94, -4.57, 2),
('West Lothian', 55.9, -3.52, 2),
('Western Isles', 58.2, -6.37, 2),

('Anglesey', 53.3, -4.41, 3),
('Blaenau Gwent', 51.75, -3.17, 3),
('Bridgend', 51.51, -3.58, 3),
('Caerphilly', 51.58, -3.22, 3),
('Cardiff', 51.48, -3.18, 3),
('Carmarthenshire', 51.86, -4.3, 3),
('Ceredigion', 52.22, -4.01, 3),
('Conwy', 53.28, -3.8, 3),
('Denbighshire', 53.18, -3.43, 3),
('Flintshire', 53.23, -3.14, 3),
('Gwynedd', 52.91, -4.1, 3),
('Merthyr Tydfil', 51.75, -3.38, 3),
('Monmouthshire', 51.77, -2.93, 3),
('Neath Port Talbot', 51.66, -3.81, 3),
('Newport', 51.58, -3.0, 3),
('Pembrokeshire', 51.7, -4.91, 3),
('Powys', 52.25, -3.41, 3),
('Rhondda Cynon Taf', 51.63, -3.45, 3),
('Swansea', 51.62, -3.94, 3),
('Torfaen', 51.68, -3.0, 3),
('Vale of Glamorgan', 51.46, -3.44, 3),
('Wrexham', 53.05, -3.0, 3),

('County Durham', 54.78, -1.57, 4),
('Northumberland', 55.27, -1.9, 4),
('Tyne and Wear', 54.97, -1.61, 4),

('Cheshire', 53.2, -2.52, 5),
('Cumbria', 54.46, -2.96, 5),
('Greater Manchester', 53.48, -2.24, 5),
('Lancashire', 53.87, -2.6, 5),
('Merseyside', 53.41, -2.99, 5),

('East Riding of Yorkshire', 53.84, -0.43, 6),
('North Yorkshire', 54.15, -1.38, 6),
('South Yorkshire', 53.5, -1.47, 6),
('West Yorkshire', 53.79, -1.54, 6),

('Derbyshire', 53.06, -1.49, 7),
('Leicestershire', 52.63, -1.14, 7),
('Lincolnshire', 53.23, -0.54, 7),
('Northamptonshire', 52.25, -0.88, 7),
('Nottinghamshire', 53.13, -1.02, 7),
('Rutland', 52.67, -0.64, 7),

('Herefordshire', 52.06, -2.71, 8),
('Shropshire', 52.68, -2.74, 8),
('Staffordshire', 52.8, -2.01, 8),
('Warwickshire', 52.28, -1.58, 8),
('West Midlands', 52.48, -1.89, 8),
('Worcestershire', 52.19, -2.22, 8),

('Bedfordshire', 52.14, -0.46, 9),
('Cambridgeshire', 52.2, 0.13, 9),
('Essex', 51.75, 0.58, 9),
('Hertfordshire', 51.83, -0.2, 9),
('Norfolk', 52.63, 1.29, 9),
('Suffolk', 52.19, 1.0, 9),

('Greater London', 51.51, -0.13, 10),

('Berkshire', 51.45, -0.97, 11),
('Buckinghamshire', 51.82, -0.83, 11),
('East Sussex', 50.92, 0.27, 11),
('Hampshire', 51.06, -1.31, 11),
('Kent', 51.28, 0.52, 11),
('Oxfordshire', 51.75, -1.26, 11),
('Surrey', 51.25, -0.45, 11),
('West Sussex', 50.91, -0.55, 11),

('Bristol', 51.45, -2.58, 12),
('Cornwall', 50.45, -5.0, 12),
('Devon', 50.71, -3.53, 12),
('Dorset', 50.75, -2.44, 12),
('Gloucestershire', 51.86, -2.24, 12),
('Somerset', 51.1, -2.75, 12),
('Wiltshire', 51.34, -1.99, 12);

INSERT INTO constellation (constellation_name, constellation_short_name) VALUES
('Andromeda', 'And'),
('Antlia', 'Ant'),
('Apus', 'Aps'),
('Aquarius', 'Aqr'),
('Aquila', 'Aql'),
('Ara', 'Ara'),
('Aries', 'Ari'),
('Auriga', 'Aur'),
('Boötes', 'Boo'),
('Caelum', 'Cae'),
('Camelopardalis', 'Cam'),
('Cancer', 'Cnc'),
('Canes Venatici', 'CVn'),
('Canis Major', 'CMa'),
('Canis Minor', 'CMi'),
('Capricornus', 'Cap'),
('Carina', 'Car'),
('Cassiopeia', 'Cas'),
('Centaurus', 'Cen'),
('Cephus', 'Cep'),
('Cetus', 'Cet'),
('Chamaeleon', 'Cha'),
('Circinus', 'Cir'),
('Columba', 'Col'),
('Coma Berenices', 'Com'),
('Corona Australis', 'CrA'),
('Corona Borealis', 'CrB'),
('Corvus', 'Crv'),
('Crater', 'Crt'),
('Crux', 'Cru'),
('Cygnus', 'Cyg'),
('Delphinus', 'Del'),
('Dorado', 'Dor'),
('Draco', 'Dra'),
('Equuleus', 'Equ'),
('Eridanus', 'Eri'),
('Fornax', 'For'),
('Gemini', 'Gem'),
('Grus', 'Gru'),
('Hercules', 'Her'),
('Horologium', 'Hor'),
('Hydra', 'Hya'),
('Hydrus', 'Hyi'),
('Indus', 'Ind'),
('Lacerta', 'Lac'),
('Leo', 'Leo'),
('Leo Minor', 'LMi'),
('Lepus', 'Lep'),
('Libra', 'Lib'),
('Lupus', 'Lup'),
('Lynx', 'Lyn'),
('Lyra', 'Lyr'),
('Mensa', 'Men'),
('Microscopium', 'Mic'),
('Monoceros', 'Mon'),
('Musca', 'Mus'),
('Norma', 'Nor'),
('Octans', 'Oct'),
('Ophiuchus', 'Oph'),
('Orion', 'Ori'),
('Pavo', 'Pav'),
('Pegasus', 'Peg'),
('Perseus', 'Per'),
('Phoenix', 'Phe'),
('Pictor', 'Pic'),
('Pisces', 'Psc'),
('Piscis Austrinus', 'PsA'),
('Puppis', 'Pup'),
('Pyxis', 'Pyx'),
('Reticulum', 'Ret'),
('Sagitta', 'Sge'),
('Sagittarius', 'Sgr'),
('Scorpius', 'Sco'),
('Sculptor', 'Scl'),
('Scutum', 'Sct'),
('Serpens', 'Ser'),
('Sextans', 'Sex'),
('Taurus', 'Tau'),
('Telescopium', 'Tel'),
('Triangulum', 'Tri'),
('Triangulum Australe', 'TrA'),
('Tucana', 'Tuc'),
('Ursa Major', 'UMa'),
('Ursa Minor', 'UMi'),
('Vela', 'Vel'),
('Virgo', 'Vir'),
('Volans', 'Vol'),
('Vulpecula', 'Vul');

INSERT INTO body (body_name) VALUES
('Mercury'),
('Venus'),
('Mars'),
('Jupiter'),
('Saturn'),
('Uranus'),
('Neptune'),
('Pluto'),
('Sun'),
('Moon');