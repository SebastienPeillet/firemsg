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
cd /home/user/firemsg/Auto/compressed

#Loop to decompress LRIT data and create decompressed path, save the compressed file into archive folder
for i in /home/user/firemsg/Auto/compressed/L*C_
	do
    cd /home/user/firemsg/Auto/compressed
	temp=$(echo $i)
	echo "Conversion de : $i"
	xRITDecompress $i
	YYYY=${temp:81:4}
	MM=${temp:85:2}
	DD=${temp:87:2}
    HHMM=${temp:89:4}
	mkdir -p /home/user/firemsg/Auto/decompressed/$YYYY/$MM/$DD/$HHMM
    mv $i /home/user/firemsg/Auto/archive
done

#Loop to move LRIT uncompressed data to decompressed path
for j in /home/user/firemsg/Auto/compressed/L*__
	do
	cd /home/user/firemsg/Auto/compressed
	cp $j /home/user/firemsg/Auto/archive
    tempo=$(echo $j)
	outYYYY=${tempo:81:4}
	outMM=${tempo:85:2}
	outDD=${tempo:87:2}
    outHHMM=${tempo:89:4}
	mv $j /home/user/firemsg/Auto/decompressed/$outYYYY/$outMM/$outDD/$outHHMM
done

exit 0