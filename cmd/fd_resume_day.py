###################################################################################
# fd_resume_day.py script
# 
# Author : Sebastien Peillet
# Project : TAIMPO, UMR Espace Dev
#
# Description : 
# This script will create a resume from TF files on a define day. Used with
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
import scipy as sp

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
    print "\nFormatage de la fenetre de temps : OK\n"
except :
    print "\nMSG_DATA_PATH non definie. Dans le cas\nd'une utilisation hors chaine veuillez preciser MSG_DATA_PATH\ndans une console par laquelle vous lancerez composition_mpop.py\ntel que : export MSG_DATA_PATH=path/to/data"

########### DATA LOAD ##################
#Sub section for data load

#Path to data
inpath=FIREMSG_PATH+'/Auto/img_TF/'+time_tab[0]+'/'+time_tab[1]+'/'+time_tab[2]+'/'
	
#Name files
infile_name0245=inpath+'0245/LRIT-MSG3-TF-%s%s%s-0245.tiff' % (time_tab[0], time_tab[1], time_tab[2])
infile_name0545=inpath+'0545/LRIT-MSG3-TF-%s%s%s-0545.tiff' % (time_tab[0], time_tab[1], time_tab[2])
infile_name0845=inpath+'0845/LRIT-MSG3-TF-%s%s%s-0845.tiff' % (time_tab[0], time_tab[1], time_tab[2])
infile_name1145=inpath+'1145/LRIT-MSG3-TF-%s%s%s-1145.tiff' % (time_tab[0], time_tab[1], time_tab[2])
infile_name1445=inpath+'1445/LRIT-MSG3-TF-%s%s%s-1445.tiff' % (time_tab[0], time_tab[1], time_tab[2])
infile_name1745=inpath+'1745/LRIT-MSG3-TF-%s%s%s-1745.tiff' % (time_tab[0], time_tab[1], time_tab[2])
infile_name2045=inpath+'2045/LRIT-MSG3-TF-%s%s%s-2045.tiff' % (time_tab[0], time_tab[1], time_tab[2])
infile_name2345=inpath+'2345/LRIT-MSG3-TF-%s%s%s-2345.tiff' % (time_tab[0], time_tab[1], time_tab[2])

#Open files
data0245=gdal.Open(infile_name0245)
data0545=gdal.Open(infile_name0545)
data0845=gdal.Open(infile_name0845)
data1145=gdal.Open(infile_name1145)
data1445=gdal.Open(infile_name1445)
data1745=gdal.Open(infile_name1745)
data2045=gdal.Open(infile_name2045)
data2345=gdal.Open(infile_name2345)

#Get raster band from files
band0245=data0245.GetRasterBand(1)
band0545=data0545.GetRasterBand(1)
band0845=data0845.GetRasterBand(1)
band1145=data1145.GetRasterBand(1)
band1445=data1445.GetRasterBand(1)
band1745=data1745.GetRasterBand(1)
band2045=data2045.GetRasterBand(1)
band2345=data2345.GetRasterBand(1)

#Get array from raster band
band0245_data=band0245.ReadAsArray()
band0545_data=band0545.ReadAsArray()
band0845_data=band0845.ReadAsArray()
band1145_data=band1145.ReadAsArray()
band1445_data=band1445.ReadAsArray()
band1745_data=band1745.ReadAsArray()
band2045_data=band2045.ReadAsArray()
band2345_data=band2345.ReadAsArray()

########### RESUME DAY ##################
#Sub section to resume all images

#output array initialize
[H,W]=band0245_data.shape
dtype=band0245_data.dtype
output=sp.empty((H,W),dtype='int32')

#Total pixel values from all images
for i in range (0,H) :
	for j in range (0,W) :
		pixelcount=0
		n=0
		for k in [band0245_data,band0545_data,band0845_data,band1145_data,band1445_data,band1745_data,band2045_data,band2345_data] :
			if k[i,j] != 0 :
				pixelcount= pixelcount + k[i,j]
				n+=1
		if n != 0 :
			output[i,j] = pixelcount/n
		else :
			output[i,j] = 0
		
#output=band0245_data+band0545_data+band0845_data+band1145_data+band1445_data+band1745_data+band2045_data+band2345_data

#Resampling on a binary images
#for i in range (0,H) :
#	for j in range (0,W) :
#		if output[i,j] > 8 :
#			output[i,j] = 2
#		else :
#			output[i,j] = 1
#
########## OUTPUT FORMATTING ###########
#Sub section to resume file configuration

try:
	outpath=FIREMSG_PATH+'/Auto/img_TF/'+time_tab[0]+'/'+time_tab[1]+'/'+time_tab[2]+'/'
	outname=outpath+'LRIT-MSG3-TF-%s%s%s-resume.tiff' % (time_tab[0], time_tab[1], time_tab[2])
	print "\nFORMATAGE SORTIE : OK\n"
except:
	print"\nFormatage fichiers sortie echoue"

try :
    os.makedirs(outpath)
except:
    print 'out path already exists'

############SAVE RESUME FILE############
#Sub section to save resume file.

try :
	driver=gdal.GetDriverByName("GTiff")
	driver.CreateCopy(outname,gdal_array.OpenArray(output,None))
	#Open new resume tiff
	imgPF=gdal.Open(outname,1)
	#Tiff projection
	imgPF.SetGeoTransform(scr)
	imgPF.SetProjection(proj)
	print "\nSAVE RESUME FILE : OK\n"
except:
	print "\nSAVE RESUME FILE : FAILED\n"