FROM linuxserver/sonarr:preview

# MOFIFY DATA PATH
RUN sed -i "s|config|data|g" /etc/services.d/sonarr/run

VOLUME [ "/data" ]
