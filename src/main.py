from src.prepare_dataset import dataset_builder
from src.utils.globals import logger
from src.prepare_dataset.dataset import VideoDataset
# TODO: change to pkg and not relative imports

datasets = [
    VideoDataset(dataset_name="violentflow", path="../data/violentflow", violence_label="violence"),
    # VideoDataset(dataset_name="movies", path="../data/movies", violence_label='fi')
]

# Iterate all datasets
for dataset in datasets:
    # pre-process datasets
    logger.debug(f'pre-processing dataset: {dataset.dataset_name}')
    x_train, x_test, y_train, y_test = dataset.dataset_builder()


