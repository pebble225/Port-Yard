# Port-Yard: Database Backup System

## Brief Overview

The goal of this project is to create a somewhat lightweight, containerized, easy-to-deploy database backup system that can take full backups of MySQL/MariaDB databases (and potentially Postgres as well) on a cron-like schedule, compress them, and save them to a modular storage backend.  Through a set of retention rules database backups can be thinned with time.  A web interface displays the live status of the different backup targets and their backup artifacts, and the interface allows backups to be restored to the servers (with the appropriate warnings).  Additionally backup files can be downloaded by web clients.

The expected deployment will be in a containerized environment, such as K8s or Docker.  We don't need to plan to support or target other environments.  Most likely we will use a Debian or Ubuntu LTS base image.

Configuration should primarily be done through a static configuration file, as the system should ideally be deployable in a degraded environment, or as part of a recovery/bootstrapping process.  The application ideally shouldn't require its own database.

Authentication/authorization can initially be done by putting it behind an authenticating proxy.  Eventually it would be nice to support a few simple authentication mechanisms, and some means of authenticating against Active Directory/LDAP (such as via OpenID Connect federated with Keycloak).

## Feature Planning/Details

The following are a list of feature ideas we can prioritize/refine/eliminate/add to:

* Support MySQL and MariaDB backups (via `mysqldump`)
* Support Postgres backups (via `pg_dump`)
* Allow multiple database targets, potentially on different servers
* Each target gets its own cron-style backup schedule
* Compression can optionally be enabled on each target, allowing the file to be zipped before being sent to storage
* Databases which support it can be read to see if updates have happened since the last backup, allowing backups to optionally be skipped if no changes have been made
* Backups, once taken, are sent to a storage backend
    * Support S3 compatible backend
    * Support filesystem backend
    * *Other options for self-hosters?*
* Backups can optionally be automatically tested by restoring to a pre-configured test server as part of the backup process
* Backups can be restored back to the source
* Backups can be deployed to a pre-configured test server and credentials generated for developers (would be a really useful feature)
* Backup failures can trigger notifications
    * Webhook style notification
    * Microsoft Teams
    * Slack
* A web interface to make the system easy to manage:
    * Lists the different backup targets
    * Shows things like time-to-next-backup, history of successful backups, backup failures since startup
    * Progress bars for backup/restore/compress progress?
* Layered retention policies for which backups to keep and which to delete (ie. keep 1 backup from every 15 minutes for 24 hours, 1 backup per hour for 72 hours, 1 backup per day for 2 weeks, 1 backup per week for 1 year) for each backup target individually
* Multiple authentication modes configurable through config file:
    * Unauthenticated access (for unprotected use or behind an authenticating proxy)
    * Simple static username/password
    * OpenID Connect and/or LDAP
* Authorization
    * Two roles at most: "can view" vs "can restore"
    * Leave hooks in that someone using a more complex authentication method can split authorization between those roles if they wanted to


