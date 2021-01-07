from abc import ABC, abstractmethod

from src.prepare_dataset.dataset_builder import dataset_video_builder


class Dataset(ABC):
    def __init__(self, dataset_name, path, violence_label):
        self.dataset_name = dataset_name
        self.path = path
        self.violence_label = violence_label
        super(Dataset, self).__init__()

    @abstractmethod
    def dataset_builder(self):
        pass


class VideoDataset(Dataset):
    def dataset_builder(self):
        return dataset_video_builder(self.path, self.violence_label)


class AudioDataset(Dataset):
    def dataset_builder(self):
        pass
