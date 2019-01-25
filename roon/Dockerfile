FROM ubuntu
MAINTAINER m.vanderveldt@outlook.com

RUN apt-get update \
        && apt-get -y install curl bzip2 ffmpeg cifs-utils alsa-utils

ENV ROON_SERVER_PKG RoonServer_linuxx64.tar.bz2
ENV ROON_SERVER_URL http://download.roonlabs.com/builds/${ROON_SERVER_PKG}
ENV ROON_DATAROOT /data
ENV ROON_ID_DIR /data

VOLUME [ "/app", "/data" ]

ADD run.sh /
ENTRYPOINT /run.sh

