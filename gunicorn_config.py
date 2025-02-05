import multiprocessing

bind = "unix:/run/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
worker_class = "gthread"
threads = 4

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# SSL Configuration
keyfile = "/etc/ssl/private/server.key"
certfile = "/etc/ssl/certs/server.crt"
