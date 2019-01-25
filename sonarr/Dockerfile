ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Install requirements for add-on
RUN apk add --no-cache jq curl mono mediainfo zip sqlite3

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

ENV PACKAGE_URL https://services.sonarr.tv/v1/download/phantom-develop/latest?version=3&os=linux


MKDIR /opt
RUN curl -sSL https://services.sonarr.tv/v1/download/phantom-develop/latest?version=3&os=linux | tar -C /opt -xzv --strip-components=1 

VOLUME [ "/data" ]
EXPOSE 8989

ADD run.sh /
RUN chmod a+x /run.sh
ENTRYPOINT /run.sh



