# INSPIRE-Based Dataset for Predicting Landslides

This repository contains the instructions to download and create a dataset of hdf5 format that can be used to predict landslides.
The raw data consists of land cover/land use, bedrock lithology (includes rock-type, rock-age, and rock-family), slope, digital elevation model (DEM),
and landslide polygons (labels) for Veneto, a region in Italy. The whole data is based on INSPIRE (Infrastructure for Spatial Information in Europe).
To learn more about INSPIRE, refer to https://inspire-geoportal.ec.europa.eu/.

Since there are copy right issues for the Digital Elevation Map, we cannot release the whole processed hdf5 dataset but to make thigs faster, we created the hdf5 dataset for all other features (land cover and bedrock lithology including rock-type, rock-age, and rock-family) that can be shared (The license is provided for each feature in its section). This dataset is available here: https://drive.google.com/open?id=1mCkOdh3kAR8JHnAvahXeoosBu5lvVKMS. Then, the only thing you need to do is to get the DEM map as mentioned in Digital Elevation Model section and add it to your the provided hdf5 dataset. It should be straight-forward.

You also have the option of downloading all of the raw data, depending on which features you want to use and create the hdf5 dataset based on the script provided in this repository (refer to the main dataset section here).

## Requirements
* `numpy`
* `h5py`
* `PIL`

## Raw Data Instructions

There are three different parts of the data that need to downloaded. They are in GIS format and should be rasterized (in a .tif format).
This state should be straight forward using a GIS software (e.g. QGIS).

### Digital Elevation Model
To download the DEM map, you should send an email to `simone.tarquini@ingv.it` with the subject of TINITALY DEM. You will then
receive an email giving the instructions on how to access the data with your own specific username and password. The DEM resolution
is 10 meters. For more information on the data, refer to http://tinitaly.pi.ingv.it/. It should be easy to get the slope map/raster based on the DEM map/raster using a GIS software.

#### Terms and Conditions of Use:
* Data is provided for research purposes only.
* Data is provided solely to the person named on this application form and should not be given to third parties. 
Third parties who might need access to the same dataset are required to fill their own application forms.
* References:
  * [1] Tarquini S., Isola I., Favalli M., Mazzarini F., Bisson M., Pareschi M. T., Boschi E. (2007). TINITALY/01: a new Triangular Irregular Network of Italy, Annals of Geophysics 50, 407 - 425.
  * [2] Tarquini S., Vinci S., Favalli M., Doumaz F., Fornaciai A., Nannipieri L., (2012). Release of a 10-m-resolution DEM for the Italian territory: Comparison with global-coverage DEMs and anaglyph-mode exploration via the web, Computers & Geosciences 38, 168-170. doi:10.1016/j.cageo.2011.04.018.
  * [3] Tarquini S., Nannipieri L.,(2017). The 10 m-resolution TINITALY DEM as a trans-disciplinary basis for the analysis of the italian territory: Current trends and new perspectives, Geomorphology doi: 10.1016/j.geomprph.2016.12.022.
* The aim is to provide scientific information to members of national and international scientific communities. 
The Istituto Nazionale di Geofisica e Vulcanologia assumes no responsibility for the downloaded data, which is not necessarily updated. 
The global accuracy of the digital elevation model is described in the above reference [1]. 
Nevertheless, we cannot exclude the presence of local higher errors.

### Land Cover
The CORINE land cover classification is used as land cover units in Veneto, Italy. To access the data
please refer to https://land.copernicus.eu/user-corner/how-to-access-our-data. For our purpose, we have used the first level land covers,
consisting of agricultural areas, artificial surfaces, forest and semi-natural areas, water bodies, and wet lands. Make sure you download
these classes. Each class is also assigned a code which is used to represent its feature name in the final dataset (refer to the following table).
You need to convert each land cover class to a binary raster (preferably 0 and 1) where the out of region areas are represented
with a negative number.
| class                     | code |
| --------------------------|:-----|
|Agricultural Areas         | 1    |
|Artificial Surfaces        | 2    |
|Forest & Semi-Natural Areas| 3    |
|Water Bodies               | 4    |
|Wet Lands                  | 5    |

#### Terms and Conditions of Use:
The Copernicus programme is governed by Regulation (EU) No 377/2014 of the European Parliament and of the Council of 3 April 2014 
establishing the Copernicus programme and repealing Regulation (EU) No 911/2010. 
Within the Copernicus programme, a portfolio of land monitoring activities has been delegated by the European Union to the EEA.
The land monitoring products and services are made available through the Copernicus land portal on a principle of full, open and
free access, as established by the Copernicus data and information policy Regulation (EU) No 1159/2013 of 12 July 2013.

The Copernicus data and information policy is in line with the EEA policy of open and easy access to the data, 
information and applications derived from the activities described in its management plan.

