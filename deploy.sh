#!/bin/bash
# This shell script deploys a new version to a server.

export PA_USER="zhangdzh"

if [ -z "$PA_PWD" ]
then
    echo "The PythonAnywhere password var (PA_PWD) must be set in the env."
    exit 1
fi

echo "SSHing to PythonAnywhere."
sshpass -p $PA_PWD ssh -o "StrictHostKeyChecking no" $PA_USER@ssh.pythonanywhere.com << EOF
    ./rebuild.sh
EOF