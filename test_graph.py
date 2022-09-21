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


# graph - crucial body
graph, label_dict = fe_util.get_graph(source_assembly_id)
crutial_bodies_source,max_degree = fe_util.get_crucial_bodies(graph)
vol_bodies_source = fe_util.get_bodies_volume(source_assembly_id,crutial_bodies_source)
fp_bodies_source = fe_util.read_bodies_fingerprint(source_assembly_id,crutial_bodies_source)
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

    # graph - crucial body
    try:
        graph, label_dict = fe_util.get_graph(assembly_id)
    except:
        dists.append(10000)
        continue
    crutial_bodies_target,max_degree = fe_util.get_crucial_bodies(graph)
    vol_bodies_target = fe_util.get_bodies_volume(assembly_id,crutial_bodies_target)
    fp_bodies_target = fe_util.read_bodies_fingerprint(assembly_id,crutial_bodies_target)

    # compare 
    N_fp_bodies_s = fp_bodies_source.shape[1]
    N_fp_bodies_t = fp_bodies_target.shape[1]

    d_crutial = 10000000
    for  i in range(N_fp_bodies_s):
        for j in range(N_fp_bodies_t):
            d_temp = np.linalg.norm(fp_bodies_target[:,j] -fp_bodies_source[:,i])/np.linalg.norm(fp_bodies_source[:,i])/np.linalg.norm(fp_source)+ \
                 np.abs(vol_bodies_target[j] - vol_bodies_source[i])*0.2
            if d_temp<d_crutial:
                d_crutial=d_temp

    d_fp = np.linalg.norm(fp_target - fp_source)/np.linalg.norm(fp_source)
    d_vol = np.abs(vol_target - vol_source)/vol_source
    d_dof = np.linalg.norm(dof_target - dof_source)

    d =  d_fp + 0.2*d_vol + 0.1*d_dof  + 0.2*d_crutial
    dists.append(d)
    print(f"iter = {iter}/{total_iter}")

indices = np.argsort(dists)
dists = np.array(dists)
assembly_id_list = np.array(assembly_id_list)
top5_assembly_ids = assembly_id_list[indices[:6]]
print(dists[indices])

print(f"total runtime = {time.time()-start_time:.0f} sec")
fe_util.plot_assembly_images(top5_assembly_ids)
plt.savefig(f'results/graph_{source_assembly_id}.png')
plt.show()