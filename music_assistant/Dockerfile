FROM python:slim

ARG MASS_VERSION=0.0.21
ARG JEMALLOC_VERSION=5.2.1
ARG S6_OVERLAY_VERSION=1.22.1.0
ARG S6_OVERLAY_ARCH=amd64
ARG BASHIO_VERSION=0.9.0

RUN apt-get update && apt-get install -y --no-install-recommends \
		# required packages
		flac sox libsox-fmt-mp3 zip curl unzip ffmpeg libsndfile1 libtag1v5 \
		# build packages
		libtag1-dev build-essential git && \
    # make sure aiohttp is installed with recommended packages
    pip install aiohttp[speedups] && \
	# install musicassistant - TODO: use pypi package once we're stable
	curl -L -s https://github.com/marcelveldt/musicassistant/archive/${MASS_VERSION}.tar.gz | tar -xzf - -C /tmp && \
    cd /tmp/musicassistant-${MASS_VERSION} && \
    python3 setup.py install && \
    rm -rf /tmp/musicassistant-${MASS_VERSION} && \
    # Setup jemalloc
    curl -L -s https://github.com/jemalloc/jemalloc/releases/download/${JEMALLOC_VERSION}/jemalloc-${JEMALLOC_VERSION}.tar.bz2 | tar -xjf - -C /usr/src && \
    cd /usr/src/jemalloc-${JEMALLOC_VERSION} && \
    ./configure && \
    make && \
    make install && \
    rm -rf /usr/src/jemalloc-${JEMALLOC_VERSION} && \
    # Setup s6 overlay
    curl -L -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-${S6_OVERLAY_ARCH}.tar.gz" | tar zxvf - -C / && \
    mkdir -p /etc/fix-attrs.d && \
    mkdir -p /etc/services.d && \
    # Setup bashio
    mkdir -p /tmp/bashio && \
    curl -L -s https://github.com/hassio-addons/bashio/archive/v${BASHIO_VERSION}.tar.gz | tar -xzf - --strip 1 -C /tmp/bashio && \
    mv /tmp/bashio/lib /usr/lib/bashio && \
    ln -s /usr/lib/bashio/bashio /usr/bin/bashio && \
    rm -rf /tmp/bashio && \
	# cleanup build packages
	apt-get purge -y --auto-remove libtag1-dev build-essential && \
	rm -rf /var/lib/apt/lists/*

# copy rootfs
COPY rootfs /

ENTRYPOINT ["/init"]