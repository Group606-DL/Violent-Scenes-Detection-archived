from abc import ABC, abstractmethod

from src.prepare_dataset.dataset_builder import dataset_video_builder


class Dataset(ABC):
    def __init__(self, dataset_name: str, path: str, train_test: bool = False):
        self.dataset_name = dataset_name
        self.path = path
        self.train_test = train_test
        super(Dataset, self).__init__()

    @abstractmethod
    def dataset_builder(self):
        pass


class VideoDataset(Dataset):
    def dataset_builder(self):
        return dataset_video_builder(self.path, self.train_test)


class AudioDataset(Dataset):
    def dataset_builder(self):
        pass
