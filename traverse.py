#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import subprocess


def get_coeff(nid, coeff_num):
    subprocess.run(
        [
            "hda-verb", "/dev/snd/hwC0D0",
            str(nid), "SET_COEF_INDEX",
            str(coeff_num)
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    retval = subprocess.run(
        ["hda-verb", "/dev/snd/hwC0D0",
         str(nid), "GET_PROC_COEF", "0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    return int(retval.stdout.split()[2], 0)


def set_coeff(nid, coeff_num, value):
    subprocess.run(
        [
            "hda-verb", "/dev/snd/hwC0D0",
            str(nid), "SET_COEF_INDEX",
            str(coeff_num)
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    subprocess.run(
        ["hda-verb", "/dev/snd/hwC0D0",
         str(nid), "SET_PROC_COEF",
         str(value)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )


parser = argparse.ArgumentParser(
    description="Fuzz coefficients",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-c", "--coeff",
    type=lambda x: int(x, 0),
    help="single coeff to operate on bit by bit",
)
parser.add_argument(
    "start",
    type=lambda x: int(x, 0),
    nargs="?",
    default=0,
    help="index of first coeff to fuzz",
)
args = parser.parse_args()

nid = 0x20

if args.coeff:
        value_orig = get_coeff(nid, args.coeff)
        for bit_num in range(16):
            value_test = value_orig ^ 1 << bit_num
            print(f"coeff {args.coeff:#04x} orig {value_orig:#06x} test {value_test:#06x} bit {bit_num}")
            set_coeff(nid, args.coeff, value_test)
            input("press enter to continue")
            set_coeff(nid, args.coeff, value_orig)
else:
    retval = subprocess.run(
        ["hda-verb", "/dev/snd/hwC0D0",
         str(nid), "PARAMETERS", "PROC_CAP"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    coeff_nb = (int(retval.stdout.split()[2], 0) & 0xff00) >> 8

    for coeff_num in range(args.start, coeff_nb):
        value_orig = get_coeff(nid, coeff_num)
        value_test = 0xffff ^ value_orig
        print(f"coeff {coeff_num:#04x} orig {value_orig:#06x} test {value_test:#06x}")
        set_coeff(nid, coeff_num, value_test)
        input("press enter to continue")
        set_coeff(nid, coeff_num, value_orig)
