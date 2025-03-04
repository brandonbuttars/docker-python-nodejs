# Generated %%NOW%%
# python: %%PYTHON_CANONICAL%%
# nodejs: %%NODEJS_CANONICAL%%
FROM python:%%PYTHON_IMAGE%%
MAINTAINER Brandon Buttars <brandonbuttars@gmail.com>

RUN groupadd --gid 1000 pn && useradd --uid 1000 --gid pn --shell /bin/bash --create-home pn
ENV POETRY_HOME=/usr/local
# Install node prereqs, nodejs and yarn
# Ref: https://deb.nodesource.com/setup_%%NODEJS%%.x
# Ref: https://yarnpkg.com/en/docs/install
RUN \
  apt-get update && apt-get install wget gnupg2 -y && \
  echo "deb https://deb.nodesource.com/node_%%NODEJS%%.x buster main" > /etc/apt/sources.list.d/nodesource.list && \
  wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
  echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
  wget -qO- https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
  apt-get update && \
  apt-get install -yqq nodejs=$(apt-cache show nodejs|grep Version|grep nodesource|cut -c 10-) yarn && \
  apt-mark hold nodejs && \
  pip install -U pip && pip install pipenv && \
  npm i -g npm@^%%NPM_VERSION%% && \
  npm cache clean -f && \
  npm i -g n && \
  n %%NODEJS_CANONICAL%% && \
  wget -q -O - https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - && \
  rm -rf /var/lib/apt/lists/*
