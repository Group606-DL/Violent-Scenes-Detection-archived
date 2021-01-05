import math
import os
import cv2

from src.utils.globals import logger, config
from src.utils.video_utils import get_video_name


# Globals
FRAMES_PER_SECOND = 10
FRAME_WIDTH = 480
FRAME_HEIGHT = 270


def video_to_frames(dataset_path: str, videos_directory: str, video_file: str, labels: [str]):
    video_path = os.path.join(videos_directory, video_file)

    # Create a folder to save frames if the folder not existed
    video_frames_path = os.path.join(dataset_path, config['PATHS']['FRAMES_FOLDER'], get_video_name(video_file))
    if os.path.exists(video_frames_path):
        return logger.debug(f'video {video_file} had been already extracted')

    try:
        os.makedirs(video_frames_path)
    except OSError:
        logger.error(f"Can't create destination directory {video_frames_path}!")

    cap = cv2.VideoCapture(video_path)

    # Video capture settings
    n_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    f_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    f_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    logger.debug(f'video_fn: {video_file}, number of frames: {n_frames}, f_width: {f_width}, f_height: {f_height}')

    # TODO: how to get another fps ?
    # Get frame rate of video
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    while cap.isOpened():
        frame_id = cap.get(1)  # current frame number
        success, frame = cap.read()  # If frame is read correctly, it will be True
        if not success:
            break
        # TODO: check this if
        if frame_id % math.floor(frame_rate) == 0:
            # Resize pixels
            # TODO: change only the width and the height as ratio
            frame = cv2.resize(src=frame, dsize=(FRAME_WIDTH, FRAME_HEIGHT))
            frame = frame.reshape(FRAME_HEIGHT, FRAME_WIDTH, 3)

            print(count/frame_rate)
            # Save the frame
            filename = f"frame{count}.jpg"
            count += 1
            cv2.imwrite(os.path.join(video_frames_path, filename), frame)

    # When everything is done, release the capture
    cap.release()
    logger.debug(f'done extraction: {video_path}')
