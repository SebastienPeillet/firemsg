#!/usr/bin/sh

export PPP_CONFIG_DIR=/home/user/.local/lib/python2.7/site-packages/mpop-v1.2.1-py2.7.egg/mpop
export XRIT_DECOMPRESS_PATH=/bin
export XRIT_DECOMPRESS_OUTDIR=/home/user/firemsg/Auto/decompressed/etc
python composition_mpop.py

exit 0