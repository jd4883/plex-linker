FROM python:alpine3.7
COPY class_objects config_files IO jobs logs messaging movies string_manipulation link-tv-specials.py Dockerfile README.md requirements.txt /plex_linker/
WORKDIR /plex_linker
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# EXPOSE 5000
CMD python ./link-tv-specials.py
