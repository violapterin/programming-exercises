#! /usr/bin/env bash

TITLE=topological-sort
DEBUG=${TITLE}-debug
rm -f "${TITLE}.o" "${DEBUG}.o"
gcc -o "${TITLE}.o" "${TITLE}".c
gcc -g -o "${DEBUG}.o" "${TITLE}".c

flag=0
for number in {1..7}; do
   echo " ~ ~ ~ ~ ~ ~ ~ ~ "
   echo "File ${number}:"
   echo " ~ ~ ~ ~ ~ ~ ~ ~ "
   ./"${TITLE}.o" "${flag}" "in-${number}.txt" "out-${number}.txt"
done
