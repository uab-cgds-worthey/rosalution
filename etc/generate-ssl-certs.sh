#!/bin/sh

# Uses mkcert to generate self-signed SSL/TLS certificates to allow Traefik to manage HTTPS
# connections for a local deployment for Rosalution. Automatically installs the generated certificate
# with the Chrome browser trust to let the browser know the certificate is valid and secure when
# accessing local.rosalutin.cgds/rosalution.

# Also creates the certificate directory path, default is ./etc/.certificates

# ./generate-ssl-certs.sh <hostname> <certificate path>
# ./generate-ssl-certs.sh local.rosalution.cgds ./etc/.certificates


HOSTNAME=$1
CERT_PATH=$2

mkdir -p "$CERT_PATH"

mkcert -cert-file "$CERT_PATH"/local-deployment-cert.pem -key-file "$CERT_PATH"/local-deployment-key.pem "$HOSTNAME"
mkcert -install
