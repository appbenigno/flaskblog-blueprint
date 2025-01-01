bind = '0.0.0.0:8000'  # Bind to all interfaces on port 8000
workers = 3  # Number of worker processes
worker_class = 'sync'  # Type of worker class (sync, gevent, etc.)
timeout = 30  # Worker timeout
loglevel = 'info'  # Logging level
accesslog = '-'  # Access log to stdout
errorlog = '-'  # Error log to stderr