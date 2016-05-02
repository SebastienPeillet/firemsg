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
    hh=int((time_tab[3])[0:2])
    mm=int((time_tab[3])[2:4])
    print "\nFormatage de la fenetre de temps : OK\n"
except :
    print "\nMSG_DATA_PATH non definie. Dans le cas\nd'une utilisation hors chaine veuillez preciser MSG_DATA_PATH\ndans une console par laquelle vous lancerez composition_mpop.py\ntel que : export MSG_DATA_PATH=path/to/data"

inpath='/home/user/firemsg/Auto/img_RA/'+time_path+'/'
infile_name039=inpath+'LRIT-MSG3-RA-%s%s%s-%s%s-039.tiff' % (YYYY, MM, DD, hh, mm)
infile_name108=inpath+'LRIT-MSG3-RA-%s%s%s-%s%s-108.tiff' % (YYYY, MM, DD, hh, mm)

data039=gdal.Open(infile_name039)
data108=gdal.Open(infile_name108)

band039=data039.GetRasterBand(1)
band108=data108.GetRasterBand(1)

band039_data=band039.ReadAsArray()
band108_data=band108.ReadAsArray()

out039=temperature.temperature039(band039_data)
print '\n'
print (out039.min(),out039.max())
print '\n'
out108=temperature.temperature108(band108_data)
print (out108.min(),out108.max())
#out=temp_data.astype(int)

outpath='/home/user/firemsg/Auto/img_BT/'+time_path+'/'
try :
    os.makedirs(outpath)
except:
    print 'out path already exists'

outfile_name039=outpath+'LRIT-MSG3-BT-%s%s%s-%s%s-16b-039.tiff' % (YYYY, MM, DD, hh, mm)
outfile_name108=outpath+'LRIT-MSG3-BT-%s%s%s-%s%s-16b-108.tiff' % (YYYY, MM, DD, hh, mm)

temperature.sauvegarde(out039,outfile_name039)
temperature.sauvegarde(out108,outfile_name108)
