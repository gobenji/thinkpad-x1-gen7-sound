#!/bin/bash -e

if [ $# != 3 ]; then
	echo "Usage: $0 <nid> <coeff> <value>" >&2
	exit 2
fi

nid=$1
coeff=$2
value=$3

hda-verb /dev/snd/hwC0D0 $nid SET_COEF_INDEX $coeff &>/dev/null
hda-verb /dev/snd/hwC0D0 $nid SET_PROC_COEF $value &>/dev/null
