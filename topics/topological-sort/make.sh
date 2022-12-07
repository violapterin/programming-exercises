#! /usr/bin/env bash

TITLE=topological-sort
DEBUG=${TITLE}-debug
rm -f "${TITLE}" "${DEBUG}"
gcc -o "${TITLE}" "${TITLE}".c
gcc -g -o "${DEBUG}" "${TITLE}".c
