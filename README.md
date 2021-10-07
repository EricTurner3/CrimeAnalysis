# Crime Analysis

Code, Data and Analysis regarding Crime & Intelligence Analysis, some data may be from my hometown of Indianapolis, and others may be of other publicly available sources.
---
## Repo Overview
* `/data`: Data files such as incidents or extracted data from GIS ready to be moved into other applications such as Excel
* `/examples`: Example analyses done
* `/scripts`: Any scripts used, currently there is a Python script for extracting the incident report data from CityProtect
* `/shapefiles`: Shapefiles used or created in GIS software
* `/visuals`: Charts and images that may be used in the example analyses files
* `impd_analysis.qgz`: My QGIS project file used for the stuff in this repo
* `Resources.md`: Helpful links that I have found that I am saving for anyone else that is curious
---
## Gathering Data
As a public citizen, I do not have access to the same level of information as actual city or public safety employees. For public use, IMPD stores crime data in CityProtect. There is a way to download bulk data from CityProtect natevely, however it misses the crucial lat & lng coordinates we need for importing into GIS software. I wrote a custom python script to use the same API the CityProtect app does to display incidents on its map.
* Run the `./scripts/impd_incidents_retrieval.py` script. Modify the begin and end dates as needed.

---
## Importing into GIS

I use QGIS because it is free and open source. Once the data is gathered, do the following:
* Ensure CRS is set to WGS 84 (EPSG:4326)
* Download police beats shapefile from https://data.indy.gov/datasets/indypolicebeats/explore and import
    * Beat ED51 was invalid in QGIS so I followed the guide [here](https://www.qgistutorials.com/en/docs/3/handling_invalid_geometries.html) to fix it. I have saved the fixed shapefile in `./shapefiles`
* Import the .csv from the PY script as a delimited text layer. Use Point Definition for Geometry and use lng as X and lat as Y.
    * The script includes categories so the dots can be recolored according to type, the parentIncidentType seems to be the best for categories.
    * Also, creating a spatial index for the point layer can help with analysis

