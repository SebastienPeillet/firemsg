#!/usr/bin/sh
###################################################################################
# fire_detect.sh script
# 
# Author : Sebastien Peillet
# Project : TAIMPO, UMR Espace Dev
#
# Description : 
# This script is a part of the fire detection processing with MSG data. It could be used with the firemsg.sh 
# script or independantly, but don't forget to define the MSG_DATA_PATH environment variable before launching
# script. Example : 'export MSG_DATA_PATH=2016/05/15/1145' 
# The script will launch fire detect.py and create several files like brigthness temperature images, potential fire image and true fire image.
#
# Thanks to Pytroll team and to OSGEO tools
###################################################################################

export PPP_CONFIG_DIR=/home/user/.local/lib/python2.7/site-packages/mpop
export XRIT_DECOMPRESS_PATH=/bin
export XRIT_DECOMPRESS_OUTDIR=/home/user/firemsg/Auto/decompressed/etc
python fire_detect.py

exit 0