from PIL import Image
import numpy as np
import os
from src.util.features import extract_features
import glob
import matplotlib.pyplot as plt
import pandas as pd
import json
from src.util.assembly_graph import AssemblyGraph
data_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'../../full_data/train/'))
json_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'../../fingerprints/json/'))
csv_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'../../fingerprints/csv/'))

font_size = 4

def read_assembly_image(assembly_id):
    return np.array(Image.open(f"{data_root}/{assembly_id}/assembly.jpg"))


def read_body_images_from_assembly(assembly_id,body_id=None):
    if body_id:
        return np.array(Image.open(f"{data_root}/{assembly_id}/{body_id}.jpg"))
    else:
        body_img_dict = {}
        image_names = glob.glob(f"{data_root}/{assembly_id}/*.jpg")
        for image_name in image_names:
            body_name = image_name.split("/")[-1][:-4]
            body_img_dict[body_name] =  np.array(Image.open(image_name))
        return body_img_dict



def plot_assembly_images(assembly_id_list):
    N = len(assembly_id_list)
    nrow = int(np.ceil(np.sqrt(N)))
    ncol = int(np.ceil(N/nrow))
    fig,axarr = plt.subplots(nrows=nrow,ncols=ncol)
    if type(axarr).__module__ == np.__name__:
        axarr = axarr.flatten()
        for assembly_id, ax in zip(assembly_id_list,axarr):
            ax.imshow(read_assembly_image(assembly_id))
            ax.set_title(f"assembly_id = {assembly_id}",fontdict={'fontsize': font_size+2})
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
    else:
        ax = axarr;assembly_id = assembly_id_list[0]
        ax.imshow(read_assembly_image(assembly_id))
        ax.set_title(f"assembly_id = {assembly_id}",fontdict={'fontsize': font_size+2})
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

    # plt.show()
    return 


def plot_body_images_from_assembly(assembly_id,body_id=None):

    body_img_dict = read_body_images_from_assembly(assembly_id,body_id=body_id)
    if body_id:
        plt.imshow(body_img_dict)
        plt.title(f"body_id = {body_id}")
    else:
        N = len(body_img_dict)
        nrow = int(np.ceil(np.sqrt(N)))
        ncol = int(np.ceil(N/nrow))
        fig,axarr = plt.subplots(nrows=nrow,ncols=ncol)
        axarr = axarr.flatten()
        axarr[0].imshow(body_img_dict["assembly"])
        axarr[0].set_title(f"assembly_id = {assembly_id}",fontdict={'fontsize': font_size})
        axarr[0].get_xaxis().set_visible(False)
        axarr[0].get_yaxis().set_visible(False)
        
        offset = 1
        for idx,bodyid in enumerate(body_img_dict):
            if bodyid == "assembly":
                offset=0
                continue
            ax = axarr[idx+offset]
            ax.imshow(body_img_dict[bodyid])
            ax.set_title(f"body_id = {bodyid}",fontdict={'fontsize': font_size})
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
        # plt.show()
    return 

def read_fingerprint(assembly_id):
    return pd.read_csv(f"{csv_root}/{assembly_id}.csv",index_col=0).T

def read_assembly_fingerprint(assembly_id):
    fp = pd.read_csv(f"{csv_root}/{assembly_id}.csv",index_col=0).T
    return fp["assembly.jpg"].to_numpy()

def read_bodies_fingerprint(assembly_id,bodies_id):
    fp = pd.read_csv(f"{csv_root}/{assembly_id}.csv",index_col=0).T
    for i in range(len(bodies_id)):
        bodies_id[i] = bodies_id[i] + '.jpg'
    bodies_fp = fp[bodies_id]
    return bodies_fp.to_numpy()

def read_json(assembly_id,property=None):
    f = open (f"{json_root}/{assembly_id}.json", "r")
    assembly_data = json.loads(f.read())
    f.close()
    
    if property:
        try:
            assembly_data = assembly_data[property]
        except:
            raise("property has to be ",assembly_data.keys())
    return assembly_data

def get_assembly_id_list():
    filenames = glob.glob(f"{json_root}/*.json")
    assembly_id_list = []
    for filename in filenames:
        if '.txt' in filename:
            continue
        assembly_id_list.append(filename.split('/')[-1][:-5])
    return assembly_id_list

def get_graph(assembly_id):
    assembly_file = f"{json_root}/{assembly_id}.json"
    ag = AssemblyGraph(assembly_file)
    graph = ag.get_graph_networkx()
    label_dict = ag.get_node_label_dict()
    return graph, label_dict

def get_volume(assembly_data_source):
    vol_source = 0
    for vol in assembly_data_source["bodies"].keys():
        vol_source+=assembly_data_source["bodies"][vol]["physical_properties"]["volume"]
    return vol_source
def get_bodies_volume(assembly_id,bodies_id):
    vol_bodies = []
    for body_id in bodies_id:
        assembly_data = read_json(assembly_id)
        v = assembly_data["bodies"][body_id]["physical_properties"]["volume"]
        vol_bodies.append(v)
    return vol_bodies

def get_dof(assembly_data):
    dof = np.zeros(6)

    if "as_built_joints" in assembly_data.keys():
        return dof
    if "joints" not in assembly_data.keys():
        return dof
    if assembly_data["joints"] == None:
        return dof
    for joint in  assembly_data["joints"].keys():
        joint_type = assembly_data["joints"][joint]["joint_motion"]["joint_type"]
        if joint_type == 'RigidJointType':
            pass
        elif joint_type == 'RevoluteJointType':
            dof[0] += 1
        elif joint_type == 'SliderJointType':
            dof[1] +=1
        elif joint_type == 'CylindricalJointType':
            dof[2] +=1
        elif joint_type == 'PinSlotJointType':
            dof[3]+=1
        elif joint_type == 'PlanarJointType':
            dof[4]+=1
        elif joint_type == 'BallJointType':
            dof[5]+=1

    return dof

def get_crucial_bodies(graph):
    V = list(graph.degree)
    max_degree = 0
    bodies = []
    for name,degree in V:
        if degree > max_degree:
            max_degree = degree
            bodies = [name.split('_')[-1]]
        elif degree == max_degree:
            bodies.append(name.split('_')[-1])
    return bodies,max_degree
