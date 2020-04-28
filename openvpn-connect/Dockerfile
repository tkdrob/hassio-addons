FROM dperson/openvpn-client:latest

# MOFIFY DATA PATH
RUN sed -i "s|config|data|g" /etc/services.d/openvpn-connect/run

VOLUME [ "/data" ]
