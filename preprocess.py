import math
import cv2
import moviepy.editor as mp
import numpy as np
import os
import logging

# Globals
# TODO: add to env file?
logger = logging.getLogger(__name__)

VIDEOS_FOLDER = 'videos'
FRAMES_FOLDER = 'frames'
AUDIOS_FOLDER = 'audio'
AUDIO_FORMAT = '.wav'
FRAMES_PER_SECOND = 10
FRAME_WIDTH = 255


def dataset_pre_process(dataset_path: str):
    videos_directory = os.path.join(dataset_path, VIDEOS_FOLDER)
    for video_file in os.listdir(videos_directory):
        video_to_audio(dataset_path=dataset_path, video_file=video_file)
        video_to_frames(dataset_path=dataset_path, video_file=video_file, videos_directory=videos_directory)


def video_to_frames(dataset_path: str, videos_directory: str, video_file: str):
    video_read_path = os.path.join(videos_directory, video_file)
    cap = cv2.VideoCapture(video_read_path)

    # Create a folder to save frames if the folder not existed
    video_frames_path = os.path.join(dataset_path, FRAMES_FOLDER, video_file.split(".")[0])
    if not os.path.exists(video_frames_path):
        try:
            os.makedirs(video_frames_path)
        except OSError:
            logger.error(f"Can't create destination directory {video_frames_path}!")

    cap.set(cv2.CAP_PROP_FPS, FRAMES_PER_SECOND)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)

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
            frame = cv2.resize(src=frame, dsize=(480, 270))
            frame = frame.reshape(270, 480, 3)

            # Save the frame
            filename = f"frame{count}.jpg"
            count += 1
            cv2.imwrite(os.path.join(video_frames_path, filename), frame)
    cap.release()


def video_to_audio(dataset_path: str, video_file: str):
    # Create a folder to save audios if the folder not existed
    video_audios_path = os.path.join(dataset_path, AUDIOS_FOLDER)
    if not os.path.exists(video_audios_path):
        try:
            os.makedirs(video_audios_path)
        except OSError:
            logger.error(f"Can't create destination directory {video_audios_path}!")

    clip = mp.VideoFileClip(os.path.join(dataset_path, VIDEOS_FOLDER, video_file))
    clip.audio.write_audiofile(os.path.join(video_audios_path, video_file.split(".")[0] + AUDIO_FORMAT))
