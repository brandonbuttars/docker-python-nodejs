import argparse
import json
import os
import re
from datetime import datetime
from io import BytesIO
from pathlib import Path

import docker
import docker.errors
import requests

DOCKER_IMAGE_NAME = "brandonbuttars/python-nodejs"
VERSIONS_PATH = Path("versions.json")
LATEST_NAME = "buster"


def fetch_node_gpg_keys():
    url = "https://raw.githubusercontent.com/nodejs/docker-node/master/keys/node.keys"
    return requests.get(url).text.replace("\n", " ")


def render_dockerfile(version, node_gpg_keys):
    dockerfile_template = Path(f'template-{version["distro"]}.Dockerfile').read_text()
    replace_pattern = re.compile("%%(.+?)%%")

    replacements = {
        "npm_version": "8",
        "now": datetime.utcnow().isoformat()[:-7],
        "node_gpg_keys": node_gpg_keys,
        **version,
    }

    def repl(matchobj):
        key = matchobj.group(1).lower()
        return replacements[key]

    return replace_pattern.sub(repl, dockerfile_template)


def load_versions():
    with VERSIONS_PATH.open() as fp:
        return json.load(fp)["versions"]

def build_and_push(docker_client, version, node_gpg_keys, dry_run=False, debug=False, latest=False):
    dockerfile = render_dockerfile(version, node_gpg_keys)
    # docker build wants bytes
    with BytesIO(dockerfile.encode()) as fileobj:
        version_name = 'latest' if latest else version['key']
        tag = f"{DOCKER_IMAGE_NAME}:{version_name}"

        nodejs_version = version["nodejs_canonical"]
        python_version = version["python_canonical"]
        print(
            f"Building image {version['key']} python: {python_version} nodejs: {nodejs_version} ...",
            end="",
            flush=True,
        )
        if not dry_run:
            docker_client.images.build(fileobj=fileobj, tag=tag, rm=True, pull=True)
        if debug:
            with Path(f"debug-{version_name}.Dockerfile").open("w") as debug_file:
                debug_file.write(fileobj.read().decode("utf-8"))
        print(f" pushing...", flush=True)
        if not dry_run:
            docker_client.images.push(DOCKER_IMAGE_NAME, version_name)


def build_or_update(versions, dry_run=False, debug=False):
    # Login to docker hub
    docker_client = docker.from_env()
    dockerhub_username = os.getenv("DOCKERHUB_USERNAME")
    try:
        docker_client.login(dockerhub_username, os.getenv("DOCKERHUB_PASSWORD"))
    except docker.errors.APIError:
        print(f"Could not login to docker hub with username:'{dockerhub_username}'.")
        print("Is env var DOCKERHUB_USERNAME and DOCKERHUB_PASSWORD set correctly?")
        exit(1)

    node_gpg_keys = fetch_node_gpg_keys()
    # Build, tag and push images
    for version in versions:
        build_and_push(docker_client, version, node_gpg_keys, dry_run, debug)
        # If key equals the latest then build the latest tag
        if version['key'] == LATEST_NAME:
            build_and_push(docker_client, version, node_gpg_keys, dry_run, debug, True)


def main(dry_run, debug):
    # Get version data from json file
    versions = load_versions()

    # Build tag and release docker images
    build_or_update(versions, dry_run, debug)

    # FIXME(perf): Generate a CircleCI config file with a workflow (parallel) and trigger this workflow via the API.
    # Ref: https://circleci.com/docs/2.0/api-job-trigger/
    # Ref: https://discuss.circleci.com/t/run-builds-on-circleci-using-a-local-config-file/17355?source_topic_id=19287


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="🐳 Build Python with Node.js docker images")
    parser.add_argument(
        "--dry-run", action="store_true", dest="dry_run", help="Skip persisting, README update, and pushing of builds"
    )
    parser.add_argument("--debug", action="store_true", help="Write generated dockerfiles to disk")
    args = vars(parser.parse_args())
    main(**args)
