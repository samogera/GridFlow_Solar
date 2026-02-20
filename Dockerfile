FROM frappe/bench:latest

USER root
RUN apt-get update && apt-get install -y git
USER frappe

# Initialize a fresh Frappe bench with Python 3.12 (Python 3.14 is incompatible with Frappe v15)
RUN bench init --skip-assets --skip-redis-config-generation --frappe-branch version-15 --python python3.12 /home/frappe/frappe-bench

WORKDIR /home/frappe/frappe-bench

# Copy the custom app into the bench apps directory
COPY --chown=frappe:frappe . /home/frappe/frappe-bench/apps/ecobright

# Install the app: pip install it, then register it in the apps list
RUN /home/frappe/frappe-bench/env/bin/pip install -e /home/frappe/frappe-bench/apps/ecobright \
    && printf "\necobright\n" >> /home/frappe/frappe-bench/sites/apps.txt

# Configure Redis and DB to use Docker Compose service names
RUN echo '{\
    "db_host": "db",\
    "redis_cache": "redis://redis:6379/0",\
    "redis_queue": "redis://redis:6379/1",\
    "redis_socketio": "redis://redis:6379/2",\
    "socketio_port": 9000\
    }' > /home/frappe/frappe-bench/sites/common_site_config.json
