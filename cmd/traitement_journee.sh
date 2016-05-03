#!usr/bin/sh

#cd /..
#cd /home/user/firemsg/Auto/compressed
#hostname="oisftp.eumetsat.org"
#name="lrit3h_412"
#password="QSxMzckd"
#ftp -i -n $hostname <<EOF
#quote USER $name
#quote PASS $password
#cd lrit3h
#mget *20160502*
#quit
#EOF

#bash appel.sh

export MSG_DATA_PATH=2016/05/02/0245
bash potfire.sh
export MSG_DATA_PATH=2016/05/02/0545
bash potfire.sh
export MSG_DATA_PATH=2016/05/02/0845
bash potfire.sh
export MSG_DATA_PATH=2016/05/02/1145
bash potfire.sh
export MSG_DATA_PATH=2016/05/02/1445
bash potfire.sh
export MSG_DATA_PATH=2016/05/02/1745
bash potfire.sh
export MSG_DATA_PATH=2016/05/02/2045
bash potfire.sh
export MSG_DATA_PATH=2016/05/02/2345
bash potfire.sh

python resume_day.py
YYYY=${MSG_DATA_PATH:0:4}
MM=${MSG_DATA_PATH:5:2}
DD=${MSG_DATA_PATH:8:2}
HHMM=${MSG_DATA_PATH:11:4}
python gdalcopyproj.py /home/user/firemsg/Auto/img_RA/$MSG_DATA_PATH/LRIT-MSG3-RA-$YYYY$MM$DD-$HHMM-039.tiff /home/user/firemsg/Auto/img_PF/$YYYY/$MM/$DD/LRIT-MSG3-PF-$YYYY$MM$DD-resume.tiff 

exit 0