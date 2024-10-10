source .env
export PGPASSWORD=$DB_PASSWORD
psql -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME -c 'TRUNCATE TABLE solar_feature, aurora_alert, image, forecast, body_assignment;'