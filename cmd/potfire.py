import os
import re

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

#decommenter pour plus d'information du aux outils pytroll lors du traitement
#debug_on()


############FORMATAGE VARIABLE TEMPS############
try:
	time_path=os.environ["MSG_DATA_PATH"]
	time_tab=time_path.split('/')
	YYYY=int(time_tab[0])
	MM=int(time_tab[1])
	DD=int(time_tab[2])
	hh=int((time_tab[3])[0:2])
	mm=int((time_tab[3])[2:4])
	print "\nFormatage de la fenetre de temps : OK\n"
except :
	print "\nMSG_DATA_PATH non definie. Dans le cas\nd'une utilisation hors chaine veuillez preciser MSG_DATA_PATH\ndans une console par laquelle vous lancerez composition_mpop.py\ntel que : export MSG_DATA_PATH=path/to/data"


############CHARGEMENT DES DONNEES PAR MPOP############
try:
	time_slot=datetime.datetime(YYYY,MM,DD,hh,mm)
	print '\n'
	print time_slot
	print '\n'
except:
	print "\nFenetre de temps non definie."

try:
	global_data=GeostationaryFactory.create_scene("meteosat","10","seviri",time_slot)
except:
	print "\nChargement des parametres satellites echoue, verifiez la presecence du fichier meteosat10.cfg a la racine de mpop."

try:
	globe=get_area_def("AfSubSahara")
except:
	print "\nChargement des parametres de zone echoue, verifiez la presecence du fichier areas.def a la racine de mpop."
    
try:
	global_data.load([0.6,1.6,3.9,6.2,10.8],area_extent=globe.area_extent,calibrate=1)
	print global_data[3.9].data.min()
	print global_data[3.9].data.max()
	print global_data[10.8].data.min()
	print global_data[10.8].data.max()
	data=global_data.project("AfSubSahara")
	print "\nChargement des donnees par mpop : OK"
except:
	print"\nChargement des donnes echoue, verifiez la presence des donnees et leur correspondance a la fenetre de temps donnee."

############FORMATAGE OUTPUT############
try:
	outpathRA='/home/user/firemsg/Auto/img_RA/'+time_path+'/'
	outpathBT='/home/user/firemsg/Auto/img_BT/'+time_path+'/'
	file_nameRA=outpathRA+'LRIT-MSG3-RA-%s%s%s-%s' % (time_tab[0], time_tab[1], time_tab[2], time_tab[3])
	file_nameBT=outpathBT+'LRIT-MSG3-BT-%s%s%s-%s' % (time_tab[0], time_tab[1], time_tab[2], time_tab[3])
	print "\nFORMATAGE SORTIE : OK\n"
except:
	print"\nFormatage fichiers sortie echoue"

try :
	os.makedirs(outpathRA)
	os.makedirs(outpathBT)
except:
    print 'out path already exists'

############SAUVEGARDE DES FICHIERS IMAGES RA############
try:
	driver=gdal.GetDriverByName("GTiff")
	
	img039=data.image.channel_image(3.9)
	file_nameRA039=file_nameRA+'-039.tiff'
	img039.save(file_nameRA039,tags={"NBITS":'16'}, floating_point=True)
	file_nameBT039=file_nameBT+'-039.tiff'
	driver.CreateCopy(file_nameBT039,gdal_array.OpenArray(data[3.9].data,None))
	
	img108=data.image.channel_image(10.8)
	file_nameRA108=file_nameRA+'-108.tiff'
	img108.save(file_nameRA108, tags={"NBITS":'16'},floating_point=True)
	file_nameBT108=file_nameBT+'-108.tiff'
	driver.CreateCopy(file_nameBT108,gdal_array.OpenArray(data[10.8].data,None))
	print "\nSAUVEGARDE FICHIER RADIANCE : OK\n"
except:
	print"\nSauvegarde fichiers radiance echoue"
	
	
###############POT FIRE##################
array039=global_data[3.9].data
array108=global_data[10.8].data

[H,W]=array039.shape
dtype=array039.dtype
potfire=sp.empty((H,W),dtype='int32')

for i in range(0,H):
	for j in range(0,W):
		img039=array039[i,j]
		img108=array108[i,j]
		delta= img039-img108
		if hh >= 8 and hh< 18:
			if (img039>300 and delta>10 and img108>290):
				#source metoffice.gov.uk, cloud detection
				potfire[i,j]=2
				#print "x="+str(i)+" et y="+str(j)
			else:
				potfire[i,j]=1
		else :
			if img039>300 and delta>3 :
				potfire[i,j]=2
			else:
				potfire[i,j]=1




############FORMATAGE OUTPUT############
try:
	outpath='/home/user/firemsg/Auto/img_PF/'+time_path+'/'
	outname=outpath+'LRIT-MSG3-PF-%s%s%s-%s.tiff' % (time_tab[0], time_tab[1], time_tab[2], time_tab[3])
	print "\nFORMATAGE SORTIE : OK\n"
except:
	print"\nFormatage fichiers sortie echoue"

try :
    os.makedirs(outpath)
except:
    print 'out path already exists'
############SAUVEGARDE DES FICHIERS IMAGES############
try:
	driver=gdal.GetDriverByName("GTiff")
	driver.CreateCopy(outname,gdal_array.OpenArray(potfire,None))
	print "\nSAUVEGARDE FICHIER PF : OK\n"
except:
	print "\nSauvegarde fichier pf echoue"

quit()
