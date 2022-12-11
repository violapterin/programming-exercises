#! /usr/bin/env bash

function run() {
   flag=$1
   echo "flag:$flag"
   for number in {0..7}; do
      echo " ~ ~ ~ ~ ~ ~ ~ ~ "
      echo "File ${number}:"
      echo " ~ ~ ~ ~ ~ ~ ~ ~ "
      rm -f "out-${number}.txt"
      ./"${TITLE}.o" "${flag}" "in-${number}.txt" "out-${number}.txt"
   done
}

# # # # # # # # # # # # # # # #

TITLE=topological-sort
DEBUG=${TITLE}-debug
rm -f "${TITLE}.o" "${DEBUG}.o"
gcc -o "${TITLE}.o" "${TITLE}".c
gcc -g -o "${DEBUG}.o" "${TITLE}".c

run 0
run 4
run 2
run 1
run 5
run 3
