from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst
import scipy as sp
import numpy as np

def temperature(indata):

	[H,W]=indata.shape
	dtype=indata.dtype
	kelvin=sp.empty((H,W),dtype='int32')

	C2=0.0143877523
	C1=1.19104273e-16
	vc=2547.771
	A=0.9915
	B=2.9002

	for i in range(0,H):
		for j in range(0,W):
			temp=indata[i,j]
			if temp==0:
				kelvin[i,j]=temp
			else:
				kelvin[i,j]=((C2*vc/np.log(C1*vc**3/temp+1)-B)/A)
	return kelvin
	
def temperaturebis(indata):

	C1 = 1.19104273e-16
	C2 = 0.0143877523
	vc = 2547.771
	alpha = 0.9915
	beta = 2.9002

	kelvin = ((C2 * 100. * vc / np.log(C1 * 1.0e6 * vc ** 3 / (1.0e-5 * indata.astype(np.float)) + 1)) - beta) / alpha
	return np.ma.masked_invalid(kelvin, copy=False)
	
def fire(indata) :

	[H,W]=indata.shape
	dtype=indata.dtype
	potfire=sp.empty((H,W),dtype='int32')
	
	temps=TIME_SLOT
	return potfire

def sauvegarde(indata,name='save.tiff'):
	driver=gdal.GetDriverByName("GTiff")
	driver.CreateCopy(name,gdal_array.OpenArray(indata,None))
	return