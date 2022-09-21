from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import src.util.feature_extract as fe_util
from src.util.features import extract_features
import time

assembly_id_list = ['7778_3a9748b3','148051_ad8f6d60','148105_610e3d11','148137_f6cfb712']
assembly_id = assembly_id_list[1]

assembly_data = fe_util.read_json(assembly_id)
print(assembly_data.keys())
print(assembly_data["joints"]["0e448cf4-059b-11ec-811b-065185b4953b"].keys())
print(assembly_data["joints"]["0e448cf4-059b-11ec-811b-065185b4953b"]["joint_motion"]["joint_type"])
print(assembly_data["bodies"]["0e3d39e2-059b-11ec-a643-065185b4953b"]["physical_properties"]["volume"])

# print(assembly_data["contacts"][0])
# print(assembly_data["joints"]["0e448cf4-059b-11ec-811b-065185b4953b"]["joint_motion"]["joint_type"])
# print(assembly_data["bodies"]["0e3d39e2-059b-11ec-a643-065185b4953b"])
