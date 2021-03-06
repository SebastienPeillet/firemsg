#!/usr/bin/sh
###################################################################################
# firemsg.sh script
# 
# Author : Sebastien Peillet
# Project : TAIMPO, UMR Espace Dev
#
# Description : 
# This script will launch proccessing for the last available data. It can be used as
# a cronjob to get data every 3 hours.
###################################################################################


#PATH environment variable, needed for cronjob
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
source /home/pi/firemsg/cmd/config_firemsg.cfg &>/dev/null

export FIREMSG_PATH
export ENABLE_POSTGRES

#ftp.sh script downloads the last available data
cd $FIREMSG_PATH/cmd
bash ftp.sh


#MSG_DATA_PATH environment variable, needed to access and create all path during processing
cd $FIREMSG_PATH/Auto/compressed
time_slot=$(ls *EPI*)
YYYY=${time_slot:46:4}
MM=${time_slot:50:2}
DD=${time_slot:52:2}
HHMM=${time_slot:54:4}
export MSG_DATA_PATH=$YYYY/$MM/$DD/$HHMM


#decompress.sh script decompresses LRIT data
cd $FIREMSG_PATH/cmd
bash decompress.sh


#fire_detect.sh script uses LRIT data to create brightness temperature, potentiel fire and true fire images
bash fire_detect.sh
if [ $ENABLE_FIRE_DETECTION = true ]
then
#convert fire from raster to vector
bash raster2vector.sh

if [ $ENABLE_POSTGRES = true ]
then bash add2pg.sh
fi
fi

if [ $SAVE_INTERMEDIATE_FILES = false ]
then
rm $FIREMSG_PATH/Auto/archive/*
rm $FIREMSG_PATH/Auto/img_TF/$YYYY/$MM/$DD/$HHMM/*
rm $FIREMSG_PATH/Auto/img_PF/$YYYY/$MM/$DD/$HHMM/*
rm $FIREMSG_PATH/Auto/img_BT/$YYYY/$MM/$DD/$HHMM/*
fi

exit 0
