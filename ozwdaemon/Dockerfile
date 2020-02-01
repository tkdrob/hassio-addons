FROM openzwave/ozwdaemon:latest

# Install additional requirements:
#    mosquitto for the mqtt bridge
#    x11vnc and alike for ozw-admin
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        mosquitto curl jq \
        bash \
        net-tools \
        novnc \
        supervisor \
        x11vnc \
        xvfb \
        nginx

# Download OZW-Admin Control panel
RUN curl -o /tmp/ozwadmin http://bamboo.my-ho.st/bamboo/browse/OZW-OZW0-26/artifact/JOB1/Linux---AppImage/OZWAdmin-0.1-x86_64.AppImage && \
    chmod a+x /tmp/ozwadmin && \
    cp /usr/share/novnc/vnc_auto.html /usr/share/novnc/index.html

# Copy data
COPY run.sh /
COPY mosquitto.conf /etc/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ozw-admin.conf /root/.config/OpenZWave/ozw-admin.conf
COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /data/

# Setup environment variables for the VNC connection
ENV HOME=/data \
    XDG_RUNTIME_DIR=/data \
    DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_ALL=C.UTF-8 \
    DISPLAY=:0.0 \
    DISPLAY_WIDTH=1024 \
    DISPLAY_HEIGHT=800

ENTRYPOINT [ "/run.sh" ]

EXPOSE 8080