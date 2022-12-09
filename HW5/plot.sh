#!/bin/bash

#check for installation of parallel-rsync

if [ "$#" -lt 1 ] ; then
	echo "Data file not supplied."
	echo "Usage ./plot {data-file.txt}"
	exit
fi

gnuplot -e "filename='$1'" graph.gnuplot

if [ "$#" -lt 2 ] ; then
  open graph.png #xdg-open graph.png # if on Ubuntu
else
  echo "Creating graph at $2"
  mv graph.png $2
fi
