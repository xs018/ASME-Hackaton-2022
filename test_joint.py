from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import src.util.feature_extract as fe_util
from src.util.features import extract_features
import time

start_time = time.time()

# source_assembly_id = "22057_4947db57"
source_assembly_id = "34103_6635d58e"
# source_assembly_id = "44400_388ed3d0"

# source_assembly_id = "72950_5074f5a3"
fp_source = fe_util.read_assembly_fingerprint(source_assembly_id)

assembly_data_source = fe_util.read_json(source_assembly_id)

# volume
vol_source = fe_util.get_volume(assembly_data_source)

# joint
dof_source =fe_util.get_dof(assembly_data_source)


assembly_id_list = fe_util.get_assembly_id_list()
total_iter = len(assembly_id_list)
dists =[]
for iter,assembly_id in enumerate(assembly_id_list):
    fp_target = fe_util.read_assembly_fingerprint(assembly_id)
    assembly_data_target = fe_util.read_json(assembly_id)

    # volume
    vol_target = fe_util.get_volume(assembly_data_target)
    # joint
    dof_target=fe_util.get_dof(assembly_data_target)

    d_fp = np.linalg.norm(fp_target - fp_source)/np.linalg.norm(fp_source)
    d_vol = np.abs(vol_target - vol_source)/vol_source
    d_dof = np.linalg.norm(dof_target - dof_source)

    d =  d_fp + 0.2*d_vol + d_dof
    dists.append(d)
    print(f"iter = {iter}/{total_iter}")

indices = np.argsort(dists)
dists = np.array(dists)
assembly_id_list = np.array(assembly_id_list)
top5_assembly_ids = assembly_id_list[indices[:6]]
print(dists[indices])

print(f"total runtime = {time.time()-start_time:.0f} sec")
fe_util.plot_assembly_images(top5_assembly_ids)
plt.savefig(f'results/joint_{source_assembly_id}.png')
plt.show()