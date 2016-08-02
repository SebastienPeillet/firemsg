###################################################################################
# fire_detect.py script
# 
# Author : Sebastien Peillet
# Project : TAIMPO, UMR Espace Dev
#
# Description : 
# This script is a part of the fire detection processing with MSG data. It could be used with the firemsg.sh 
# script or independantly by launching fire_detect.sh, but don't forget to define the MSG_DATA_PATH environment variable before launching
# script. Example : 'export MSG_DATA_PATH=2016/05/15/1145'
# Don't launch the script using "python fire_detect.py" ! You need to use "bash fire_detect.sh" to get needed environment variable.
# The script will create several files like brigthness temperature images, potential fire image and true fire image.
#
# Thanks to Pytroll team and to OSGEO tools
###################################################################################


#############LIBRAIRIES IMPORT##########
import os

from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst

from mpop.satellites import GeostationaryFactory
from mpop.projector import get_area_def
from mpop.utils import debug_on
from mipp.xrit import MSG

import scipy as sp
import numpy
import datetime

#uncomment to get more information about pytroll tools
#debug_on()

############ VARIABLES #################
#Sub section for variable initialization

#Firemsg_path variable
FIREMSG_PATH=os.environ["FIREMSG_PATH"]

#Projection variable
proj='PROJCS["geos0",GEOGCS["GCS_unnamed ellipse",DATUM["D_unknown",SPHEROID["Unknown",6378169,295.4880658970008]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Geostationary_Satellite"],PARAMETER["central_meridian",0],PARAMETER["satellite_height",35785831],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["Meter",1]]'
scr=(-1815176.8232086236, 3001.127145141965, 0.0, 1767937.3415769583, 0.0, -3000.110727186341)

#Time variable
try:
	time_path=os.environ["MSG_DATA_PATH"]
	time_tab=time_path.split('/')
	YYYY=int(time_tab[0])
	MM=int(time_tab[1])
	DD=int(time_tab[2])
	hh=int((time_tab[3])[0:2])
	mm=int((time_tab[3])[2:4])
	print "\nTIME SLOT : OK\n"
except :
	print "\nMSG_DATA_PATH UNDEFINED, YOU MUST USE BASH SCRIPT WITH 'export MSG_DATA_PATH=path/to/data'"

#Threshold args
MSG_FILE_TYPE=os.environ["MSG_FILE_TYPE"]
ENABLE_FIRE_DETECTION=os.environ["ENABLE_FIRE_DETECTION"]
T039=int(os.environ["T039"])
T108=int(os.environ["T108"])
delta_day=int(os.environ["delta_day"])
delta_night=int(os.environ["delta_night"])
day_start=int(os.environ["day_start"])
day_end=int(os.environ["day_end"])
window_width=int(os.environ["window_width"])
potfire_nb_limit=int(os.environ["potfire_nb_limit"])
level_requirement=float(os.environ["level_requirement"])
if MSG_FILE_TYPE=='H':
	cloud_test=float(os.environ["cloud_test"])

############ DATA LOAD WITH PYTROLL############
#Sub section for data load with pytroll

#Time_slot
try:
	time_slot=datetime.datetime(YYYY,MM,DD,hh,mm)
	print '\n'
	print time_slot
	print '\n'
except:
	print "\nTIME SLOT UNDEFINED"

#Scene Configuration
try:
	global_data=GeostationaryFactory.create_scene("meteosat","10","seviri",time_slot)
except:
	print "\nSATELLITE DEFINITION LOAD FAILED, CHECK THAT meteosat10.cfg EXISTS IN THE MPOP FOLDER OR CHANGE ARGUMENT IF YOU USE ANOTHER SATELLITE DEFINITION."

try:
	globe=get_area_def("AfSubSahara")
except:
	print "\nAREA DEFINITION LOAD FAILED, CHECK THAT areas.def EXISTS IN THE MPOP FOLDER."

#Data load
try:
	if MSG_FILE_TYPE=='L':
		IRchannelList=['IR_039','IR_108']
		global_data.load(IRchannelList,area_extent=globe.area_extent,calibrate=1)
		print global_data[3.9].data.min()
		print global_data[3.9].data.max()
		print global_data[10.8].data.min()
		print global_data[10.8].data.max()
		data=global_data.project("AfSubSahara")
		print "\nDATA LOAD : OK"
	else :
		IRchannelList=['IR_039','IR_108','IR_120']
		VISchannelList=['VIS006','VIS008']
		global_data.load(IRchannelList,area_extent=globe.area_extent,calibrate=1)
		global_data.load(VISchannelList,area_extent=globe.area_extent,calibrate=2)
		print global_data[3.9].data.min()
		print global_data[3.9].data.max()
		print global_data[10.8].data.min()
		print global_data[10.8].data.max()
		data=global_data.project("AfSubSahara")
		print "\nDATA LOAD : OK"
except:
	print"\nDATA LOAD FAILED, CHECK DATA AND TIME SLOT."

