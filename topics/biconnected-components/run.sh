#! /usr/bin/env bash

clear
for file_in in ./input/*.txt; do
   echo "testing ${file_in}:"
   file_out="./output/$(basename ${file_in})"
   file_out="${file_out/in/out}"  
   rm -f "${file_out}"
   python3 ./main.py ${file_in} > ${file_out}
done