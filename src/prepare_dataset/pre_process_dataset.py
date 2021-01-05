import os

# TODO: change to pkg and not relative imports
from src.prepare_dataset.get_video_label import get_video_label
from src.prepare_dataset.video_to_audio import video_to_audio
from src.prepare_dataset.video_to_frames import video_to_frames
from src.utils.globals import logger, config


def dataset_pre_process_media(dataset_path: str):
    logger.debug(f'preparing dataset: {dataset_path}')
    videos_directory = os.path.join(dataset_path, config['PATHS']['VIDEOS_FOLDER'])

    # TODO: process in parallel?
    for video_file in os.listdir(videos_directory):
        labels = get_video_label(dataset_path=dataset_path, video_file=video_file)
        video_to_audio(dataset_path=dataset_path, video_file=video_file)
        video_to_frames(dataset_path=dataset_path, video_file=video_file, videos_directory=videos_directory,
                        labels=labels)
