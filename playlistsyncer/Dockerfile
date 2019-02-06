FROM python:3-alpine3.9

# install deps
RUN apk --no-cache add taglib-dev gcc g++ flac
RUN pip install --upgrade roonapi spotipy pytaglib simplejson requests spotipy

# copy files and crontab
COPY crontab /etc/crontabs/root
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY app /usr/src/app

VOLUME ["/data"]

# start crond with log level 8 in foreground, output to stderr
CMD ["crond", "-f", "-d", "8"]