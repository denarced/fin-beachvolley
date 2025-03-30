#!/usr/bin/env bash

set -u


while : ; do
    clear
    date -Iseconds

    uv run coverage run -m pytest -x --ff
    uv run coverage report
    uv run coverage html
    inotifywait -e modify ./*.py
done
