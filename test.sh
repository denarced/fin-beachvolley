#!/usr/bin/env bash

set -u


if [ -z "${VIRTUAL_ENV}" ] ; then
    echo "Venv not activated, quitting." >&2
    exit 1
fi

while : ; do
    clear
    date -Iseconds

    coverage run -m pytest -vv -x --ff
    coverage report
    coverage html
    inotifywait -e modify ./*.py
done
