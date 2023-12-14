cwlVersion: v1.0
s:softwareVersion: 0.1.2

$graph:
  - class: Workflow
    id: download_and_run_ndvi
    doc: Gathers specified EO data from GEE and then uses previous s_expression cwl tool to apply ndvi processing
    label: run OpenEO on Google Earth Engine backend to extract data and then compute ndvi
    requirements:
    - class: ScatterFeatureRequirement
    inputs:
      dataSet:
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
      s_expression:
        doc: s expression
        label: s expression
        type: string #[]

    outputs:
      outs:
        type: Directory
        outputSource:
          - comp_ndvi/outs

    steps:
      get_data:
        run: "#get_data"
        in:
          dataSet: dataSet
          coords_east: coords_east
          coords_south: coords_south
          coords_north: coords_north
          coords_west: coords_west
          tempExt: tempExt
        out:
          - outs

      comp_ndvi:
        run: "#comp_ndvi"
        #scatter: [input_reference, s_expression]
        #scatterMethod: flat_crossproduct
        in:
          input_reference:
            source: get_data/outs
          s_expression: s_expression
        out:
          - outs

  - class: CommandLineTool
    id: get_data
    #main(dataSet, funcName, coords, tempExt, outFileName)
    #baseCommand: ["python", "-m", "openeo-load_local"]
    inputs:
      dataSet:
        type: string
        inputBinding:
          #prefix: --data
          position: 1
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

    outputs:
      outs:
        type: Directory
        outputBinding:
          glob: .

    requirements:
      DockerRequirement:
        dockerPull: tjellicoetpzuk/openeo_load_local:latest

  - class: CommandLineTool
    id: comp_ndvi
    #main(dataSet, funcName, coords, tempExt, outFileName)
    baseCommand: s-expression
    arguments:
    - --input_reference
    - valueFrom: $( inputs.input_reference )
    - --s-expression
    - valueFrom: ${ return inputs.s_expression.split(":")[1]; }
    - --cbn
    - valueFrom: ${ return inputs.s_expression.split(":")[0]; }
    inputs:
      input_reference:
        type: Directory # need to find tif file in here
        inputBinding:
          position: 1
      s_expression:
        type: string
    outputs:
      outs:
        type: Directory
        outputBinding:
          glob: .

    requirements:
      DockerRequirement:
        dockerPull: eoepca/s-expression:dev0.0.2 # eoepca/snuggs:0.3.0
      ResourceRequirement: {}
      InlineJavascriptRequirement: {}
      EnvVarRequirement:
        envDef:
          PATH: /srv/conda/envs/env_app_snuggs/bin:/srv/conda/bin:/srv/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

          
