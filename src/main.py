from src.prepare_dataset import dataset_builder
from src.utils.globals import logger
from src.prepare_dataset.dataset import VideoDataset
# TODO: change to pkg and not relative imports

datasets = [
    VideoDataset(dataset_name="violentflow", path="../data/violentflow"),
    VideoDataset(dataset_name="movies", path="../data/movies"),
    VideoDataset(dataset_name="ming", path="../data/ming", train_test=True)
]

# Iterate all datasets
for dataset in datasets:
    # pre-process datasets
    logger.debug(f'pre-processing dataset: {dataset.dataset_name}')
    x_train, x_test, x_validation, y_train, y_test, y_validation = dataset.dataset_builder()


