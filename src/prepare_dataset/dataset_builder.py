import os
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from src.prepare_dataset.video_to_frames import video_to_frames
from src.utils.globals import logger, config
from src.utils.video_utils import get_video_name


# def dataset_generator(data_paths: [str], labels: [int], figure_shape,seq_length,use_aug,use_crop,crop_x_y,classes = 1):
#     while True:
#         indexes = np.arange(len(data_paths))
#         np.random.shuffle(indexes)
#         select_indexes = indexes[:config['TRAIN']['BATCH_SIZE']]
#         data_paths_batch = [data_paths[i] for i in select_indexes]
#         labels_batch = [labels[i] for i in select_indexes]
#
#         # X, y = get_sequences(data_paths_batch,labels_batch,figure_shape,seq_length, classes, use_augmentation = use_aug,use_crop=use_crop,crop_x_y=crop_x_y)
#
#         # yield X, y


def dataset_video_builder(dataset_path: str, violence_label: str, force: bool = False):
    logger.debug(f'preparing dataset: {dataset_path}')
    videos_directory = os.path.join(dataset_path, config['PATHS']['VIDEOS_FOLDER'])

    dataset_frames = []
    videos_seq_length = []
    videos_frames_paths = []
    videos_labels = []

    # TODO: process in parallel?
    for video_file in os.listdir(videos_directory):
        video_frames_path = os.path.join(dataset_path, config['PATHS']['FRAMES_FOLDER'], get_video_name(video_file))
        video_sum_img_file = os.path.join(video_frames_path, 'video_summary.pkl')

        # Check if there is already file summary of the video so we don't need to analyze it
        if os.path.isfile(video_sum_img_file) and not force:
            with open(video_sum_img_file, 'rb') as f:
                video_frames = pickle.load(f)
        else:
            video_frames, video_frames_path = video_to_frames(dataset_path=dataset_path, video_file=video_file)

            if violence_label in get_video_name(video_file):
                video_frames['label'] = 1

            with open(video_sum_img_file, 'wb') as f:
                pickle.dump(video_frames, f, pickle.HIGHEST_PROTOCOL)

        dataset_frames.append(video_frames)
        videos_seq_length.append(video_frames['sequence_length'])
        videos_frames_paths.append(video_frames['images_path'])
        videos_labels.append(video_frames['label'])

    # Split dataset to test and train
    x_train, x_test, y_train, y_test = train_test_split(videos_frames_paths, videos_labels, test_size=0.20,
                                                        random_state=42)

    # Split dataset to test and validation
    x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.20, random_state=42)

    return x_train, x_test, x_valid, y_train, y_test, y_valid
