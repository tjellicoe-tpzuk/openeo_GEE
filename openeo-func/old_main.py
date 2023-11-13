import openeo
import json
from openeo.internal.graph_building import PGNode
#from ee import normalised_difference
import sys
from time import sleep
import math


## this script will take as an input a STAC catelogue of EO data, which it will them compute some complex process using OpenEO in-build processes and return the output STAC catelogue item

testing = False #True

# def abs(x:float):
#     return abs(x)


def main(dataName: str, funcName: str, coords: dict, tempExt: [str], outFileName: str):

    try:
        connection = openeo.connect("https://earthengine.openeo.org")
    except:
        raise Exception("fail")
    
    connection.authenticate_basic("group11", "test123")
    #print(connection.list_processes())

    #json_object = json.dumps(connection.list_processes(), indent=2)

    #with open("available_processes.json", "w") as outfile:
    #    outfile.write(json_object)

    ## add exception to determine whether required bands are present in selected dataset
    print(coords)

    datacube = connection.load_collection(dataName,
                               spatial_extent=coords,
                               temporal_extent=tempExt,
                               bands=["B4", "B8", "B11"])


    B4 = datacube.band("B4")
    B8 = datacube.band("B8")
    
    ## This function doesn't seem to work, as bands cannot be found? Possible issue in source code: https://github.com/Open-EO/openeo-earthengine-driver/blob/master/src/processes/rename_dimension.js
    ## sends error if it find the source name, while it should only error if the opposite is true?
    #datacube = datacube.rename_dimension(source="bandss", target="wavelengths")

    #B4 = datacube.band("B4")

    ## Defining Process Graph Nodes to extract array elements (here bands) and calculate NVDI.
    red = PGNode("array_element", arguments={"data": {"from_parameter": "data"}, "label": "B4"})
    nir = PGNode("array_element", arguments={"data": {"from_parameter": "data"}, "label": "B8"})
    swir = PGNode("array_element", arguments={"data": {"from_parameter": "data"}, "label": "B11"})

    absol = PGNode("absolute", arguments={"data": {"from_parameter": "data"}})

    datacube_abs = datacube.apply("absolute")
    datacube_abs = datacube_abs.save_result(format="GTIFF-THUMB")
    job = datacube_abs.create_job()
    job.start_and_wait().download_results(f"output_files/testing_abs")

    ndvi = PGNode("normalized_difference", arguments={"x": {"from_node": nir}, "y": {"from_node": red}})
    ndwi = PGNode("normalized_difference", arguments={"x": {"from_node": nir}, "y": {"from_node": swir}})

    if funcName == "ndvi":
        datacube = datacube.reduce_dimension(dimension="bands2", reducer=ndvi)
    elif funcName == "ndwi":
        datacube = datacube.reduce_dimension(dimension="bands2", reducer=ndwi)
    else:
        raise Exception("function not supported (yet!!)", funcName)
    



    #datacube = datacube.process(process_id="normalized_difference",
    #                            arguments={
    #                                "data": "datacube",
    #                                "nir": "B8",
    #                                "red": "B4"
    #                            })
    
    ## This only works for a single band inputs, e.g. "VV"
    # march = datacube.filter_temporal("2017-03-01", "2017-04-01")
    # april = datacube.filter_temporal("2017-04-01", "2017-05-01")
    # may = datacube.filter_temporal("2017-05-01", "2017-06-01")

    # # Now that we split it into the correct time range, we have to aggregate the timeseries values into a single image.
    # # Therefore, we make use of the Python Client function `mean_time`, which reduces the time dimension, 
    # # by taking for every timeseries the mean value.

    # mean_march = march.mean_time()
    # mean_april = april.mean_time()
    # mean_may = may.mean_time()

    # # Now the three images will be combined into the temporal composite. 
    # # Before merging them into one datacube, we need to rename the bands of the images, because otherwise, 
    # # they would be overwritten in the merging process.  
    # # Therefore, we rename the bands of the datacubes using the `rename_labels` process to "R", "G" and "B".
    # # After that we merge them into the "RGB" datacube, which has now three bands ("R", "G" and "B")

    # R_band = mean_march.rename_labels(dimension="bands", target=["R"])
    # G_band = mean_april.rename_labels(dimension="bands", target=["G"])
    # B_band = mean_may.rename_labels(dimension="bands", target=["B"])

    # RG = R_band.merge_cubes(G_band)
    # RGB = RG.merge_cubes(B_band)

    # kernel = [[0,0,0,1,0,0,0],
    #           [0,0,0,1,0,0,0],
    #           [0,0,0,1,0,0,0],
    #           [1,1,1,1,1,1,1],
    #           [0,0,0,1,0,0,0],
    #           [0,0,0,1,0,0,0],
    #           [0,0,0,1,0,0,0]
    #          ]

    ## Kernel not supported by Google Earth Engine
    #RGB = RGB.apply_kernel(kernel, 10)

    # Last but not least, we add the process to save the result of the processing. There we define that 
    # the result should be a GeoTiff file.
    # We also set, which band should be used for "red", "green" and "blue" color in the options.

    datacube = datacube.save_result(format="GTIFF-THUMB")
    job = datacube.create_job()
    job.start_and_wait().download_results(f"output_files/{outFileName}")

    #datacube_ndwi = datacube_ndwi.save_result(format="GTIFF-THUMB")
    #job = datacube_ndwi.create_job()
    #job.start_and_wait().download_results("output_files_ndwi")
    # With the last process we have finished the datacube definition and can create and start the job at the back-end.

    #job.get_results()


if __name__ == "__main__":
    #main("COPERNICUS/S1_GRD", "ndvi")

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

    #for (index, inp) in enumerate(args):
    #    print(str(index) + " " + inp)
    
    main(dataSet, funcName, coords, tempExt, outFileName)