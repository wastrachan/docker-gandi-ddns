#!/usr/bin/env sh
set -e

# Generate CRON entry
echo "${UPDATE_SCHEDULE:-"*/5 * * * *"} python /gandi-ddns.py" > /etc/crontabs/root

# Exec CMD
exec "$@"
