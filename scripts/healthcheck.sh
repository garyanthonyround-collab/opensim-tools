#!/bin/bash

echo "===== OpenSimulator Health Check ====="
echo

echo "Date:"
date

echo
echo "OpenSimulator:"
systemctl is-active opensim

echo
echo "MariaDB:"
systemctl is-active mariadb

echo
echo "Memory:"
free -h

echo
echo "Disk:"
df -h /

echo
echo "OpenSimulator Port:"
ss -ltn | grep 9000

echo
echo "Database Size:"
du -sh /var/lib/mysql
