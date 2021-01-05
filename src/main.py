from src.prepare_dataset import pre_process_mat, pre_process_dataset
from src.utils.globals import logger

# static parameter for the network
datasets = dict(
    # hollywood_dev="../data/Hollywood-dev",
    # youtube_gen="../data/YouTube-gen"

)

# pre-process datasets
for dataset_name, dataset_path, dataset_class in datasets.items():
    logger.debug(f'pre-processing dataset: {dataset_name}')
    # pre_process_mat.pre_process_features(dataset_path=dataset_path)
    pre_process_dataset.dataset_pre_process_media(dataset_path=dataset_path)
