#!/bin/bash

# Install PostgreSQL if not installed
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE steganography_db;
CREATE USER steganography_user WITH PASSWORD 'your_secure_password';
ALTER ROLE steganography_user SET client_encoding TO 'utf8';
ALTER ROLE steganography_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE steganography_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE steganography_db TO steganography_user;
EOF

# Backup cron job
echo "0 0 * * * pg_dump steganography_db > /path/to/backups/backup_\$(date +\%Y\%m\%d).sql" | sudo tee -a /etc/crontab
