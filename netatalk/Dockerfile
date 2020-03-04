ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# install packages
RUN apk add netatalk avahi

# copy files
COPY entrypoint.sh /entrypoint.sh
COPY afp.conf /etc/afp.conf

CMD ["/entrypoint.sh"]