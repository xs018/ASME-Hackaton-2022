from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import src.util.feature_extract as fe_util
from src.util.features import extract_features
import time

assembly_id_list = ['7778_3a9748b3','148051_ad8f6d60','148105_610e3d11','148137_f6cfb712']
assembly_id = assembly_id_list[0]

# Option #1
fingerprint = fe_util.read_fingerprint(assembly_id)
print(fingerprint["assembly.jpg"])
print(fingerprint['6d4460c0-0600-11ec-a945-020dc2b44123.jpg'])

assembly_fp = fingerprint["assembly.jpg"].to_numpy()
print(len(assembly_fp))
print(assembly_fp)

# Option #2
fingerprint = fe_util.read_assembly_fingerprint(assembly_id)
print(fingerprint)

