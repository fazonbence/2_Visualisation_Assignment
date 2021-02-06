# 2IMV20 Visualization - Information Visualization and Interaction Assignment 

## Setup

### Python environment
```bash
$ git clone https://github.com/fazonbence/2_Visualisation_Assignment
$ cd 2_Visualisation_Assignment
$ conda env create -f env.yml -n dataviz
$ conda activate dataviz
```

### Download images
Tissue images are stored in this [Google Drive folder](https://drive.google.com/drive/folders/1uwxa6H4jQVrVnEJQdfYQOnSoURxdYiOx?usp=sharing). 

Download them and put them in the `heart-failure/static/tiles_flat` folder.

## Start Bokeh server
```bash
$ bokeh serve heart-failure
```

To start the server in development mode (so that Bokeh will reload application on any code change):
```bash
$ bokeh serve heart-failure --dev
```