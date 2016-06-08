#!/usr/bin/sh
###################################################################################
# decompress.sh script
# 
# Author : Sebastien Peillet
# Project : TAIMPO, UMR Espace Dev
#
# Description : 
# This script is a part of the fire detection processing with MSG data. It could be 
# used with the firemsg.sh script or independantly.
# The script will decompress all LRIT data in the compressed folder.
###################################################################################

source config_firemsg.cfg

cd $FIREMSG_PATH/Auto/compressed

#Loop to decompress LRIT data and create decompressed path, save the compressed file into archive folder
for i in $FIREMSG_PATH/Auto/compressed/L*C_
	do
    cd $FIREMSG_PATH/Auto/compressed
	temp=$(basename $i)
	echo "Conversion de : $i"
	xRITDecompress $i
	YYYY=${temp:46:4}
	MM=${temp:50:2}
	DD=${temp:52:2}
    HHMM=${temp:54:4}
	mkdir -p $FIREMSG_PATH/Auto/decompressed/$YYYY/$MM/$DD/$HHMM
    mv $i $FIREMSG_PATH/Auto/archive
done

#Loop to move LRIT uncompressed data to decompressed path
for j in $FIREMSG_PATH/Auto/compressed/L*__
	do
	cd $FIREMSG_PATH/Auto/compressed
	cp $j $FIREMSG_PATH/Auto/archive
    temp=$(basename $j)
	outYYYY=${temp:46:4}
	outMM=${temp:50:2}
	outDD=${temp:52:2}
    outHHMM=${temp:54:4}
	mv $j $FIREMSG_PATH/Auto/decompressed/$outYYYY/$outMM/$outDD/$outHHMM
done

exit 0