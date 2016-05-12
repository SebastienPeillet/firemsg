#!usr/bin/sh
cd /home/user/firemsg/cmd
bash ftp.sh

cd /home/user/firemsg/Auto/compressed
time_slot=$(ls *EPI*)
YYYY=${time_slot:46:4}
MM=${time_slot:50:2}
DD=${time_slot:52:2}
HHMM=${time_slot:54:4}
export MSG_DATA_PATH=$YYYY/$MM/$DD/$HHMM

cd /home/user/firemsg/cmd
bash appel.sh

bash potfire.sh

exit 0