FROM frappe/bench:latest

USER root
RUN apt-get update && apt-get install -y git
USER frappe

COPY --chown=frappe:frappe . /home/frappe/frappe-bench/apps/ecobright

RUN bench get-app --skip-assets --resolve-deps ecobright
