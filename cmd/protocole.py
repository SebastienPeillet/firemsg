import os
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst
import scipy as sp
from numpy import amax
import temperature

data_path='/home/user/firemsg/Auto/img_raw/'+os.environ['MSG_DATA_PATH']+'/*16b*'
# /!\ the asterix doesn't work, even if there is only one file...
data=gdal.Open(datapath)
band=data.GetRasterBand(1)
band_data=band.ReadAsArray()

temp_data=temperature.temperaturebis(band_data)
out=temp_data.astype(int)
temperature.sauvegarde(out,name="/home/user/firemsg/Auto/img_pretraite/save.tiff")
