#! /usr/bin/env bash

update() {
   # # $1: absolute input folder
   # # $2: absolute output folder
   # # Copy input files to output files.
   suffix_in=.cpp
   suffix_out=.o
   for path_in in $1/*; do
      if [ ! -f $path_in ]; then
         continue
      fi
      if  [[ $path_in != *${suffix_in} ]] ; then
         continue
      fi
      name="${path_in##*/}"
      bare="${name%$suffix_in}"
      path_out="$2/$bare$suffix_out"
      if [ -f $path_out ]; then
         # # Compare time stamps.
         if [ $path_out -nt $path_in ]; then
            continue
         fi
      fi
      set -x
      g++ -std=c++11 -g -o $path_out $path_in
      set +x
   done

   # # Delete output files matching no input file.
   for path_out in $2/*; do
      if [ ! -f $path_out ]; then
         continue
      fi
      if  [[ $path_out != *${suffix_out} ]] ; then
         continue
      fi
      name="${path_out##*/}"
      bare="${name%$suffix_out}"
      path_in="$1/$bare$suffix_in"
      if [ ! -f $path_in ]; then
         set -x
         rm $path_out
         set +x
      fi
   done
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

THIS=`dirname "$0"`
update "$THIS" "$THIS"
