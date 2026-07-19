\#!/bin/bash

\# Wazuh Active Response: contain-ssh-persistence.sh

\# Triggered by rule 100012 (unauthorized authorized\_keys write)



LOG\_FILE="/var/ossec/logs/active-responses.log"



\# Read the JSON alert data Wazuh sends via stdin

read INPUT\_JSON



\# Extract the attacker's source IP and affected agent/user info

ATTACKER\_IP=$(echo "$INPUT\_JSON" | jq -r '.parameters.alert.data.srcip // "unknown"')



echo "$(date '+%Y-%m-%d %H:%M:%S') contain-ssh-persistence.sh triggered - attacker IP: $ATTACKER\_IP" >> $LOG\_FILE



\# --- Action 1: Backup and clear authorized\_keys for all local users ---

for USER\_HOME in /home/\*; do

&#x20; AUTH\_KEYS="$USER\_HOME/.ssh/authorized\_keys"

&#x20; if \[ -f "$AUTH\_KEYS" ]; then

&#x20;   BACKUP\_FILE="${AUTH\_KEYS}.bak.$(date +%s)"

&#x20;   cp "$AUTH\_KEYS" "$BACKUP\_FILE"

&#x20;   echo "$(date '+%Y-%m-%d %H:%M:%S') Backed up $AUTH\_KEYS to $BACKUP\_FILE" >> $LOG\_FILE



&#x20;   > "$AUTH\_KEYS"

&#x20;   echo "$(date '+%Y-%m-%d %H:%M:%S') Cleared $AUTH\_KEYS" >> $LOG\_FILE

&#x20; fi

done



\# Also check root, since attackers sometimes target it directly

ROOT\_AUTH\_KEYS="/root/.ssh/authorized\_keys"

if \[ -f "$ROOT\_AUTH\_KEYS" ]; then

&#x20; BACKUP\_FILE="${ROOT\_AUTH\_KEYS}.bak.$(date +%s)"

&#x20; cp "$ROOT\_AUTH\_KEYS" "$BACKUP\_FILE"

&#x20; echo "$(date '+%Y-%m-%d %H:%M:%S') Backed up $ROOT\_AUTH\_KEYS to $BACKUP\_FILE" >> $LOG\_FILE



&#x20; > "$ROOT\_AUTH\_KEYS"

&#x20; echo "$(date '+%Y-%m-%d %H:%M:%S') Cleared $ROOT\_AUTH\_KEYS" >> $LOG\_FILE

fi

