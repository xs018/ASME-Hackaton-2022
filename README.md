# IDETC 2022

Characterizing Similarity from Computer-Aided Design (CAD) Assemblies

# 0 - Prepare Dataset
a) Clone this repository to your local directory.

b) This competition only uses the subset of the Fusion 360 Gallery Assembly Dataset. Please download the dataset following this [link](https://myshare.autodesk.com/personal/daniele_grandi_autodesk_com/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fdaniele%5Fgrandi%5Fautodesk%5Fcom%2FDocuments%2FData%2FFusionGallery%2FIDETC%20Hackathon%2Ftraining%20set&ga=1).

c) create a new folder `full_data`, and copy the `train` and `validation` folders from `IDETC22-Hackathon-Dataset` to `full_data`.

# 1 - Setting up the System Environment
This will install the independencies for the tools (e.g. tensorflow).
```sh
cd [path to this repository]                      # go to where you saved this repository on your local machine
conda env create -f IDETC22-Hackathon.yml  # reproduce conda environment from .yml
conda activate IDETC22-Hackathon               # activate the created environment
```


# 2 - Extract Fingerprints from Thumbnail
In the assembly folder, we have the `assembly.jpg` and `[body_id].jpg`. A pretrained `Resnet50` model is adopted to extract, and save the fingerprints. 
- Method 1: extract fingerprints from source
```sh
python computing_all_fingerprints.py
```
The whole process will take about 8 hours, and the results will be saved in `fingerprints/csv/*.csv` and `fingerprints/json/*.json`

- Method 2: download the fingerprints from [here](https://drive.google.com/file/d/1-2sJIt5V0zTQ5c0h2dl3OVfILs5S4hU3/view?usp=sharing). Extract the zip file into the `IDETC2022` folder.