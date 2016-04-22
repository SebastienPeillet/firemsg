from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst
import scipy as sp
import numpy as np

def radiance (indata):

	[H,W]=indata.shape
	out=sp.empty((H,W),dtype='f')

	for i in range(0,H):
		for j in range(0,W):
			temp=indata[i,j]
			if temp==0:
				out[i,j]=0
			else:
				out[i,j]=temp/a
return out