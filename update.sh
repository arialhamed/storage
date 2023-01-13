#!/bin/bash

if [ $(find `pwd` -type f -size +100M ! -path '*/.git/*' | wc -l) -eq 0 ]; then
	dt=$(date '+%d-%b-%Y %H:%M:%S');
	echo "creating commit on \"$dt\""
	ms=""
	if [ -n "$1" ]; then
	   	ms=": $1"
	fi
	git fetch && git pull && git add . && git commit -m "$dt$ms" && git push
else
	find `pwd` -type f -size +100M ! -path '*/.git/*'
	echo "there are files larger than 100M, git cannot upload files that size and larger, fix it."
fi

notify-send "git operations are done"
