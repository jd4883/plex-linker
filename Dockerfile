FROM python:alpine3.7
MAINTAINER 'Jacob Dresdale'
LABEL name=plex_linker version=1.5
USER root
VOLUME /config /media
ENV app /config

ENV RADARR_API_KEY="${RADARR_API_KEY}"
ENV SONARR_API_KEY="${RADARR_API_KEY}"
ENV PLEX_API_KEY="${PLEX_API_KEY}"
ENV GIT_REPO="https://github.com/jd4883/plex-linker-beta.git"
ENV GIT_BRANCH="develop-docker-prototype"
ENV APPEND_ABSOLUTE_PATH=""
# append to all absolute paths, defaults as blank if not defined as an environment
WORKDIR ${app}
COPY . ${app}/
RUN apk add --no-cache bash git openssh &wait
RUN pip install --upgrade pip; pip install -r requirements.txt
RUN ["chmod", "+x", "link-tv-specials.py"]
CMD python ./link-tv-specials.py
