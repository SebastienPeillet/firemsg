import os
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst
import scipy as sp
from numpy import amax
import temperature

data_path='/home/user/firemsg/Auto/img_brute/'+os.environ['MSG_DATA_PATH']+'/*16b*'
data=gdal.Open('/home/user/firemsg/Auto/img_brute/2016/04/18/1445/LRIT-MSG3-RA-2016418-1445-16b.tiff')
band=data.GetRasterBand(1)
band_data=band.ReadAsArray()

temp_data=temperature.temperaturebis(band_data)
out=temp_data.astype(int)
temperature.sauvegarde(out,name="/home/user/firemsg/Auto/img_pretraite/save.tiff")