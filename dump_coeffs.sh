#!/bin/bash -e

if [ $# != 1 ]; then
	echo "Usage: $0 <nid>" >&2
	exit 2
fi

nid=$1
a=0
b=$(hda-verb /dev/snd/hwC0D0 $nid PARAMETERS PROC_CAP 2>/dev/null | \
	awk '$1 == "value" {printf "0x%s\n", substr($3, 3, 2)}')

hda-verb /dev/snd/hwC0D0 $nid SET_COEF_INDEX $a &>/dev/null
for i in $(seq $a $((b - 1))); do
	printf "0x%02x " $i
	# Auto-advances after each read
	hda-verb /dev/snd/hwC0D0 $nid GET_PROC_COEF 0 2>/dev/null | \
		awk '$1 == "value" {print $3}'
done
