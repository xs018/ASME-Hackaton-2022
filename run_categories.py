from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import src.util.feature_extract as fe_util
from src.util.features import extract_features
import time
import json

assembly_id_list = fe_util.get_assembly_id_list()
assembly_id = assembly_id_list[2000]
assembly_data = fe_util.read_json(assembly_id)
print(assembly_data["properties"]['categories'])

all_categories = set()
for iter,assembly_id in enumerate(assembly_id_list):
    assembly_data = fe_util.read_json(assembly_id)
    for cat in assembly_data["properties"]['categories']:
        all_categories.add(cat)

with open('all_categories.txt', 'w') as f:
    for cat in all_categories:
        f.write("/results/"+cat+"\n")
