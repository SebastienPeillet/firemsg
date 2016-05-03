#!/usr/bin/sh

export PPP_CONFIG_DIR=/home/user/.local/lib/python2.7/site-packages/mpop
export XRIT_DECOMPRESS_PATH=/bin
export XRIT_DECOMPRESS_OUTDIR=/home/user/firemsg/Auto/decompressed/etc
python potfire.py
YYYY=${MSG_DATA_PATH:0:4}
MM=${MSG_DATA_PATH:5:2}
DD=${MSG_DATA_PATH:8:2}
HHMM=${MSG_DATA_PATH:11:4}
python gdalcopyproj.py /home/user/firemsg/Auto/img_RA/$MSG_DATA_PATH/LRIT-MSG3-RA-$YYYY$MM$DD-$HHMM-039.tiff /home/user/firemsg/Auto/img_PF/$MSG_DATA_PATH/LRIT-MSG3-PF-$YYYY$MM$DD-$HHMM.tiff 

exit 0
