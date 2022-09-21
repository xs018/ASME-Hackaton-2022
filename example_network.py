from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import src.util.feature_extract as fe_util
from src.util.features import extract_features
import time

import networkx as nx
import random

from pathlib import Path
import networkx as nx
import numpy as np
import trimesh
import meshplot as mp

from src.util.assembly_graph import AssemblyGraph



# assembly_id = "72950_5074f5a3"
assembly_id = "34103_6635d58e"

graph, label_dict = fe_util.get_graph(assembly_id)

print(list(graph.nodes))
print(list(graph.nodes)[0].split("_")[-1])

nx.draw(graph,connectionstyle="arc3, rad = 0.1", labels=label_dict, with_labels=True)
plt.show()