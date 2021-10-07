# Resources

* [Indy Data Portal](https://data.indy.gov/) - Data released to the public from the City of Indianapolis
    * [IndyPoliceBeats](https://data.indy.gov/datasets/indypolicebeats/explore) - Shapefile that contains breakdowns of all the police beats for Marion County. Beat ED51 errored for me in QGIS, so I have a [fixed](https://www.qgistutorials.com/en/docs/3/handling_invalid_geometries.html) version of this in `./shapefiles`
* [Crime Analysis Basics - YouTube](https://www.youtube.com/watch?v=917x-eD-K9o) - video from the 2019 Law Enforcement Symposium in New York. This video discusses three main forms of Crime Analysis: Administrative, Strategic, Tactical
* [Crime Analyst Tool Bar and ArcGIS Panel - YouTube](https://www.youtube.com/watch?v=hvoSPgOhorM&t=3430s) - video from the 2019 Law Enforcement Symposium in New York. This video encompasses a wealth of information about features in ArcGIS Pro, mainly geared towards the Crime Analysis add-on, which is packed full of tools
* [IMPD - CityProtect](https://cityprotect.com/agency/impd) - Data hub for incident data for IMPD on CityProtect
    * NOTE: While you can download bulk data from here, it misses crucial information. I wrote a custom python script in `./scripts` to download incident data from CityProtect's public (undocumented) API with lat & lng for use in GIS software
* [Seattle Crime Data 2008-Present](https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5) - Large CSV file with over 900k records for incidents in Seattle
