# Database Scripts

Streamlining the operations to backup and restore a rosalution_db database from a docker container.
These bash scripts are intended for documentation of how these operations are done and can be used
for reference for deployments elsewhere.

* backup-database.sh - Backs up a mongodb 'rosalution_db' with an archived dump from the target docker container  
`./backup-database.sh <docker-container> <output-path (optional)>`

* restore-database.sh - Executes a mongo restore of a mongodb 'rosalution_db' from an archived dump  
`./restore-database.sh <docker-container> <target-restore-database-archive>`

* ./deploy-development-prod-database.sh - Deploys the mongodb 'rosalution-db' service which attaches
to the existing 'rosalution-network-prod' docker network with a placement contrain of being on the
primary swarm node to mount the data directory for mongodb so that the data for mongodb may be persisted  
`./deploy-development-prod-database.sh`
