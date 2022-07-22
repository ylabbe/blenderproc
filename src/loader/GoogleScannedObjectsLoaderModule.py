"""
Helper methods to load acronym/shapenet objects.
"""

import argparse
import os
import random
import numpy as np
import shutil
import uuid
import time

from pathlib import Path
import h5py
import json
import yaml

from typing import List, Union

# BlenderProc
import bpy
from src.loader.LoaderInterface import LoaderInterface
from src.loader.ObjectLoaderModule import ObjectLoaderModule
from src.utility.loader.ObjectLoader import ObjectLoader

class GoogleScannedObjectsLoaderModule(LoaderInterface):
    def __init__(self, config):
        LoaderInterface.__init__(self, config)
    
    def run(self):
        dataset_path = self.config.get_string("dataset_path")
        obj_id = self.config.get_string("obj_id") 
        move_object_origin = self.config.get_bool("move_object_origin", True)

        mesh_path = os.path.join(dataset_path, obj_id, 'meshes', 'model.obj')
        loaded_obj = ObjectLoader.load(mesh_path)
        if move_object_origin:
            loaded_obj.move_origin_to_bottom_mean_point()
        self._set_properties(loaded_obj)