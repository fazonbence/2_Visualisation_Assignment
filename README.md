# 2_Visualisation_Assignment

## Setup
```bash
$ git clone https://github.com/fazonbence/2_Visualisation_Assignment
$ cd 2_Visualisation_Assignment
$ conda env create -f env.yml -n dataviz
$ conda activate dataviz
```

## Start Bokeh server
```bash
$ bokeh serve heart-failure
```

To start the server in development mode (so that Bokeh will reload application on any code change):
```bash
$ bokeh serve heart-failure --dev
```