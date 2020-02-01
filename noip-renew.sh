#!/bin/bash

USERNAME=""
PASSWORD=""

LOGDIR=$1
PROGDIR=$(dirname $0)

if [ -z "$LOGDIR" ]; then
    echo Executing "$PROGDIR/noip-renew.py "$USERNAME" "$PASSWORD""
    $PROGDIR/noip-renew.py "$USERNAME" "$PASSWORD"
else
    cd $LOGDIR
    $PROGDIR/noip-renew.py "$USERNAME" "$PASSWORD" >> $USERNAME.log
fi
