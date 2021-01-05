import os
import glob
from src.utils.globals import logger, config
from src.utils.video_utils import get_video_name


LABELS_FORMAT = 'txt'


def get_video_label(dataset_path: str, video_file: str):
    labels_directory = os.path.join(dataset_path, config['PATHS']['LABELS_PATH'])
    video_labels_files = glob.glob(f'{labels_directory+"/"+get_video_name(video_file)}*.{LABELS_FORMAT}')
    video_labels = []

    for video_labels_file in video_labels_files:
        with open(video_labels_file) as f:
            video_labels.extend([[int(num) for num in line.split()] for line in f])

    return video_labels
