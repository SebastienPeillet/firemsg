import os
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst
import scipy as sp
import numpy as np

	
def temperature039(indata):

	C1 = 1.19104273e-16
	C2 = 0.0143877523
	vc = 2547.771
	alpha = 0.9915
	beta = 2.9002

	kelvin = ((C2 * 100. * vc / np.log(C1 * 1.0e6 * vc ** 3 / (1.0e-5 * indata.astype(np.float)) + 1)) - beta) / alpha
	return np.ma.masked_invalid(kelvin, copy=False)

def temperature108(indata):
	
	C1 = 1.19104273e-16
	C2 = 0.0143877523
	vc = 929.842
	alpha = 0.9983
	beta = 0.6084
	
	kelvin = ((C2 * 100. * vc / np.log(C1 * 1.0e6 * vc ** 3 / (1.0e-5 * indata.astype(np.float)) + 1)) - beta) / alpha
	return np.ma.masked_invalid(kelvin, copy=False)

def potentialfire(indata039,indata108) :
    
    [H,W]=indata039.shape
    dtype=indata039.dtype
    potfire=sp.empty((H,W),dtype='int32')
    
    time=os.environ["MSG_DATA_PATH"]
    time_tab=time.split('/')
    hh=int((time_tab[3])[0:2])

    for i in range(0,H):
        for j in range(0,W):
            img039=indata039[i,j]
            img108=indata108[i,j]
            delta= img039-img108
            if hh >= 8 and hh< 18:
                if img039>315 and delta>10 :
                    potfire[i,j]=1
                else:
                    potfire[i,j]=0
            else :
                if img039>305 and delta>3 :
                    potfire[i,j]=1
                else:
                    potfire[i,j]=0
    return potfire

def sauvegarde(indata,name='save.tiff'):
	driver=gdal.GetDriverByName("GTiff")
	driver.CreateCopy(name,gdal_array.OpenArray(indata,None))
	return
