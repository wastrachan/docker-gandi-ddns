#!/usr/bin/env sh
set -e

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Starting gandi-ddns..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "    [+] Creating CRON entry..."
echo "${UPDATE_SCHEDULE:-"*/5 * * * *"} python /gandi-ddns.py" > /etc/crontabs/root

echo "    [+] Running..."
echo ""
exec "$@"
