FROM linuxserver/sonarr

# MOFIFY DATA PATH
RUN sed -i "s|config|data|g" /var/run/s6/services/sonarr/run

VOLUME [ "/data" ]



