INSERT INTO aurora_alert (alert_time, aurora_colour_id)
VALUES 
('2024-10-07 08:15:30', 1),
('2024-10-07 09:20:45', 1),
('2024-10-07 10:35:50', 2),
('2024-10-07 11:50:05', 3),
('2024-10-07 12:55:20', 1),
('2024-10-07 14:10:35', 1),
('2024-10-07 15:25:40', 3),
('2024-10-07 16:40:55', 2),
('2024-10-07 17:55:10', 1),
('2024-10-07 19:10:25', 1),
('2024-10-07 20:25:40', 2),
('2024-10-07 21:40:55', 1),
('2024-10-07 22:55:10', 1),
('2024-10-08 00:10:25', 3),
('2024-10-08 01:25:40', 2),
('2024-10-08 02:40:55', 1),
('2024-10-08 03:55:10', 1),
('2024-09-30 14:20:35', 2),
('2024-10-01 08:45:20', 1),
('2024-10-02 19:30:50', 3),
('2024-10-03 11:55:15', 1),
('2024-10-04 16:10:40', 2),
('2024-10-05 09:25:30', 1),
('2024-10-06 13:50:45', 3),
('2024-10-06 18:05:55', 1),
('2024-10-07 07:40:10', 2),
('2024-10-07 22:15:25', 1);


INSERT INTO forecast (county_id, temperature_c, precipitation_probability_percent, precipitation_mm, cloud_coverage_percent, visibility_m, at)
VALUES
(12, 18.5, 30, 1.1, 20, 10000, '2024-09-30 14:20:35'),
(45, 15.2, 60, 2.5, 85, 8000, '2024-10-01 09:30:45'),
(8, 21.1, 10, 1.1, 10, 15000, '2024-10-02 18:15:20'),
(91, 13.8, 70, 3.2, 90, 5000, '2024-10-03 12:45:55'),
(67, 17.6, 40, 1.5, 60, 12000, '2024-10-04 16:25:10'),
(23, 20.1, 20, 1.1, 25, 14000, '2024-10-05 08:50:05'),
(58, 14.3, 80, 4.8, 95, 6000, '2024-10-06 14:55:35'),
(30, 19.4, 50, 1.2, 45, 11000, '2024-10-06 19:20:50'),
(7, 22.1, 15, 1.1, 12, 16000, '2024-10-07 07:10:25'),
(83, 16.5, 65, 2.9, 80, 9000, '2024-10-07 22:35:40');


