#!/bin/sh

# Updates the /etc/hosts with a new record to redirect a Domain Name System (DNS)
# lookup to allow custom addresses such as 'local.rosalution.cgds' & 'local.delphi.cgds'
# for local development so that is more fluent between applications.

# ./etc-hosts.sh
# ./etc-hosts.sh <dns-hostname-to-spoof>

HOSTNAME=$1
echo "checking for DNS spoofing $HOSTNAME entry in host file ... "
if ! grep "$HOSTNAME" /etc/hosts; then
  echo "Adding $HOSTNAME to your /etc/hosts";
  printf "%s\t%s\n" "127.0.0.1" "$HOSTNAME" | sudo tee -a /etc/hosts > /dev/null;
else
  echo "Entry already present"
fi
