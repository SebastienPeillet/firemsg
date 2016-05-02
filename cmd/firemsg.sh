#!usr/bin/sh
cd /home/user/firemsg/cmd
bash ftp.sh

cd /home/user/firemsg/Auto/compressed

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
	
for j in /home/user/firemsg/Auto/compressed/L*__
	do
	cd /home/user/firemsg/Auto/compressed
	cp $j /home/user/firemsg/Auto/archive
    tempo=$(echo $j)
	outYYYY=$(echo ${tempo:81:4})
	outMM=$(echo ${tempo:85:2})
	outDD=$(echo ${tempo:87:2})
    outHHMM=${tempo:89:4}
	mv $j /home/user/firemsg/Auto/decompressed/$outYYYY/$outMM/$outDD/$outHHMM
	export MSG_DATA_PATH=$outYYYY/$outMM/$outDD/$outHHMM
done

cd /home/user/firemsg/cmd
bash composition_mpop.sh
exit 0