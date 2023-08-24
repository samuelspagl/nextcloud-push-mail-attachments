FROM python:3.11.4-alpine3.18

LABEL maintainer="samuel@spagl-media.de"
LABEL org.label-schema.name = "NextCloud sync mail attachments"
LABEL org.label-schema.description = "A Python based service to push mail attachements to a specified NextCloud folder."
LABEL org.label-schema.vendor = "Samuel Spagl"

RUN pip install --no-cache-dir --upgrade pip==22.3.1
RUN pip install --no-cache-dir pipenv
RUN pip install cache purge

COPY Pipfile /
COPY Pipfile.lock /

RUN pipenv install --system --deploy --ignore-pipfile

ARG user=1001
ARG group=1001
ENV APP_HOME=/home/${user}
WORKDIR ${APP_HOME}
RUN chown ${user}:${group} ${APP_HOME}
USER ${user}:${group}

COPY imap_box.py ${APP_HOME}/imap_box.py

CMD ["python", "imap_box.py"]