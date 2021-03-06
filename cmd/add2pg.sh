#!/usr/bin/bash
###################################################################################
# add2pg.sh script
# 
# Author : Sebastien Peillet
# Project : TAIMPO, UMR Espace Dev
#
# Description : 
# This script is a part of the fire detection processing with MSG data. It could be used with the firemsg.sh 
# script or independantly, but don't forget to define the MSG_DATA_PATH environment variable before launching
# script. Example : 'export MSG_DATA_PATH=2016/05/15/1145'
# The script will add all vector feature into postgresql database.
#
###################################################################################
source config_firemsg.cfg &>/dev/null
export FIREMSG_PATH
export MSG_FILE_TYPE
export ENABLE_POSTGRES
export PG_DBNAME
export PG_HOST
export PG_TABLENAME
export PG_USER
export PG_PW

python add2pg.py