# firemsg
Dev architecture to use LRIT meteosat data

This will be the build for automatic process of MSG LRIT DATA, applied to fire detection. This application has been produced for the TAIMPO project. 
The data have to be downloaded from the Eumetsat Service: http://www.eumetsat.int/website/home/index.html
This has been produced under Ubuntu 14.04 and Debian Jessie.

Some requierement :
  - xRITDecompress tools, free, available at http://www.eumetsat.int/website/home/Data/DataDelivery/SupportSoftwareandTools/index.html
  - Pytroll librairies : mipp (0.10.0), mpop (1.2.1), pyproj (1.9.5.1), pyresample (1.2.3) (https://github.com/pytroll)
  - Gdal 1.10.1 (from distrib repository gdal-bin)

Installation :
Read install_cli.txt and follow instructions.
