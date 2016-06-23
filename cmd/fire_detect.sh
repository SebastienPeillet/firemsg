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
source config_firemsg.cfg &>/dev/null

#Main_config
export FIREMSG_PATH
#Threshold args
export T039
export T108
export ENABLE_FIRE_DETECTION
export delta_day
export delta_night
export day_start
export day_end
export window_width
export potfire_nb_limit
export level_requirement


export PPP_CONFIG_DIR
export XRIT_DECOMPRESS_PATH=/bin
export XRIT_DECOMPRESS_OUTDIR=$FIREMSG_PATH/Auto/decompressed/etc
python fire_detect.py

exit 0