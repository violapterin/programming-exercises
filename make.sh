#! /usr/bin/env bash

update() {
   # # $1: input absolute folder
   # # $2: output absolute folder
   # # copy input files to output files
	suffix_in=.cpp
	suffix_out=.o
   for path_in in $1/*; do
      if [ ! -f $path_in ]; then
         continue
      fi
      name="${path_in##*/}"
      path_out="$2/$name$suffix_in"
      if [ -f $path_out ]; then
         if [ $path_out -nt $path_in ]; then
            continue
         fi
      fi
		set -x
		echo g++ -std=c++11 -g -o $path_out $path_in
		set +x
   done

   # # delete output files matching no input file
   for path_out in $2/*; do
      if [ ! -f $path_out ]; then
         continue
      fi
      name="${path_out##*/}"
      path_in="$1/$name$suffix_out"
      if [ ! -f $path_in ]; then
			set -x
         echo rm $path_out
			set +x
      fi
   done
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

THIS=`dirname "$0"`
update "$THIS" "$THIS"
