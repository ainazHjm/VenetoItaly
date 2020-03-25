# INSPIRE-Based Dataset for Predicting Landslides

This repository contains the instructions to download and create a dataset of hdf5 format that can be used to predict landslides.
The raw data consists of land cover/land use, bedrock lithology (includes rock-type, rock-age, and rock-family), slope, digital elevation model (DEM),
and landslide polygons (labels) for Veneto, a region in Italy. To learn more about INSPIRE, refer to https://inspire-geoportal.ec.europa.eu/.

## Step by Step Instructions (Recommended)

1. Download the pre-proccessed dataset from https://drive.google.com/open?id=1mCkOdh3kAR8JHnAvahXeoosBu5lvVKMS that is in hdf5 format. This dataset consists of two nested keys:
    1. 'Veneto/data', which is of shape (n, h, w) where n is the total number of features in the data. The features include rock-type, rock-age, rock-family, and land cover classes. Refer to tables folder for more information about the features.
    2. 'Veneto/gt', which includes landslide polygons that can be used as labels and is of shape (1, h', w'). This is a binary image; ones show landslides and zeros represent non-landslide points. Out of region areas have a negative value.
2. Submit a request to download the DEM map by sending an email to `simone.tarquini@ingv.it` with a subject of TINITALY DEM.
3. [Optional] Create a slope map based on the newly downloaded DEM using a GIS software.
4. Add the newly downloaded DEM to the current existing hdf5 dataset. If you get the slope map, you will need to add it to the dataset as well:
    1. Create a new empty hdf5 dataset with the same keys (*'Veneto/data'* & *'Veneto/gt'*). The *data* part should have a shape of `(n+1, h, w)` if you only downloaded DEM otherwise, `(n+2, h, w)` to account for both slope and DEM. The *gt* part, ground truth, is the same shape as before.
    2. Copy the *gt* from the previous dataset to the new created hdf5 dataset.
    3. Depending on where you want to put DEM (or both DEM and slope) in the new hdf5 dataset, update the `data_dict.json` file so that it represents your features correctly. In the current existing file, slope is the first feature (0<sup>th</sup> index) and DEM is the last feature (93<sup>th</sup> index).    
    4. After updating `data_dict.json`, copy DEM (or both DEM and slope) to its (their) corresponding position in the new hdf5 dataset. If the index for DEM is `i` in the json file, copy DEM to index `(i, h, w)` in the new hdf5 dataset.    
    5. Copy the rest of the data from the previous hdf5 dataset to the new hdf5 dataset.
    6. The new hdf5 dataset is now ready to be used in your experiments.

For more information on hdf5 datasets, refer to http://docs.h5py.org/en/stable/. You will find feature names such as *litho_44* in `data_dict.json`; the number, in this case 44, corresponds to the INSPIRE code assigned to that type of rock. All feature names with their corresponding INSPIRE codes are available in the *tables* folder.

## Creating the Dataset from Scratch (Not Recommended)
You can also create the dataset from scratch. You need to have all the features that you want to use ready in one folder in .tif format to use this method. Refer to the *Raw Data Instructions* section about the instructions on how to download the data. The current `data_dict.json` file represents 94 features including slope, DEM, rock-type, rock-age, rock-family, and land cover with their corresponding feature numbers, showing their locations in the dataset. You need to update this file if you plan on not choosing some of the features or adding more features.

### Requirements
* `numpy`
* `h5py`
* `PIL`

### Arguments
* `data_dir`: The path to the region's raw image files that we previously downloaded (In our case we only have one region that is Veneto).
* `save_to`: The path to save the hdf5 dataset.
* `feature_num`: The number of total features. The default value is 94 but you can use any number of features that you want.
* `shape`: This argument is an array of form "name,height,width". "name" is the name of the region (e.g. Veneto), "height,width" represents the image shape (all maps/rasters should have the same shape).
* `data_format`: The format of the rasters. The default value is '.tif' and is recommend to use.
* `pad`: The number of pixels used to pad each side of the image. This padding number is used later for loading the data coherently but is not necessary to do. You can pass this to be zero if you do not want to pad your images.

### Run
To get the h5py dataset, simply pass the required arguments and call preprocess.py:

`python3 preprocess.py --data_dir <path to raw data/rasters> --save_to <path to save the hdf5 dataset> --feature_num <feature_num> --shape <region_name,height,width> --data_format <data format> --pad <padding number>`

