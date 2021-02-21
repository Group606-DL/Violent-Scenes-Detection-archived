import glob
import os
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split

from src.prepare_dataset.video_builder import video_to_npy
from src.utils.globals import logger, config
from src.utils.video_utils import get_video_name

NPY_FILE_TYPE = '.npy'


def dataset_video_builder(dataset_path: str, train_test: bool, force: bool = False):
    videos_directories = [x[0] for x in os.walk(os.path.join(dataset_path, config['PATHS']['VIDEOS_FOLDER']))]
    npy_directory = os.path.join(dataset_path, config['PATHS']['NPY_FOLDER'])

    # Create a folder to save frames if the folder not existed
    if not os.path.exists(npy_directory):
        try:
            os.makedirs(npy_directory)
        except OSError:
            logger.error(f"Can't create destination directory {npy_directory}!")

    dataset_frames = []
    videos_seq_length = []
    videos_frames_paths = []
    videos_labels = []

    for video_directory in tqdm(videos_directories):
        files = [video_file for video_file in tqdm(os.listdir(video_directory)) if
                 os.path.isfile(os.path.join(video_directory, video_file))]
        if not files:
            continue

        for video_file in files:
            # Destination npy path
            video_npy_path = os.path.join(dataset_path, 'npy', get_video_name(video_file) + NPY_FILE_TYPE)

            # Check if there is already file summary of the video so we don't need to analyze it
            if os.path.isfile(video_npy_path) and not force:
                with open(video_npy_path, 'rb') as f:
                    result = np.load(f)
            else:
                result = video_to_npy(video_directory=video_directory, video_file=video_file)

                # Save as .npy file
                np.save(video_npy_path, result)

            dataset_frames.append(result['frames'])
            videos_seq_length.append(result['sequence_length'])
            videos_frames_paths.append(result['images_path'])
            videos_labels.append(result['label'])

        # Split dataset to test and train
        x_train, x_test, y_train, y_test = train_test_split(videos_frames_paths, videos_labels, test_size=0.20,
                                                            random_state=42)

    # Split dataset to test and validation
    x_train, x_validation, y_train, y_validation = train_test_split(x_train, y_train, test_size=0.20,
                                                                    random_state=42)

    return x_train, x_test, x_validation, y_train, y_test, y_validation
