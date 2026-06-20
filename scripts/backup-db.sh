#!/bin/bash

BACKUPDIR="/opt/opensim-admin/backups/sql"
DATE=$(date +%Y-%m-%d_%H-%M)

mkdir -p "$BACKUPDIR"

mysqldump opensim \
| gzip > "$BACKUPDIR/opensim-$DATE.sql.gz"

find "$BACKUPDIR" -name "*.gz" -mtime +14 -delete
