#! /usr/bin/env sh
set -e

if [ -f /${PROJECT_NAME:-app}/app/main.py ]; then
    DEFAULT_MODULE_NAME=app.main
elif [ -f /app/main.py ]; then
    DEFAULT_MODULE_NAME=main
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}
CERT_KEY_FILE=/certs/${CERT_KEY_FILE:-example.com+4-key.pem}
CERT_FILE=/certs/${CERT_FILE:-example.com+4.pem}

if [ -f /app/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/app/gunicorn_conf.py
elif [ -f /${PROJECT_NAME}/app/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/${PROJECT_NAME}/app/gunicorn_conf.py
else
    DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
fi
export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=/app/prestart.sh
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ]; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else 
    echo "There is no script $PRE_START_PATH"
fi

# Start Gunicorn
if [ -f ${CERT_KEY_FILE} ] && [ -f ${CERT_FILE} ]; then
    exec gunicorn --keyfile=${CERT_KEY_FILE} --certfile=${CERT_FILE} -k uvicorn.workers.UvicornWorker -c "$GUNICORN_CONF" "$APP_MODULE"
else
    exec gunicorn -k uvicorn.workers.UvicornWorker -c "$GUNICORN_CONF" "$APP_MODULE"
fi
