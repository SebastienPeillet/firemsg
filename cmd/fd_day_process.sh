#!/usr/bin/sh
###################################################################################
# fd_day_process.sh script
# 
# Author : Sebastien Peillet
# Project : TAIMPO, UMR Espace Dev
#
# Description : 
# The script will process the all the data for one day if available on the Eumetsat FTP (or in archive).
###################################################################################
source config_firemsg.cfg &>/dev/null

export FIREMSG_PATH
export ENABLE_POSTGRES
if [ $FTP_download = "true" ] 
	then
	download_day1=$(date --date=$dateDeb +'%Y%m%d')
	download_day2=$(date --date=$dateDeb'+1 days' +'%Y%m%d')
	#FTP download, change the mget argument (YYYYMMDD) to select the day you want
	cd $FIREMSG_PATH/Auto/compressed
	hostname=$FTP_host
	name=$FTP_name
	password=$FTP_pw
ftp -i -n $hostname <<EOF
quote USER $name
quote PASS $password
binary
cd lrit3h
mget *$download_day1*
mget *$download_day2*
quit 
EOF
fi

#Decompress all LRIT files
cd $FIREMSG_PATH/cmd
bash decompress.sh

script1=fire_detect.sh
script2=raster2vector.sh
script3=add2pg.sh

#Day variable to process
dateDeb=$dateDeb
dateFin=$dateFin

while [ "$dateDeb" != "$dateFin" ]; do
	date_slot=$(date --date=$dateDeb +'%Y/%m/%d')
	
	time=('0245' '0545' '0845' '1145' '1445' '1745' '2045' '2345')
	for time_slot in ${time[@]}; do
	#Process files for one day
		cd $FIREMSG_PATH/cmd
		export MSG_DATA_PATH=$date_slot/$time_slot
		echo Begin $MSG_DATA_PATH process | sed 's/[[:blank:]]/\\\ /g'
		bash $script1
		bash $script2
		bash $script3
	
	done
	echo End $MSG_DATA_PATH process
	dateDeb=$(date --date=$dateDeb'+1 days' +'%Y-%m-%d')
done
exit 0