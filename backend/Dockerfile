#./train-departure-viewer/backend/Dockerfile
FROM python:3.8.9-buster as base

LABEL maintainer="info@fabiocionini.it"
LABEL vendor="fabiocionini"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv

RUN apt-get update && apt-get install -y --no-install-recommends gcc nginx vim
#wget netcat-traditional
#RUN apt-get -q update && apt-get -qy install netcat

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

COPY . /opt/app/backend/

# set work directory
WORKDIR /opt/app/backend
