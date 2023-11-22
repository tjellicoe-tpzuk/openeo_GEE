cwlVersion: v1.2

class: CommandLineTool
id: "get_eo_data"
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
    dockerPull: getopeneo:latest
  NetworkAccess:
    networkAccess: true
    

