from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import src.util.feature_extract as fe_util
from src.util.features import extract_features
import time

start_time = time.time()

source_assembly_id = "44400_388ed3d0"
fp_source = fe_util.read_assembly_fingerprint(source_assembly_id)

# fe_util.plot_assembly_images([source_assembly_id])

assembly_id_list = fe_util.get_assembly_id_list()
total_iter = len(assembly_id_list)
dists =[]
for iter,assembly_id in enumerate(assembly_id_list):
    fp_target = fe_util.read_assembly_fingerprint(assembly_id)
    d = np.linalg.norm(fp_target - fp_source)
    dists.append(d)
    print(f"iter = {iter}/{total_iter}")

indices = np.argsort(dists)
assembly_id_list = np.array(assembly_id_list)
top5_assembly_ids = assembly_id_list[indices[:6]]

print(f"total runtime = {time.time()-start_time:.0f} sec")
fe_util.plot_assembly_images(top5_assembly_ids)
plt.savefig(f'results/bench_{source_assembly_id}.png')
plt.show()