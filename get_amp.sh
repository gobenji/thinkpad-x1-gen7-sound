#!/bin/bash -e

if [ $# != 1 ]; then
	echo "Usage: $0 <nid>" >&2
	exit 2
fi

nid=$1

gain () {
	local param=$1

	local value=$(hda-verb /dev/snd/hwC0D0 $nid GET_AMP_GAIN_MUTE \
		$param 2>/dev/null | \
		awk '$1 == "value" {print $3}')
	echo "$((value))"
}

# AC_AMP_GET_{LEFT,RIGHT} | AC_AMP_GET_OUTPUT
echo "$(gain 0xa000), $(gain 0x8000)"