### Raw Data Instructions
There are three different parts of the data that need to downloaded and rasterized (in a .tif format).

#### Digital Elevation Model
To download the DEM map, you should send an email to `simone.tarquini@ingv.it` with the subject of TINITALY DEM. You will then
receive an email giving the instructions on how to access the data with your own specific username and password. The DEM resolution is 10 meters. For more information on the data, refer to http://tinitaly.pi.ingv.it/.

##### Terms and Conditions of Use:
* Data is provided for research purposes only.
* Data is provided solely to the person named on this application form and should not be given to third parties. 
Third parties who might need access to the same dataset are required to fill their own application forms.
* References:
  * [1] Tarquini S., Isola I., Favalli M., Mazzarini F., Bisson M., Pareschi M. T., Boschi E. (2007). TINITALY/01: a new Triangular Irregular Network of Italy, Annals of Geophysics 50, 407 - 425.
  * [2] Tarquini S., Vinci S., Favalli M., Doumaz F., Fornaciai A., Nannipieri L., (2012). Release of a 10-m-resolution DEM for the Italian territory: Comparison with global-coverage DEMs and anaglyph-mode exploration via the web, Computers & Geosciences 38, 168-170. doi:10.1016/j.cageo.2011.04.018.
  * [3] Tarquini S., Nannipieri L.,(2017). The 10 m-resolution TINITALY DEM as a trans-disciplinary basis for the analysis of the italian territory: Current trends and new perspectives, Geomorphology doi: 10.1016/j.geomprph.2016.12.022.
* The aim is to provide scientific information to members of national and international scientific communities. 
The Istituto Nazionale di Geofisica e Vulcanologia assumes no responsibility for the downloaded data, which is not necessarily updated. The global accuracy of the digital elevation model is described in the above reference [1].

#### Land Cover
The CORINE land cover classification is used as land cover units in Veneto, Italy. To access the data
please refer to https://land.copernicus.eu/user-corner/how-to-access-our-data. It is recommended to used first level land cover maps, consisting of agricultural areas, artificial surfaces, forest and semi-natural areas, water bodies, and wet lands. Each class should be a binary raster in .tif format. You can find more information about the features in the *tables* folder.

##### Terms and Conditions of Use:
The Copernicus programme is governed by Regulation (EU) No 377/2014 of the European Parliament and of the Council of 3 April 2014 establishing the Copernicus programme and repealing Regulation (EU) No 911/2010. Within the Copernicus programme, a portfolio of land monitoring activities has been delegated by the European Union to the EEA. The land monitoring products and services are made available through the Copernicus land portal on a principle of full, open and free access, as established by the Copernicus data and information policy Regulation (EU) No 1159/2013 of 12 July 2013.

The Copernicus data and information policy is in line with the EEA policy of open and easy access to the data, 
information and applications derived from the activities described in its management plan.

For more information, please refer to https://land.copernicus.eu/terms-of-use.

#### Bedrock Lithology
The bedrock lithology contains rock-age, rock-family, and rock-type features. These maps can be obtained from the freely available datasets of the Veneto region Geoportal. To download the data, refer to https://idt2.regione.veneto.it/. Each class should be a binary raster in .tif format. You can find more information about the features in the *tables* folder.

##### Terms and Conditions of Use:
All the Data and Services present in the Geoportal of the Veneto Region produced by the Regional Structures, 
by instrumental Bodies of the Region or Local Bodies, are distributed according to the **Italian Open Data License v2.0**. For
more information about the license, refer to https://www.dati.gov.it/content/italian-open-data-license-v20.

#### Landslide Polygons
The landslides that are identified for Veneto are published as part of the IFFI project. The INSPIRE Natural Hazard Category
Value code list was extended<sup>1</sup> to include the updated Varnes classification of landslide types, and the data are aligned to this standard.

<sup>1</sup> http://minerva.codes/codelist/NaturalHazardCategoryLandslideExtension

##### Reference:
Hungr, O., Leroueil, S. & Picarelli, L. The Varnes classification of landslide types, an update. Landslides 11, 167–194 (2014). https://doi.org/10.1007/s10346-013-0436-y

##### Terms and Conditions of Use:
The data is free to use, modify, and share under CC BY-NC-SA 3.0 IT License. 
For more information refere to https://creativecommons.org/licenses/by-nc-sa/3.0/it/deed.en.

## LICENSE
<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://licensebuttons.net/l/by-nc-sa/3.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/3.0/">Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License</a>.
