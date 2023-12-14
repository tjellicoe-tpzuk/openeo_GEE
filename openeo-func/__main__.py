import openeo 
#from openeo import download_results
import json
from openeo.internal.graph_building import PGNode
import sys
from time import sleep
import math
import os
import time
import mimetypes
import datetime as dt

out_dir = os.getcwd()

## this script will take as an input a dataset name for EO data available via Google Earth Engine (https://developers.google.com/earth-engine/datasets/catalog), 
## which it will them compute some complex process using OpenEO in-build processes and return the output STAC catelogue item

testing = False #True

def main(dataName: str, funcName: str, coords: dict, tempExt: [str], outFileName: str="output_file"):

    outName = outFileName

    print("HERE")
    connection = openeo.connect("https://earthengine.openeo.org")

    connection.authenticate_basic("group11", "test123")

    datacube = connection.load_collection(dataName,
                               spatial_extent=coords,
                               temporal_extent=tempExt,
                               bands=["B4", "B8", "B11"])

    B4 = datacube.band("B4")
    B8 = datacube.band("B8")

    ## Defining Process Graph Nodes to extract array elements (here bands) and calculate NVDI.
    red = PGNode("array_element", arguments={"data": {"from_parameter": "data"}, "label": "B4"})
    nir = PGNode("array_element", arguments={"data": {"from_parameter": "data"}, "label": "B8"})
    swir = PGNode("array_element", arguments={"data": {"from_parameter": "data"}, "label": "B11"})

    ndvi = PGNode("normalized_difference", arguments={"x": {"from_node": nir}, "y": {"from_node": red}})
    ndwi = PGNode("normalized_difference", arguments={"x": {"from_node": nir}, "y": {"from_node": swir}})

    if funcName == "ndvi":
        datacube = datacube.reduce_dimension(dimension="bands", reducer=ndvi)
    elif funcName == "ndwi":
        datacube = datacube.reduce_dimension(dimension="bands", reducer=ndwi)
    else:
        raise Exception("function not supported (yet!!)", funcName)

    datacube = datacube.save_result(format="GTIFF-THUMB")
    job = datacube.create_job()
    outputResults = job.start_and_wait()
    outputResults.download_results(f"{out_dir}/{outName}.tif")
    createStac(outName)
    print("To see your results open https://hub.openeo.org/")

    
## This needs to be created correctly in future
def createStac(outName):
    createStacItem(outName)
    createStacCatalogRoot(outName)

def createStacItem(outName) :
    now = time.time_ns()/1_000_000_000
    dateNow = dt.datetime.fromtimestamp(now)
    dateNow = dateNow.strftime('%Y-%m-%dT%H:%M:%S.%f') + "Z"
    size = os.path.getsize(f"{outName}.tif")
    mime = mimetypes.guess_type(f"{outName}.tif")[0]
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
    print("created")


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
    if testing:
        dataSet = "COPERNICUS/S2_SR_HARMONIZED"
        funcName = "ndvi"
        coords = {
            "west": -3.33,
            "north": 52.56,
            "east" : 1.25,
            "south" : 50.98
        }
        tempExt = ["2017-06-01", "2017-07-01"]
        outFileName = f"{dataSet}_".replace("/","-") + funcName + "_applied.tiff"
    else:
        args = sys.argv
        dataSet = args[1]
        funcName = args[2]
        n = 3
        coords = {
            "west": float(args[n+3]),
            "north": float(args[n+2]),
            "east" : float(args[n]),
            "south" : float(args[n+1])
        }
        tempExt = [args[7], args[8]]
        outFileName = args[9]
    
    main(dataSet, funcName, coords, tempExt, outFileName)
