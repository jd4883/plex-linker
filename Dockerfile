FROM python:alpine3.7
MAINTAINER 'Jacob Dresdale'
LABEL name=plex_linker version=1.5
USER root
ENV RADARR_API_KEY="${RADARR_API_KEY}"
ENV SONARR_API_KEY="${RADARR_API_KEY}"
ENV PLEX_API_KEY="${PLEX_API_KEY}"
ENV GIT_REPO="https://github.com/jd4883/plex-linker-beta.git"
ENV GIT_BRANCH="develop-docker-prototype"
VOLUME /config /media /var/data/media/video
WORKDIR /config
RUN apk add --no-cache bash git openssh &wait
# cut clone temporarily in favor of copy as clone was not working
# recommended git clone approach online
# https://stackoverflow.com/questions/33682123/dockerfile-strategies-for-git
# or
# RUN cd ${app}/; git clone "https://github.com/jd4883/plex-linker-beta.git"
# or
COPY . /config/
# RUN cd /config; git clone ${GIT_REPO} &wait; echo 'git clone completed'
# git checkout "develop-docker-prototype"
RUN pip install --upgrade pip; pip install -r requirements.txt
RUN echo '*/15  *  *  *  *    /config/link-tv-specials.py' > /etc/crontabs/root; cat /etc/crontabs/root
RUN ls -hla /config
# RUN chmod 775 -R ${app}
RUN ["chmod", "+x", "/config/link-tv-specials.py"]
CMD python ./link-tv-specials.py



# this docker file works, need to figure out how to make output go to dockers log
# need to improve pathing and figure out how to publish the container, looking good for API testing though
