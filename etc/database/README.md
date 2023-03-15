# Database Scripts

Streamlining the operations to backup and restore a rosalution_db database from a docker container.
These bash scripts are intended for documentation of how these operations are done and can be used
for reference for deployments elsewhere.

* backup-database.sh - Backs up a MongoDB 'rosalution_db' with an archived dump from the target docker container  
`./backup-database.sh <docker-container> <output-path (optional)>`

* restore-database.sh - Executes a mongo restore of a MongoDB 'rosalution_db' from an archived dump  
`./restore-database.sh <docker-container> <target-restore-database-archive>`

* ./deploy-development-prod-database.sh - Deploys the MongoDB 'rosalution-db' service which attaches
to the existing 'rosalution-network-prod' docker network. The new container deployment
is constrained to being on the primary swarm node in order to mount the data directory for MongoDB.  This
persists the data for MongoDB within the container.
`./deploy-development-prod-database.sh`

* ./remove-analysis - Searches mongo for an analysis name provided by the user and prompts to delete.
`./remove-analysis.sh -c <mongo_connection_string> -d <docker_container_name> -m <mongo_database>`

* ./set-new-annotations-configuration.sh - Backups the existing Rosalution Annotation Configuration as an
Extended JSON with the current date to the backup directory. Then replaces the existing collection with
the provided annotation configuration.

```bash
./set-new-annotations-configuration.sh -f <annotation-config-collection-json-file-path> \
-c <mongo_connection_string> -d <docker_container_name> -m <mongo_database> -b backup-directory
```
