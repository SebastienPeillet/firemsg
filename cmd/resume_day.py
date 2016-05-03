import os
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst
import scipy as sp
import temperature

############FORMATAGE VARIABLE TEMPS############
try:
    time_path=os.environ["MSG_DATA_PATH"]
    time_tab=time_path.split('/')
    YYYY=int(time_tab[0])
    MM=int(time_tab[1])
    DD=int(time_tab[2])
    print "\nFormatage de la fenetre de temps : OK\n"
except :
    print "\nMSG_DATA_PATH non definie. Dans le cas\nd'une utilisation hors chaine veuillez preciser MSG_DATA_PATH\ndans une console par laquelle vous lancerez composition_mpop.py\ntel que : export MSG_DATA_PATH=path/to/data"

inpath='/home/user/firemsg/Auto/img_PF/'+time_tab[0]+'/'+time_tab[1]+'/'+time_tab[2]+'/'
infile_name0245=inpath+'0245/LRIT-MSG3-PF-%s%s%s-0245.tiff' % (time_tab[0], time_tab[1], time_tab[2])
infile_name0545=inpath+'0545/LRIT-MSG3-PF-%s%s%s-0545.tiff' % (time_tab[0], time_tab[1], time_tab[2])
infile_name0845=inpath+'0845/LRIT-MSG3-PF-%s%s%s-0845.tiff' % (time_tab[0], time_tab[1], time_tab[2])
infile_name1145=inpath+'1145/LRIT-MSG3-PF-%s%s%s-1145.tiff' % (time_tab[0], time_tab[1], time_tab[2])
infile_name1445=inpath+'1445/LRIT-MSG3-PF-%s%s%s-1445.tiff' % (time_tab[0], time_tab[1], time_tab[2])
infile_name1745=inpath+'1745/LRIT-MSG3-PF-%s%s%s-1745.tiff' % (time_tab[0], time_tab[1], time_tab[2])
infile_name2045=inpath+'2045/LRIT-MSG3-PF-%s%s%s-2045.tiff' % (time_tab[0], time_tab[1], time_tab[2])
infile_name2345=inpath+'2345/LRIT-MSG3-PF-%s%s%s-2345.tiff' % (time_tab[0], time_tab[1], time_tab[2])

data0245=gdal.Open(infile_name0245)
data0545=gdal.Open(infile_name0545)
data0845=gdal.Open(infile_name0845)
data1145=gdal.Open(infile_name1145)
data1445=gdal.Open(infile_name1445)
data1745=gdal.Open(infile_name1745)
data2045=gdal.Open(infile_name2045)
data2345=gdal.Open(infile_name2345)

band0245=data0245.GetRasterBand(1)
band0545=data0545.GetRasterBand(1)
band0845=data0845.GetRasterBand(1)
band1145=data1145.GetRasterBand(1)
band1445=data1445.GetRasterBand(1)
band1745=data1745.GetRasterBand(1)
band2045=data2045.GetRasterBand(1)
band2345=data2345.GetRasterBand(1)

band0245_data=band0245.ReadAsArray()
band0545_data=band0545.ReadAsArray()
band0845_data=band0845.ReadAsArray()
band1145_data=band1145.ReadAsArray()
band1445_data=band1445.ReadAsArray()
band1745_data=band1745.ReadAsArray()
band2045_data=band2045.ReadAsArray()
band2345_data=band2345.ReadAsArray()

[H,W]=band0245_data.shape
dtype=band0245_data.dtype
output=sp.empty((H,W),dtype='int32')

output=band0245_data+band0545_data+band0845_data+band1145_data+band1445_data+band1745_data+band2045_data+band2345_data

for i in range (0,H) :
	for j in range (0,W) :
		if output[i,j] > 8 :
			output[i,j] = 2
		else :
			output[i,j] = 1

try:
	outpath='/home/user/firemsg/Auto/img_PF/'+time_tab[0]+'/'+time_tab[1]+'/'+time_tab[2]+'/'
	outname=outpath+'LRIT-MSG3-PF-%s%s%s-resume.tiff' % (time_tab[0], time_tab[1], time_tab[2])
	print "\nFORMATAGE SORTIE : OK\n"
except:
	print"\nFormatage fichiers sortie echoue"

try :
    os.makedirs(outpath)
except:
    print 'out path already exists'
############SAUVEGARDE DES FICHIERS IMAGES############
driver=gdal.GetDriverByName("GTiff")
driver.CreateCopy(outname,gdal_array.OpenArray(output,None))