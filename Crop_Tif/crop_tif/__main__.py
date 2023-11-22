from PIL import Image
import sys
import os
import rpy2
import re
import numpy as np
import gdal
import rasterio
from affine import Affine
import time
import mimetypes
import json
import datetime as dt

#print(sys.path)

out_dir = os.getcwd()

## inputs are pathName, we then want to find the .tif file here

#im = Image.open('a_image.tif')

def convertFile(fileName: str):
    with Image.open(fileName) as openTif:
        print(openTif)
        imarray = np.array(openTif)
        width = imarray.shape[0]
        height = imarray.shape[1]
        outImage = Image.fromarray(imarray[:round(width/2), :round(height/2)])
        outImage.save("output_invert.tif")

def convertTiff(fileName: str):
    #print(fileName)
    outName = os.path.split(fileName)[1]
    outName = outName.replace(".tif","")
    outName = f'{outName}_invert.tif'
    #print(outName)
    step1 = gdal.Open(fileName, gdal.GA_ReadOnly)
    GT_input = step1.GetGeoTransform()
    #print(GT_input)
    transf = Affine.from_gdal(*GT_input)
    step2 = step1.GetRasterBand(1)
    img_as_array = step2.ReadAsArray()
    size1,size2=img_as_array.shape
    output=np.zeros(shape=(size1,size2))
    for i in range(0,size1):
        for j in range(0,size2):
            output[i,j]=img_as_array[i,j] * -1
    dst_crs='EPSG:4326'
    output = np.float32(output)
    with rasterio.open(
    outName,
    'w',
    driver='GTiff',
    height=output.shape[0],
    width=output.shape[1],
    count=1,
    dtype=np.float32,
    crs=dst_crs,
    transform=transf,
    ) as dest_file:
        dest_file.write(output, 1)
        dest_file.close()
    
    createStac(outName.replace(".tif",""))

## This needs to be created correctly in future
def createStac(outName):
    createStacItem(outName)
    createStacCatalogRoot(outName)

def createStacItem(outName) :
    now = time.time_ns()/1_000_000_000
    dateNow = dt.datetime.fromtimestamp(now)
    dateNow = dateNow.strftime('%Y-%m-%dT%H:%M:%S.%f') + "Z"
    size = os.path.getsize(f"{out_dir}/{outName}.tif")
    mime = mimetypes.guess_type(f"{out_dir}/{outName}.tif")[0]
    data = {"stac_version": "1.0.0",
  "id": f"{outName}-{now}",
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [-180, -90],
        [-180, 90],
        [180, 90],
        [180, -90],
        [-180, -90]
      ]
    ]
  },
  "properties": {
    "created": f"{dateNow}",
    "datetime": f"{dateNow}",
    "updated": f"{dateNow}"
  },
  "bbox": [-180, -90, 180, 90],
  "assets": {
    f"{outName}": {
      "type": f"{mime}",
      "roles": ["data"],
      "href": f"{outName}.tif",
      "file:size": size
    }
    },
  "links": [{
    "type": "application/json",
    "rel": "parent",
    "href": "catalog.json"
  }, {
    "type": "application/geo+json",
    "rel": "self",
    "href": f"{outName}.json"
  }, {
    "type": "application/json",
    "rel": "root",
    "href": "catalog.json"
  }]
}
    with open(f'{out_dir}/{outName}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def createStacCatalogRoot(outName) :
    data = {
  "stac_version": "1.0.0",
  "id": "catalog",
  "type": "Catalog",
  "description": "Root catalog",
  "links": [{
    "type": "application/geo+json",
    "rel": "item",
    "href": f"{outName}.json"
  }, {
    "type": "application/json",
    "rel": "self",
    "href": "catalog.json"
  }]
}
    with open(f'{out_dir}/catalog.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    args = sys.argv
    directory = args[1]
    #print(directory)
    files = os.listdir(directory)
    #print(files)
    for file in files:
        if file.endswith(".tif"):
            fileName = file
            #print(fileName)
            break
    dataset = rasterio.open(directory + "/" + fileName)
    #print(dataset.bounds[0], dataset.bounds[1], dataset.bounds[2], dataset.bounds[3])
    #convertFile(directory + "/" + fileName)
    convertTiff(directory + "/" + fileName)
    

