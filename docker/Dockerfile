FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-alpine3.8

LABEL maintainer="George T. C. <george@innotech.me>" \
      description="This is an example to run fastapi as an API server."

#ARG CERT_KEY_FILE
#ARG CERT_FILE
#ARG HOST
#ARG PORT

# The environemt variables needed to configure the container.
ENV MODULE_NAME=${MODULE_NAME:-app.main} \
    VARIABLE_NAME=${VARIABLE_NAME:-app} \
    LOG_LEVEL=${LOG_LEVEL:-info} \
    WORKERS_PER_CORE=${WORKERS_PER_CORE:-2} \
    CERT_KEY_FILE=${CERT_KEY_FILE:-example.com+4-key.pem} \
    CERT_FILE=${CERT_FILE:-example.com+4.pem} \
    HOST=${HOST:-0.0.0.0} \
    PORT=443

COPY scripts/* /
COPY requirements.txt /
RUN chmod 755 /*.sh \
    && mkdir -p /app/app
RUN apk update && apk upgrade
RUN apk add --no-cache gcc python3-dev linux-headers musl-dev
RUN pip install --upgrade pip \
    && pip install -r /requirements.txt
VOLUME /app/app
VOLUME /certs
EXPOSE 443