###################################################################################
# add2pg.py script
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
import os
import ogr
import psycopg2

############ VARIABLES #################
#Sub section for variable initialization

#Firemsg_path variable
FIREMSG_PATH=os.environ["FIREMSG_PATH"]

#Time variable
time_path=os.environ["MSG_DATA_PATH"]
time_tab=time_path.split('/')
YYYY=int(time_tab[0])
MM=int(time_tab[1])
DD=int(time_tab[2])
hh=int((time_tab[3])[0:2])
mm=int((time_tab[3])[2:4])



inDataFilePath=FIREMSG_PATH+'/Auto/vec_TF/'+time_tab[0]+'/'+time_tab[1]+'/'+time_tab[2]+'/'+time_tab[3]+'/'
inDataFileName='LRIT-MSG3-vecTF-%s%s%s-%s-WGS84' % (time_tab[0], time_tab[1], time_tab[2], time_tab[3])
inDataFile=inDataFilePath+inDataFileName+'.shp'

#Initialize connexion to pg_database
connection=psycopg2.connect("dbname='firemsg' user='user' host='localhost' password='seasoi'")
cursor=connection.cursor()

#Open data
driver=ogr.GetDriverByName("ESRI Shapefile")
dataSource=driver.Open(inDataFile)
layer=dataSource.GetLayer()

for feature in layer :
	date=feature.GetField("Date")
	time=feature.GetField("Time")
	temp=feature.GetField("Count")
	geom=str(feature.GetGeometryRef())
	cursor.execute("""INSERT INTO fire(date,time,temp_kelvin,geom) VALUES (%s,%s,%s,ST_GeomFromText(%s,4326));""",(date, time, temp, geom))
connection.commit()