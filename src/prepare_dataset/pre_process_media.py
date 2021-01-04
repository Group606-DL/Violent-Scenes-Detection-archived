import os
from src.utils.globals import logger, config  # TODO: change to pkg and not relative imports
import math
import cv2
import moviepy.editor as mp

# Globals
# TODO: add to config file?
AUDIO_FORMAT = '.wav'
FRAMES_PER_SECOND = 10
FRAME_WIDTH = 480
FRAME_HEIGHT = 270


def dataset_pre_process_media(dataset_path: str):
    videos_directory = os.path.join(dataset_path, config['PATHS']['VIDEOS_FOLDER'])

    # TODO: process in parallel
    for video_file in os.listdir(videos_directory):
        video_to_audio(dataset_path=dataset_path, video_file=video_file)
        video_to_frames(dataset_path=dataset_path, video_file=video_file, videos_directory=videos_directory)


def video_to_frames(dataset_path: str, videos_directory: str, video_file: str):
    video_path = os.path.join(videos_directory, video_file)

    # Create a folder to save frames if the folder not existed
    video_frames_path = os.path.join(dataset_path, config['PATHS']['FRAMES_FOLDER'], video_file.split(".")[0])
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

    cap.set(cv2.CAP_PROP_FPS, FRAMES_PER_SECOND)

    # Get frame rate of video
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    while cap.isOpened():
        frame_id = cap.get(1)  # current frame number
        success, frame = cap.read()  # If frame is read correctly, it will be True
        if not success:
            break
        if frame_id % math.floor(frame_rate) == 0:
            # Resize pixels
            # TODO: change only the width and the height as ratio
            frame = cv2.resize(src=frame, dsize=(FRAME_WIDTH, FRAME_HEIGHT))
            frame = frame.reshape(FRAME_HEIGHT, FRAME_WIDTH, 3)

            # Save the frame
            filename = f"frame{count}.jpg"
            count += 1
            cv2.imwrite(os.path.join(video_frames_path, filename), frame)

    # When everything is done, release the capture
    cap.release()
    logger.debug(f'done extraction: {video_path}')


def video_to_audio(dataset_path: str, video_file: str):
    # Create a folder to save audios if the folder not existed
    video_audios_path = os.path.join(dataset_path, config['PATHS']['AUDIOS_FOLDER'])
    if not os.path.exists(video_audios_path):
        try:
            os.makedirs(video_audios_path)
        except OSError:
            logger.error(f"Can't create destination directory {video_audios_path}!")

    audio_path = os.path.join(video_audios_path, video_file.split(".")[0] + AUDIO_FORMAT)
    if not os.path.isfile(audio_path):
        clip = mp.VideoFileClip(os.path.join(dataset_path, config['PATHS']['VIDEOS_FOLDER'], video_file))
        clip.audio.write_audiofile(audio_path)
