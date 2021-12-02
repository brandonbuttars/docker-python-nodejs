[![Pulls](https://img.shields.io/docker/pulls/brandonbuttars/python-nodejs.svg?style=flat-square)](https://hub.docker.com/r/brandonbuttars/python-nodejs/)
[![CircleCI](https://img.shields.io/circleci/project/github/brandonbuttars/docker-python-nodejs.svg?style=flat-square)](https://circleci.com/gh/brandonbuttars/docker-python-nodejs)

Last updated by Brandon Buttars: 2021-12-02

## 🐳 Python with Node.js

#### FORKED FROM nikolaik/docker-python-nodejs

These images are build from `brandonbuttars/docker-python-nodejs` based on `nikolaik/docker-python-nodejs`. I use strict node versions and was using this in some pipelines and the updates broke my pipelines so I forked the project and took out all the automation so I could manage the versions I was interested in and prevent any future fragility.

If you're OK using the latest, use [https://hub.docker.com/r/nikolaik/python-nodejs](https://hub.docker.com/r/nikolaik/python-nodejs) and there a ton of different tags and versions you can choose from. I just needed to customize and thin out that list a bit and make sure I kept stability in my pipelines.

The `latest` tag is currently:

- Node: 16.13.0
- npm: 8.x
- yarn: latest
- Python: 3.7.12
- pip: latest
- pipenv: latest
- poetry: latest

## 🏷 Tags

To use a specific combination of Python and Node.js see the following table of available image tags.

## Typical tasks

```bash
# Pull from Docker Hub
docker pull brandonbuttars/python-nodejs:latest
# Build from GitHub
docker build -t brandonbuttars/python-nodejs github.com/brandonbuttars/docker-python-nodejs
# Run image
docker run -it brandonbuttars/python-nodejs bash
```

| Tag      | Python | Node.js | Distro |
| -------- | ------ | ------- | ------ |
| `buster` | 3.7.12 | 16.13.0 | buster |
| `slim`   | 3.7.12 | 16.13.0 | slim   |
| `alpine` | 3.7.12 | 16.13.0 | alpine |

### Use as base image

```Dockerfile
FROM brandonbuttars/python-nodejs:latest

USER pn
WORKDIR /home/pn/app
```

All images have a default user `pn` with uid 1000 and gid 1000.

## Disclaimer

_This is experimental and might break from time to time. Use at your own risk!_