############ FORMATAGE OUTPUT ############
#Sub section for BT files configuration

try:
	outpathBT=FIREMSG_PATH+'/Auto/img_BT/'+time_path+'/'
	if MSG_FILE_TYPE=='L':
		file_nameBT=outpathBT+'LRIT-MSG3-BT-%s%s%s-%s-' % (time_tab[0], time_tab[1], time_tab[2], time_tab[3])
	else :
		file_nameBT=outpathBT+'HRIT-MSG3-BT-%s%s%s-%s-' % (time_tab[0], time_tab[1], time_tab[2], time_tab[3])
	print "\nOUTPUT FORMATTING : OK\n"
except:
	print "\nOUTPUT FORMATTING : FAILED\n"

#Create path if it doesn't exist
try :
	os.makedirs(outpathBT)
except:
    print 'OUTPATH EXISTS'

############ SAVE BT FILE ############
#Sub section to save channel image. Variable to change for other use : proj, src (see above)

try:
	if MSG_FILE_TYPE=='L':
		driver=gdal.GetDriverByName("GTiff")
		
		for channel in IRchannelList:
			#Save channel into tiff
			file_name=file_nameBT+channel+'.tiff'
			driver.CreateCopy(file_name,gdal_array.OpenArray(data[channel].data,None))
			#Open new tiff
			img=gdal.Open(file_name,1)
			#Tiff projection
			img.SetGeoTransform(scr)
			img.SetProjection(proj)

		print "\nSAVE BRIGHTNESS TEMPERATURE FILES : OK\n"

	else :
		driver=gdal.GetDriverByName("GTiff")

		for channel in IRchannelList:
			file_name=file_nameBT+channel+'.tiff'
			driver.CreateCopy(file_name,gdal_array.OpenArray(data[channel].data,None))
			img=gdal.Open(file_name,1)
			img.SetGeoTransform(scr)
			img.SetProjection(proj)

		for channel in VISchannelList:
			file_name=file_nameBT+channel+'.tiff'
			driver.CreateCopy(file_name,gdal_array.OpenArray(data[channel].data,None))
			img=gdal.Open(file_name,1)
			img.SetGeoTransform(scr)
			img.SetProjection(proj)

		print "\nSAVE BRIGHTNESS TEMPERATURE FILES : OK\n"
except:
	print"\nSAVE BRIGHTNESS TEMPERATURE FILES : FAILED"
	
	
