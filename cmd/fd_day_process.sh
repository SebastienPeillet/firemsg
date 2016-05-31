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
source /home/user/firemsg/cmd/config_firemsg.cfg

export FIREMSG_PATH
export ENABLE_POSTGRES
#FTP download, change the mget argument (YYYYMMDD) to select the day you want
cd $FIREMSG_PATH/Auto/compressed
hostname="oisftp.eumetsat.org"
name="lrit3h_412"
password="QSxMzckd"
ftp -i -n $hostname <<EOF
quote USER $name
quote PASS $password
binary
cd lrit3h
mget *20160528*
mget *20160529*
mget *20160530*
quit
EOF

#Decompress all LRIT files
cd $FIREMSG_PATH/cmd
bash decompress.sh

script1=fire_detect.sh
script2=raster2vector.sh
script3=add2pg.py

#Day variable to process
dateDeb=2016-05-28
dateFin=2016-05-31

while [ "$dateDeb" != "$dateFin" ]; do
	date_slot=$(date --date=$dateDeb +'%Y/%m/%d')
	
	time=('0245' '0545' '0845' '1145' '1445' '1745' '2045' '2345')
	for time_slot in ${time[@]}; do
	#Process files for one day
		cd $FIREMSG_PATH/cmd
		export MSG_DATA_PATH=$date_slot/$time_slot
		bash $script1
		bash $script2
		#python $script3
	
	done
	
	cd $FIREMSG_PATH/cmd
	python fd_resume_day.py
	bash raster2vector_resume.sh

	dateDeb=$(date --date=$dateDeb'+1 days' +'%Y-%m-%d')
done
exit 0