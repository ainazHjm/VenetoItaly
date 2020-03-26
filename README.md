# Introducing an INSPIRE Motivated Dataset for Predicting Landslides

This repository contains the instructions to download and create a dataset of hdf5 format that can be used to predict landslides. The raw data consists of land cover/land use, bedrock lithology (includes rock-type, rock-age, and rock-family), slope, digital elevation model (DEM), and landslide polygons (labels) for Veneto, a region in Italy. We used INSPIRE terms to label different features that are used in this dataset. To learn more about INSPIRE, refer to https://inspire-geoportal.ec.europa.eu/.

## Requirements
* `numpy`
* `h5py`
* `PIL`

## Step by Step Instructions
1. Download the pre-proccessed dataset from https://drive.google.com/open?id=1tEqHF83ju1ccn3Z75vOXShIWmxVb84FF and extract it (it should be in hdf5 format).
2. Submit a request to download the DEM map by sending an email to `simone.tarquini@ingv.it` with subject *TINITALY DEM*.
3. [Optional] Create a slope map based on the newly downloaded DEM using a GIS software if you want to reproduce the exact dataset proposed in the paper: "Predicting Landslides Using Contour-Aligning Convolutional Neural Networks".
4. Create a folder named *images* in the project repository and place DEM (& slope if you have it) in that folder. Rename it to `DEM.tif` (slope map to `slope.tif`) if it has another name. The maps should be in *.tif* format for the script to work.
5. Run the provided `script.py` with the downloaded dataset path as following:
`python3 script.py --dataset_path <path to the downloaded dataset>`
6. Now, the downloaded dataset is rewritten and updated with the DEM map. You can use it in your experiments.

For more information on hdf5 datasets, refer to http://docs.h5py.org/en/stable/. 

## Dataset Structure
The dataset includes two nested key components:
* *'Veneto/data'*, which is of shape `(n, h, w)` where `n` is the total number of features in the data.
* *'Veneto/gt'*, which includes landslide polygons that can be used as labels and is of shape `(1, h', w')`. This is a binary image; ones show landslides and zeros represent non-landslide points. Out of region areas have a negative value.

The proposed dataset here, contains 94 different features that are labeled based on INSPIRE terms. Except DEM and slope, the rest of the features are binary features representing different classes in bedrock lithology (rock-type, rock-family, and rock-age) and land cover. The detailed information about these features can be found in their corresponding tables under the *tables* folder in the repository. If all the values for a feature are zero in the dataset, it means that feature does not exist in that particular region.

The features with their corresponding feature numbers are stored in `data_dict.json`. You will find feature names such as *litho_44* in it; the number, in this case 44, corresponds to the INSPIRE code assigned to that type of rock, which can be found in the lithology table (`tables/Litho_rocktype_Lookup_Table.xlsx`). All feature names with their corresponding INSPIRE codes are available in the *tables* folder.

## Further Details on Source Files
In this section, we provide more information on source files for each type of feature in the dataset.

### Digital Elevation Model
The DEM map is downloaded by sending an email to `simone.tarquini@ingv.it` with the subject of TINITALY DEM. The resolution of the map is 10 meters. Refer to http://tinitaly.pi.ingv.it/ for more info.

**Terms and Conditions of Use**:
* Data is provided for research purposes only.
* Data is provided solely to the person named on this application form and should not be given to third parties. 
Third parties who might need access to the same dataset are required to fill their own application forms.
* References:
  * [1] Tarquini S., Isola I., Favalli M., Mazzarini F., Bisson M., Pareschi M. T., Boschi E. (2007). TINITALY/01: a new Triangular Irregular Network of Italy, Annals of Geophysics 50, 407 - 425.
  * [2] Tarquini S., Vinci S., Favalli M., Doumaz F., Fornaciai A., Nannipieri L., (2012). Release of a 10-m-resolution DEM for the Italian territory: Comparison with global-coverage DEMs and anaglyph-mode exploration via the web, Computers & Geosciences 38, 168-170. doi:10.1016/j.cageo.2011.04.018.
  * [3] Tarquini S., Nannipieri L.,(2017). The 10 m-resolution TINITALY DEM as a trans-disciplinary basis for the analysis of the italian territory: Current trends and new perspectives, Geomorphology doi: 10.1016/j.geomprph.2016.12.022.
* The aim is to provide scientific information to members of national and international scientific communities. 
The Istituto Nazionale di Geofisica e Vulcanologia assumes no responsibility for the downloaded data, which is not necessarily updated. The global accuracy of the digital elevation model is described in the above reference [1].

### Land Cover
The CORINE land cover classification is used as land cover units in Veneto, Italy. To access the source data
please refer to https://land.copernicus.eu/user-corner/how-to-access-our-data.

**Terms and Conditions of Use**: The Copernicus programme is governed by Regulation (EU) No 377/2014 of the European Parliament and of the Council of 3 April 2014 establishing the Copernicus programme and repealing Regulation (EU) No 911/2010. Within the Copernicus programme, a portfolio of land monitoring activities has been delegated by the European Union to the EEA. The land monitoring products and services are made available through the Copernicus land portal on a principle of full, open and free access, as established by the Copernicus data and information policy Regulation (EU) No 1159/2013 of 12 July 2013. The Copernicus data and information policy is in line with the EEA policy of open and easy access to the data, 
information and applications derived from the activities described in its management plan. For more information, please refer to https://land.copernicus.eu/terms-of-use.

### Bedrock Lithology
The bedrock lithology contains rock-age, rock-family, and rock-type features. The source data can be obtained from the freely available datasets of the Veneto region Geoportal. To download the data, refer to https://idt2.regione.veneto.it/.

**Terms and Conditions of Use**: All the Data and Services present in the Geoportal of the Veneto Region produced by the Regional Structures, by instrumental Bodies of the Region or Local Bodies, are distributed according to the **Italian Open Data License v2.0**. For more information about the license, refer to https://www.dati.gov.it/content/italian-open-data-license-v20.

### Landslide Polygons
The landslides that are identified for Veneto are published as part of the IFFI project. The INSPIRE Natural Hazard Category
Value code list was extended (refer to http://minerva.codes/codelist/NaturalHazardCategoryLandslideExtension for more information) to include the updated Varnes classification of landslide types, and the data are aligned to this standard. 

**Reference**: Hungr, O., Leroueil, S. & Picarelli, L. The Varnes classification of landslide types, an update. Landslides 11, 167–194 (2014). https://doi.org/10.1007/s10346-013-0436-y

**Terms and Conditions of Use**: The data is free to use, modify, and share under CC BY-NC-SA 3.0 IT License. 
For more information refere to https://creativecommons.org/licenses/by-nc-sa/3.0/it/deed.en.

## LICENSE
<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://licensebuttons.net/l/by-nc-sa/3.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/3.0/">Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License</a>.
