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

#FTP download, change the mget argument (YYYYMMDD) to select the day you want
#cd /home/user/firemsg/Auto/compressed
#hostname="oisftp.eumetsat.org"
#name="lrit3h_412"
#password="QSxMzckd"
#ftp -i -n $hostname <<EOF
#quote USER $name
#quote PASS $password
#binary
#cd lrit3h
#mget *20160519*
#quit
#EOF

#Decompress all LRIT files
cd /home/user/firemsg/cmd
bash decompress.sh

script1=fire_detect.sh
script2=raster2vector.sh
script3=add2pg.py

#Day variable to process
time_slot=2016/05/21

#Process files for one day
cd /home/user/firemsg/cmd
export MSG_DATA_PATH=$time_slot/0245
bash $script1
bash $script2
python $script3
export MSG_DATA_PATH=$time_slot/0545
bash $script1
bash $script2
python $script3
export MSG_DATA_PATH=$time_slot/0845
bash $script1
bash $script2
python $script3
export MSG_DATA_PATH=$time_slot/1145
bash $script1
bash $script2
python $script3
export MSG_DATA_PATH=$time_slot/1445
bash $script1
bash $script2
python $script3
export MSG_DATA_PATH=$time_slot/1745
bash $script1
bash $script2
python $script3
export MSG_DATA_PATH=$time_slot/2045
bash $script1
bash $script2
python $script3
export MSG_DATA_PATH=$time_slot/2345
bash $script1
bash $script2
python $script3

cd /home/user/firemsg/cmd
python fd_resume_day.py
bash raster2vector_resume.sh

exit 0