# Prometheus Backup Exporter
Custom Prometheus exporter for monitoring backup status in my personal server. Developed in Python3 language and has been tested on Ubuntu v18.04.

## Info
Custom exporter made to monitor backup files in different directories and report status for Prometheus to collect. The exporter checks the dates of all backup files/directories in the main directory and reports if there's any missing backups.

Since this exporter was developed for my needs, feel free to take this script and modify it for your use. I left my directory paths there as an example. This works with both files and directories. For example, MongoDB dumps into a directory while MySQL/MariaDB & ZIP creates a single file. If the backup directory is missing or it is unable to access it due to permissions issue or data corruption, it will return `0.0`.

### 1st Example
```
/backups/db
    10-11-2018.sql
    10-12-2018.sql
    10-13-2018.sql
    10-14-2018.sql
    10-15-2018.sql
```
With current date as 10-15-2018 at 2PM with auto daily backups at 2AM. This would report as `2.0` because all files are there, including today's backup.

### 2nd Example
```
/backups/db
    10-11-2018.sql
    10-12-2018.sql
    10-14-2018.sql
    10-15-2018.sql
```
With current date as 10-15-2018 at 2PM with auto daily backups at 2AM. This would report as `1.0` because one of the files `10-13-2018.sql` is missing. This would help sysadmins know which day the backup failed and get notification that it didn't back up properly. **Since this exporter would run 24/7, it will report on the same day it fails to backup regardless.**

## Metrics Example
```
# HELP mariadb_backup MariaDB Backup Status
# TYPE mariadb_backup gauge
mariadb_backup 2.0
# HELP cloud_backup Cloud Backup Status
# TYPE cloud_backup gauge
cloud_backup 2.0
# HELP mongodb_backup MongoDB Backup Status
# TYPE mongodb_backup gauge
mongodb_backup 2.0
# HELP docker_backup Docker Backup Status
# TYPE docker_backup gauge
docker_backup 0.0
```