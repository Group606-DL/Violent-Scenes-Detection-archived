import math
import os
import cv2

from src.utils.globals import logger, config
from src.utils.video_utils import get_video_name

# Globals
FRAMES_PER_SECOND = 5
FRAME_WIDTH = 480
FRAME_HEIGHT = 270


def video_to_frames(dataset_path: str, video_file: str):
    video_path = os.path.join(dataset_path, config['PATHS']['VIDEOS_FOLDER'], video_file)
    video_frames_path = os.path.join(dataset_path, config['PATHS']['FRAMES_FOLDER'], get_video_name(video_file))

    # Create a folder to save frames if the folder not existed
    if not os.path.exists(video_frames_path):
        try:
            os.makedirs(video_frames_path)
        except OSError:
            logger.error(f"Can't create destination directory {video_frames_path}!")

    # Configure a video capture stream
    cap = cv2.VideoCapture(video_path)

    # Video capture settings
    n_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    f_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    f_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    f_rate = cap.get(cv2.CAP_PROP_FPS)  # Get frame rate of video

    logger.debug(f'video_fn: {video_file}, number of frames: {n_frames}, '
                 f'f_width: {f_width}, f_height: {f_height}, fps: {f_rate}')

    count = 0
    label = 0
    files = []
    while cap.isOpened():
        frame_id = cap.get(1)  # current frame number
        success, frame = cap.read()  # if the frame is read correctly, it will be True
        if not success:
            break
        # TODO: check this if
        if frame_id % math.floor(FRAMES_PER_SECOND) == 0:
            # Resize pixels
            # TODO: change only the width and the height as ratio
            frame = cv2.resize(src=frame, dsize=(FRAME_WIDTH, FRAME_HEIGHT))
            frame = frame.reshape(FRAME_HEIGHT, FRAME_WIDTH, 3)

            # Save the frame
            filename = f"frame{count}.jpg"
            frame_path = os.path.join(video_frames_path, filename)
            files.append(frame_path)
            cv2.imwrite(frame_path, frame)
        count += 1

    # When everything is done, release the capture
    cap.release()
    logger.debug(f'done extraction: {video_path}')

    # TODO: Change to class
    video_images = dict(images_path=video_frames_path, name=video_file,
                        images_files=files, label=label, sequence_length=count)

    return video_images, video_frames_path
