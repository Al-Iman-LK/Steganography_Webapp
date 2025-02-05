#!/bin/bash

# Install certbot
sudo apt-get update
sudo apt-get install -y certbot python3-certbot-nginx

# Generate SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal cron job
echo "0 0 1 * * certbot renew --quiet" | sudo tee -a /etc/crontab
