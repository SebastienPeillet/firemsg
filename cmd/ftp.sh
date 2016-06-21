#!/usr/bin/sh
###################################################################################
# ftp.sh script
# 
# Author : Sebastien Peillet
# Project : TAIMPO, UMR Espace Dev
#
# Description : 
# This script is a part of the fire detection processing with MSG data. It could be 
# used with the firemsg.sh script or independantly.
# The script will download the last available data on the Eumetsat FTP.
###################################################################################
source config_firemsg.cfg

cd $FIREMSG_PATH/Auto/compressed

#Connexion variables
hostname=$FTP_host
name=$FTP_name
password=$FTP_pw

#First FTP connexion to get files list
ftp -i -n $hostname <<EOF
quote USER $name
quote PASS $password
cd lrit3h
mls L* list.txt
quit
EOF

#Loop to determine the last available data
a=$(wc -l list.txt)
a=${a:0:3}
time_slot=0
for i in $(seq 1 $a)
	do 
	temp=$(sed -n $i'p' list.txt)
	temp=${temp:46:12}
	if (("$temp" > "$time_slot"))
		then time_slot=$temp
	fi
done
echo $time_slot

#Second connexion to download the files that go with times_slot
ftp -i -n $hostname <<EOF
quote USER $name
quote PASS $password
binary
cd lrit3h
mget *$time_slot*
quit
EOF

exit 0