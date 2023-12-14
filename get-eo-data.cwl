cwlVersion: v1.2
s:softwareVersion: 0.1.2

$graph:
  - class: Workflow
    id: run_openeo
    doc: Gathers specified EO data from GEE and applies ndvi process
    label: run OpenEO on Google Earth Engine backend
    inputs:
      dataSet:
        type: string
      funcName:
        type: string
      coords_east:
        type: float
      coords_south:
        type: float
      coords_north:
        type: float
      coords_west:
        type: float
      tempExt:
        type: string[]
      outFileName:
        type: string

    outputs:
      outs:
        type: Directory
        outputSource:
          - get_data/outs

    steps:
      get_data:
        run: "#get_data"
        in:
          dataSet: dataSet
          funcName: funcName
          coords_east: coords_east
          coords_south: coords_south
          coords_north: coords_north
          coords_west: coords_west
          tempExt: tempExt
          outFileName: outFileName
        
        out:
          - outs
        

  - class: CommandLineTool
    id: get_data
    #main(dataSet, funcName, coords, tempExt, outFileName)
    #baseCommand: ["python", "-m", "openeo-func"]
    inputs:
      dataSet:
        type: string
        inputBinding:
          #prefix: --data
          position: 1
      funcName:
        type: string
        inputBinding:
          #prefix: --fn
          position: 2
      coords_east:
        type: float
        inputBinding:
          #prefix: --east
          position: 3
      coords_south:
        type: float
        inputBinding:
          #prefix: --south
          position: 4
      coords_north:
        type: float
        inputBinding:
          #prefix: --north
          position: 5
      coords_west:
        type: float
        inputBinding:
          #prefix: --west
          position: 6
      tempExt:
        type: string[]
        inputBinding:
          #prefix: --tempExt
          position: 7
      outFileName:
        type: string
        inputBinding:
          position: 8
    outputs:
      outs:
        type: Directory
        outputBinding:
          glob: .

    requirements:
      DockerRequirement:
        dockerPull: tjellicoetpzuk/openeo:latest
      NetworkAccess:
        networkAccess: true
        