###############POT FIRE##################
if ENABLE_FIRE_DETECTION=='true' :
	#Sub section to detect potentiel fire

	#Load channel array
	if MSG_FILE_TYPE=='L':
		array039=global_data[3.9].data
		array108=global_data[10.8].data
	else :
		array039=global_data[3.9].data
		array108=global_data[10.8].data
		array008=global_data[0.8].data
		array006=global_data[0.6].data
		array120=global_data[12.0].data

	#Initialize potential fire array
	[H,W]=array039.shape
	dtype=array039.dtype
	potfire=sp.empty((H,W),dtype='int32')

	#Potential fire counter initialize
	countpotf=0

	#Loop to detect potential fire pixel
	if MSG_FILE_TYPE=='L':
		for i in range(0,H):
			for j in range(0,W):
				img039=array039[i,j]
				img108=array108[i,j]
				delta= img039-img108
				
				#Threshold to detect potentiel fire pixel, formula depends on time, indices can be change
				#Day time
				if hh >= day_start and hh< day_end:
					if (img039>T039 and delta>delta_day and img108>T108):
						potfire[i,j]=2
						countpotf+=1
					else:
						potfire[i,j]=1
				#Night time
				else :
					if img039>T039 and delta>delta_night :
						potfire[i,j]=2
						countpotf+=1
					else:
						potfire[i,j]=1

		print countpotf

	else :
		for i in range(0,H):
			for j in range(0,W):
				img039=array039[i,j]
				img108=array108[i,j]
				img006=array006[i,j]
				img008=array008[i,j]
				vis_cloud=img006+img008
				img120=array120[i,j]
				delta= img039-img108
				
				#Threshold to detect potentiel fire pixel, formula depends on time, indices can be change
				#Day time
				if hh >= day_start and hh< day_end:
					if (img039>T039 and delta>delta_day and img108>T108 and vis_cloud<cloud_test and img120>265):
						potfire[i,j]=2
						countpotf+=1
					else:
						potfire[i,j]=1
				#Night time
				else :
					if img039>T039 and delta>delta_night :
						potfire[i,j]=2
						countpotf+=1
					else:
						potfire[i,j]=1

		print countpotf	


	############ PF OUTPUT FORMATTING ############
	#Sub section to PF files configuration. Can be comment to skip PF save, no influence on the TF file

	try:
		outpath=FIREMSG_PATH+'/Auto/img_PF/'+time_path+'/'
		if MSG_FILE_TYPE=='L':
			outname=outpath+'LRIT-MSG3-PF-%s%s%s-%s.tiff' % (time_tab[0], time_tab[1], time_tab[2], time_tab[3])
		else:
			outname=outpath+'HRIT-MSG3-PF-%s%s%s-%s.tiff' % (time_tab[0], time_tab[1], time_tab[2], time_tab[3])
		print "\nOUTPUT FORMATTING : OK\n"
	except:
		print"\nOUTPUT FORMATTING : FAILED\n"

	#Create path if it doesn't exist
	try :
	    os.makedirs(outpath)
	except:
	    print "OUTPATH EXISTS"
		
	############ SAVE PF FILE ############
	#Sub section to save PF files. Can be comment to skip PF save, no influence on the TF file

	try:
		driver=gdal.GetDriverByName("GTiff")
		
		driver.CreateCopy(outname,gdal_array.OpenArray(potfire,None))
		#Open new 3.9um tiff
		imgPF=gdal.Open(outname,1)
		#Tiff projection
		imgPF.SetGeoTransform(scr)
		imgPF.SetProjection(proj)
		print "\nSAVE POTENTIAL FIRE FILE : OK\n"
	except:
		print "\nSAVE POTENTIAL FIRE FILE : FAILED\n"

	##########CONTEXTUAL THRESHOLD##########
	#Sub section to validate true fire from potential fire

	#True fire array initialize
	fire=sp.empty((H,W),dtype='int32')

	#Window width
	p=window_width
	q=(p-1)/2

	#Border processing
	fire[:q,:]=0
	fire[:,:q]=0
	fire[:-q,:]=0
	fire[:,:-q]=0

	#True fire counter initialize
	countf=0

	#Loop to detect true fire
	for k in range (q,H-q) :
		for l in range (q,W-q) :
			if potfire[k,l]==2 :
				
				#Pixel value in [k,l]
				potf039=array039[k,l]
				potf108=array108[k,l]
				
				potfirecount=sum(sum(potfire[k-q:(k+q+1),l-q:(l+q+1)]))
				
				#Pixel values in the windows for 3.9um
				temp039=array039[k-q:(k+q+1),l-q:(l+q+1)]
				[h,w]=temp039.shape
				n=h*w
				#Mean and mean absolute deviation pixel of the window for 3.9um channel
				meanpotf039=temp039.mean()
				devpotf039=sum(sum([abs(x-meanpotf039) for x in temp039]))/n
				
				#Pixel values in the windows for 10.8um
				temp108=array108[k-q:(k+q+1),l-q:(l+q+1)]
				#Mean and mean absolute deviation pixel of the window for 10.8um channel
				meanpotf108=temp108.mean()
				devpotf108=sum(sum([abs(x-meanpotf108) for x in temp108]))/n
				
				#Delta in [k,l]
				deltapotf=potf039-potf108
				#Delta pixel values in the windows
				tempdeltapotf=array039[k-q:(k+q+1),l-q:(l+q+1)]-array108[k-q:(k+q+1),l-q:(l+q+1)]
				#Delta mean and mean absolute deviation pixel of the window
				meandeltapotf=tempdeltapotf.mean()
				devdeltapotf=sum(sum([abs(x-meandeltapotf) for x in tempdeltapotf]))/n
				
				if potfirecount > potfire_nb_limit :
					fire[k,l]=0
				
				else :
					if deltapotf > (meandeltapotf+level_requirement*devdeltapotf) and potf039 > (meanpotf039+level_requirement*devpotf039):
						#source Manyangadze "Forest fire detection for near real-time monitoring using geostationary satellites"
						fire[k,l]=array039[k,l]
						countf+=1
					else:
						fire[k,l]=0
					
			else:
				fire[k,l]=0

	print countf

	############TF OUTPUT FORMATTING############
	#Sub section to TF files configuration.

	try:
		outpath=FIREMSG_PATH+'/Auto/img_TF/'+time_path+'/'
		if MSG_FILE_TYPE=='L':
			outname=outpath+'LRIT-MSG3-TF-%s%s%s-%s.tiff' % (time_tab[0], time_tab[1], time_tab[2], time_tab[3])
		else :
			outname=outpath+'HRIT-MSG3-TF-%s%s%s-%s.tiff' % (time_tab[0], time_tab[1], time_tab[2], time_tab[3])
		print "\nOUTPUT FORMATTING : OK\n"
	except:
		print"\nOUTPUT FORMATTING : FAILED\n"

	try :
	    os.makedirs(outpath)
	except:
	    print 'OUTPATH EXISTS'


	############SAVE TF FILE############
	#Sub section to save TF files.

	try :
		driver=gdal.GetDriverByName("GTiff")
		
		driver.CreateCopy(outname,gdal_array.OpenArray(fire,None))
		#Open new TF file
		imgPF=gdal.Open(outname,1)
		#Tiff projection
		imgPF.SetGeoTransform(scr)
		imgPF.SetProjection(proj)
		print "\nSAVE TRUE FIRE FILE : OK\n"
	except:
		print "\nSAVE TRUE FIRE FILE : FAILED\n"

quit()