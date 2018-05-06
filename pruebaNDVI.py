import gdal
import numpy

def read_tiff_file(file_name):
  ds = gdal.Open(file_name)
  band = ds.GetRasterBand(1)
  arr = band.ReadAsArray()
  return arr, ds

def save_file(file_name, data, f):
    driver = gdal.GetDriverByName("GTiff")
    [cols, rows] = data.shape
    outdata = driver.Create(file_name, rows, cols, 1, gdal.GDT_UInt16)

    ##sets same geotransform as input
    outdata.SetGeoTransform(f.GetGeoTransform())

    ##sets same projection as input
    outdata.SetProjection(f.GetProjection())

    outdata.GetRasterBand(1).WriteArray(data)

    ##if you want these values transparent
    outdata.GetRasterBand(1).SetNoDataValue(10000)

    ##saves to disk!!
    outdata.FlushCache()

def proccess_data():
    data, f = read_tiff_file("LC80190472016212LGN00_B1.TIF")
    data2, f = read_tiff_file("LC80190472016212LGN00_B2.TIF")
    vis3, f = read_tiff_file("LC80190472016212LGN00_B3.TIF")
    nir4, f = read_tiff_file("LC80190472016212LGN00_B4.TIF")

def ndvi (nir, vis):
    res = (nir4 - vis3) / (nir4 + vis3)
    return res
    #arr_mean = int(data.mean())
    #arr_out = numpy.where((data < arr_mean), 10000, data)
    NDVI = ndvi(nir4, vis3)
    save_file("ndvi.tif", NDVI, f)

if __name__ == "__main__":
    proccess_data()
