import openeo 
#from openeo import download_results
import json
from openeo.internal.graph_building import PGNode
import sys
from time import sleep
import math


## this script will take as an input a dataset name for EO data available via Google Earth Engine (https://developers.google.com/earth-engine/datasets/catalog), 
## which it will them compute some complex process using OpenEO in-build processes and return the output STAC catelogue item

testing = True

def main(dataName: str, funcName: str, coords: dict, tempExt: [str], outFileName: str):

    print("HERE")
    connection = openeo.connect("https://earthengine.openeo.org")

    connection.authenticate_basic("group11", "test123")

    datacube = connection.load_uploaded_files()

    datacube = connection.load_collection(dataName,
                               spatial_extent=coords,
                               temporal_extent=tempExt,
                               bands=["B4", "B8", "B11"])
    



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
        outFileName = "COPERNICUS/S2_SR_HARMONIZED_".replace("/","-") + funcName + "_applied.tiff"
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
        outFileName = "test"
    
    main(dataSet, funcName, coords, tempExt, outFileName)

