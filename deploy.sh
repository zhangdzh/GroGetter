#!/bin/bash
# This shell script deploys a new version to a server.

export PA_USER=GROC

if [ -z "$DEMO_PA_PWD" ]
then
    echo "The PythonAnywhere password var (PA_PWD) must be set in the env."
    exit 1
fi

echo "SSHing to PythonAnywhere."
sshpass -p $DEMO_PA_PWD ssh -o "StrictHostKeyChecking no" $PA_USER@ssh.pythonanywhere.com << EOF
    cd GroGetter; ./rebuild.sh
EOF