INSERT INTO image (image_name, image_url, image_date, region_id, constellation_id)
VALUES
('NASA_apod', 'https://science.nasa.gov/wp-content/uploads/2023/09/Carina_Nebula-1.jpeg', '2024-10-01', 1, 1),
('NASA_apod', 'https://science.nasa.gov/wp-content/uploads/2023/09/Carina_Nebula-1.jpeg', '2024-10-02', 2, 2),
('NASA_apod', 'https://science.nasa.gov/wp-content/uploads/2023/09/Carina_Nebula-1.jpeg', '2024-10-03', 3, 3),
('ASTRO_moon', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/1200px-FullMoon2010.jpg', '2024-10-04', 4, 4),
('ASTRO_moon', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/1200px-FullMoon2010.jpg', '2024-10-05', 5, 5),
('ASTRO_star', 'https://dq0hsqwjhea1.cloudfront.net/Interactive-Sky-Chart-600px.jpg', '2024-10-06', 6, 6),
('ASTRO_star', 'https://dq0hsqwjhea1.cloudfront.net/Interactive-Sky-Chart-600px.jpg', '2024-10-07', 7, 7),
('NASA_apod', 'https://science.nasa.gov/wp-content/uploads/2023/09/Carina_Nebula-1.jpeg', '2024-10-08', 8, 8),
('NASA_apod', 'https://science.nasa.gov/wp-content/uploads/2023/09/Carina_Nebula-1.jpeg', '2024-10-09', 9, 9),
('ASTRO_moon', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/1200px-FullMoon2010.jpg', '2024-10-10', 10, 10),
('ASTRO_star', 'https://dq0hsqwjhea1.cloudfront.net/Interactive-Sky-Chart-600px.jpg', '2024-10-11', 11, 11),
('NASA_apod', 'https://science.nasa.gov/wp-content/uploads/2023/09/Carina_Nebula-1.jpeg', '2024-10-12', 12, 12),
('ASTRO_moon', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/1200px-FullMoon2010.jpg', '2024-10-13', 13, 13),
('ASTRO_star', 'https://dq0hsqwjhea1.cloudfront.net/Interactive-Sky-Chart-600px.jpg', '2024-10-14', 14, 14),
('NASA_apod', 'https://science.nasa.gov/wp-content/uploads/2023/09/Carina_Nebula-1.jpeg', '2024-10-15', 15, 15),
('ASTRO_star', 'https://dq0hsqwjhea1.cloudfront.net/Interactive-Sky-Chart-600px.jpg', '2024-10-16', 3, 25),
('NASA_apod', 'https://science.nasa.gov/wp-content/uploads/2023/09/Carina_Nebula-1.jpeg', '2024-10-17', 5, 12),
('ASTRO_moon', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/1200px-FullMoon2010.jpg', '2024-10-18', 7, 45),
('NASA_apod', 'https://science.nasa.gov/wp-content/uploads/2023/09/Carina_Nebula-1.jpeg', '2024-10-19', 10, 88),
('ASTRO_star', 'https://dq0hsqwjhea1.cloudfront.net/Interactive-Sky-Chart-600px.jpg', '2024-10-20', 12, 36),
('ASTRO_moon', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/1200px-FullMoon2010.jpg', '2024-10-21', 15, 55),
('NASA_apod', 'https://science.nasa.gov/wp-content/uploads/2023/09/Carina_Nebula-1.jpeg', '2024-10-22', 20, 8),
('ASTRO_star', 'https://dq0hsqwjhea1.cloudfront.net/Interactive-Sky-Chart-600px.jpg', '2024-10-23', 25, 73),
('ASTRO_moon', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/1200px-FullMoon2010.jpg', '2024-10-24', 30, 21),
('NASA_apod', 'https://science.nasa.gov/wp-content/uploads/2023/09/Carina_Nebula-1.jpeg', '2024-10-25', 35, 50);

-- NASA_apod: https://science.nasa.gov/wp-content/uploads/2023/09/Carina_Nebula-1.jpeg
-- ASTRO_moon: https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/1200px-FullMoon2010.jpg
-- ASTRO_star: https://dq0hsqwjhea1.cloudfront.net/Interactive-Sky-Chart-600px.jpg


INSERT INTO subscriber (subscriber_username, subscriber_phone, subscriber_email)
VALUES
('johndoe', '+12345678901', 'johndoe@example.com'),
('janedoe', '+12345678902', 'janedoe@example.com'),
('samsmith', '+12345678903', 'samsmith@example.com'),
('alicewong', '+12345678904', 'alicewong@example.com'),
('michaelbrown', '+12345678905', 'michaelbrown@example.com'),
('emilydavis', '+12345678906', 'emilydavis@example.com'),
('davidjohnson', '+12345678907', 'davidjohnson@example.com'),
('sarahwilson', '+12345678908', 'sarahwilson@example.com'),
('chrislee', '+12345678909', 'chrislee@example.com'),
('lauragarcia', '+12345678910', 'lauragarcia@example.com')
('robertmartin', '+12345678911', 'robertmartin@example.com'),
('lisawalker', '+12345678912', 'lisawalker@example.com'),
('tommyadams', '+12345678913', 'tommyadams@example.com'),
('nataliebell', '+12345678914', 'nataliebell@example.com'),
('jacobwhite', '+12345678915', 'jacobwhite@example.com'),
('oliviayoung', '+12345678916', 'oliviayoung@example.com'),
('ethanturner', '+12345678917', 'ethanturner@example.com'),
('gracehall', '+12345678918', 'gracehall@example.com'),
('ryanallen', '+12345678919', 'ryanallen@example.com'),
('amandacook', '+12345678920', 'amandacook@example.com');


INSERT INTO subscriber_county_assignment (subscriber_id, county_id)
VALUES
(5, 3),
(12, 7),
(23, 1),
(45, 14),
(66, 19),
(32, 1),
(89, 4),
(19, 10),
(76, 2),
(41, 13)
(14, 9),
(27, 11),
(33, 5),
(2, 18),
(60, 6),
(73, 15),
(11, 17),
(22, 8),
(4, 12),
(39, 1),
(85, 3),
(8, 1),
(56, 19),
(78, 16),
(30, 7),
(67, 2);


INSERT INTO solar_feature (sunrise_timestamp, sunset_timestamp, county_id)
VALUES
('2024-10-01 06:30:00', '2024-10-01 18:45:00', 1),
('2024-10-01 06:32:00', '2024-10-01 18:47:00', 1),
('2024-10-01 06:34:00', '2024-10-01 18:49:00', 2),
('2024-10-01 06:29:00', '2024-10-01 18:44:00', 3),
('2024-10-01 06:31:00', '2024-10-01 18:46:00', 4),
('2024-10-01 06:33:00', '2024-10-01 18:48:00', 5),
('2024-10-01 06:35:00', '2024-10-01 18:50:00', 6),
('2024-10-01 06:36:00', '2024-10-01 18:51:00', 7),
('2024-10-01 06:37:00', '2024-10-01 18:52:00', 8),
('2024-10-01 06:38:00', '2024-10-01 18:53:00', 9),
('2024-10-01 06:39:00', '2024-10-01 18:54:00', 10),
('2024-10-01 06:40:00', '2024-10-01 18:55:00', 11),
('2024-10-01 06:41:00', '2024-10-01 18:56:00', 12),
('2024-10-01 06:42:00', '2024-10-01 18:57:00', 13),
('2024-10-01 06:43:00', '2024-10-01 18:58:00', 14),
('2024-10-01 06:44:00', '2024-10-01 18:59:00', 15),
('2024-10-01 06:45:00', '2024-10-01 19:00:00', 16),
('2024-10-01 06:46:00', '2024-10-01 19:01:00', 17),
('2024-10-01 06:47:00', '2024-10-01 19:02:00', 18),
('2024-10-01 06:48:00', '2024-10-01 19:03:00', 19),
('2024-10-01 06:49:00', '2024-10-01 19:04:00', 20),
('2024-10-01 06:50:00', '2024-10-01 19:05:00', 21),
('2024-10-01 06:51:00', '2024-10-01 19:06:00', 22),
('2024-10-01 06:52:00', '2024-10-01 19:07:00', 23),
('2024-10-01 06:53:00', '2024-10-01 19:08:00', 24),
('2024-10-01 06:54:00', '2024-10-01 19:09:00', 25),
('2024-10-01 06:55:00', '2024-10-01 19:10:00', 26),
('2024-10-01 06:56:00', '2024-10-01 19:11:00', 27),
('2024-10-01 06:57:00', '2024-10-01 19:12:00', 28),
('2024-10-01 06:58:00', '2024-10-01 19:13:00', 29),
('2024-10-01 06:59:00', '2024-10-01 19:14:00', 30),
('2024-10-01 07:00:00', '2024-10-01 19:15:00', 31),
('2024-10-01 07:01:00', '2024-10-01 19:16:00', 32),
('2024-10-01 07:02:00', '2024-10-01 19:17:00', 33),
('2024-10-01 07:03:00', '2024-10-01 19:18:00', 34),
('2024-10-01 07:04:00', '2024-10-01 19:19:00', 35),
('2024-10-01 07:05:00', '2024-10-01 19:20:00', 36),
('2024-10-01 07:06:00', '2024-10-01 19:21:00', 37),
('2024-10-01 07:07:00', '2024-10-01 19:22:00', 38),
('2024-10-01 07:08:00', '2024-10-01 19:23:00', 39),
('2024-10-01 07:09:00', '2024-10-01 19:24:00', 40),
('2024-10-01 07:10:00', '2024-10-01 19:25:00', 41),
('2024-10-01 07:11:00', '2024-10-01 19:26:00', 42),
('2024-10-01 07:12:00', '2024-10-01 19:27:00', 43),
('2024-10-01 07:13:00', '2024-10-01 19:28:00', 44),
('2024-10-01 07:14:00', '2024-10-01 19:29:00', 45),
('2024-10-01 07:15:00', '2024-10-01 19:30:00', 46),
('2024-10-01 07:16:00', '2024-10-01 19:31:00', 47),
('2024-10-01 07:17:00', '2024-10-01 19:32:00', 48),
('2024-10-01 07:18:00', '2024-10-01 19:33:00', 49),
('2024-10-01 07:19:00', '2024-10-01 19:34:00', 50),
('2024-10-01 07:20:00', '2024-10-01 19:35:00', 51),
('2024-10-01 07:21:00', '2024-10-01 19:36:00', 52),
('2024-10-01 07:22:00', '2024-10-01 19:37:00', 53),
('2024-10-01 07:23:00', '2024-10-01 19:38:00', 54),
('2024-10-01 07:24:00', '2024-10-01 19:39:00', 55),
('2024-10-01 07:25:00', '2024-10-01 19:40:00', 56),
('2024-10-01 07:26:00', '2024-10-01 19:41:00', 57),
('2024-10-01 07:27:00', '2024-10-01 19:42:00', 58),
('2024-10-01 07:28:00', '2024-10-01 19:43:00', 59),
('2024-10-01 07:29:00', '2024-10-01 19:44:00', 60),
('2024-10-01 07:30:00', '2024-10-01 19:45:00', 61),
('2024-10-01 07:31:00', '2024-10-01 19:46:00', 62),
('2024-10-01 07:32:00', '2024-10-01 19:47:00', 63),
('2024-10-01 07:33:00', '2024-10-01 19:48:00', 64),
('2024-10-01 07:34:00', '2024-10-01 19:49:00', 65),
('2024-10-01 07:35:00', '2024-10-01 19:50:00', 66),
('2024-10-01 07:36:00', '2024-10-01 19:51:00', 67),
('2024-10-01 07:37:00', '2024-10-01 19:52:00', 68),
('2024-10-01 07:38:00', '2024-10-01 19:53:00', 69),
('2024-10-01 07:39:00', '2024-10-01 19:54:00', 70),
('2024-10-01 07:40:00', '2024-10-01 19:55:00', 71),
('2024-10-01 07:41:00', '2024-10-01 19:56:00', 72),
('2024-10-01 07:42:00', '2024-10-01 19:57:00', 73),
('2024-10-01 07:43:00', '2024-10-01 19:58:00', 74),
('2024-10-01 07:44:00', '2024-10-01 19:59:00', 75),
('2024-10-01 07:45:00', '2024-10-01 20:00:00', 76),
('2024-10-01 07:46:00', '2024-10-01 20:01:00', 77),
('2024-10-01 07:47:00', '2024-10-01 20:02:00', 78),
('2024-10-01 07:48:00', '2024-10-01 20:03:00', 79),
('2024-10-01 07:49:00', '2024-10-01 20:04:00', 80),
('2024-10-01 07:50:00', '2024-10-01 20:05:00', 81),
('2024-10-01 07:51:00', '2024-10-01 20:06:00', 82),
('2024-10-01 07:52:00', '2024-10-01 20:07:00', 83),
('2024-10-01 07:53:00', '2024-10-01 20:08:00', 84),
('2024-10-01 07:54:00', '2024-10-01 20:09:00', 85),
('2024-10-01 07:55:00', '2024-10-01 20:10:00', 86),
('2024-10-01 07:56:00', '2024-10-01 20:11:00', 87),
('2024-10-01 07:57:00', '2024-10-01 20:12:00', 88),
('2024-10-01 07:58:00', '2024-10-01 20:13:00', 89),
('2024-10-01 07:59:00', '2024-10-01 20:14:00', 90),
('2024-10-01 08:00:00', '2024-10-01 20:15:00', 91);


INSERT INTO body_assignment (region_id, body_id, at, azimuth, altitude)
VALUES
(1, 1, '2024-10-01 12:00:00', 45.1, 30.1),
(1, 1, '2024-10-01 12:15:00', 90.1, 40.1),
(2, 2, '2024-10-01 12:30:00', 135.1, 20.1),
(3, 3, '2024-10-01 12:45:00', 180.1, 25.1),
(4, 4, '2024-10-01 13:00:00', 225.1, 35.1),
(5, 5, '2024-10-01 13:15:00', 270.1, 45.1),
(6, 6, '2024-10-01 13:30:00', 315.1, 15.1),
(7, 7, '2024-10-01 13:45:00', 360.1, 50.1),
(8, 8, '2024-10-01 14:00:00', 30.1, 60.1),
(9, 9, '2024-10-01 14:15:00', 75.1, 55.1),
(10, 1, '2024-10-01 14:30:00', 120.1, 65.1),
(11, 1, '2024-10-01 14:45:00', 150.1, 70.1),
(12, 2, '2024-10-01 15:00:00', 210.1, 80.1),
(1, 1, '2024-10-01 15:15:00', 45.5, 30.5),
(2, 2, '2024-10-01 15:30:00', 95.2, 40.4),
(3, 3, '2024-10-01 15:45:00', 140.3, 20.8),
(4, 4, '2024-10-01 16:00:00', 185.0, 25.7),
(5, 5, '2024-10-01 16:15:00', 230.6, 35.8),
(6, 6, '2024-10-01 16:30:00', 275.4, 45.3),
(7, 7, '2024-10-01 16:45:00', 320.2, 15.4),
(8, 8, '2024-10-01 17:00:00', 365.1, 50.9),
(9, 9, '2024-10-01 17:15:00', 30.7, 60.8),
(10, 1, '2024-10-01 17:30:00', 80.4, 55.5),
(11, 3, '2024-10-01 17:45:00', 120.9, 65.7),
(12, 4, '2024-10-01 18:00:00', 150.2, 70.3);
