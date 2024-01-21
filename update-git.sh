#!/usr/bin/env bash
#
# This speeds up git for you sooo fast. Not only does this pull, create a commit, & push it, but this also checks for any file over 100M.
# The only limitation of this script (as of 2023 Oct 10) is that it cannot detect if the commit packet is more than 2GB.
# Works for Linux, may work for Windows & Mac

if [ $(find "`pwd`" -type f -size +100M ! -path '*/.git/*' | wc -l) -eq 0 ]; then
	dt=$(date '+%d-%b-%Y %H:%M:%S');
	echo "creating commit on \"$dt\""
	ms=""
	if [ -n "$1" ]; then
	   	ms=": $1"
	fi
	git pull && git add . && git commit -m "$dt$ms" && git push
else
	find `pwd` -type f -size +100M ! -path '*/.git/*'
	echo "there are files larger than 100M, git cannot upload files that size and larger, fix it."
fi

notify-send "git operations are done" "repo is in `pwd`"
