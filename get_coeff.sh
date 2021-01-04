#!/bin/bash -e

if [ $# != 2 ]; then
	echo "Usage: $0 <nid> <coeff>" >&2
	exit 2
fi

nid=$1
coeff=$2

hda-verb /dev/snd/hwC0D0 $nid SET_COEF_INDEX $coeff &>/dev/null
hda-verb /dev/snd/hwC0D0 $nid GET_PROC_COEF 0 2>/dev/null | \
	awk '$1 == "value" {print $3}'
