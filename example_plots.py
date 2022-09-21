from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import src.util.feature_extract as fe_util
from src.util.features import extract_features
import time


# plot all the assembly drawings in a list, the input has to be a list
assembly_id_list = ['7778_3a9748b3','148051_ad8f6d60','148105_610e3d11','148137_f6cfb712']
fe_util.plot_assembly_images(assembly_id_list)

# plot all the body drawings in a assembly
# assembly_id = assembly_id_list[0]
# fe_util.plot_body_images_from_assembly(assembly_id)