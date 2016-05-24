#!/usr/bin/sh

###################################################################################
# raster2vector_resume.sh script
# 
# Author : Sebastien Peillet
# Project : TAIMPO, UMR Espace Dev
#
# Description : 
# This script is a part of the fire detection processing with MSG data. It could be used with the firemsg.sh 
# script or independantly, but don't forget to define the MSG_DATA_PATH environment variable before launching
# script. Example : 'export MSG_DATA_PATH=2016/05/15/1145'
# The script will polygonize raster fire data into point vector. Script built for "resume" raster.
#
# code inspired by the following page : https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html
###################################################################################

python raster2vector_resume.py

YYYY=${MSG_DATA_PATH:0:4}
MM=${MSG_DATA_PATH:5:2}
DD=${MSG_DATA_PATH:8:2}

input=/home/user/firemsg/Auto/vec_TF/$YYYY/$MM/$DD/LRIT-MSG3-vecTF-$YYYY$MM$DD-resume.shp
output=/home/user/firemsg/Auto/vec_TF/$YYYY/$MM/$DD/LRIT-MSG3-vecTF-$YYYY$MM$DD-resume-WGS84.shp

ogr2ogr $output $input -f "ESRI Shapefile" -s_srs "+proj=geos +lon_0=0 +h=35785831 +x_0=0 +y_0=0 +a=6378169 +b=6356583.8 +units=m +no_defs" -t_srs "+proj=longlat +datum=WGS84 +no_defs"

rm /home/user/firemsg/Auto/vec_TF/$YYYY/$MM/$DD/LRIT-MSG3-vecTF-$YYYY$MM$DD-resume.shp
rm /home/user/firemsg/Auto/vec_TF/$YYYY/$MM/$DD/LRIT-MSG3-vecTF-$YYYY$MM$DD-resume.dbf
rm /home/user/firemsg/Auto/vec_TF/$YYYY/$MM/$DD/LRIT-MSG3-vecTF-$YYYY$MM$DD-resume.shx