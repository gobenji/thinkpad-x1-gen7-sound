#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

if len(sys.argv) != 2:
    if len(sys.argv) < 1:
        name = "(unknown)"
    else:
        name = sys.argv[0]
    print("Usage: %s <value>" % (name,), file=sys.stderr)
    sys.exit(2)

value = int(sys.argv[1], 0)
print(f"{value:#04x}")

field = (value & 0x0060) >> 5
print(f"\tB {field:02b}  ", end="")
if field:
    print("expose headphone/line-in on 1Ah")
else:
    print("expose PC Beep on 1Ah")

field = (value & 0x1000) >> 12
print(f"\tL {field:>2b}  ", end="")
if field:
    print("       amplify 1Ah left")
else:
    print("do not amplify 1Ah left")

field = (value & 0x0010) >> 4
print(f"\tR {field:>2b}  ", end="")
if field:
    print("       amplify 1Ah right")
else:
    print("do not amplify 1Ah right")

field = (value & 0x4000) >> 14
print(f"\th {field:>2b}  ", end="")
if field:
    print("do not mix 1Ah into 21h")
else:
    print("       mix 1Ah into 21h")

field = (value & 0x2000) >> 13
print(f"\tS {field:>2b}  ", end="")
if field:
    print("       mix 1Ah into 14h")
else:
    print("do not mix 1Ah into 14h")
