cwlVersion: v1.0
$namespaces:
  s: https://schema.org/
schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf
s:softwareVersion: 0.1.2

$graph:
  - class: Workflow
    id: run_openeo
    doc: Gathers specified EO data from GEE and applies ndvi process
    label: run OpenEO on Google Earth Engine backend
    inputs: []

    outputs:
      outs:
        type: Directory
        outputSource:
          - get_data/outs

    steps:
      get_data:
        run: "#get_data"
        in: []
        
        out:
          - outs
        

  - class: CommandLineTool
    id: get_data
    #main(dataSet, funcName, coords, tempExt, outFileName)
    #baseCommand: ["python", "-m", "openeo-func"]
    inputs: []

    outputs:
      outs:
        type: Directory
        outputBinding:
          glob: .

    requirements:
      DockerRequirement:
        dockerPull: tjellicoetpzuk/openeo_testing:latest
      #NetworkAccess:
      #  networkAccess: true
        
