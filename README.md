[![DOI](https://zenodo.org/badge/xxxx.svg)](https://zenodo.org/doi/10.5281/zenodo.xxxx)


# Oelsmann-etal_2026_NatComm

**Subsidence more than doubles sea-level rise today along densely populated coasts**


## Author Information

Julius Oelsmann<sup>1,2*</sup>, Robert J. Nicholls<sup>3,4</sup>, Daniel Lincke<sup>5</sup>, Marta Marcos<sup>6</sup>, Manoochehr Shirzaei<sup>7</sup>, Laura Sánchez<sup>1</sup>, Leonard Ohenhen<sup>8</sup>, Denise Dettmering<sup>1</sup>, Jochen Hinkel<sup>5,9</sup>, Benjamin P. Horton<sup>10</sup>, Florian Seitz<sup>1</sup>

<sup>1</sup> Deutsches Geodätisches Forschungsinstitut, Technische Universität München, Arcisstraße 21 80333 München, Germany  
<sup>2</sup> Department of River-Coastal Science and Engineering, Tulane University, 6823 St. Charles Avenue, New Orleans, LA 70118, USA, Email: joelsmann@tulane.edu  
<sup>3</sup> Tyndall Centre for Climate Change Research, University of East Anglia, Norwich, UK  
<sup>4</sup> School of Engineering, University of Southampton, Southampton, SO17 1BJ, UK  
<sup>5</sup> Global Climate Forum, Neue Promenade 6, 10178 Berlin, Germany  
<sup>6</sup> IMEDEA, (UIB-CSIC), Miquel Marquès, 21, Esporles, 07190, Balearic Islands, Spain  
<sup>7</sup> Department of Geosciences, Virginia Tech, Blacksburg, VA, USA.; Virginia Tech National Security Institute, Virginia Tech, Blacksburg, VA, USA. Institute for Water, Environment and Health, United Nations University, Hamilton, Ontario, Canada.  
<sup>8</sup> University of California, Department of Earth System Science, Irvine, CA, USA  
<sup>9</sup> Resource Economics Group, Albrecht Daniel Thaer-Institute and Berlin Workshop in Institutional Analysis of Social-Ecological Systems (WINS), Humboldt-Universität zu Berlin, Germany  
<sup>10</sup> School of Energy and Environment, City University of Hong Kong, Hong Kong SAR  

### Corresponding author

Correspondence to: *Julius Oelsmann*, joelsmann@tulane.edu; julius.oelsmann@tum.de

## Abstract

Coastal subsidence can substantially increase rates of relative sea-level (RSL) rise beyond the climate-change induced variations. However, there is currently low confidence in vertical land motion (VLM) estimates and hence its effect on RSL rise. To address this problem, we synergize diverse multi-technique VLM data to investigate the impact of VLM on RSL rise at the highest possible spatial resolution. Our high-resolution VLM estimates now cover almost 65% of the coastal population, and are key to resolve small scale subsidence, including East, South, and Southeast Asian cities and populated deltaic regions, which have been largely not covered by earlier geodetic measurements. We find that the average modern (1995-2019) global RSL rise experienced by coastal populations (6 mm/year) is at minimum three times as large as the currently estimated average coastal RSL change (2.1 mm/year), and twice as large as the climate-driven absolute sea-level rise. This reflects a strong tendency for higher rates of subsidence in densely populated areas such that 55% (43%) of the global coastal population experiences subsidence rates of at least 1 (2) mm/year. Paired with ongoing community efforts to extend consistent observations, these data are essential to ensure reliable estimates of present and future RSL rise to support risk and adaptation assessment.


## Journal reference
_To be added upon publication._


## Data reference

### Input data


Please download the following datasets and place them in their respective subfolders under `input_data/`:

- `input_data/OE24/`  
  The global VLM reconstruction from Oelsmann et al., 2024 [OE24] is available at  
  https://zenodo.org/records/8308347

- `input_data/NGL_GNSS/`  
  GNSS VLM data [Blewitt et al., 2018] are available at  
  https://geodesy.unr.edu/velocities/midas.IGS14.txt

- `input_data/InSAR_EU/`  
  InSAR VLM estimates for Europe can be downloaded from the EGMS data explorer:  
  https://egms.land.copernicus.eu/

  Note, that this dataset can so far only be downloaded by selecting tiles manually. 

- `input_data/InSAR_US/`  
  InSAR VLM data for the US [Ohenhen et al., 2024] are provided for different regions:  
  - Pacific coast: https://doi.org/10.7294/17711000  
  - Atlantic coast: https://doi.org/10.7294/19350959  
  - Gulf coast: https://doi.org/10.7294/22731326

- `input_data/InSAR_Cities/`  
  The InSAR city subsidence data from Shirzaei et al., 2024 are available at:  
  https://data.lib.vt.edu/articles/dataset/InSAR-Based_Coastal_Land_Subsidence/25864435/1

- `input_data/InSAR_Tay/`
   Download data from Tay et al., 2022 from:
   https://researchdata.ntu.edu.sg/dataset.xhtml?persistentId=doi:10.21979/N9/GPVX0F
   (Note that this data is only needed for obtaining a list of some of the largest coastal cities)

- `input_data/Mississippi_Delta/`  
  Delta InSAR data from Nienhuis and Törnqvist, 2017 are available at:  
  https://osf.io/m83z4/files/osfstorage

- `input_data/InSAR_Deltas/`  
  The delta-subsidence data from Ohenhen et al., 2025 / Ohenhen et al., 2026 are available at Zenodo:  
  https://doi.org/10.5281/zenodo.15015923

- `input_data/InSAR_China/`  
  Subsidence data for Chinese cities [Ao et al., 2024] can be obtained from:  
  https://www.science.org/doi/10.1126/science.adl4366#supplementary-materials

- `input_data/Caron2018/`  
  The GIA estimates contained in the VLM data are available at:  
  https://vesl.jpl.nasa.gov/solid-earth/gia/

- `input_data/CMEMS/`  
  The ASLC data were obtained from:  
  https://data.marine.copernicus.eu/product/SEALEVEL_GLO_PHY_L4_MY_008_047/description

- `input_data/Nicholls2021/`  
  The information on the coastal segments of the DIVA model (location, population, length) and the VLM estimates of NI21b can be obtained from the source files provided at:  
  https://www.nature.com/articles/s41558-021-00993-z#Sec16


## Notes:

- Most of these datasets have been interpolated on the high-resolution DIVA coastal grid (see Methods).
- The original datasets are not published in this repositories, but are available in their original repositories
- The EGMS data needs to be downloaded manually. The converted *netcdf file can be obtained from the author on request.
- Efforts to make these datasets more accesible are underway!
- Some of the datasets are also important for plotting Figure 1.



### Output data

Output Data is provided on zenodo and at : ./scripts/data/


| description | size | filename |
| --- | --- | --- |
|VLM data in large coastal cities |4.0K|	`City_VLM_comparison.csv`|
|VLM data in large coastal cities with additional information |16K|	`City_VLM_comparison.xlsx`|
|Global VLM estimates on DIVA grid (main file) |1.7M|	`Global_VLM_data_Oelsmann_2025_data_supplement.nc`|
|VLM data in deltas (averages) |16K|	`SI_Deltas_overview.xlsx`|


## Contributing modeling software

We recommend using a dedicated Conda environment for this repository.

### Requirements

- Conda
- Python 3.6.10

### 1. Create the environment

Create the Conda environment from the provided `environment.yml` file:

```bash
conda env create -f environment.yml
conda activate sl_iq
```

### 2. Install additional required packages

Install `sealeveltools` from GitHub:

```bash
pip install git+https://github.com/oelsmann/sea_level_tool.git@master#egg=sealeveltools
```

Install `cartopy` from conda-forge if needed:

```bash
conda install -c conda-forge cartopy
```


### 3. Verify the installation

Start Python, Jupyter Notebook, or JupyterLab within the activated environment and confirm that the required packages import without error.

### Notes

* The `environment.yml` file contains the main package requirements for this repository.
* Geospatial packages such as `cartopy`, `geopandas`, and `rasterio` are generally installed most reliably through `conda-forge`.
* The `sealeveltools` package must currently be installed manually from GitHub.


## Reproduce my experiment


1. Install the software components required to conduct the experiment from [contributing modeling software](#contributing-modeling-software)
2. Download and install the supporting [input data](#input-data) required to conduct the experiment
3. Run the following scripts in the `scripts` directory to compare my outputs to those from the publication

| Script Name | Description | How to Run |
| --- | --- | --- |
| 1_estimate_china_VLM.ipynb | script to map china csv city averages to DIVA rgid | execute in jp-notebook|
| 2_combine_VLMsources_globally.ipynb | script to combine VLM data from OE24, GIA, EU, USA, New Zealand | execute in jp-notebook|
| 3_add_delta_VLM.ipynb| script to add Delta data from Ohenhen et al., 2026 and Nienhuis and Törnqvist, 2017  | execute in jp-notebook|
| 4_plots.ipynb| script to make all main paper plots, and some SI figures | execute in jp-notebook|
| 5_SI_plots.ipynb| script to generate remaining SI figures | execute in jp-notebook|


## Reproduce my figures
Use this script to reproduce the figures used in this publication.

| Script Name | Description | How to Run |
| --- | --- | --- |
| 4_plots.ipynb| script to plot results | execute in jp-notebook

