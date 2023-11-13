# OpenEO Project To Load And Process EO Datasets

## First project using OpenEO and Google Earth Engine backend to extract and process data from Google Earth Engine observation data using Common Workflow Language and Python OpenEO Client

This project has been created following the OpenEO documentation for the [Python client](https://openeo.org/documentation/1.0/python/) to compute the NDVI and NDWI values across a dataset. 
A process graph is constructed using the GEE backend and this is then processed and the output saved to the local computer as a tif file. This file can then be opened for further analysis in QGIS or other applications with tif file support. For simplicity the entire application can be run via a command line tool (get-eo-data.cwl).

## How to use this application
The application is run using a CWL Runner while passing in the required inputs. The inpuy.yml file is provided as an example input and this will set up the application to request data from the Sentinel 2 data available via the [Google Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets/catalog)
To run this application use a cwl runner (e.g. cwltool) and call the get-eo-data.cwl file with the inputs as specified in the `input.yml` file:
`cwltool get-eo-data.cwl input.yml`
Or in a more general format:
`<your_cwl_runner> get-eo-data.cwl <your_yml_file.yml>`
You can also provide the inputs on the command line itself (DO NOT USE, for example only):
`cwltool get-eo-data.cwl --coords_west -3.33 --coords_east 1.25 --coords_north 52.56 --coords_south 50.98 --dataSet "COPERNICUS/S2_SR_HARMONIZED" --funcName "ndvi" --outFileName "COPERNICUS-S2_SR_HARMONIZED_ndvi_applied" --tempExt "2017-06-01","2017-07-01"` - **note, this currently doesn't work as the final string element is passed incorrectly into the Python script**

## Further work on this project
The next step is to integrate this with an EOEPCA application package so that this can be run via the ADES allowing for further integration between the two applications

## Other links
More information about the GEE backend for OpenEO can be found on the [GitHub for that project](https://github.com/Open-EO/openeo-earthengine-driver)
More information on the OpenEO Python Client can be found [here](https://openeo.org/documentation/1.0/python/#installation)
