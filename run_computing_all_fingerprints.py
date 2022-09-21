from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import src.util.feature_extract as fe
from src.util.features import extract_features
import time
import shutil

data_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'full_data/validation/'))

if __name__ == "__main__":
    start_time = time.time()
    if not os.path.exists('fingerprints'):
        os.mkdir('fingerprints')
        os.mkdir('fingerprints/json')
        os.mkdir('fingerprints/csv')

    assembly_paths = glob.glob(data_root+'/*')
    N = len(assembly_paths)
    for iter,filepath in enumerate(assembly_paths):
        assembly_id = filepath.split('/')[-1]
        if '.txt' in assembly_id:
            continue 
        current_run_time = int(time.time() - start_time)
        remain_run_time = int(current_run_time/(iter+1)*N)
        print(f"\niter = {iter}/{len(assembly_paths)}, assembly_id = {assembly_id}")
        print(f"current runtime = {current_run_time//60} min {current_run_time % 60} sec")
        print(f"time remain = {remain_run_time//60} min {remain_run_time % 60} sec")
        extract_features(filepath, model='ResNet50', write_to =f'fingerprints/csv/{assembly_id}.csv' , recursive=False)
        shutil.copyfile(filepath+'/assembly.json', f'fingerprints/json/{assembly_id}.json')

    