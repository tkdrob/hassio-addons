FROM openzwave/ozwdaemon:latest

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    mosquitto curl jq

# Copy data
COPY run.sh /
COPY mosquitto.conf /etc/

WORKDIR /data/

ENTRYPOINT [ "/run.sh" ]