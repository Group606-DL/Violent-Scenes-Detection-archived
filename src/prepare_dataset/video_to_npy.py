from src.utils.globals import config
from src.prepare_dataset.video_frames import video_to_frames, get_optical_flow
import numpy as np


def video_to_npy(video_directory, video_file):
    video_frames = video_to_frames(video_directory=video_directory,
                                   video_file=video_file)

    if config['LABELS']['NON_FIGHT'] not in video_directory:
        video_frames['label'] = 1

    flows = get_optical_flow(video_frames['frames'])

    result = np.zeros((len(flows), 224, 224, 5))
    result[..., :3] = video_frames['frames']
    result[..., 3:] = flows

    return result
