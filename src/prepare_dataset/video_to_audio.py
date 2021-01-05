import os
import moviepy.editor as mp
from src.utils.globals import logger, config
from src.utils.video_utils import get_video_name

AUDIO_FORMAT = '.wav'


def video_to_audio(dataset_path: str, video_file: str):
    # Create a folder to save audios if the folder not existed
    video_audios_path = os.path.join(dataset_path, config['PATHS']['AUDIOS_FOLDER'])
    if not os.path.exists(video_audios_path):
        try:
            os.makedirs(video_audios_path)
        except OSError:
            logger.error(f"Can't create destination directory {video_audios_path}!")

    audio_path = os.path.join(video_audios_path, get_video_name(video_file) + AUDIO_FORMAT)
    if not os.path.isfile(audio_path):
        clip = mp.VideoFileClip(os.path.join(dataset_path, config['PATHS']['VIDEOS_FOLDER'], video_file))
        clip.audio.write_audiofile(audio_path)