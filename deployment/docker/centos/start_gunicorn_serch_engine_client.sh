#!/bin/sh
NAME="omero_search_client"
USER=root
PYTHONPATH=~/.pyenv/versions/searchengineclient/bin/
APPPATH=/searchengineclient
SOCKFILE=/etc/searchengineclient/sock4 #change this to project_dir/sock (new file will be created)
echo "Starting $NAME as `whoami`"
export PATH="$PYTHONPATH:$PATH"
export PATH="$APPPATH:$PATH"
echo "staring the app" 
# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
echo "$RUNDIR"
test -d $RUNDIR || mkdir -p $RUNDIR
LOGS=/etc/searchengineclient/logs
LOGSDIR=$(dirname $LOGS)
test -d $LOGSDIR || mkdir -p $LOGSDIR
user=$USER
echo "Start Gunicorn ...."
#exec ls -l  ~/.pyenv/versions/searchengine/bin/ 
echo "$HOME"
echo pwd
cd $APPPATH
#exec gunicorn "omero_search_client:create_app('production')" -b 0.0.0.0:5577 --timeout 60 --name "$NAME"   --bind=unix:$SOCKFILE  --log-file=$LOGSDIR/logs/client_gunilog.log --access-logfile=$LOGSDIR/logs/client_access.log -error#-logfile=$LOGSDIR/logs/engine_logs/client_error.log  --workers 2

exec gunicorn "omero_search_client:create_app('production')" -b 0.0.0.0:5567 --timeout 60 --name $NAME --user=$USER --bind=unix:$SOCKFILE --log-file=$LOGSDIR/logs/client_gunilog.log --access-logfile=$LOGSDIR/logs/client_access.log -error-logfile=$LOGSDIR/logs/client_error.log --workers 2

