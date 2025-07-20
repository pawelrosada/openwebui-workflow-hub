#!/bin/bash
set -e

# Create additional databases for Open WebUI
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create Open WebUI database if it doesn't exist
    SELECT 'CREATE DATABASE openwebui'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'openwebui')\gexec

    -- Grant privileges to the user
    GRANT ALL PRIVILEGES ON DATABASE openwebui TO $POSTGRES_USER;
EOSQL

echo "Database initialization completed successfully!"