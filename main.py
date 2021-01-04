import os
import preprocess
from globals import logger

# static parameter for the network
datasets = dict(
    # hollywood_dev="data/Hollywood-dev",
    youtube_gen="data/YouTube-gen"
)

# pre-process datasets
for dataset_name, dataset_path in datasets.items():
    logger.debug(f'pre-processing dataset: {dataset_name}')
    preprocess.dataset_pre_process(dataset_path=dataset_path)
