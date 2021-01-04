import os
import numpy as np
import h5py
from src.utils.globals import logger, config  # TODO: change to pkg and not relative imports


def pre_process_features(dataset_path: str):
    features_directory = os.path.join(dataset_path, config['PATHS']['FEATURES_FOLDER'])
    for feature in os.listdir(features_directory):
        if feature.split('.')[1] == 'mat':
            arrays = {}
            f = h5py.File(os.path.join(features_directory, feature))
            for k, v in f.items():
                arrays[k] = np.array(v)

