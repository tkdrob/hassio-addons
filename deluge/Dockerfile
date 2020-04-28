FROM linuxserver/deluge:latest

# MOFIFY DATA PATH
RUN sed -i "s|config|data|g" /etc/services.d/deluge/run

VOLUME [ "/data" ]
