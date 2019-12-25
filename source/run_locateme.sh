#!/bin/sh

INSTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $INSTDIR
SOURCEDIR="$(dirname "$INSTDIR")"
echo $SOURCEDIR

cd $SOURCEDIR
source LocateMeEnv/bin/activate
cd $INSTDIR
start()
{
python3 manage.py runserver 0.0.0.0:9000
}
start
