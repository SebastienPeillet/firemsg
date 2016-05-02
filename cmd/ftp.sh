#!/usr/bin/sh
cd /..
cd /home/user/firemsg/Auto/compressed
hostname="oisftp.eumetsat.org"
name="lrit3h_412"
password="QSxMzckd"
ftp -i -n $hostname <<EOF
quote USER $name
quote PASS $password
cd lrit3h
mls L* list.txt
quit
EOF

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

ftp -i -n $hostname <<EOF
quote USER $name
quote PASS $password
binary
cd lrit3h
mget *$time_slot*
quit
EOF
