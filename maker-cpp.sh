#! /usr/bin/env bash

# # $1: absolute input folder
# # $2: absolute output folder
# # Copy input files to output files.
suffix_in="cpp"
suffix_out="o"
for path_in in $1/*; do
   if [ ! -f "${path_in}" ]
   then
      continue
   fi
   name="$(basename ${path_in})"
   bare="${name%.*}"
   extension="${name##*.}"
   if [ "${extension}" != "${suffix_in}" ]
   then
      continue
   fi
   path_out="$2/${bare}.${suffix_out}"
   if [ -f "${path_out}" ]
   then
      # # Compare time stamps.
      if [ "${path_out}" -nt "${path_in}" ]
      then
         continue
      fi
   fi
   set -x
   g++ -std=c++11 -g -o "${path_out}" "${path_in}"
   { set +x; } 2>/dev/null
done
