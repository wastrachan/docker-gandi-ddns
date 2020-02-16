#!/usr/bin/env sh
set -e

PUID="${PUID:-100}"
PGID="${PGID:-101}"

echo ""
echo "----------------------------------------"
echo " Starting up using the following:       "
echo "                                        "
echo "     UID: $PUID                         "
echo "     GID: $PGID                         "
echo "----------------------------------------"
echo ""

# Copy default config files
if [ ! -f "/config/config.yml" ]; then
    cp /defaults/config.yml /config/config.yml
fi

# Set UID/GID of software user
sed -i "s/^software\:x\:100\:101/software\:x\:$PUID\:$PGID/" /etc/passwd
sed -i "s/^software\:x\:101/software\:x\:$PGID/" /etc/group

# Set permissions
chown -R $PUID:$PGID /config

exec "$@"
