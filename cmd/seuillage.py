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
    
inpath='/home/user/firemsg/Auto/img_BT/'+time_path+'/'
infile039_name=inpath+'LRIT-MSG3-BT-%s%s%s-%s%s-16b-039.tiff' % (YYYY, MM, DD, hh, mm)
infile108_name=inpath+'LRIT-MSG3-BT-%s%s%s-%s%s-16b-108.tiff' % (YYYY, MM, DD, hh, mm)

data039=gdal.Open(infile039_name)
data108=gdal.Open(infile108_name)

band039=data039.GetRasterBand(1)
band108=data108.GetRasterBand(1)

band_data039=band039.ReadAsArray()
band_data108=band108.ReadAsArray()

out=temperature.potentialfire(band_data039,band_data108)

outpath='/home/user/firemsg/Auto/img_PF/'+time_path+'/'
try :
    os.makedirs(outpath)
except:
    print 'out path already exists'

outfile_name=outpath+'LRIT-MSG3-PF-%s%s%s-%s%s-16b.tiff' % (YYYY, MM, DD, hh, mm)
temperature.sauvegarde(out,outfile_name)