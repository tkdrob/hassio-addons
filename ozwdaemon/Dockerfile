FROM openzwave/ozwdaemon:latest

# Install additional requirements:
#    mosquitto for the mqtt bridge
#    x11vnc and alike for ozw-admin
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl jq \
        bash \
        supervisor

# Copy data
COPY run.sh /
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /data/

ENTRYPOINT [ "/run.sh" ]