For more information, please refer to https://land.copernicus.eu/terms-of-use.

### Bedrock Lithology
The bedrock lithology contains rock-age, rock-family, and rock-type features. These maps can be obtained from the freely available
datasets of the Veneto region Geoportal. To download the data, refer to https://idt2.regione.veneto.it/. As in the previous section,
the data should be converted to binary rasters using a GIS software. For our of the region values, use a negative number as before.
Download `Litho_rocktype_Lookup_Table.xlsx`, `Litho_Family_Lookup_Table.xlsx`,
and `Litho_Age_Lookup_Table.xlsx` tables to access class names along with their correspnding codes.

#### Terms and Conditions of Use:
All the Data and Services present in the Geoportal of the Veneto Region produced by the Regional Structures, 
by instrumental Bodies of the Region or Local Bodies, are distributed according to the **Italian Open Data License v2.0**. For
more information about the license, refer to https://www.dati.gov.it/content/italian-open-data-license-v20.

### Landslide Polygons
The landslides that are identified for Veneto are published as part of the IFFI project. The INSPIRE Natural Hazard Category
Value code list was extended to include the updated Varnes classification of landslide types, and the data are aligned to this standard.
We used all landslide polygons available for Veneto to create the lables in the dataset. The data should be converted into one single
binary raster using GIS software.

#### Reference:
Hungr, O., Leroueil, S. & Picarelli, L. The Varnes classification of landslide types, an update. Landslides 11, 167–194 (2014). https://doi.org/10.1007/s10346-013-0436-y

#### Terms and Conditions of Use:
The data is free to use, modify, and share under CC BY-NC-SA 3.0 IT License. 
For more information refere to https://creativecommons.org/licenses/by-nc-sa/3.0/it/deed.en.

## How to Create hdf5 Dataset
The hdf5 datasets that are created in this repository are used to train the models proposed by the paper: "Predicing Landslides Using Contour-Aligning Convolutional Neural Networks". However, the data can be used for training any other type of model.

### Main Dataset
The main dataset, consisting of 94 features in total (DEM, land cover, rock type, rock age, rock family, and slope), can be used for any type of model. All the features in the dataset with their corresponding feature number in the data are stored in 
the `data_dict.json` file.

#### Arguments
* `data_dir`: The path to the region's raw image files that we previously downloaded (In our case we only have one region that is Veneto).
* `save_to`: The path to save the hdf5 dataset.
* `feature_num`: The number of total features. The default value is 94 but you can use any number of features that you want.
* `shape`: This argument is an array of form "name,height,width". "name" is the name of the region (e.g. Veneto), "height,width" represents the image shape (all maps/rasters should have the same shape).
* `data_format`: The format of the rasters. The default value is '.tif' and is recommend to use.
* `pad`: The number of pixels used to pad each side of the image. This padding number is used later for loading the data coherently but is not necessary to do. You can pass this to be zero if you do not want to pad your images.

#### Run
To get the h5py dataset, simply pass the required arguments and call preprocess.py:

`python3 preprocess.py --data_dir <path to raw data/rasters> --save_to <path to save the hdf5 dataset> --feature_num <feature_num> --shape <region_name,height,width> --data_format <data format> --pad <padding number>`

**The hdf5 dataset contains feature maps in `['<RegionName>/data']` and groundtruth/labels in `['<RegionName>/gt']`. In this case, region name is Veneto.**

### Dist Dataset
This dataset is specifically for the LACNN model proposed in paper: "Predicing Landslides Using Contour-Aligning Convolutional Neural Networks". Only create this dataset if you want to re-implement or build on the LACNN model. Otherwise, use the main dataset.

#### Arguments
* `data_path`: The path to the main dataset of hdf5 format (This data can be generated from previous section).
* `dist`: The distances that are going to be looked at in order to find the features at highest elevation value (refer to Figure 1 in the paper).
* `region`: The name of the region you got the data for. In our case it is Veneto.
* `save_to`: The path to save the new dataset.
* `pad`: The padding number to pad the data with.
* `features`: This argument is an array of integers that show which features you want to extract when you find the highest elevation value at some distance. The deafult value is chosen based on the weights of a linear regression model (top 21 features are chosen).

#### Run
To create the dist dataset, simply run find_dist_features.py with the arguments specified in the arguments section. The code uses a lot of memory if the distances are big. The current code only contains masks for 30, 100, and 300 pixels (x10 meters). If your memory is below 32G, only run it with `--dist 30`.

### Extra Links:
Further documentation on how to use hdf5 with python: http://docs.h5py.org/en/stable/

## LICENSE
<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://licensebuttons.net/l/by-nc-sa/3.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/3.0/">Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License</a>.
